from typing import Dict, Any, List

class PipelineContext:
    def __init__(self, run_id: int, source: str, is_incremental: bool = False):
        self.run_id = run_id
        self.source = source
        self.is_incremental = is_incremental
        self.records_received = 0
        self.records_valid = 0
        self.records_rejected = 0
        self.duplicates_found = 0
        self.records_enriched = 0
        self.signals_generated = 0
        self.leads_generated = 0
        self.error_count = 0
        
        # State tracking for data
        self.raw_df = None
        self.valid_df = None
        self.rejected_df = None
        self.canonical_records = []
        self.leads = []
        
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "records_received": self.records_received,
            "records_valid": self.records_valid,
            "records_rejected": self.records_rejected,
            "duplicates_found": self.duplicates_found,
            "records_enriched": self.records_enriched,
            "signals_generated": self.signals_generated,
            "leads_generated": self.leads_generated,
            "error_count": self.error_count
        }
