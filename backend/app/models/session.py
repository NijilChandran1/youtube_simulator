from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(String, ForeignKey("videos.video_id"))
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default='in_progress') # 'in_progress', 'completed', 'abandoned'
    
    user = relationship("User", back_populates="sessions")
    video = relationship("Video", back_populates="sessions")
    attempts = relationship("UserAttempt", back_populates="session")
