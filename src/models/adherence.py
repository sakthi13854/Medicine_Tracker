
from sqlalchemy import Column, Integer, String, DateTime,  ForeignKey
from src.database import Base
from sqlalchemy.sql import func

class Adherence(Base):
    __tablename__ = 'adherence_logs',
    id = Column(Integer, primary_key=True,index=True)
    Userid = Column(Integer, ForeignKey('users.id'))
    MedicineId = Column(Integer, ForeignKey('medicines.id'))
    ScheduledTime = Column(DateTime,nullable=False)
    AdherenceTime = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String,nullable=False)
    dosage = Column(String,ForeignKey('scheduler.dosage'))
