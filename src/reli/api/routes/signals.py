from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from reli.api.dependencies import get_db
from reli.api.schemas.properties import SignalSchema
from reli.database.models import Signal

router = APIRouter()

@router.get("/signals", response_model=List[SignalSchema])
def get_signals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Signal).offset(skip).limit(limit).all()
