from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.users import Medicine
from src.Schemas.Medicine_schema import AddMedicine, ResponseModel, ExpiryMedicinesResponse
from sqlalchemy.exc import IntegrityError
from datetime import date
from sqlalchemy import and_
async def add_medicines(db: AsyncSession, medicine : AddMedicine):
    result = await db.execute(
        select(Medicine).where(Medicine.MedicineName == medicine.MedicineName , Medicine.UserId == medicine.UserId)
    )
    existing_medicine = result.scalar_one_or_none()
    if existing_medicine:
        raise HTTPException(status_code=400, detail="medicine already added")
    new_medicine = Medicine(
        MedicineName=medicine.MedicineName,
        UserId=medicine.UserId,
        dosage=medicine.dosage,
        routine=medicine.routine,
        start_date=medicine.start_date,
        end_date=medicine.end_date,
        expiry_date=medicine.expiry_date,
        Type=medicine.Type,
    )
    db.add(new_medicine)
    try:
        await db.commit()
        await db.refresh(new_medicine)
        return {"success": True, "message": f"Medicine '{new_medicine.MedicineName}' added successfully"}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Sorry medicine could not be added")

async def my_medicines(db: AsyncSession, user_id : int):
    result = await db.execute(
        select(Medicine).where(Medicine.UserId == user_id)
    )
    user_medicines = result.scalar_one_or_none()
    try:
        if not user_medicines:
            raise HTTPException(status_code=404, detail="You have no medicines. Please add medicines first")
        return user_medicines
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Sorry medicine could not be added")

async def expiry_medicines(db: AsyncSession, user_id : int):
    today = date.today()
    result = await db.execute(
        select(Medicine).where(
            and_(Medicine.UserId == user_id,
                 Medicine.expiry_date < today)
        )

    )
    medicines= result.scalars().all()
    medicineslist = [
        ExpiryMedicinesResponse(
            id = med.id,
            MedicineName = med.MedicineName,
            expiry_date  =  med.expiry_date
        )
        for med in medicines
    ]
    try:
        if not medicines:
            raise HTTPException(status_code=404,detail="You have no medicines. Please add medicines first")
        return ResponseModel(
            success=True,
            message="Medicines expired,Please consider the following medicines",
            data=medicineslist
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Sorry medicine could not be added")