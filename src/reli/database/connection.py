import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default to local SQLite for MVP as specified in Phase 8
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reli.db")

# SQLite requires specific connect args for multithreading
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for providing a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
