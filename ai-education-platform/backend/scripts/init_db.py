"""Database initialization script"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.utils.database import Base


async def init_database():
    """Initialize database with all tables"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    print("Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_database())