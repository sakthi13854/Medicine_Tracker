from fastapi import FastAPI
from src.Authentication import signup
from src.database import Base , engine
from src.database import sessionLocal
from fastapi.requests import Request
app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
async def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



app.include_router(signup.router)
