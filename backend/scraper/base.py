from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from app.models import PriceType


@dataclass
class EventRaw:
    provider: str
    provider_event_id: str
    title: str
    start_at: datetime
    end_at: datetime | None
    min_price: int | None
    max_price: int | None
    price_type: PriceType
    ticket_url: str | None
    info_url: str | None
    venue_name: str
    venue_city: str
    venue_address: str | None = None
    artist_names: list[str] = field(default_factory=list)

    @property
    def searchable_text(self) -> str:
        """Combined text used for whitelist matching."""
        parts = [self.title] + self.artist_names + [self.venue_name]
        return " ".join(parts).lower()


class BaseScraper(ABC):
    provider: str

    @abstractmethod
    async def fetch(self) -> str:
        """Fetch raw HTML (or JSON string) from the provider."""
        ...

    @abstractmethod
    def parse(self, content: str) -> list[EventRaw]:
        """Parse raw content into a list of EventRaw."""
        ...

    async def run(self) -> list[EventRaw]:
        content = await self.fetch()
        return self.parse(content)
