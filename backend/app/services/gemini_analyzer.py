from google import genai
from google.genai import types
from typing import List, Dict
import json
import logging
import re
import os

logger = logging.getLogger(__name__)

class GeminiAnalyzer:
    def __init__(self, project_id: str, location: str = "us-central1", credentials_path: str = None, model_id: str = "gemini-2.0-flash-001"):
        if not project_id:
            raise ValueError("Google Cloud Project ID is required")
        
        # Set service account credentials if provided
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            logger.info(f"Using service account credentials from: {credentials_path}")
        
        # Initialize Vertex AI client
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )
        self.model_id = model_id 
    
    def analyze_frames(
        self, 
        frames: List[tuple[float, bytes]],
        attribute_types: List[str]
    ) -> List[Dict]:
        
        prompt = self._build_analysis_prompt(attribute_types, frames)
        
        # Build contents list beginning with the prompt
        contents = [prompt]
        
        # Add frames as separate parts
        for timestamp, frame_bytes in frames:
            contents.append(
                types.Part.from_bytes(
                    data=frame_bytes,
                    mime_type="image/jpeg"
                )
            )
            
        try:
            logger.info(f"Sending {len(frames)} frames to Gemini for analysis...")
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents
            )
            return self._parse_gemini_response(response.text, frames)
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            raise

    def _build_analysis_prompt(self, attribute_types: List[str], frames: List) -> str:
        frame_info = "\n".join([
            f"Frame {i}: {ts:.2f}s" 
            for i, (ts, _) in enumerate(frames)
        ])
        
        return f"""
You are an expert EPG analyst for sports broadcasts.

Analyze these {len(frames)} frames and identify these event types:
{', '.join(attribute_types)}

Frame timestamps (in seconds):
{frame_info}

For each event detected:
1. Specify the frame number (index in the list, 0 to {len(frames)-1})
2. Provide a detailed visual clue description
3. Rate confidence (0.0 to 1.0)

Focus on TRANSITIONS: new elements appearing, graphics changing, or scene shifts.

Output ONLY valid JSON in this exact format:
{{
  "events": [
    {{
      "attribute": "Main Logo",
      "frame_number": 5,
      "clue_description": "Broadcaster watermark appears in top-right",
      "confidence": 0.92
    }}
  ]
}}
"""
    
    def _parse_gemini_response(self, text: str, frames: List) -> List[Dict]:
        try:
            # Clean markdown code blocks if present
            clean_text = re.sub(r'```json\s*', '', text)
            clean_text = re.sub(r'```\s*$', '', clean_text)
            
            # Extract JSON substring
            json_start = clean_text.find('{')
            json_end = clean_text.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
                
            json_str = clean_text[json_start:json_end]
            
            data = json.loads(json_str)
            events = []
            
            for event in data.get('events', []):
                frame_num = event.get('frame_number')
                if frame_num is not None and 0 <= frame_num < len(frames):
                    timestamp = frames[frame_num][0]
                    events.append({
                        'attribute': event.get('attribute'),
                        'timestamp_seconds': timestamp,
                        'clue_description': event.get('clue_description'),
                        'confidence_score': event.get('confidence', 0.0)
                    })
            
            return events
        except Exception as e:
            logger.error(f"Failed to parse Gemini response: {e}. Raw text: {text}")
            # Return empty list or re-raise? Re-raising helps debug.
            raise ValueError(f"Failed to parse Gemini response: {e}")
