from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class PropertyRecord(BaseModel):
    """The canonical internal representation of a property."""
    model_config = ConfigDict(from_attributes=True)

    # Identifiers
    source_id: str
    source_record_id: str
    canonical_key: Optional[str] = None
    parcel_id: Optional[str] = None

    # Location
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    county: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Characteristics
    property_type: Optional[str] = None
    property_subtype: Optional[str] = None
    year_built: Optional[int] = None
    bedrooms: Optional[float] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[float] = None
    lot_size: Optional[float] = None
    
    # Financial/History
    assessed_value: Optional[float] = None
    estimated_value: Optional[float] = None
    last_sale_price: Optional[float] = None
    last_sale_date: Optional[date] = None
    
    # Status
    owner_occupied: Optional[bool] = None
    absentee_owner: Optional[bool] = False
    is_vacant: Optional[bool] = False
    tax_issue: Optional[bool] = False
    distress_issue: Optional[bool] = False
