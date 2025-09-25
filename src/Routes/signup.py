from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src import database
from src.crud.user_crud import create_user,check_user
from src.Schemas.Users_schema import UsersCreate, UsersCheck
from src.Schemas.Users_schema import UsersUpdate

router = APIRouter(prefix="/signup", tags=["signup"])
@router.post("/", response_model=UsersUpdate)
async def signup(user:UsersCreate, db: AsyncSession = Depends(database.get_db)):
    result = await create_user(db, user)
    return result

loginrouter = APIRouter(prefix="/login", tags=["login"])
@loginrouter.post("/", response_model=UsersUpdate)
async def login(user:UsersCheck ,db: AsyncSession = Depends(database.get_db)):
    result = await check_user(db, user)
    return result