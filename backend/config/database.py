
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

DATABASE_URI = ''

# Create engine
engine = create_engine(DATABASE_URI)

# Create session factory
db_session = scoped_session(sessionmaker(bind=engine))

# Create declarative base
Base = declarative_base()

def get_db():
    """Provide a database session."""
    return db_session