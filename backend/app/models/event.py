from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class GroundTruthEvent(Base):
    __tablename__ = "ground_truth_events"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.video_id"))
    attribute = Column(String) # "Main Logo", "Copyright", etc.
    timestamp_seconds = Column(Float)
    live_clock_time = Column(String)
    clue_description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    video = relationship("Video", back_populates="events")
