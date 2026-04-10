"""initial

Revision ID: 0001
Revises:
Create Date: 2026-04-09

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
    )

    op.create_table(
        "venues",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("city", sa.String(100), nullable=False),
    )

    op.create_table(
        "artists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False, unique=True),
        sa.Column("genre_id", sa.Integer(), sa.ForeignKey("genres.id"), nullable=True),
    )

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("min_price", sa.Integer(), nullable=True),
        sa.Column("max_price", sa.Integer(), nullable=True),
        sa.Column("price_type", sa.Enum("paid", "free", "donation", "tbd", name="price_type_enum", create_type=True), nullable=False),
        sa.Column("ticket_url", sa.String(1000), nullable=True),
        sa.Column("info_url", sa.String(1000), nullable=True),
        sa.Column("venue_id", sa.Integer(), sa.ForeignKey("venues.id"), nullable=False),
        sa.Column("provider", sa.String(100), nullable=False),
        sa.Column("provider_event_id", sa.String(200), nullable=False),
        sa.Column("is_cancelled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_sold_out", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_hidden", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("scraped_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("provider", "provider_event_id", name="uq_event_provider"),
    )

    op.create_table(
        "event_artists",
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artists.id"), primary_key=True),
    )

    op.create_table(
        "scraper_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(100), nullable=False),
        sa.Column("run_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("events_count", sa.Integer(), nullable=False),
        sa.Column("has_warning", sa.Boolean(), nullable=False, server_default="false"),
    )

    # Index for common queries
    op.create_index("ix_events_start_at", "events", ["start_at"])
    op.create_index("ix_events_is_hidden", "events", ["is_hidden"])


def downgrade() -> None:
    op.drop_table("scraper_logs")
    op.drop_table("event_artists")
    op.drop_index("ix_events_is_hidden", table_name="events")
    op.drop_index("ix_events_start_at", table_name="events")
    op.drop_table("events")
    sa.Enum(name="price_type_enum").drop(op.get_bind())
    op.drop_table("artists")
    op.drop_table("venues")
    op.drop_table("genres")
