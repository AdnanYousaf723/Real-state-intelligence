import re
import pandas as pd
from typing import Optional

def normalize_currency(val) -> Optional[float]:
    """
    Extracts a clean float from messy currency strings.
    Converts "$450,000", "450000", or "320,000 USD" into 450000.0
    """
    if pd.isna(val) or val == "":
        return None
    if isinstance(val, (int, float)):
        return float(val)
    
    # Remove '$', ',', and alphabetical characters (like 'USD')
    clean = re.sub(r'[^\d.-]', '', str(val))
    if not clean:
        return None
        
    try:
        return float(clean)
    except ValueError:
        return None

def normalize_year(val) -> Optional[int]:
    """
    Extracts a clean 4-digit integer year.
    """
    if pd.isna(val) or val == "":
        return None
    if isinstance(val, (int, float)):
        return int(val)
    
    # Strip any non-digit characters
    clean = re.sub(r'[^\d]', '', str(val))
    if not clean:
        return None
        
    try:
        return int(clean)
    except ValueError:
        return None

def normalize_square_feet(val) -> Optional[float]:
    """
    Extracts square footage from strings like '2,400 sqft'
    """
    if pd.isna(val) or val == "":
        return None
    if isinstance(val, (int, float)):
        return float(val)
        
    # Isolate numbers before typical text suffixes
    clean = str(val).lower().replace(',', '')
    # Match the first sequence of digits/decimals
    match = re.search(r'(\d+(?:\.\d+)?)', clean)
    if match:
        return float(match.group(1))
    return None
