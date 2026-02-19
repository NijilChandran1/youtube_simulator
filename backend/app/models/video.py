from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True)
    title = Column(String)
    file_path = Column(String)
    duration_seconds = Column(Float)
    broadcast_start_time = Column(String) # ISO format: "2026-02-11T19:00:00"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    events = relationship("GroundTruthEvent", back_populates="video")
    sessions = relationship("TrainingSession", back_populates="video")
