from pydantic import BaseModel
from datetime import datetime,time
from enum import Enum
from typing import Optional




class Type(str, Enum):
    normal = "normal"
    priority = "priority"
    extra_dose = "extra_dose"

class AddSchedule(BaseModel):
    Medicine_id: int
    time_of_data :time
    Day_of_week :str
    dosage :str
    reminder_type :str


    class Config:
        from_attributes= True
class SchedulerResponse(BaseModel):
    Medicine_id: int
    time_of_data: time
    Day_of_week: str
    dosage: str
    reminder_type: Type = Type.normal
    created_at: Optional[
        datetime
    ]=None
    updated_at: Optional[datetime]=None
    class Config:
        from_attributes= True

class Today_Medicine(BaseModel):
    medicine_id: int
    MedicineName :str
    dosage : str
    reminder_type : str
    success : bool
    message: str
    class Config:
        orm_mode= True



