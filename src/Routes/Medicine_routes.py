from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.crud.medicine_crud import add_medicines,my_medicines , expiry_medicines, edit_medicine, del_medicine, today_medicine
from src.Schemas.Medicine_schema import AddMedicine,AddMedicineResponse,MyMedicinesResponse,ExResponseModel,updatemedicine, deletemedicine
from datetime import date 

router = APIRouter(prefix="/Medicine", tags=["Medicine"])

@router.post("/add", response_model=AddMedicineResponse)
async def add_medicine(user_id : int,medicine : AddMedicine,db: AsyncSession = Depends(database.get_db)):
    result = await add_medicines(db, medicine,user_id)
    return result
@router.get("/today_medicines",response_model = MyMedicinesResponse)
async def today_medicines(date: date ,user_id : int = Query(...) ,db : AsyncSession = Depends(database.get_db)):
    result = await today_medicine(db, user_id, date )
    return result
@router.get("/my_medicines", response_model=MyMedicinesResponse)
async def get_medicines(user_id : int = Query(...) ,db: AsyncSession = Depends(database.get_db)):
    result = await my_medicines(db , user_id)
    return result
@router.get("/expiry_medicines", response_model=ExResponseModel)
async def expiry_medicne(user_id : int = Query(...) ,db: AsyncSession = Depends(database.get_db)):
    result = await expiry_medicines(db, user_id)
    return result

@router.put("/update_medicine",response_model = AddMedicineResponse)
async def updatemedicne(user_id: int ,medicine : updatemedicine , db : AsyncSession = Depends(database.get_db)):
    result = await edit_medicine(db , medicine, user_id)
    return result 

@router.delete("/delete_medicine",response_model = AddMedicineResponse)
async def deletemedicine(user_id : int , medicine :deletemedicine ,db : AsyncSession = Depends(database.get_db) ):
    result = await del_medicine(db , medicine , user_id)
    return result