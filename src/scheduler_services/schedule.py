from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.Scheduler import Scheduler
from src.scheduler_services.Scheduler_schema import  AddSchedule
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from datetime import date
from src.models.users import Medicine

async def Add_Schedule(db: AsyncSession, schedule : AddSchedule):

    new_schedule = Scheduler(
        Medicine_id=schedule.Medicine_id,
        time_of_data=schedule.time_of_data,
        Day_of_week=schedule.Day_of_week,
        dosage=schedule.dosage,
        reminder_type=schedule.reminder_type,

    )
    db.add(new_schedule)
    try:
        await db.commit()
        await db.refresh(new_schedule)
        return new_schedule
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Schedule could not be initiated")

today = date.today()
weekday = today.strftime("%A")
async def today_medicine(db: AsyncSession):
    today = date.today()
    weekday = today.strftime("%A")
    result = await db.execute(
        select(Medicine,Scheduler).
        join(Medicine,Scheduler.Medicine_id==Medicine.id)
        .where(
            and_(
                Medicine.start_date <= today,
                Medicine.end_date >= today,
                Scheduler.Day_of_week == weekday
            )
       )
    )
    Medicines = result.all()
    try:
        return Medicine
    except IntegrityError:
        raise HTTPException(status_code=400, detail="You Have no Medicine Today")
