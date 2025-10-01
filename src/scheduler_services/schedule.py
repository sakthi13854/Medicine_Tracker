from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.Scheduler import Scheduler
from src.scheduler_services.Scheduler_schema import AddSchedule, Today_Medicine
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
async def today_medicine(db: AsyncSession,user_id:int)->List[Today_Medicine]:
    today = date.today()
    weekday = today.strftime("%A")
    result = await db.execute(
        select(Medicine,Scheduler).
        join(Medicine,Scheduler.Medicine_id==Medicine.id)
        .where(
            and_(
                Medicine.UserId==user_id,
                Medicine.start_date <= today,
                Medicine.end_date >= today,
                Scheduler.Day_of_week == weekday
            )
       )
    )
    Medicines = result.all()
    try:
        if not Medicines:
            raise HTTPException(status_code=404, detail="You dont have any medicine today or add schedule first")
        response = []
        for med, sched in Medicines:
            response.append(
                Today_Medicine(
                    medicine_id=med.id,
                    MedicineName=med.MedicineName,
                    dosage=med.dosage,
                    reminder_type=sched.reminder_type,
                    success=True,
                    message="Medicine scheduled for today"
                )
            )
        return response
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Something went wrong")
