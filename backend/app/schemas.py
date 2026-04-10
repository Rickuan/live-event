from datetime import datetime
from pydantic import BaseModel
from app.models import PriceType


class GenreSchema(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class VenueSchema(BaseModel):
    id: int
    name: str
    address: str | None
    city: str

    model_config = {"from_attributes": True}


class ArtistSchema(BaseModel):
    id: int
    name: str
    genre: GenreSchema | None

    model_config = {"from_attributes": True}


class EventSchema(BaseModel):
    id: int
    title: str
    start_at: datetime
    end_at: datetime | None
    min_price: int | None
    max_price: int | None
    price_type: PriceType
    ticket_url: str | None
    info_url: str | None
    venue: VenueSchema
    artists: list[ArtistSchema]
    is_cancelled: bool
    is_sold_out: bool
    provider: str
    scraped_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_artists(cls, event):
        data = {
            **{c.key: getattr(event, c.key) for c in event.__table__.columns},
            "venue": event.venue,
            "artists": [ea.artist for ea in event.event_artists],
        }
        return cls.model_validate(data)


class EventListResponse(BaseModel):
    items: list[EventSchema]
    total: int


class AdminHealthResponse(BaseModel):
    provider: str
    run_at: datetime | None
    events_count: int | None
    has_warning: bool


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminEventPatchRequest(BaseModel):
    is_hidden: bool | None = None
    is_cancelled: bool | None = None
    is_sold_out: bool | None = None


class AdminEventCreateRequest(BaseModel):
    title: str
    start_at: datetime
    end_at: datetime | None = None
    min_price: int | None = None
    max_price: int | None = None
    price_type: PriceType = PriceType.tbd
    ticket_url: str | None = None
    info_url: str | None = None
    venue_name: str
    venue_city: str
    venue_address: str | None = None
    artist_names: list[str] = []
