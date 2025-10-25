
from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.crud.schedule import Add_Schedule
from src.Schemas.Scheduler_schema import AddSchedule, SchedulerResponse
from typing import List

router = APIRouter(
    prefix="/Schedule",
    tags=["schedule"]
)

@router.post("/add_schedule", response_model=SchedulerResponse)
async def add_schedule(user_id:int,schedule: AddSchedule,db: AsyncSession = Depends(database.get_db)):
    result = await Add_Schedule(db, schedule, user_id)
    return result

