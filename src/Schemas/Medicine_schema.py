from pydantic import BaseModel
from datetime import date

class AddMedicine(BaseModel):
    UserId :int
    MedicineName : str
    dosage :str
    routine : str
    expiry_date : date

class AddMedicineResponse(BaseModel):
    success : bool
    message: str

