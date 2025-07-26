import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# API Settings
	API_V1_STR: str = "/api/v1"
	PROJECT_NAME: str = "A-Live-Grid"

	# Security
	SECRET_KEY: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

	# File Upload
	UPLOAD_DIR: str = "uploads"
	MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

	# Google Cloud Platform
	GOOGLE_CLOUD_PROJECT_ID: str | None = None
	GOOGLE_APPLICATION_CREDENTIALS: str | None = None

	# Firestore Collections
	USERS_COLLECTION: str = "users"
	POSTS_COLLECTION: str = "posts"
	VOTES_COLLECTION: str = "votes"

	# Agent Configuration
	OPENAI_API_KEY: str | None = None
	OPENAI_MODEL_NAME: str = "gpt-4.1"  # Default to gpt-4.1
	LANGSMITH_TRACING: bool = False
	LANGSMITH_ENDPOINT: str | None = None
	LANGSMITH_API_KEY: str | None = None
	LANGSMITH_PROJECT: str | None = None

	# Flask (if used by agent, otherwise can be removed)
	FLASK_DEBUG: bool = False
	FLASK_ENV: str = "production"

	class Config:
		env_file = ".env"
		extra = "ignore"  # Allow extra fields from .env without validation error


settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
