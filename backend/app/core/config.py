from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Google APIs
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    GOOGLE_ADDRESS_VALIDATION_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 