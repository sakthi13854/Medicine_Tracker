from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.users import Medicine
from src.Schemas.Medicine_schema import AddMedicine, ExResponseModel, ExpiryMedicinesResponse,MyMedicinesResponse,MyMedicines,updatemedicine, deletemedicine
from sqlalchemy.exc import IntegrityError
from datetime import date
from sqlalchemy import and_
from typing import List

async def add_medicines(db: AsyncSession, medicine : AddMedicine , user_id : int):
    result = await db.execute(
        select(Medicine).where(Medicine.MedicineName == medicine.MedicineName , Medicine.UserId == user_id)
    )
    existing_medicine = result.scalar_one_or_none()
    if existing_medicine:
        raise HTTPException(status_code=400, detail="medicine already added")
    new_medicine = Medicine(
        MedicineName=medicine.MedicineName,
        UserId=user_id,
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
    user_medicines = result.scalars().all()

    medicines_list = [
        MyMedicines(
            id=med.id,
            MedicineName=med.MedicineName,
            dosage=med.dosage,
            routine=med.routine,
            expiry_date=med.expiry_date,
            type=med.Type
        )
        for med in user_medicines
    ]
    try:
        if not user_medicines:
            raise HTTPException(status_code=404, detail="You have no medicines. Please add medicines first")
        return MyMedicinesResponse(
            success = True,
            message="you have the following medicines:",
            data=medicines_list
        )
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
            raise HTTPException(status_code=404,detail="You have no medicines that is expired")
        return ExResponseModel(
            success=True,
            message="Medicines expired,Please consider the following medicines",
            data=medicineslist
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Sorry medicine could not be added")

async def get_medid(db :AsyncSession, medicinename : str, userid: int ):
    result =  await db.execute(
        select(Medicine.id).where(Medicine.MedicineName == medicinename, Medicine.UserId == userid)
    )
    medid = result.scalar()

    return medid if medid else None


async def edit_medicine(db : AsyncSession,medicine : deletemedicine , user_id :int):
    medid = await get_medid(db = db ,medicinename = medicine.MedicineName, userid = user_id )
    print(medid)
    result = await db.execute(
        select(Medicine).where(Medicine.id == medid)
    )
    user_exist = result.scalar_one_or_none()
    try:
        if user_exist:
            update_data = medicine.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(user_exist, key, value)

            await db.commit()
            await db.refresh(user_exist)
            return {'success' : True ,
                       'message':'changes added successfully' }
        else:
            raise HTTPException(status_code = 404 , detail = "You have no medicine to change.please add medicinec first")
    except IntegrityError:
        raise HTTPException(status_code = 400,deatil = "internal server error")

        
async def del_medicine(db : AsyncSession,medicine : updatemedicine , user_id :int):
    medid = await get_medid(db = db ,medicinename = medicine.MedicineName, userid = user_id )
    print(medid)
    result = await db.execute(
        select(Medicine).where(Medicine.id == medid)
    )
    user_exist = result.scalar_one_or_none()
    try:
        if user_exist:
            await db.delete(user_exist)
            await db.commit()
            return {'success' : True ,
                       'message':' deleted successfully' }
        else:
            raise HTTPException(status_code = 404 , detail = "You have no medicine to change.please add medicinec first")
    except IntegrityError:
        raise HTTPException(status_code = 400,deatil = "internal server error")

async def today_medicine(db: AsyncSession,user_id : int,tdate : date ):
    today = date.today()
    weekday = today.strftime("%A")
    result = await db.execute(
        select(Medicine)
        .where(
            Medicine.UserId==user_id,
            Medicine.start_date <= today,
            Medicine.end_date >= today,
            tdate == today
       )
    )
    Medicines = result.scalars().all()
    try:
        if not Medicines:
            raise HTTPException(status_code=404, detail="You dont have any medicine today or add medicine first")
        medicines_list = [
        MyMedicines(
            id=med.id,
            MedicineName=med.MedicineName,
            dosage=med.dosage,
            routine=med.routine,
            expiry_date=med.expiry_date,
            type=med.Type
        )
        for med in Medicines]
        return MyMedicinesResponse(
            success = True,
            message="you have the following medicines:",
            data=medicines_list
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Something went wrong")
 

       
