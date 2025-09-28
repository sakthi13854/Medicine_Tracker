from typing import Optional ,Any
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
class Status(str, Enum):
    taken = "taken"
    missed = "missed"
    late = "late"
    skipped = "skipped"

class AdherenceLogs(BaseModel):
    Userid :int
    MedicineId :int
    ScheduledTime : datetime
    AdherenceTime : Optional[datetime]
    status : Status = Status.missed
    dosage : str
    class Config:
        from_attributes = True

class AdherenceLogsResponse(BaseModel):
    success : bool
    message : Optional[str]
    data : Optional[AdherenceLogs]
    class Config:
        from_attributes = True
