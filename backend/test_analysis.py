import httpx
import os
import asyncio
from pathlib import Path

async def test_video_analysis():
    # Base configuration
    API_URL = "http://localhost:8000/api/videos/analyze"
    VIDEO_PATH = r"c:\Users\NijilChandran\workspace\transformation\youtube_simulator\video\video.mp4"
    
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: Video file not found at {VIDEO_PATH}")
        return

    print(f"Uploading video: {VIDEO_PATH}")
    print(f"Target URL: {API_URL}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Prepare multipart form data
            files = {
                'video_file': ('video.mp4', open(VIDEO_PATH, 'rb'), 'video/mp4')
            }
            data = {
                'broadcast_start_time': '2026-02-11T19:00:00',
                'attribute_types': 'Main Logo,Copyright,Post-Game Start,Scoreboard,Replay Graphic'
            }
            
            print("Sending request... (this may take a minute depending on video size)")
            response = await client.post(API_URL, files=files, data=data)
            
            if response.status_code == 200:
                print("✅ Analysis Successful!")
                print("Response JSON:")
                import json
                print(json.dumps(response.json(), indent=2))
                
                # Verify key fields
                result = response.json()
                assert 'events' in result
                assert 'video_id' in result
                assert 'broadcast_start_time' in result
                print(f"Found {len(result['events'])} events.")
                
            else:
                print(f"❌ Analysis Failed with status {response.status_code}")
                print(response.text)
                
    except httpx.ConnectError:
        print("❌ connection error: Could not connect to server. Is uvicorn running?")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_video_analysis())
