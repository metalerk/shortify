from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/url_shortener")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def initialize_database():
    """
    Initializes the database by creating all tables.
    This function should be called at the start of the application.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency to get a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
