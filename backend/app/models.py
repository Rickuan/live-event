import enum
from datetime import datetime
from sqlalchemy import (
    Boolean, DateTime, Enum, ForeignKey, Integer, String, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class PriceType(enum.Enum):
    paid = "paid"
    free = "free"
    donation = "donation"
    tbd = "tbd"


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    artists: Mapped[list["Artist"]] = relationship("Artist", back_populates="genre")


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(100), nullable=False)

    events: Mapped[list["Event"]] = relationship("Event", back_populates="venue")


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    genre_id: Mapped[int | None] = mapped_column(ForeignKey("genres.id"), nullable=True)

    genre: Mapped[Genre | None] = relationship("Genre", back_populates="artists")
    event_artists: Mapped[list["EventArtist"]] = relationship("EventArtist", back_populates="artist")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    min_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price_type: Mapped[PriceType] = mapped_column(
        Enum(PriceType, name="price_type_enum"), nullable=False, default=PriceType.tbd
    )
    ticket_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    info_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_event_id: Mapped[str] = mapped_column(String(200), nullable=False)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_sold_out: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    venue: Mapped[Venue] = relationship("Venue", back_populates="events")
    event_artists: Mapped[list["EventArtist"]] = relationship(
        "EventArtist", back_populates="event", cascade="all, delete-orphan"
    )


class EventArtist(Base):
    __tablename__ = "event_artists"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), primary_key=True)

    event: Mapped[Event] = relationship("Event", back_populates="event_artists")
    artist: Mapped[Artist] = relationship("Artist", back_populates="event_artists")


class ScraperLog(Base):
    __tablename__ = "scraper_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    run_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    events_count: Mapped[int] = mapped_column(Integer, nullable=False)
    has_warning: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
