from datetime import datetime, timedelta
from typing import List, Dict

class GroundTruthGenerator:
    def generate_json(
        self,
        video_id: str,
        broadcast_start_time: str,
        events: List[Dict],
        duration_seconds: float
    ) -> Dict:
        """
        Generate ground truth JSON from detected events
        """
        try:
            start_time = datetime.fromisoformat(broadcast_start_time)
        except ValueError:
            # Fallback if isoformat parsing fails (try without T or other formats?)
            # Usually FastAPI ensures ISO format string
            start_time = datetime.now() # Should not happen with valid input
        
        formatted_events = []
        for event in events:
            timestamp_sec = event['timestamp_seconds']
            live_time = start_time + timedelta(seconds=timestamp_sec)
            
            formatted_events.append({
                'attribute': event['attribute'],
                'timestamp_seconds': timestamp_sec,
                'live_clock_time': live_time.strftime('%H:%M:%S.%f')[:-3],
                'clue_description': event['clue_description'],
                'confidence_score': event.get('confidence_score', 0.0)
            })
        
        # Sort by timestamp
        formatted_events.sort(key=lambda x: x['timestamp_seconds'])
        
        return {
            'video_id': video_id,
            'duration_seconds': duration_seconds,
            'broadcast_start_time': broadcast_start_time,
            'events': formatted_events
        }
