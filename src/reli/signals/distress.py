from typing import Optional, Dict, Any
from .base import SignalGenerator

class DistressSignal(SignalGenerator):
    def generate(self, property_record: Any) -> Optional[Dict[str, Any]]:
        if getattr(property_record, 'distress_issue', False):
            return {
                "signal_type": "DISTRESS_SIGNAL",
                "value_numeric": None,
                "value_boolean": True,
                "confidence": 1.0,
                "evidence": "Public record indicates foreclosure, lien, or other distress."
            }
        return None
