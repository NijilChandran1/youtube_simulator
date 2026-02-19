import cv2
from typing import List, Tuple
import os
import logging

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self, frame_interval_seconds: float = 2.0):
        self.frame_interval = frame_interval_seconds
    
    def extract_frames(self, video_path: str) -> List[Tuple[float, bytes]]:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if fps == 0:
            # Fallback or error
            logger.warning("Could not determine FPS, assuming 30")
            fps = 30.0
            
        frame_interval = int(fps * self.frame_interval)
        if frame_interval < 1: frame_interval = 1
        
        frames = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Extract keyframe
            if frame_count % frame_interval == 0:
                timestamp = frame_count / fps
                # Encode to JPEG with optimization
                success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
                if success:
                    frames.append((timestamp, buffer.tobytes()))
            
            frame_count += 1
        
        cap.release()
        return frames

    def get_video_duration(self, video_path: str) -> float:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if fps == 0: return 0.0
        duration = frame_count / fps
        cap.release()
        return duration
