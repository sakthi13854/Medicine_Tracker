from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.adherence import Adherence
from src.Adherecnce_logs.adherence_schema import AdherenceLogs,AdherenceLogsResponse
from sqlalchemy.exc import IntegrityError

async def adherence_log(db : AsyncSession,adherence : AdherenceLogs ):
    log = Adherence(
        Userid=adherence.Userid,
        MedicineId = adherence.MedicineId,
        ScheduledTime = adherence.ScheduledTime,
        AdherenceTime = adherence.AdherenceTime,
        status =adherence.status,
        dosage = adherence.dosage,
    )
    db.add(log)
    try :
        await db.commit()
        await db.refresh(log)
        return AdherenceLogsResponse(success=True, message="Adherence Log Created",data = AdherenceLogs.from_orm(log))
    except IntegrityError :
        await db.rollback()
        raise HTTPException(status_code=400,detail="adherence cannot be added")
