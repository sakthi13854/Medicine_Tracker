from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.crud.medicine_crud import add_medicines,my_medicines , expiry_medicines
from src.Schemas.Medicine_schema import AddMedicine,AddMedicineResponse,MyMedicinesResponse,ExResponseModel

router = APIRouter(prefix="/Medicine", tags=["Medicine"])

@router.post("/add", response_model=AddMedicineResponse)
async def add_medicine(user_id : int,medicine : AddMedicine,db: AsyncSession = Depends(database.get_db)):
    result = await add_medicines(db, medicine,user_id)
    return result
@router.get("/my_medicines", response_model=MyMedicinesResponse)
async def get_medicines(user_id : int = Query(...) ,db: AsyncSession = Depends(database.get_db)):
    result = await my_medicines(db , user_id)
    return result
@router.get("/expiry_medicines", response_model=ExResponseModel)
async def expiry_medicne(user_id : int = Query(...) ,db: AsyncSession = Depends(database.get_db)):
    result = await expiry_medicines(db, user_id)
    return result