from typing import Optional, Dict, Any
from .base import SignalGenerator

class TaxIssueSignal(SignalGenerator):
    def generate(self, property_record: Any) -> Optional[Dict[str, Any]]:
        if getattr(property_record, 'tax_issue', False):
            return {
                "signal_type": "TAX_SIGNAL",
                "value_numeric": None,
                "value_boolean": True,
                "confidence": 1.0,
                "evidence": "Public tax delinquency or related tax issue detected."
            }
        return None
