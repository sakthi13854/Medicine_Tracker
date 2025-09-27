from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.users import Medicine
from src.Schemas.Medicine_schema import AddMedicine
from sqlalchemy.exc import IntegrityError

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