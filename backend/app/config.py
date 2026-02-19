from pydantic_settings import BaseSettings
from typing import Optional, List
from pathlib import Path

# Get the directory where this config.py file is located
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Vertex AI Configuration
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None  # Path to service account key file
    GEMINI_MODEL: str = "gemini-2.0-flash-001"  # Default model
    
    # Path relative to project root (where uvicorn is run)
    DATABASE_URL: str = "sqlite:///./data/training.db"
    
    UPLOAD_DIR: str = "uploads/videos"
    MAX_VIDEO_SIZE_MB: int = 500
    ALLOWED_VIDEO_FORMATS: List[str] = ["mp4", "webm", "mov"]

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
