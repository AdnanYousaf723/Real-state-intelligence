import logging
from sqlalchemy.orm import Session
from typing import Optional

from reli.ingestion.base import DataSource
from reli.pipeline.context import PipelineContext
from reli.pipeline.stages import PipelineStages
from reli.database.repositories import PipelineRepository
from reli.deduplication.resolver import MatchDecision
from reli.database.models import PipelineRun

logger = logging.getLogger(__name__)

class PipelineRunner:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.pipeline_repo = PipelineRepository(self.db)
        self.stages = PipelineStages(self.db)

    def run(self, source: DataSource, source_name: str) -> PipelineContext:
        """Executes the full pipeline for a given data source."""
        # Check for incremental state
        last_run = self.db.query(PipelineRun).filter(PipelineRun.source == source_name, PipelineRun.status == "SUCCESS").order_by(PipelineRun.finished_at.desc()).first()
        is_incremental = last_run is not None
        
        # Create pipeline run tracking in DB
        db_run = self.pipeline_repo.create_run(source=source_name)
        ctx = PipelineContext(run_id=db_run.id, source=source_name, is_incremental=is_incremental)
        
        try:
            logger.info(f"[Run {ctx.run_id}] START Ingestion from {source_name} (Incremental: {is_incremental})")
            df = source.fetch()
            ctx.records_received = len(df)
            logger.info(f"[Run {ctx.run_id}] END Ingestion. Received {ctx.records_received} records.")

            if ctx.records_received == 0:
                self.pipeline_repo.complete_run(db_run, "SUCCESS", ctx.get_metrics())
                return ctx

            logger.info(f"[Run {ctx.run_id}] START Validation")
            valid_df, rejected_df, report = self.stages.validate(df)
            ctx.records_valid = report['valid']
            ctx.records_rejected = report['rejected']
            ctx.valid_df = valid_df
            ctx.rejected_df = rejected_df
            logger.info(f"[Run {ctx.run_id}] END Validation. Valid: {ctx.records_valid}, Rejected: {ctx.records_rejected}")

            logger.info(f"[Run {ctx.run_id}] START Normalization")
            canonical_records = self.stages.normalize_to_canonical(valid_df, source_name)
            ctx.canonical_records = canonical_records
            logger.info(f"[Run {ctx.run_id}] END Normalization")

            # Process individual records
            logger.info(f"[Run {ctx.run_id}] START Deduplication, Enrichment, Scoring & Persistence")
            for record in canonical_records:
                try:
                    # Deduplication
                    decision, match = self.stages.deduplicate(record)
                    if decision == MatchDecision.AUTO_MERGED:
                        ctx.duplicates_found += 1
                        # In a real incremental setup, we would update `last_seen_at` on the existing record here
                        continue
                    
                    # Enrichment (Skipped for now per spec MVP)
                    ctx.records_enriched += 1
                    
                    # Signals
                    signals = self.stages.generate_signals(record)
                    ctx.signals_generated += len(signals)
                    
                    # Score
                    lead_data = self.stages.score(signals)
                    if lead_data['score'] > 0:
                        ctx.leads_generated += 1
                        
                    # Persist
                    self.stages.persist_property_and_lead(record, signals, lead_data)
                    
                except Exception as e:
                    logger.error(f"[Run {ctx.run_id}] Error processing record {record.canonical_key}: {e}")
                    ctx.error_count += 1
                    
            logger.info(f"[Run {ctx.run_id}] END Deduplication, Enrichment, Scoring & Persistence")
            
            # Finalize run
            self.pipeline_repo.complete_run(db_run, "SUCCESS", ctx.get_metrics())
            logger.info(f"[Run {ctx.run_id}] Pipeline completed successfully.")
            return ctx
            
        except Exception as e:
            logger.exception(f"[Run {ctx.run_id}] Pipeline failed: {e}")
            self.pipeline_repo.complete_run(db_run, "FAILED", ctx.get_metrics())
            raise
