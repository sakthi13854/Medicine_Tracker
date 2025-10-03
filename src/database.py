
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import ssl
import os

Database_Url =os.environ.get("DATABASE_URL")
if not Database_Url:
    raise ValueError("DATABASE_URL environment variable not set!")
ssl_context = ssl.create_default_context()
ssl_context.verify_mode = ssl.CERT_REQUIRED
engine = create_async_engine(
    Database_Url,
    echo=True,
    connect_args={"ssl": ssl_context}
)

sessionLocal = sessionmaker( bind=engine,
                             class_=AsyncSession,
                             expire_on_commit=False)
Base = declarative_base()

async def get_db() -> sessionLocal:
    async with sessionLocal() as session:
        yield session


