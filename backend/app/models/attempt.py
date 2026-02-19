from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class UserAttempt(Base):
    __tablename__ = "user_attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("training_sessions.id"))
    
    attribute = Column(String)
    user_timestamp_seconds = Column(Float)
    user_live_clock_time = Column(String)
    
    ground_truth_event_id = Column(Integer, ForeignKey("ground_truth_events.id"), nullable=True)
    
    time_difference_ms = Column(Float, nullable=True)
    accuracy_level = Column(String, nullable=True) # 'perfect', 'acceptable', 'miss', 'false_positive'
    ai_feedback = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("TrainingSession", back_populates="attempts")
    ground_truth_event = relationship("GroundTruthEvent") # One-way relationship mostly
