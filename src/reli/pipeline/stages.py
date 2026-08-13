import logging
import pandas as pd
from typing import List, Tuple

from reli.models.domain import PropertyRecord
from reli.validation.validator import DataValidator
from reli.normalization.address import normalize_address
from reli.normalization.dates import normalize_date
from reli.normalization.numbers import normalize_currency, normalize_year, normalize_square_feet
from reli.normalization.property_types import normalize_property_type
from reli.deduplication.exact import generate_canonical_key
from reli.deduplication.resolver import DeduplicationResolver, MatchDecision
from reli.signals.absentee import AbsenteeOwnerSignal
from reli.signals.ownership import LongOwnershipSignal
from reli.signals.vacancy import VacancySignal
from reli.signals.tax import TaxIssueSignal
from reli.signals.distress import DistressSignal
from reli.scoring.scorer import LeadScorer
from reli.database.repositories import PropertyRepository
from reli.database.models import Signal, Lead

logger = logging.getLogger(__name__)

class PipelineStages:
    def __init__(self, db_session):
        self.db = db_session
        self.validator = DataValidator()
        self.dedup_resolver = DeduplicationResolver()
        self.scorer = LeadScorer()
        self.property_repo = PropertyRepository(self.db)
        
        self.signal_generators = [
            AbsenteeOwnerSignal(),
            LongOwnershipSignal(),
            VacancySignal(),
            TaxIssueSignal(),
            DistressSignal()
        ]

    def validate(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, dict]:
        """Validates incoming raw dataframe."""
        valid_df, rejected_df, report = self.validator.validate_properties(df)
        return valid_df, rejected_df, report

    def normalize_to_canonical(self, df: pd.DataFrame, source_name: str) -> List[PropertyRecord]:
        """Converts raw validated dataframe rows into normalized PropertyRecords."""
        records = []
        for idx, row in df.iterrows():
            try:
                # Fallbacks and basic parsing
                raw_address = str(row.get('raw_address', ''))
                city = str(row.get('city', ''))
                state = str(row.get('state', ''))
                zip_code = str(row.get('zip_code', ''))
                
                # Normalization
                norm_addr = normalize_address(raw_address)
                c_key = generate_canonical_key(norm_addr, city, state, zip_code)
                
                absentee = str(row.get('absentee_owner', '')).lower() == 'true'
                vacant = str(row.get('is_vacant', '')).lower() == 'true'
                
                # Instantiate canonical model
                record = PropertyRecord(
                    source_id=source_name,
                    source_record_id=raw_address,  # Fallback source record ID for MVP
                    canonical_key=c_key,
                    address_line_1=raw_address,  # Store original as requested
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    property_type=normalize_property_type(row.get('property_type')),
                    year_built=normalize_year(row.get('year_built')),
                    last_sale_price=normalize_currency(row.get('last_sale_price')),
                    last_sale_date=normalize_date(row.get('last_sale_date')),
                    absentee_owner=absentee,
                    is_vacant=vacant
                )
                records.append(record)
            except Exception as e:
                logger.error(f"Error normalizing row {idx}: {e}")
        return records

    def deduplicate(self, record: PropertyRecord) -> Tuple[MatchDecision, any]:
        """Checks for existing record in database."""
        # Check by canonical key
        if record.canonical_key:
            existing = self.property_repo.get_by_canonical_key(record.canonical_key)
            if existing:
                return MatchDecision.AUTO_MERGED, existing
        
        # Fuzzy logic can be added later using db queries if needed, skipping for MVP exact match
        return MatchDecision.NEW_RECORD, None

    def generate_signals(self, record: PropertyRecord) -> List[dict]:
        """Generates signals based on property characteristics."""
        signals = []
        for generator in self.signal_generators:
            sig = generator.generate(record)
            if sig:
                signals.append(sig)
        return signals

    def score(self, signals: List[dict]) -> dict:
        """Scores a property based on its signals."""
        return self.scorer.score_property(signals)
        
    def persist_property_and_lead(self, record: PropertyRecord, signals: List[dict], lead_data: dict) -> any:
        """Upserts property, writes signals and leads to DB."""
        # For MVP, we insert as new. An upsert requires more complex logic.
        prop_data = record.model_dump(exclude={'source_id', 'source_record_id'})
        db_prop = self.property_repo.create(prop_data)
        
        for sig in signals:
            db_sig = Signal(property_id=db_prop.id, **sig)
            self.db.add(db_sig)
            
        if lead_data['score'] > 0:
            db_lead = Lead(
                property_id=db_prop.id,
                score=lead_data['score'],
                priority=lead_data['priority'],
                reason_summary=lead_data['reasons'],
                scoring_version=lead_data['scoring_version']
            )
            self.db.add(db_lead)
            
        self.db.commit()
        return db_prop
