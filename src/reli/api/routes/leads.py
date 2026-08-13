from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from reli.api.dependencies import get_db
from reli.api.schemas.leads import LeadSchema, LeadDetailResponse
from reli.database.models import Lead, Property

router = APIRouter()

@router.get("/leads", response_model=List[LeadDetailResponse])
def get_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Include related property via ORM
    return db.query(Lead).order_by(Lead.score.desc()).offset(skip).limit(limit).all()

@router.get("/leads/{lead_id}", response_model=LeadDetailResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # We construct the response dynamically as SQLAlchemy will lazy-load the relationships
    return {
        **db_lead.__dict__,
        "property": db_lead.property,
        "signals": db_lead.property.signals
    }
