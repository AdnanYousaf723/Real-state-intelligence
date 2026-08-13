from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    source_type = Column(String)
    base_url = Column(String, nullable=True)
    license = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    canonical_key = Column(String, unique=True, index=True)
    parcel_id = Column(String, index=True, nullable=True)
    address_line_1 = Column(String)
    address_line_2 = Column(String, nullable=True)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    county = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    property_type = Column(String, nullable=True)
    property_subtype = Column(String, nullable=True)
    year_built = Column(Integer, nullable=True)
    bedrooms = Column(Float, nullable=True)
    bathrooms = Column(Float, nullable=True)
    square_feet = Column(Float, nullable=True)
    lot_size = Column(Float, nullable=True)
    assessed_value = Column(Float, nullable=True)
    estimated_value = Column(Float, nullable=True)
    last_sale_price = Column(Float, nullable=True)
    last_sale_date = Column(Date, nullable=True)
    owner_occupied = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    signals = relationship("Signal", back_populates="property")
    lead = relationship("Lead", back_populates="property", uselist=False)

class PropertySource(Base):
    __tablename__ = "property_sources"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    source_record_id = Column(String)
    raw_hash = Column(String, nullable=True)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint('source_id', 'source_record_id', name='uix_source_record'),)

class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    signal_type = Column(String)
    value_numeric = Column(Float, nullable=True)
    value_boolean = Column(Boolean, nullable=True)
    confidence = Column(Float)
    evidence = Column(Text)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())

    property = relationship("Property", back_populates="signals")

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), unique=True)
    score = Column(Integer)
    priority = Column(String)
    reason_summary = Column(Text)
    scoring_version = Column(String)
    scored_at = Column(DateTime(timezone=True), server_default=func.now())

    property = relationship("Property", back_populates="lead")

class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String)
    source = Column(String)
    records_received = Column(Integer, default=0)
    records_valid = Column(Integer, default=0)
    records_rejected = Column(Integer, default=0)
    duplicates_found = Column(Integer, default=0)
    records_enriched = Column(Integer, default=0)
    signals_generated = Column(Integer, default=0)
    leads_generated = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    duration_seconds = Column(Float, nullable=True)
