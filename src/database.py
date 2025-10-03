
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio
import os

Database_Url =os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:9625015@localhost:5432/medicine_tracker"
)

engine = create_async_engine(Database_Url,echo=True)

sessionLocal = sessionmaker( bind=engine,
                             class_=AsyncSession,
                             expire_on_commit=False)
Base = declarative_base()

async def get_db() -> sessionLocal:
    async with sessionLocal() as session:
        yield session


