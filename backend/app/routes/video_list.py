from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.models import Video

router = APIRouter(prefix="/api/videos", tags=["videos"])

class VideoListResponse(BaseModel):
    id: int
    video_id: str
    title: str
    duration_seconds: float
    file_path: str
    broadcast_start_time: str

@router.get("/list", response_model=List[VideoListResponse])
async def get_video_list(db: Session = Depends(get_db)):
    """
    Fetch all available videos from the database
    """
    videos = db.query(Video).all()
    
    return [
        VideoListResponse(
            id=video.id,
            video_id=video.video_id,
            title=video.title,
            duration_seconds=video.duration_seconds,
            file_path=video.file_path,
            broadcast_start_time=video.broadcast_start_time
        )
        for video in videos
    ]

@router.get("/{video_id}/attributes", response_model=List[str])
async def get_video_attributes(video_id: str, db: Session = Depends(get_db)):
    """
    Fetch distinct event attributes for a specific video
    """
    from app.models import GroundTruthEvent
    
    # Query distinct attributes for the given video_id
    results = db.query(GroundTruthEvent.attribute).filter(
        GroundTruthEvent.video_id == video_id
    ).distinct().all()
    
    # results is list of tuples [('Main Logo',), ('Copyright',)]
    attributes = [r[0] for r in results]
    
    # If no attributes found (e.g. manual video without ground truth), return default list?
    if not attributes:
        # Default fallback for legacy/manual videos
        return [
            "Main Logo",
            "Copyright", 
            "Post-Game Start", 
            "Scoreboard", 
            "Replay Graphic"
        ]
        
    return attributes
