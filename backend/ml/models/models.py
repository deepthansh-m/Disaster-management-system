# backend/ml/models/models.py
from backend.config.database import Base
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, JSON, DateTime
from datetime import datetime

class DisasterHistory(Base):
    __tablename__ = 'disaster_history'

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(String, nullable=True)
    parameters = Column(JSON, nullable=True)
    disaster_type = Column(String, nullable=True)
    type_confidence = Column(Float, nullable=True)
    possible_deaths = Column(Float, nullable=True)
    infrastructure_loss = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "parameters": self.parameters,
            "prediction": self.prediction,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "disaster_type": self.disaster_type,
            "date": self.date.isoformat() if self.date else None,
            "description": self.description,
            "rainfall": self.rainfall,
            "temperature": self.temperature,
            "disaster_occurred": self.disaster_occurred
        }