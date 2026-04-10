from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Artist, Event, EventArtist, Venue
from scraper.base import EventRaw


class UpsertRunner:
    def __init__(self, db: Session) -> None:
        self.db = db

    def run(self, events: list[EventRaw]) -> int:
        count = 0
        for raw in events:
            self._upsert_event(raw)
            count += 1
        self.db.commit()
        return count

    def _get_or_create_venue(self, name: str, city: str, address: str | None) -> Venue:
        venue = self.db.query(Venue).filter_by(name=name, city=city).first()
        if not venue:
            venue = Venue(name=name, city=city, address=address)
            self.db.add(venue)
            self.db.flush()
        return venue

    def _get_or_create_artist(self, name: str) -> Artist:
        artist = self.db.query(Artist).filter_by(name=name).first()
        if not artist:
            artist = Artist(name=name)
            self.db.add(artist)
            self.db.flush()
        return artist

    def _upsert_event(self, raw: EventRaw) -> None:
        venue = self._get_or_create_venue(raw.venue_name, raw.venue_city, raw.venue_address)

        event = (
            self.db.query(Event)
            .filter_by(provider=raw.provider, provider_event_id=raw.provider_event_id)
            .first()
        )

        if event:
            # Update mutable fields; preserve admin flags (is_hidden)
            event.title = raw.title
            event.start_at = raw.start_at
            event.end_at = raw.end_at
            event.min_price = raw.min_price
            event.max_price = raw.max_price
            event.price_type = raw.price_type
            event.ticket_url = raw.ticket_url
            event.info_url = raw.info_url
            event.venue_id = venue.id
            event.scraped_at = datetime.now(tz=timezone.utc)
        else:
            event = Event(
                title=raw.title,
                start_at=raw.start_at,
                end_at=raw.end_at,
                min_price=raw.min_price,
                max_price=raw.max_price,
                price_type=raw.price_type,
                ticket_url=raw.ticket_url,
                info_url=raw.info_url,
                venue_id=venue.id,
                provider=raw.provider,
                provider_event_id=raw.provider_event_id,
            )
            self.db.add(event)
            self.db.flush()

        # Sync artists
        self.db.query(EventArtist).filter_by(event_id=event.id).delete()
        for name in raw.artist_names:
            artist = self._get_or_create_artist(name)
            self.db.add(EventArtist(event_id=event.id, artist_id=artist.id))
