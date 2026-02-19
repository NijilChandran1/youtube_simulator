from google import genai
from app.config import settings
import logging
import os

logger = logging.getLogger(__name__)

class VertexAIService:
    def __init__(self):
        if not settings.GOOGLE_CLOUD_PROJECT:
            logger.warning("GOOGLE_CLOUD_PROJECT not set. Feedback generation will fail.")
            self.client = None
        else:
            # Set service account credentials if provided
            if settings.GOOGLE_APPLICATION_CREDENTIALS:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
                logger.info(f"Using service account credentials from: {settings.GOOGLE_APPLICATION_CREDENTIALS}")
            
            # Initialize Vertex AI client
            self.client = genai.Client(
                vertexai=True,
                project=settings.GOOGLE_CLOUD_PROJECT,
                location=settings.GOOGLE_CLOUD_LOCATION
            )
        
        # Use model from settings
        self.model_id = settings.GEMINI_MODEL
    
    def generate_feedback(
        self,
        attribute: str,
        user_time: str,
        actual_time: str,
        clue_description: str,
        time_difference_ms: float
    ) -> str:
        if not self.client:
            return "AI Feedback unavailable (Vertex AI not configured)."

        prompt = f"""
You are a patient and helpful EPG training mentor.

The user logged the event '{attribute}' at {user_time}. 
The actual Ground Truth time was {actual_time}. 
The visual clue for this event is: '{clue_description}'.
The time difference was: {time_difference_ms:.0f}ms.

Scenario: 
- If the user was late (user time > actual time), explain the visual transition they missed or reacted slowly to.
- If the user was early (user time < actual time), warn them about 'False Starts' or anticipating too much.
- If they were close (within 2000ms), provide encouragement and a tip to be even more precise.

Keep the feedback concise (max 2 sentences) and encouraging. Focus on the visual cue.
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Feedback generation failed: {e}")
            return "Great job spotting that! Keep watching for the visual cues."
