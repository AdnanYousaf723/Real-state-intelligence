import pandas as pd
from typing import Optional

def normalize_property_type(prop_type: str) -> str:
    """
    Maps various string formats to standard PropertyType enumerations.
    """
    if pd.isna(prop_type) or not isinstance(prop_type, str):
        return "UNKNOWN"
        
    pt_clean = prop_type.lower().strip()
    
    # Hardcoded mapping based on common real estate notations
    mapping = {
        "sfr": "SINGLE_FAMILY",
        "single family": "SINGLE_FAMILY",
        "single-family residence": "SINGLE_FAMILY",
        "single_family": "SINGLE_FAMILY",
        
        "condo": "CONDO",
        "condominium": "CONDO",
        
        "townhouse": "TOWNHOUSE",
        "townhome": "TOWNHOUSE",
        
        "multi family": "MULTI_FAMILY",
        "multi_family": "MULTI_FAMILY",
        "multifamily": "MULTI_FAMILY",
        "duplex": "MULTI_FAMILY",
        "triplex": "MULTI_FAMILY",
        
        "commercial": "COMMERCIAL",
        "retail": "COMMERCIAL",
        "office": "COMMERCIAL",
        
        "land": "LAND",
        "vacant land": "LAND",
        "lot": "LAND"
    }
    
    return mapping.get(pt_clean, "UNKNOWN")
