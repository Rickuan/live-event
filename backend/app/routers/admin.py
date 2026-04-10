from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_admin, verify_password
from app.config import settings
from app.database import get_db
from app.models import Artist, Event, EventArtist, ScraperLog, Venue
from app.schemas import (
    AdminEventCreateRequest,
    AdminEventPatchRequest,
    AdminHealthResponse,
    AdminLoginRequest,
    AdminLoginResponse,
    EventListResponse,
    EventSchema,
)

router = APIRouter(prefix="/admin", tags=["admin"])

Admin = Annotated[str, Depends(get_current_admin)]


# ── Auth ──────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=AdminLoginResponse)
def login(body: AdminLoginRequest):
    if body.username != settings.admin_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(body.password, settings.admin_password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=body.username)
    return AdminLoginResponse(access_token=token)


# ── Health ────────────────────────────────────────────────────────────────────

@router.get("/health", response_model=AdminHealthResponse)
def health(_: Admin, db: Annotated[Session, Depends(get_db)]):
    log = (
        db.query(ScraperLog)
        .order_by(ScraperLog.run_at.desc())
        .first()
    )
    if not log:
        return AdminHealthResponse(provider="fansi_go", run_at=None, events_count=None, has_warning=False)
    return AdminHealthResponse(
        provider=log.provider,
        run_at=log.run_at,
        events_count=log.events_count,
        has_warning=log.has_warning,
    )


# ── Events ────────────────────────────────────────────────────────────────────

@router.get("/events", response_model=EventListResponse)
def list_all_events(_: Admin, db: Annotated[Session, Depends(get_db)]):
    """Return all events including hidden ones, ordered by start_at desc."""
    from app.models import EventArtist as EA
    from sqlalchemy.orm import joinedload
    events = (
        db.query(Event)
        .options(
            joinedload(Event.venue),
            joinedload(Event.event_artists).joinedload(EA.artist),
        )
        .order_by(Event.start_at.desc())
        .all()
    )
    items = [EventSchema.from_orm_with_artists(e) for e in events]
    return EventListResponse(items=items, total=len(items))

@router.post("/events", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
def create_event(body: AdminEventCreateRequest, _: Admin, db: Annotated[Session, Depends(get_db)]):
    venue = db.query(Venue).filter_by(name=body.venue_name, city=body.venue_city).first()
    if not venue:
        venue = Venue(name=body.venue_name, city=body.venue_city, address=body.venue_address)
        db.add(venue)
        db.flush()

    event = Event(
        title=body.title,
        start_at=body.start_at,
        end_at=body.end_at,
        min_price=body.min_price,
        max_price=body.max_price,
        price_type=body.price_type,
        ticket_url=body.ticket_url,
        info_url=body.info_url,
        venue_id=venue.id,
        provider="manual",
        provider_event_id=f"manual-{body.title[:40]}",
    )
    db.add(event)
    db.flush()

    for name in body.artist_names:
        artist = db.query(Artist).filter_by(name=name).first()
        if not artist:
            artist = Artist(name=name)
            db.add(artist)
            db.flush()
        db.add(EventArtist(event_id=event.id, artist_id=artist.id))

    db.commit()
    db.refresh(event)
    return EventSchema.from_orm_with_artists(event)


@router.patch("/events/{event_id}", response_model=EventSchema)
def patch_event(event_id: int, body: AdminEventPatchRequest, _: Admin, db: Annotated[Session, Depends(get_db)]):
    event = db.query(Event).filter_by(id=event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if body.is_hidden is not None:
        event.is_hidden = body.is_hidden
    if body.is_cancelled is not None:
        event.is_cancelled = body.is_cancelled
    if body.is_sold_out is not None:
        event.is_sold_out = body.is_sold_out

    db.commit()
    db.refresh(event)
    return EventSchema.from_orm_with_artists(event)


# ── Scraper trigger ───────────────────────────────────────────────────────────

_KNOWN_PROVIDERS = {"fansi_go"}


@router.post("/scrape/{provider}", status_code=status.HTTP_202_ACCEPTED)
async def trigger_scrape(provider: str, background_tasks: BackgroundTasks, _: Admin):
    if provider not in _KNOWN_PROVIDERS:
        raise HTTPException(status_code=404, detail=f"Unknown provider: {provider}")
    from scraper.run import run_scraper
    background_tasks.add_task(run_scraper)
    return {"message": f"Scrape for '{provider}' started"}
