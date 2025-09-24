from sqlalchemy import Column, Integer, String ,Date
from src.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    age = Column(Integer,nullable=False)

class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    dosage = Column(String,nullable=False)
    routine = Column(String,nullable=False)
    expiry_date = Column(Date,nullable=False)
