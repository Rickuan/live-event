from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models import Event

RETENTION_DAYS = 400


def delete_expired_events(db: Session) -> int:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=RETENTION_DAYS)
    deleted = (
        db.query(Event)
        .filter(Event.start_at < cutoff)
        .all()
    )
    count = len(deleted)
    for event in deleted:
        db.delete(event)
    db.commit()
    return count
