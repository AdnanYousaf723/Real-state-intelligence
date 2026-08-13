import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from reli.database.connection import Base
from reli.pipeline.runner import PipelineRunner
from reli.ingestion.csv_source import CSVDataSource
from reli.database.models import Property, Lead

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_full_pipeline_run(db_session):
    # Setup
    fixture_path = os.path.join(os.path.dirname(__file__), "../fixtures/dirty_properties.csv")
    source = CSVDataSource(file_path=fixture_path, source_name="test_csv")
    runner = PipelineRunner(db_session)
    
    # Execute
    ctx = runner.run(source, "test_csv")
    
    # Assert context metrics
    assert ctx.records_received == 6
    # 789 Pine Rd has no city and invalid year; 555 ERROR ST has 999 zip, 1750 year, -500 price
    # Both should be rejected based on schemas, so valid should be 4
    assert ctx.records_valid == 4
    assert ctx.records_rejected == 2
    
    # Deduplication should find 2 duplicates (123 Main St has 3 variations, so 2 are duplicates of the 1st)
    assert ctx.duplicates_found == 2
    
    # Assert DB State
    properties = db_session.query(Property).all()
    # 4 valid records - 2 duplicates = 2 unique properties stored
    assert len(properties) == 2
    
    # 123 Main St should have a high score because absentee=True (15) and last_sale is 2001 (20+ years = 25) => 40 points (Medium)
    main_st = db_session.query(Property).filter(Property.address_line_1 == "123 MAIN ST.").first()
    assert main_st is not None
    assert main_st.lead is not None
    assert main_st.lead.score == 40
    assert main_st.lead.priority == "MEDIUM"

    # 456 Oak Ave has absentee=False, no other signals triggering > 0, so no lead might be created if score is 0. 
    # Let's check. Actually, wait. The test says 1 lead might be created or 2 depending on if Oak Ave triggers anything.
    # Oak ave: 2015 last sale = 11 years (no points). So score 0. Lead shouldn't be generated.
    assert ctx.leads_generated == 1
