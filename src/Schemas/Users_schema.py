
from pydantic import BaseModel


class UsersCreate(BaseModel):
    name : str
    email : str
    password : str
    age : int
    class Config:
        from_attributes = True
class UsersUpdate(BaseModel):
    name : str
    id : int
    age : int
    email : str

class UsersCheck(BaseModel):
    email : str
    password : str
