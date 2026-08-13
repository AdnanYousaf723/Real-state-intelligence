import os
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from reli.api.dependencies import get_db
from reli.api.schemas.pipeline import PipelineRunSchema, PipelineRunRequest
from reli.database.models import PipelineRun
from reli.pipeline.runner import PipelineRunner
from reli.ingestion.csv_source import CSVDataSource
from reli.ingestion.attom_source import ATTOMDataSource

router = APIRouter()

def execute_pipeline(db: Session, source_name: str):
    runner = PipelineRunner(db)
    
    if source_name == "sample_csv":
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        file_path = os.path.join(base_dir, "data", "sample", "properties.csv")
        source = CSVDataSource(file_path=file_path)
    elif source_name == "attom":
        source = ATTOMDataSource()
    else:
        raise ValueError(f"Unknown source: {source_name}")
        
    runner.run(source, source_name)

@router.get("/pipeline/runs", response_model=List[PipelineRunSchema])
def get_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(PipelineRun).order_by(PipelineRun.started_at.desc()).offset(skip).limit(limit).all()

@router.post("/pipeline/run")
def trigger_run(request: PipelineRunRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        # Trigger synchronously for testing simplicity
        execute_pipeline(db, request.source)
        return {"status": "Pipeline triggered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
