from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TrainingSession, GroundTruthEvent, UserAttempt
from app.schemas.event import EventLogRequest, FeedbackResponse
from app.utils.proximity_comparator import ProximityComparator
from app.services.vertex_ai_service import VertexAIService

router = APIRouter(prefix="/api/events", tags=["events"])

@router.post("/log", response_model=FeedbackResponse)
async def log_event(
    event_data: EventLogRequest,
    db: Session = Depends(get_db)
):
    # 1. Get session
    session = db.query(TrainingSession).filter(TrainingSession.id == event_data.session_id).first()
    if not session:
        # For testing without real session, maybe create one? No, fail.
        # Check if user creates session first.
        # Or simplify for MVP: if session_id is 0, allow? No.
        raise HTTPException(404, "Session not found")
    
    # 2. Find matching ground truth event within radius (e.g. 5s)
    radius = 5.0
    
    potential_matches = db.query(GroundTruthEvent).filter(
        GroundTruthEvent.video_id == session.video_id,
        GroundTruthEvent.attribute == event_data.attribute
    ).all()
    
    nearest_event = None
    min_diff = float('inf')
    
    # Simple linear scan for nearest match
    for event in potential_matches:
        diff = abs(event.timestamp_seconds - event_data.user_timestamp_seconds)
        if diff < min_diff and diff <= radius:
            min_diff = diff
            nearest_event = event
    
    comparator = ProximityComparator()
    vertex_ai = VertexAIService()
    
    if not nearest_event:
        # False Positive logic
        attempt = UserAttempt(
            session_id=session.id,
            attribute=event_data.attribute,
            user_timestamp_seconds=event_data.user_timestamp_seconds,
            user_live_clock_time=event_data.user_live_clock_time,
            accuracy_level="false_positive",
            ai_feedback="This attribute was not expected here.",
            time_difference_ms=0.0
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        
        return FeedbackResponse(
            attempt_id=attempt.id,
            clicked_attribute=event_data.attribute,
            user_clicked_time=event_data.user_live_clock_time,
            accuracy_level="false_positive",
            time_difference_ms=0.0,
            ai_feedback=f"'{event_data.attribute}' was not expected here."
        )

    # 3. Evaluate
    # use signed diff for feedback context (early/late)
    raw_diff = event_data.user_timestamp_seconds - nearest_event.timestamp_seconds
    
    accuracy, diff_ms = comparator.evaluate_attempt(
        event_data.user_timestamp_seconds,
        nearest_event.timestamp_seconds
    )
    
    # 4. Generate simple feedback message (AI feedback removed for speed)
    if accuracy == "perfect":
        ai_feedback = f"Perfect timing! You were within 1 second."
    elif accuracy == "acceptable":
        ai_feedback = f"Good timing! You were within 2 seconds."
    elif accuracy == "miss":
        ai_feedback = f"Missed! You were {abs(raw_diff):.2f} seconds {'late' if raw_diff > 0 else 'early'}."
    else:  # false_positive (>5 seconds)
        ai_feedback = f"Wrong timing! You were {abs(raw_diff):.2f} seconds {'late' if raw_diff > 0 else 'early'}."
    
    # 5. Save
    attempt = UserAttempt(
        session_id=session.id,
        attribute=event_data.attribute,
        user_timestamp_seconds=event_data.user_timestamp_seconds,
        user_live_clock_time=event_data.user_live_clock_time,
        ground_truth_event_id=nearest_event.id,
        time_difference_ms=diff_ms,
        accuracy_level=accuracy,
        ai_feedback=ai_feedback
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    ground_truth_dict = {
        "timestamp_seconds": nearest_event.timestamp_seconds,
        "live_clock_time": nearest_event.live_clock_time,
        "clue_description": nearest_event.clue_description
    }

    return FeedbackResponse(
        attempt_id=attempt.id,
        clicked_attribute=event_data.attribute,
        user_clicked_time=event_data.user_live_clock_time,
        accuracy_level=accuracy,
        time_difference_ms=diff_ms,
        ground_truth=ground_truth_dict,
        ai_feedback=ai_feedback
    )
