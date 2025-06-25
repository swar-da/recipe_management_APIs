from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from config import settings
DATABASE_URL = (
    f"postgresql://postgres:root@localhost:5432/Recipe"
)

engine = create_async_engine(settings.POSTGRES_URL, echo=True)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def connect_to_db() -> None:
    return async_session()

async def disconnect() -> None:
    await engine.dispose()
    
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        
base = declarative_base()
        
        
