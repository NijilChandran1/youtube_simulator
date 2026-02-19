import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_start_session():
    print("Testing Start Session Endpoint...")
    url = f"{BASE_URL}/api/sessions/start"
    payload = {
        "user_email": "test_user@example.com"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Session Started: {data}")
        
        if "session_id" not in data:
            print("❌ No session_id in response")
            sys.exit(1)
            
        if "broadcast_start_time" not in data:
            print("❌ No broadcast_start_time in response")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Failed: {e}")
        if response is not None:
             print(f"Response Content: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_start_session()
