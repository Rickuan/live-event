from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Genre
from app.schemas import GenreSchema

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("", response_model=list[GenreSchema])
def list_genres(db: Annotated[Session, Depends(get_db)]):
    return db.query(Genre).order_by(Genre.name).all()
