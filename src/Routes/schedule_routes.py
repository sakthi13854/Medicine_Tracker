from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.scheduler_services.schedule import Add_Schedule,today_medicine
from src.scheduler_services.Scheduler_schema import AddSchedule, SchedulerResponse, Today_Medicine

router = APIRouter(
    prefix="/Schedule",
    tags=["schedule"]
)

@router.post("/add_schedule", response_model=SchedulerResponse)
async def add_schedule(schedule: AddSchedule,db: AsyncSession = Depends(database.get_db)):
    result = await Add_Schedule(db, schedule)
    return result
@router.get("/Today_Medicine", response_model=Today_Medicine)
async def get_schedule(db: AsyncSession = Depends(database.get_db)):
    result = await today_medicine(db)
    return result
