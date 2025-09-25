from fastapi import FastAPI
from src.Authentication import signup
from src.database import Base, engine
import asyncio
app = FastAPI()


app.include_router(signup.router)
app.include_router(signup.loginrouter)
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully!")
if __name__ == "__main__":
    asyncio.run(init_db())