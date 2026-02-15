from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Inventory Platform Gateway"
    API_V1_STR: str = "/api/v1"
    
    # Microservices URLs
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    INVENTORY_SERVICE_URL: str = "http://inventory-service:8000"
    ORDER_SERVICE_URL: str = "http://order-service:8000"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

settings = Settings()
