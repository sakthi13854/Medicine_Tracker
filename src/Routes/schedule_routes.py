
from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.scheduler_services.schedule import Add_Schedule,today_medicine
from src.scheduler_services.Scheduler_schema import AddSchedule, SchedulerResponse, Today_Medicine
from typing import List

router = APIRouter(
    prefix="/Schedule",
    tags=["schedule"]
)

@router.post("/add_schedule", response_model=SchedulerResponse)
async def add_schedule(user_id:int,schedule: AddSchedule,db: AsyncSession = Depends(database.get_db)):
    result = await Add_Schedule(db, schedule, user_id)
    return result
@router.get("/Today_Medicine", response_model=List[Today_Medicine])
async def get_schedule(user_id: int = Query(..., title="User ID", description="ID of the logged-in user")
,db: AsyncSession = Depends(database.get_db)):
    result = await today_medicine(db,user_id)
    return result
