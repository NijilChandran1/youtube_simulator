from pydantic import BaseModel
from typing import Optional, Dict, Any

class EventLogRequest(BaseModel):
    session_id: int
    attribute: str
    user_timestamp_seconds: float
    user_live_clock_time: str
    video_timestamp_seconds: float

class FeedbackResponse(BaseModel):
    attempt_id: int
    clicked_attribute: str  # The attribute the user clicked
    user_clicked_time: str  # When the user clicked (live clock time)
    accuracy_level: str
    time_difference_ms: float
    ground_truth: Optional[Dict[str, Any]] = None
    ai_feedback: Optional[str] = None
