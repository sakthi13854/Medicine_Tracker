from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

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
    UserId = Column(Integer, ForeignKey('users.id'))
    MedicineName = Column(String,nullable=False)
    dosage = Column(String,nullable=False)
    routine = Column(String,nullable=False)
    start_date = Column(Date,nullable=False)
    end_date = Column(Date,nullable=False)
    expiry_date = Column(Date,nullable=False)
    Type = Column(String,nullable=False)

