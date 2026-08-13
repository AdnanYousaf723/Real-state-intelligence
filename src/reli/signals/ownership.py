from typing import Optional, Dict, Any
from datetime import date
from .base import SignalGenerator

class LongOwnershipSignal(SignalGenerator):
    def generate(self, property_record: Any) -> Optional[Dict[str, Any]]:
        last_sale_date = getattr(property_record, 'last_sale_date', None)
        if not last_sale_date:
            return None
        
        today = date.today()
        # Approximate years calculation
        days_owned = (today - last_sale_date).days
        years_owned = days_owned / 365.25
        
        if years_owned >= 15.0:
            return {
                "signal_type": "LONG_OWNERSHIP",
                "value_numeric": round(years_owned, 2),
                "value_boolean": True,
                "confidence": 1.0,
                "evidence": f"Ownership duration is {years_owned:.1f} years."
            }
        return None
