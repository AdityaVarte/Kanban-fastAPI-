# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Base class that all our ORM models will inherit from
class Base(DeclarativeBase):
    pass


# The engine manages a pool of connections to PostgreSQL
engine = create_async_engine(settings.database_url, echo=True)

# Factory that produces new AsyncSession objects on demand
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency that FastAPI routes will use to get a DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session