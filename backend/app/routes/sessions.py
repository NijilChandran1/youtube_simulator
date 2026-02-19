from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models import TrainingSession, User, Video, UserAttempt

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

class StartSessionRequest(BaseModel):
    video_filename: Optional[str] = "video.mp4"
    user_email: Optional[str] = "guest@example.com"
    video_id: Optional[str] = None # Added video_id

class SessionResponse(BaseModel):
    session_id: int
    video_id: str
    broadcast_start_time: str
    status: str

class SessionHistoryItem(BaseModel):
    session_id: int
    created_at: str
    video_name: str
    total_events: int
    perfect_count: int
    good_count: int
    missed_count: int
    wrong_count: int
    accuracy_percentage: int


@router.post("/start", response_model=SessionResponse)
async def start_session(
    request: StartSessionRequest,
    db: Session = Depends(get_db)
):
    print(f"DEBUG: start_session request: {request}")
    
    # 1. Get or Create User
    user = db.query(User).filter(User.email == request.user_email).first()
    if not user:
        user = User(username=request.user_email.split('@')[0], email=request.user_email)
        db.add(user)
        db.commit()
        db.refresh(user)
        
    # 2. Get Video
    video = None
    if request.video_id:
        print(f"DEBUG: Searching for specific video_id: {request.video_id}")
        video = db.query(Video).filter(Video.video_id == request.video_id).first()
        if video:
             print(f"DEBUG: Found video: {video.video_id} ({video.title})")
        else:
             print("DEBUG: Video not found by ID")
    
    # Fallback to existing logic if no video_id provided or not found
    if not video:
        print("DEBUG: video_id not provided or not found, falling back")
        # Try to get ANY video if ID wasn't specific
        if not request.video_id:
             video = db.query(Video).first()

        if not video:
            # Create default if absolutely nothing exists
            fixed_broadcast_time = "2026-02-11T19:00:00"
            
            video = Video(
                video_id="default_video_1",
                title="Default Training Video",
                file_path=request.video_filename,
                duration_seconds=600.0,
                broadcast_start_time=fixed_broadcast_time
            )
            db.add(video)
            db.commit()
            db.refresh(video)
    
    print(f"DEBUG: Final selected video: {video.video_id}")

    # 3. Create Session
    session = TrainingSession(
        user_id=user.id,
        video_id=video.video_id,
        started_at=datetime.now(),
        status="in_progress"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return SessionResponse(
        session_id=session.id,
        video_id=video.video_id,
        broadcast_start_time=video.broadcast_start_time,
        status=session.status
    )


@router.get("/history", response_model=List[SessionHistoryItem])
async def get_session_history(
    user_email: str = "guest@example.com",
    db: Session = Depends(get_db)
):
    """Get session history with statistics for a user"""
    
    # Get user
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return []
    
    # Get all sessions for this user
    sessions = db.query(TrainingSession).filter(
        TrainingSession.user_id == user.id
    ).order_by(TrainingSession.started_at.desc()).all()
    
    history = []
    for session in sessions:
        # Get all attempts for this session
        attempts = db.query(UserAttempt).filter(
            UserAttempt.session_id == session.id
        ).all()
        
        if not attempts:
            continue
        
        # Calculate statistics
        total_events = len(attempts)
        perfect_count = sum(1 for a in attempts if a.accuracy_level == 'perfect')
        good_count = sum(1 for a in attempts if a.accuracy_level == 'acceptable')
        missed_count = sum(1 for a in attempts if a.accuracy_level == 'miss')
        wrong_count = sum(1 for a in attempts if a.accuracy_level == 'false_positive')
        
        # Calculate accuracy percentage
        successful = perfect_count + good_count
        accuracy_percentage = round((successful / total_events) * 100) if total_events > 0 else 0
        
        # Get video name
        video_name = session.video.title if session.video else "Unknown Video"
        
        history.append(SessionHistoryItem(
            session_id=session.id,
            created_at=session.started_at.isoformat(),
            video_name=video_name,
            total_events=total_events,
            perfect_count=perfect_count,
            good_count=good_count,
            missed_count=missed_count,
            wrong_count=wrong_count,
            accuracy_percentage=accuracy_percentage
        ))
    
    return history
