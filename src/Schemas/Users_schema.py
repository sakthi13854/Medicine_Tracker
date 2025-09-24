
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
