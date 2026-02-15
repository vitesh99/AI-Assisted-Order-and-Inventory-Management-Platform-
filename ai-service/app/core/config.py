from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Service"
    API_V1_STR: str = "/api/v1"
    
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "openai/gpt-3.5-turbo")

    INVENTORY_SERVICE_URL: str = os.getenv("INVENTORY_SERVICE_URL", "http://inventory-service:8000/api/v1/inventory")
    ORDER_SERVICE_URL: str = os.getenv("ORDER_SERVICE_URL", "http://order-service:8000/api/v1/orders")
    ANALYTICS_SERVICE_URL: str = os.getenv("ANALYTICS_SERVICE_URL", "http://analytics-service:8000/api/v1/analytics")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()
