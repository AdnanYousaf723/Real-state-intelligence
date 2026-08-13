import pytest
import pandas as pd
from datetime import date
from reli.normalization.address import normalize_address
from reli.normalization.dates import normalize_date
from reli.normalization.numbers import normalize_currency, normalize_year, normalize_square_feet
from reli.normalization.property_types import normalize_property_type
from reli.validation.schemas import check_valid_year, check_valid_numeric, check_zip_code
from reli.deduplication.exact import generate_canonical_key
from reli.deduplication.fuzzy import calculate_similarity

def test_address_normalization():
    assert normalize_address("123 MAIN ST.") == "123 main st"
    assert normalize_address("123 Main Street") == "123 main st"
    assert normalize_address("123   Main   St") == "123 main st"

def test_currency_normalization():
    assert normalize_currency("$450,000") == 450000.0
    assert normalize_currency("450000") == 450000.0
    assert normalize_currency("320,000 USD") == 320000.0
    assert normalize_currency("invalid") is None

def test_date_normalization():
    assert normalize_date("2020-08-14") == date(2020, 8, 14)
    assert normalize_date("08/14/2020") == date(2020, 8, 14)

def test_property_type_normalization():
    assert normalize_property_type("SFR") == "SINGLE_FAMILY"
    assert normalize_property_type("Single Family") == "SINGLE_FAMILY"
    assert normalize_property_type("Condo") == "CONDO"
    assert normalize_property_type("Random") == "UNKNOWN"

def test_validation_rules():
    assert check_zip_code("80202") is True
    assert check_zip_code("802") is False
    assert check_valid_year("1985") is True
    assert check_valid_year("1750") is False
    assert check_valid_year("nineteen") is False
    assert check_valid_numeric("450000") is True
    assert check_valid_numeric("-500") is False

def test_canonical_key():
    k1 = generate_canonical_key("123 main st", "Denver", "CO", "80202")
    k2 = generate_canonical_key("123 main st", "denver ", "co", " 80202")
    assert k1 == "123-main-st|denver|co|80202"
    assert k1 == k2

def test_fuzzy_match():
    sim = calculate_similarity("123 Main Street", "123 Main St")
    assert sim > 0.90
