from app.database import SessionLocal
from app.models import Video, GroundTruthEvent

db = SessionLocal()

print("--- VIDEOS ---")
videos = db.query(Video).all()
for v in videos:
    print(f"ID: {v.id}, VideoID: '{v.video_id}', Title: '{v.title}', File: '{v.file_path}'")

print("\n--- GROUND TRUTH EVENTS ---")
events = db.query(GroundTruthEvent).all()
for e in events:
    print(f"ID: {e.id}, VideoID: '{e.video_id}', Attribute: '{e.attribute}', Time: {e.timestamp_seconds}")

db.close()
