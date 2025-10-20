from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base\


DATABASE_URL = "sqlite+aiosqlite:///./medicine-tracker.db"

engine = create_async_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with sessionLocal() as session:
        yield session


