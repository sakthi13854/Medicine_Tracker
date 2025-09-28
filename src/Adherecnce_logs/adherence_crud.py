from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.adherence import Adherence
from src.Adherecnce_logs.adherence_schema import AdherenceLogs,AdherenceLogsResponse
from sqlalchemy.exc import IntegrityError
import numpy as np
import joblib

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
        model = joblib.load('src/Ml/adherence_model.pkl')
        scaler = joblib.load('src/Ml/scaler.pkl')


        hour = adherence.ScheduledTime.hour
        day_of_week = adherence.ScheduledTime.weekday()
        medicine_id = adherence.MedicineId
        past_rate = 0.8
        dosage_map = {"1tablet": 1, "2tablets": 2, "10mg": 10, "20mg": 20}
        dosage_numeric = dosage_map.get(adherence.dosage, 0)


        X_new = np.array([[adherence.Userid, medicine_id, hour, day_of_week, dosage_numeric]])
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
