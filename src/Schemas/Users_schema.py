
from pydantic import BaseModel


class UsersCreate(BaseModel):
    name : str
    email : str
    password : str
    age : int
class SignupResponse(BaseModel):
    username : str
    class Config:
        orm_mode = True
