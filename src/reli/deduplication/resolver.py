from enum import Enum
from typing import Optional, List, Dict, Any
from .exact import generate_canonical_key
from .fuzzy import calculate_similarity

class MatchDecision(Enum):
    AUTO_MERGED = "AUTO_MERGED"
    REVIEW = "REVIEW"
    REJECTED = "REJECTED"
    NEW_RECORD = "NEW_RECORD"

class DeduplicationResolver:
    """
    Orchestrates the 3-level deduplication strategy:
    Level 1: Exact identifier (parcel_id)
    Level 2: Canonical address key
    Level 3: Fuzzy matching on address string
    """
    def __init__(self, exact_match_threshold: float = 0.97, review_threshold: float = 0.90):
        self.exact_match_threshold = exact_match_threshold
        self.review_threshold = review_threshold

    def resolve(self, new_record: Any, existing_records: List[Any]) -> Dict[str, Any]:
        """
        Attempts to find a match for new_record within existing_records.
        Returns a dict containing the decision, the matched record (if any), and reason.
        """
        # Level 1: Exact Identifier (Parcel ID)
        if getattr(new_record, "parcel_id", None):
            for existing in existing_records:
                if getattr(existing, "parcel_id", None) == new_record.parcel_id:
                    return {"decision": MatchDecision.AUTO_MERGED, "match": existing, "reason": "Exact parcel_id match", "similarity": 1.0}

        # Level 2: Canonical Address Key
        if getattr(new_record, "canonical_key", None):
            for existing in existing_records:
                if getattr(existing, "canonical_key", None) == new_record.canonical_key:
                    return {"decision": MatchDecision.AUTO_MERGED, "match": existing, "reason": "Canonical address key match", "similarity": 1.0}

        # Level 3: Fuzzy Matching (constrained by location)
        best_match = None
        highest_score = 0.0

        for existing in existing_records:
            # Only compare if they are in the same general area
            if existing.zip_code == new_record.zip_code and existing.city.lower() == new_record.city.lower():
                score = calculate_similarity(new_record.address_line_1, existing.address_line_1)
                if score > highest_score:
                    highest_score = score
                    best_match = existing

        if best_match:
            if highest_score >= self.exact_match_threshold:
                return {"decision": MatchDecision.AUTO_MERGED, "match": best_match, "reason": "Fuzzy match above automatic threshold", "similarity": highest_score}
            elif highest_score >= self.review_threshold:
                return {"decision": MatchDecision.REVIEW, "match": best_match, "reason": "Fuzzy match requires manual review", "similarity": highest_score}
            else:
                return {"decision": MatchDecision.REJECTED, "match": best_match, "reason": "Fuzzy match below threshold", "similarity": highest_score}

        return {"decision": MatchDecision.NEW_RECORD, "match": None, "reason": "No match candidates found", "similarity": 0.0}
