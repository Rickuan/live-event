from datetime import date, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Event, EventArtist
from app.schemas import EventListResponse, EventSchema

router = APIRouter(prefix="/events", tags=["events"])


def _base_query(db: Session):
    return (
        db.query(Event)
        .options(
            joinedload(Event.venue),
            joinedload(Event.event_artists).joinedload(EventArtist.artist),
        )
        .filter(Event.is_hidden.is_(False))
    )


@router.get("", response_model=EventListResponse)
def list_events(
    db: Annotated[Session, Depends(get_db)],
    city: str | None = None,
    genre_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    include_past: bool = Query(False),
):
    q = _base_query(db)

    if not include_past:
        today = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        q = q.filter(Event.start_at >= today)

    if city:
        from app.models import Venue
        q = q.join(Event.venue).filter(Venue.city == city)

    if genre_id:
        from app.models import Artist, EventArtist as EA
        q = (
            q.join(EA, Event.id == EA.event_id)
            .join(Artist, EA.artist_id == Artist.id)
            .filter(Artist.genre_id == genre_id)
        )

    if date_from:
        q = q.filter(Event.start_at >= datetime(date_from.year, date_from.month, date_from.day, tzinfo=timezone.utc))

    if date_to:
        q = q.filter(Event.start_at < datetime(date_to.year, date_to.month, date_to.day + 1, tzinfo=timezone.utc))

    q = q.order_by(Event.start_at.asc())

    events = q.all()
    items = [EventSchema.from_orm_with_artists(e) for e in events]
    return EventListResponse(items=items, total=len(items))


@router.get("/{event_id}", response_model=EventSchema)
def get_event(event_id: int, db: Annotated[Session, Depends(get_db)]):
    event = _base_query(db).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventSchema.from_orm_with_artists(event)
