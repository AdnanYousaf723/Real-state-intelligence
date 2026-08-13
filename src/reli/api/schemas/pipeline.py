from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PipelineRunSchema(BaseModel):
    id: int
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: str
    source: str
    records_received: int
    records_valid: int
    records_rejected: int
    duplicates_found: int
    records_enriched: int
    signals_generated: int
    leads_generated: int
    error_count: int
    duration_seconds: Optional[float] = None

    class Config:
        from_attributes = True

class PipelineRunRequest(BaseModel):
    source: str = "sample_csv"
