from sqlalchemy.orm import Session
from .models import Property, Source, PipelineRun, Lead, Signal

class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_canonical_key(self, canonical_key: str):
        return self.db.query(Property).filter(Property.canonical_key == canonical_key).first()
        
    def get_by_parcel_id(self, parcel_id: str):
        return self.db.query(Property).filter(Property.parcel_id == parcel_id).first()
        
    def create(self, property_data: dict):
        db_prop = Property(**property_data)
        self.db.add(db_prop)
        self.db.commit()
        self.db.refresh(db_prop)
        return db_prop
        
    def update(self, db_prop: Property, update_data: dict):
        for key, value in update_data.items():
            setattr(db_prop, key, value)
        self.db.commit()
        self.db.refresh(db_prop)
        return db_prop

class PipelineRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_run(self, source: str) -> PipelineRun:
        run = PipelineRun(status="RUNNING", source=source)
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run
        
    def complete_run(self, run: PipelineRun, status: str, metrics: dict):
        run.status = status
        from datetime import datetime
        run.finished_at = datetime.utcnow()
        for k, v in metrics.items():
            if hasattr(run, k):
                setattr(run, k, v)
        if run.started_at and run.finished_at:
            run.duration_seconds = (run.finished_at - run.started_at).total_seconds()
        self.db.commit()
        self.db.refresh(run)
        return run
