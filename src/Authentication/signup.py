from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.crud.user_crud import create_user
from src.Schemas.Users_schema import UsersCreate
from src.Schemas.Users_schema import UsersUpdate

router = APIRouter(prefix="/signup", tags=["signup"])
@router.post("/", response_model=UsersUpdate)
async def signup(user:UsersCreate, db: AsyncSession = Depends(database.get_db)):
    result = await create_user(db, user)
    return result