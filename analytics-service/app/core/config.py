from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Analytics Service"
    API_V1_STR: str = "/api/v1"
    
    # Needs access to Order and Inventory DBs. 
    # For this modular setup, we point to the main DB.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db/ai_inventory_db")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()
