from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

class SignalSchema(BaseModel):
    id: int
    signal_type: str
    value_numeric: Optional[float] = None
    value_boolean: Optional[bool] = None
    confidence: float
    evidence: str
    detected_at: datetime

    class Config:
        from_attributes = True

class PropertyBase(BaseModel):
    id: int
    canonical_key: str
    parcel_id: Optional[str] = None
    address_line_1: str
    city: str
    state: str
    zip_code: str
    property_type: Optional[str] = None
    year_built: Optional[int] = None
    bedrooms: Optional[float] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[float] = None
    last_sale_price: Optional[float] = None
    last_sale_date: Optional[date] = None

class PropertyResponse(PropertyBase):
    signals: List[SignalSchema] = []

    class Config:
        from_attributes = True
