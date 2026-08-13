import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema
from datetime import datetime

current_year = datetime.now().year

def check_valid_year(year_val) -> bool:
    """Soft validation for year_built strings/ints before normalization."""
    if pd.isna(year_val) or year_val == "": 
        return True
    try:
        y = int(year_val)
        return 1800 <= y <= current_year
    except ValueError:
        return False

def check_valid_numeric(val) -> bool:
    """Soft validation for currency/number strings before normalization."""
    if pd.isna(val) or val == "": 
        return True
    if isinstance(val, (int, float)): 
        return val >= 0
    import re
    # Strip typical currency symbols, commas, and letters like 'USD'
    clean = re.sub(r'[^\d.-]', '', str(val))
    if not clean:
        return False
    try:
        return float(clean) >= 0
    except ValueError:
        return False

def check_zip_code(zip_val) -> bool:
    """Validates standard US ZIP codes (5 or 9 digits)."""
    if pd.isna(zip_val) or zip_val == "":
        return False
    import re
    # Match exactly 5 digits, optionally followed by a dash and 4 digits.
    # Note: we cast to string first in case Pandas read it as an int.
    return bool(re.match(r'^\d{5}(?:-\d{4})?$', str(zip_val).strip()))

# Validation occurs before transformation, so we handle raw string/object types
# but apply custom regex and conversion checks.
raw_property_schema = DataFrameSchema(
    {
        "raw_address": Column(str, Check(lambda s: s.str.strip().str.len() > 0), required=True, nullable=False),
        "city": Column(str, required=True, nullable=False),
        "state": Column(str, required=True, nullable=False),
        "zip_code": Column(object, Check(check_zip_code, element_wise=True), required=True, nullable=False),
        "property_type": Column(str, nullable=True, required=False),
        "year_built": Column(object, Check(check_valid_year, element_wise=True), nullable=True),
        "last_sale_price": Column(object, Check(check_valid_numeric, element_wise=True), nullable=True),
        "last_sale_date": Column(str, nullable=True, required=False),
        "absentee_owner": Column(object, nullable=True, required=False),
    }
)
