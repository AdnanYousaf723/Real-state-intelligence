from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .properties import PropertyBase, SignalSchema

class LeadSchema(BaseModel):
    id: int
    property_id: int
    score: int
    priority: str
    reason_summary: str
    scoring_version: str
    scored_at: datetime

    class Config:
        from_attributes = True

class LeadDetailResponse(LeadSchema):
    property: PropertyBase
    signals: List[SignalSchema] = []

    class Config:
        from_attributes = True
