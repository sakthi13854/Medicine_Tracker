
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio
import os

Database_Url =os.environ.get("DATABASE_URL")

engine = create_async_engine(Database_Url,echo=True)

sessionLocal = sessionmaker( bind=engine,
                             class_=AsyncSession,
                             expire_on_commit=False)
Base = declarative_base()

async def get_db() -> sessionLocal:
    async with sessionLocal() as session:
        yield session


