from sqlmodel import create_engine, SQLModel, Session
from contextlib import contextmanager
from fastapi import Depends
import os

# Use SQLite for local development, PostgreSQL for production
database_url = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

# For PostgreSQL, we need to handle asyncpg driver differently
if database_url.startswith('postgresql'):
    # Replace postgresql+asyncpg with postgresql+psycopg2 for sync operations
    if '+asyncpg' in database_url:
        database_url = database_url.replace('+asyncpg', '+psycopg2')

engine = create_engine(
    database_url,
    echo=False,  # Set to True to see SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections after 5 minutes
)

def create_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(bind=engine)

@contextmanager
def get_session_context():
    """Get a database session"""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def get_session():
    with get_session_context() as session:
        yield session