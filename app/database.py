"""Database configuration and session management."""
from sqlmodel import create_engine, Session
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def get_db():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session

