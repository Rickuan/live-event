"""
Entry point for the scraper.

Local usage:
    cd backend
    python -m scraper.run

GitHub Actions runs this via the same command with DATABASE_URL set as a secret.
"""

import asyncio
import logging
import sys

from app.cleanup import delete_expired_events
from app.database import SessionLocal
from app.models import ScraperLog
from scraper.fansi_go import FansiGoScraper
from scraper.whitelist import WhitelistFilter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)


async def run_scraper() -> None:
    scraper = FansiGoScraper()
    whitelist = WhitelistFilter()
    db = SessionLocal()

    try:
        log.info("Fetching events from %s...", scraper.provider)
        raw_events = await scraper.run()
        log.info("Fetched %d raw events", len(raw_events))

        filtered = whitelist.filter(raw_events)
        log.info("Passed whitelist: %d events", len(filtered))

        from scraper.upsert import UpsertRunner
        runner = UpsertRunner(db)
        upserted = runner.run(filtered)
        log.info("Upserted %d events", upserted)

        has_warning = upserted == 0
        if has_warning:
            log.warning(
                "events_count is 0 after scraping %s — possible site change or parsing failure",
                scraper.provider,
            )

        db.add(
            ScraperLog(
                provider=scraper.provider,
                events_count=upserted,
                has_warning=has_warning,
            )
        )
        db.commit()

        # Cleanup expired events (> 400 days old)
        deleted = delete_expired_events(db)
        if deleted:
            log.info("Deleted %d expired events (> 400 days old)", deleted)

    except Exception as exc:
        log.error("Scraper failed: %s", exc, exc_info=True)
        db.add(ScraperLog(provider=scraper.provider, events_count=0, has_warning=True))
        db.commit()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(run_scraper())
