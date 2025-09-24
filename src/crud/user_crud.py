from fastapi.dependencies import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.users import User
from src.Schemas.Users_schema import UsersCreate,SignupResponse

async def create_user(db:AsyncSession,user:UsersCreate):
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        age=user.age
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
