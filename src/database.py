from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Database_Url = "sqlite:///medicine-tracker.db"
engine = create_engine(Database_Url,connect_args={'check_same_thread': False})

sessionLocal = sessionmaker( bind=engine,
                             class_=AsyncSession,
                             expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with engine.begin() as conn:
        yield conn