from typing import Optional, Dict, Any
from .base import SignalGenerator

class VacancySignal(SignalGenerator):
    def generate(self, property_record: Any) -> Optional[Dict[str, Any]]:
        if getattr(property_record, 'is_vacant', False):
            return {
                "signal_type": "VACANCY_SIGNAL",
                "value_numeric": None,
                "value_boolean": True,
                "confidence": 1.0,
                "evidence": "Public source explicitly indicates property is vacant."
            }
        return None
