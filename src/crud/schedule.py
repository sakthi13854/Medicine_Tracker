from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.Scheduler import Scheduler
from src.Schemas.Scheduler_schema import AddSchedule, Today_Medicine
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from datetime import date
from src.models.users import Medicine
from typing import List

#Add schedule to the user

async def Add_Schedule(db: AsyncSession, schedule : AddSchedule,user_id : int):
    result = await db.execute(
        select(Medicine).where(Medicine.UserId == user_id)
    )
    existing_user = result.scalars().all()
    if existing_user:
        new_schedule = Scheduler(
            Medicine_id=schedule.Medicine_id,
            time_of_data=schedule.time_of_data,
            Day_of_week=schedule.Day_of_week,
            Total_dosage_today=schedule.Total_dosage_today,
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
    else:
        raise HTTPException(status_code=404, detail="User not found")


#medicines for the user on the selected day

