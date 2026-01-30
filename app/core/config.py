import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Inventory Platform"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changesthis_to_a_secure_random_secret_key_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        case_sensitive = True

settings = Settings()
