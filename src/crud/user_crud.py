from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.users import User
from src.Schemas.Users_schema import UsersCreate, UsersCheck,UsersUpdate
from sqlalchemy.exc import IntegrityError

async def create_user(db:AsyncSession,user:UsersCreate):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        age=user.age
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return UsersUpdate(
            success=True,
            message=f"User {user.email} has been registered",
            id=new_user.id
        )
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="User could not be created")

async def check_user(db:AsyncSession ,user:UsersCheck):
    try:
        result = await db.execute(
            select(User).where(User.email == user.email  )
        )
        details = result.scalar_one_or_none()


        if details is  None or details.password != user.password or details.email != user.email:
            raise HTTPException(status_code=401, detail="Please enter a correct email and password")

        return UsersUpdate(
            success=True,
            message="loggin successful",
            id=details.id
        )
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Something went wrong")



