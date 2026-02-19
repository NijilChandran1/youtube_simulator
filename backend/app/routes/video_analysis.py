from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import tempfile
import time
from pathlib import Path
import os
import shutil

from app.services.video_processor import VideoProcessor
from app.services.gemini_analyzer import GeminiAnalyzer
from app.services.ground_truth_generator import GroundTruthGenerator
from app.config import settings
from app.database import get_db
from app.models import Video, GroundTruthEvent

router = APIRouter(prefix="/api/videos", tags=["video-analysis"])

@router.post("/analyze")
async def analyze_video(
    video_file: UploadFile = File(...),
    broadcast_start_time: str = Form(...),
    attribute_types: str = Form(
        default="Main Logo,Copyright,Post-Game Start,Scoreboard,Replay Graphic"
    ),
    db: Session = Depends(get_db)
):
    """
    Analyze a video and generate ground truth JSON.
    Also saves the Video and GroundTruthEvent records to the database.
    """
    start_time = time.time()
    print(f"Analyzing video: {video_file.filename}")
    
    # Validate file type
    allowed_types = ['video/mp4', 'video/webm', 'video/quicktime', 'application/octet-stream'] # Octet stream sometimes sent
    if video_file.content_type not in allowed_types:
        # Check by extension if content-type is generic
        ext = Path(video_file.filename).suffix.lower()
        if ext not in ['.mp4', '.webm', '.mov']:
             raise HTTPException(400, f"Invalid video format: {video_file.content_type}")
    
    # Save uploaded file temporarily
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    tmp_path = os.path.join(settings.UPLOAD_DIR, f"temp_{int(time.time())}_{video_file.filename}")
    
    try:
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
            
        # Initialize services
        # Note: frame_interval could be dynamic based on video length
        processor = VideoProcessor(frame_interval_seconds=2.0)
        analyzer = GeminiAnalyzer(
            project_id=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION,
            credentials_path=settings.GOOGLE_APPLICATION_CREDENTIALS,
            model_id=settings.GEMINI_MODEL
        )
        generator = GroundTruthGenerator()
        
        # Extract frames
        print("Extracting frames...")
        frames = processor.extract_frames(tmp_path)
        print(f"Extracted {len(frames)} frames")
        
        duration = processor.get_video_duration(tmp_path)
        
        if not frames:
             raise HTTPException(400, "Could not extract any frames from the video")
        
        # Analyze with Gemini
        attributes = [a.strip() for a in attribute_types.split(',')]
        print(f"Analyzing frames with Gemini... looking for {attributes}")
        events = analyzer.analyze_frames(frames, attributes)
        print(f"Gemini found {len(events)} events")
        
        # Generate ground truth JSON
        video_id = Path(video_file.filename).stem
        ground_truth = generator.generate_json(
            video_id=video_id,
            broadcast_start_time=broadcast_start_time,
            events=events,
            duration_seconds=duration
        )
        
        # === NEW: Save to Database ===
        try:
            # 1. Check if video already exists, if not create it
            video_record = db.query(Video).filter(Video.video_id == video_id).first()
            if not video_record:
                video_record = Video(
                    video_id=video_id,
                    title=video_file.filename,
                    file_path=video_file.filename,
                    duration_seconds=duration,
                    broadcast_start_time=broadcast_start_time
                )
                db.add(video_record)
                db.commit()
                db.refresh(video_record)
                print(f"✅ Created Video record: {video_id}")
            else:
                print(f"✅ Video record already exists: {video_id}")
            
            # 2. Delete existing ground truth events for this video (if re-analyzing)
            existing_count = db.query(GroundTruthEvent).filter(
                GroundTruthEvent.video_id == video_id
            ).count()
            
            if existing_count > 0:
                db.query(GroundTruthEvent).filter(
                    GroundTruthEvent.video_id == video_id
                ).delete()
                db.commit()
                print(f"🗑️  Deleted {existing_count} existing ground truth events")
            
            # 3. Save new ground truth events
            for event_data in ground_truth['events']:
                gt_event = GroundTruthEvent(
                    video_id=video_id,
                    attribute=event_data['attribute'],
                    timestamp_seconds=event_data['timestamp_seconds'],
                    live_clock_time=event_data['live_clock_time'],
                    clue_description=event_data['clue_description']
                )
                db.add(gt_event)
            
            db.commit()
            print(f"✅ Saved {len(ground_truth['events'])} ground truth events to database")
            
            ground_truth['database_saved'] = True
            ground_truth['events_saved'] = len(ground_truth['events'])
            
        except Exception as db_error:
            print(f"⚠️  Database save failed: {db_error}")
            db.rollback()
            ground_truth['database_saved'] = False
            ground_truth['database_error'] = str(db_error)
        
        # Add metadata
        ground_truth['analysis_status'] = 'completed'
        ground_truth['processing_time_seconds'] = time.time() - start_time
        ground_truth['frames_analyzed'] = len(frames)
        
        return JSONResponse(content=ground_truth)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Analysis failed: {str(e)}")
    
    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
