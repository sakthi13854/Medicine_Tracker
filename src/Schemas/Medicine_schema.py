from pydantic import BaseModel
from datetime import date
from enum import Enum
class MType(str, Enum):
    Tablet="Tablet"
    Injection="Injection"
    Syrup="Syrup"

class AddMedicine(BaseModel):
    UserId :int
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

