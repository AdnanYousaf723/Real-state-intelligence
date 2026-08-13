import pandas as pd
from datetime import date
from typing import Optional

def normalize_date(date_val) -> Optional[date]:
    """
    Parses messy date formats into a standard YYYY-MM-DD python date object.
    Robustly handles formats like '08/14/2020', '2020-08-14', and 'August 14, 2020'.
    """
    if pd.isna(date_val) or date_val == "":
        return None
        
    try:
        # pd.to_datetime is extremely robust for parsing multiple mixed formats
        dt = pd.to_datetime(date_val)
        return dt.date()
    except Exception:
        return None
