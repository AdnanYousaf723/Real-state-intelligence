from typing import Optional, Dict, Any
from .base import SignalGenerator

class AbsenteeOwnerSignal(SignalGenerator):
    def generate(self, property_record: Any) -> Optional[Dict[str, Any]]:
        if getattr(property_record, 'absentee_owner', False):
            return {
                "signal_type": "ABSENTEE_OWNER",
                "value_numeric": None,
                "value_boolean": True,
                "confidence": 1.0,
                "evidence": "Property is marked as absentee-owned in the source record."
            }
        return None
