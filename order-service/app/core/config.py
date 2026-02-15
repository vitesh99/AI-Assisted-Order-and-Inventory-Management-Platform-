from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Assisted Order and Inventory Management Platform"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

    # Internal Services
    INVENTORY_SERVICE_URL: str
    AUTH_SERVICE_URL: str

    # AI
    AI_API_KEY: str = ""
    AI_MODEL: str = "google/gemini-2.0-flash-lite-preview-02-05:free" # OpenRouter model
    ENABLE_AI: bool = True

settings = Settings()
