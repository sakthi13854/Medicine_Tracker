from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.crud.medicine_crud import add_medicines
from src.Schemas.Medicine_schema import AddMedicine,AddMedicineResponse

router = APIRouter(prefix="/AddMedicine", tags=["Medicine"])

@router.post("/", response_model=AddMedicineResponse)
async def add_medicine(medicine : AddMedicine,db: AsyncSession = Depends(database.get_db)):
    result = await add_medicines(db, medicine)
    return result