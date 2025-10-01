from sqlalchemy import Column, Integer, String, Time, ForeignKey,DateTime
from src.database import Base
from sqlalchemy.sql import func

class Scheduler(Base):
    __tablename__ = 'scheduler'
    id = Column(Integer, primary_key=True)
    Medicine_id = Column(Integer, ForeignKey('medicines.id'),nullable=False)
    time_of_data = Column(Time,nullable=False)
    Day_of_week = Column(String,nullable=False)
    Total_dosage_today = Column(String,nullable=False)
    reminder_type = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

