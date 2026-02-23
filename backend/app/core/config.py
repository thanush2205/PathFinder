"""
Configuration settings for PathFinder Backend
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    APP_NAME: str = os.getenv("APP_NAME", "PathFinder")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")
    FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL", "")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "")
    
    # CORS - use string to avoid pydantic JSON parsing
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:19006")
    
    @property
    def get_allowed_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # AI Configuration
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "./models/yolov8n.pt")
    DETECTION_CONFIDENCE: float = float(os.getenv("DETECTION_CONFIDENCE", 0.5))
    DETECTION_FPS: int = int(os.getenv("DETECTION_FPS", 20))
    
    # Voice Assistant
    TTS_ENGINE: str = os.getenv("TTS_ENGINE", "gtts")
    STT_LANGUAGE: str = os.getenv("STT_LANGUAGE", "en-US")
    VOICE_TIMEOUT: int = int(os.getenv("VOICE_TIMEOUT", 5))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        case_sensitive = True


settings = Settings()
