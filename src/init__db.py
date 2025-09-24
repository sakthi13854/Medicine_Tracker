import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_async_engine("sqlite+aiosqlite:///medicine-tracker.db", echo=True)


Base = declarative_base()

async def init_db():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
    print('Database initialized')

if __name__ == "__main__":
    asyncio.run(init_db())
