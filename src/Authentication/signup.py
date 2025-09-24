from fastapi import APIRouter, Depends, HTTPException,requests
from sqlalchemy.ext.asyncio import AsyncSession
from .. import database
from src.crud.user_crud import create_user
from src.Schemas.Users_schema import UsersCreate
from ..Schemas.Users_schema import SignupResponse

router = APIRouter(prefix="/signup", tags=["signup"])
@router.post("/signup", response_model=SignupResponse)
async def signup(user:UsersCreate, db: AsyncSession = Depends(database.get_db)):
    return await create_user(db, user)