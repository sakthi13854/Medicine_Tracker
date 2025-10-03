from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Any,List,Optional



class MType(str, Enum):
    Tablet="Tablet"
    Injection="Injection"
    Syrup="Syrup"

class AddMedicine(BaseModel):
    MedicineName : str
    dosage :str
    routine : str
    expiry_date : date
    start_date : date
    end_date : date
    Type : MType = MType.Tablet

class AddMedicineResponse(BaseModel):
    success : bool
    message: str
class MyMedicines(BaseModel):
    id : int
    MedicineName : str
    dosage : str
    routine : str
    expiry_date : date
    type : MType = MType.Tablet
    class Config:
        from_attributes = True

class MyMedicinesResponse(BaseModel):
    success : bool
    message: str
    data : Optional[List[MyMedicines]] = None


class ExpiryMedicinesResponse(BaseModel):
    id : int
    MedicineName : str
    expiry_date : date
    class Config:
        from_attributes = True
class ExResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[List[ExpiryMedicinesResponse]] = None


