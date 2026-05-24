from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class SymptomLog(Base):

    __tablename__ = "symptom_logs"

    id = Column(Integer, primary_key=True, index=True)

    symptoms = Column(String)

    urgency = Column(String)

    recommendation = Column(String)