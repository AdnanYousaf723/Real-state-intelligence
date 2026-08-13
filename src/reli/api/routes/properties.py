from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from reli.api.dependencies import get_db
from reli.api.schemas.properties import PropertyResponse
from reli.database.models import Property

router = APIRouter()

@router.get("/properties", response_model=List[PropertyResponse])
def get_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Property).offset(skip).limit(limit).all()

@router.get("/properties/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    db_prop = db.query(Property).filter(Property.id == property_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_prop
