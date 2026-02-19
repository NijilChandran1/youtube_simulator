from app.database import SessionLocal
from app.models import Video

db = SessionLocal()
videos = db.query(Video).all()

print(f"Total videos found: {len(videos)}")
for v in videos:
    print(f"ID: {v.id}, VideoID: {v.video_id}, Title: {v.title}, Path: {v.file_path}")

db.close()
