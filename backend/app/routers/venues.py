from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Venue

router = APIRouter(prefix="/venues", tags=["venues"])


@router.get("/cities", response_model=list[str])
def list_cities(db: Annotated[Session, Depends(get_db)]):
    rows = db.query(Venue.city).distinct().order_by(Venue.city).all()
    return [r.city for r in rows]
