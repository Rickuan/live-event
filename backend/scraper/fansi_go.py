"""
FANSI GO scraper (go.fansi.me)

FANSI GO is a Next.js/React app — pages are client-side rendered.
fetch() uses Playwright (headless Chromium) to get fully rendered HTML.
parse() uses BeautifulSoup on the rendered output.

Confirmed HTML structure (2026-04-09):
  Outer link : <a href="/events/{EVENTID}">
  Card body  : div.card-body
  Venue name : div.card-body > p.text-gray-76   (first <p>)
  Title      : div.card-body > h3
  Date       : <time datetime="YYYY/MM/DD">
  Price      : not present in listing cards → default tbd
  Artists    : not present in listing cards → empty list
  City       : resolved via venue_lookup.py
"""

import re
from datetime import datetime, timezone

from bs4 import BeautifulSoup, Tag
from playwright.async_api import async_playwright

from app.models import PriceType
from scraper.artist_parser import ArtistParser
from scraper.base import BaseScraper, EventRaw
from scraper.venue_lookup import lookup as venue_lookup

PROVIDER = "fansi_go"
BASE_URL = "https://go.fansi.me"
LISTING_URL = f"{BASE_URL}/events"

_DONATION_KEYWORDS = ("樂捐", "自由樂捐", "donation", "pay what you want")
_FREE_KEYWORDS = ("免費", "free", "0元", "0 元")

# TODO: 把這個function移動到service共用的base class
def _detect_price_type(price_text: str, min_price: int | None) -> PriceType:
    lower = price_text.lower()
    if any(kw in lower for kw in _DONATION_KEYWORDS):
        return PriceType.donation
    if any(kw in lower for kw in _FREE_KEYWORDS) or min_price == 0:
        return PriceType.free
    if min_price is not None and min_price > 0:
        return PriceType.paid
    return PriceType.tbd


def _parse_price(price_text: str) -> tuple[int | None, int | None]:
    numbers = re.findall(r"\d+", price_text.replace(",", ""))
    if not numbers:
        return None, None
    prices = [int(n) for n in numbers]
    return min(prices), max(prices)


def _parse_date(raw: str) -> datetime | None:
    """Parse FANSI GO date string 'YYYY/MM/DD' into UTC datetime (midnight Taiwan time)."""
    try:
        # FANSI GO shows date only — assume event starts at midnight local time
        # Taiwan is UTC+8, so midnight local = UTC-8h → store as date at 00:00 UTC
        # TODO: confirm — if FANSI GO ever shows time, update this parser
        dt = datetime.strptime(raw.strip(), "%Y/%m/%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


class FansiGoScraper(BaseScraper):
    provider = PROVIDER

    def __init__(self) -> None:
        self._artist_parser = ArtistParser()

    async def fetch(self) -> str:
        """Launch headless Chromium, wait for event cards to render, return HTML."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(LISTING_URL, wait_until="networkidle", timeout=60_000)
            await page.wait_for_selector("div.card-body", timeout=15_000)
            content = await page.content()
            await browser.close()
        return content

    def parse(self, content: str) -> list[EventRaw]:
        soup = BeautifulSoup(content, "html.parser")
        events: list[EventRaw] = []

        for card_body in soup.select("div.card-body"):
            try:
                event = self._parse_card(card_body)
                if event:
                    events.append(event)
            except Exception:
                continue

        return events

    def _parse_card(self, card_body: Tag) -> EventRaw | None:
        # Outer <a href="/events/{EVENTID}">
        a_tag = card_body.find_parent("a")
        if not a_tag:
            return None
        href = str(a_tag.get("href", ""))
        # e.g. "https://go.fansi.me/events/100101" or "/events/100101"
        provider_event_id = href.rstrip("/").split("/")[-1]
        if not provider_event_id:
            return None
        ticket_url = href if href.startswith("http") else f"{BASE_URL}{href}"

        # Venue name — first <p> inside card-body
        venue_el = card_body.select_one("p.text-gray-76")
        venue_name = venue_el.get_text(strip=True) if venue_el else "未知場地"
        venue_info = venue_lookup(venue_name)

        # Title — <h3>
        title_el = card_body.select_one("h3")
        title = title_el.get_text(strip=True) if title_el else ""
        if not title:
            return None

        # Date — <time datetime="YYYY/MM/DD">
        time_el = card_body.select_one("time[datetime]")
        if not time_el:
            return None
        start_at = _parse_date(str(time_el.get("datetime", "")))
        if not start_at:
            return None

        artist_names = self._artist_parser.parse(title)

        return EventRaw(
            provider=PROVIDER,
            provider_event_id=provider_event_id,
            title=title,
            start_at=start_at,
            end_at=None,
            min_price=None,
            max_price=None,
            price_type=PriceType.tbd,
            ticket_url=ticket_url,
            info_url=None,
            venue_name=venue_name,
            venue_city=venue_info.city,
            venue_address=venue_info.address,
            artist_names=artist_names,
        )
