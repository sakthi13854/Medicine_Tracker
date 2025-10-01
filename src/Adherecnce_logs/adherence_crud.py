
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.adherence import Adherence
from src.Adherecnce_logs.adherence_schema import AdherenceLogs,AdherenceLogsResponse
from sqlalchemy.exc import IntegrityError
import numpy as np
import joblib
from sqlalchemy.future import select
from sqlalchemy.sql import func
from datetime import datetime

def dosage_to_numeric(dosage_str):
    dosage_str = dosage_str.lower().replace(" ", "")
    if "tablet" in dosage_str or "capsule" in dosage_str:
        return float(dosage_str.replace("tablet","").replace("capsule","") or 1)
    elif "mg" in dosage_str:
        return float(dosage_str.replace("mg",""))
    elif "ml" in dosage_str:
        return float(dosage_str.replace("ml",""))
    else:
        return 0

async def adherence_log(db : AsyncSession,adherence : AdherenceLogs,user_id :int ):
    log = Adherence(
        Userid=user_id,
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
        Model_path = 'src/Ml/adherence_model2.pkl'
        scaler_path = 'src/Ml/scaler (1).pkl'

        model = joblib.load(Model_path)
        scaler = joblib.load(scaler_path)


        hour = adherence.ScheduledTime.hour
        day_of_week = adherence.ScheduledTime.weekday()
        medicine_id = adherence.MedicineId
        status = adherence.status
        status_map = {"taken": 1, "missed": 0}
        status_numeric = status_map.get(status.lower(), 0)
        is_weekend = 0
        if day_of_week == 5 or day_of_week == 6:
            is_weekend = 1
        dosage_numeric = dosage_to_numeric(adherence.dosage)
        query = await db.execute(
            select(
                func.sum(Adherence.dosage).label("taken"),
                func.count(Adherence.id).label("scheduled")
            ).where(
                Adherence.Userid == adherence.Userid,
                Adherence.MedicineId == adherence.MedicineId
            )
        )
        result = query.first()
        taken = result.taken or 0
        scheduled = result.scheduled or 1
        past_rate = taken / scheduled
        feature8 = 0
        feature9 = 0
        feature10 = 0


        X_new = np.array([[  hour, day_of_week, is_weekend,medicine_id, dosage_numeric,past_rate,status_numeric,feature8,feature9,feature10],])
        X_scaled = scaler.transform(X_new)
        missed_prob = float(model.predict_proba(X_scaled)[0, 1])

        if missed_prob < 0.3:
            reminder_type = "normal"
        elif missed_prob < 0.7:
            reminder_type = "priority"
        else:
            reminder_type = "extra"

        return AdherenceLogsResponse(success=True,
                                     message=f"Adherence Log Created. Reminder Type: {reminder_type}, Missed Probability: {missed_prob:.2f}",
                                     data = AdherenceLogs.from_orm(log))
    except IntegrityError :
        await db.rollback()
        raise HTTPException(status_code=400,detail="adherence cannot be added")
