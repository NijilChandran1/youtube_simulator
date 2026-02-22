"""
Seed script to populate ground truth events for the sample video.
Run this script to add sample ground truth data to the training database.
"""

from app.database import SessionLocal
from app.models import Video, GroundTruthEvent

def seed_ground_truth():
    db = SessionLocal()
    
    # ==========================================
    # TEMPLATE: HOW TO ADD A NEW VIDEO
    # ==========================================
    # 1. Define your video details:
    # target_video_id = "my_new_video"
    # target_title = "My New Video Title"
    # target_filename = "my_video.mp4"  # Ensure this file is in frontend/public/assets/
    # target_broadcast_start = "2026-03-01T12:00:00"
    # target_duration = 300.0
    #
    # 2. Define your events:
    # new_events = [
    #     {"attribute": "Kickoff", "timestamp_seconds": 10.5, "clue_description": "Game start"},
    #     {"attribute": "Goal", "timestamp_seconds": 45.0, "clue_description": "First goal"},
    # ]
    # ==========================================
    
    # Current Configuration
    target_video_id = "super_bowl_2026"
    target_title = " Super Bowl 2026"
    target_filename = "superbowl-2026.mp4"
    target_duration = 320.0
    target_broadcast_start = "2026-02-08T15:30:00"

    try:
        # Check if video exists, if not create it
        video = db.query(Video).filter(Video.video_id == target_video_id).first()
        if not video:
            print(f"Creating video: {target_title}...")
            video = Video(
                video_id=target_video_id,
                title=target_title,
                file_path=target_filename,
                duration_seconds=target_duration,
                broadcast_start_time=target_broadcast_start
            )
            db.add(video)
            db.commit()
            db.refresh(video)
            print(f"✅ Created video: {video.video_id}")
        else:
            print(f"✅ Video already exists: {video.video_id}")
        
        # Check if ground truth events already exist
        existing_events = db.query(GroundTruthEvent).filter(
            GroundTruthEvent.video_id == target_video_id
        ).count()
        
        if existing_events > 0:
            print(f"✅ {existing_events} ground truth events already seeded — skipping.")
            return
        
        # Sample ground truth events for the video
        # Adjusted for 192s duration
        sample_events = [
            {
                "attribute": "Broadcaster Logo",
                "timestamp_seconds": 5.0,
                "live_clock_time": "15:30:05.000",
                "clue_description": "NBCLogo appears at the start of the broadcast."
            },
            {
                "attribute": "Start of 3rd Quarter",
                "timestamp_seconds": 102,
                "live_clock_time": "15:31:42.000",
                "clue_description": "Considering covergae from promo of the super bowl.Play resumed with the opening of the third quarter"
            },
            {
                "attribute": "End of game",
                "timestamp_seconds": 244,
                "live_clock_time": "15:34:04.000",
                "clue_description": "Appearance of final slate is considered as the official conclusion of the game."
            },
            {
                "attribute": "Post gameshow",
                "timestamp_seconds": 285,
                "live_clock_time": "15:35:45.000",
                "clue_description": "Broadcast transitioned to the post game show segment after the commercial interval. Considered start of postgame presentation."
            },
        ]
        
        print(f"\nAdding {len(sample_events)} ground truth events...")
        for event_data in sample_events:
            event = GroundTruthEvent(
                video_id=target_video_id,
                attribute=event_data["attribute"],
                timestamp_seconds=event_data["timestamp_seconds"],
                live_clock_time=event_data["live_clock_time"],
                clue_description=event_data["clue_description"]
            )
            db.add(event)
        
        db.commit()
        print(f"✅ Successfully added {len(sample_events)} ground truth events!")
        
        # Display summary
        print("\n📊 Ground Truth Events Summary:")
        print("-" * 60)
        for event_data in sample_events:
            print(f"  {event_data['timestamp_seconds']:6.1f}s | {event_data['attribute']:20s} | {event_data['clue_description']}")
        print("-" * 60)
        print(f"\nTotal events: {len(sample_events)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Ground Truth Data Seeding Script")
    print("=" * 60)
    seed_ground_truth()
    print("\n✅ Done!")
