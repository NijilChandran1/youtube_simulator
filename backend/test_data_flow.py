import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import datetime

# Add empty init files if missing to make packages importable
import app.models
import app.schemas

from app.database import Base, get_db
from app.main import app
from app.models import User, Video, TrainingSession, GroundTruthEvent, UserAttempt

# Setup Test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/data/test_persistence.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_timestamp_persistence():
    db = TestingSessionLocal()
    
    # 1. Seed Data
    print("Seeding data...")
    video = Video(
        video_id="test_vid_123",
        title="Test Video",
        file_path="test_video.mp4",
        duration_seconds=600,
        broadcast_start_time="2026-02-11T19:00:00"
    )
    db.add(video)
    db.commit()
    
    user = User(username="test_user", email="test@example.com")
    db.add(user)
    db.commit()
    
    session = TrainingSession(user_id=user.id, video_id=video.id)
    db.add(session)
    db.commit()
    
    # Ground Truth Event
    gt_event = GroundTruthEvent(
        video_id="test_vid_123",
        attribute="Main Logo",
        timestamp_seconds=10.5,
        live_clock_time="19:00:10.500",
        clue_description="Logo appears top right"
    )
    db.add(gt_event)
    db.commit()
    
    print(f"Created Session ID: {session.id}")
    
    # 2. Simulate Frontend Call
    payload = {
        "session_id": session.id,
        "attribute": "Main Logo",
        "user_timestamp_seconds": 10.6,
        "user_live_clock_time": "19:00:10.600",
        "video_timestamp_seconds": 10.6
    }
    
    print(f"Sending payload with user_live_clock_time: {payload['user_live_clock_time']}")
    
    response = client.post("/api/events/log", json=payload)
    
    if response.status_code != 200:
        print(f"❌ API Call Failed: {response.text}")
        return
        
    print("✅ API Call Successful")
    data = response.json()
    print(f"Response: {data}")
    
    # 3. Verify Database Persistence
    attempt = db.query(UserAttempt).filter(UserAttempt.session_id == session.id).first()
    
    if attempt:
        print(f"Retrieved Attempt from DB. ID: {attempt.id}")
        print(f"Stored user_live_clock_time: '{attempt.user_live_clock_time}'")
        
        if attempt.user_live_clock_time == payload["user_live_clock_time"]:
            print("✅ SUCCESS: Timestamp matched exactly!")
        else:
            print(f"❌ FAILURE: Mismatch. Expected '{payload['user_live_clock_time']}', got '{attempt.user_live_clock_time}'")
    else:
        print("❌ FAILURE: No attempt found in database.")
    
    db.close()

if __name__ == "__main__":
    test_timestamp_persistence()
