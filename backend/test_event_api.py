"""
Test script to verify the /api/events/log endpoint is working correctly
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
SESSION_ID = 3  # Use the latest session ID from database

def test_event_logging():
    print("=" * 60)
    print("Testing Event Logging API")
    print("=" * 60)
    
    # Test payload
    payload = {
        "session_id": SESSION_ID,
        "attribute": "Main Logo",
        "user_timestamp_seconds": 5.5,
        "user_live_clock_time": "19:00:05.500",
        "video_timestamp_seconds": 5.5
    }
    
    print(f"\n📤 Sending test event:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/events/log",
            json=payload
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS! Feedback received:")
            print(json.dumps(data, indent=2))
            
            print(f"\n📊 Feedback Summary:")
            print(f"   Accuracy: {data.get('accuracy_level')}")
            print(f"   Time Difference: {data.get('time_difference_ms')}ms")
            if data.get('ground_truth'):
                print(f"   Ground Truth Time: {data['ground_truth']['live_clock_time']}")
                print(f"   Clue: {data['ground_truth']['clue_description']}")
            if data.get('ai_feedback'):
                print(f"   AI Feedback: {data['ai_feedback']}")
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Request failed: {e}")

if __name__ == "__main__":
    test_event_logging()
