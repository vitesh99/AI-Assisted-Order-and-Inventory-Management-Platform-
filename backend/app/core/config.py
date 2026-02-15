from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Assisted Order and Inventory Management Platform"
    API_V1_STR: str = "/api/v1"
    
    # Database
    # Default to a single DB for the monolith
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db/ai_inventory_db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey123")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI (OpenRouter)
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "google/gemini-2.0-flash-lite-preview-02-05:free")
    ENABLE_AI: bool = True

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore" # Ignore extra fields from old .env files
    }

settings = Settings()
