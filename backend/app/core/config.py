from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    api_v1_prefix: str = "/api/v1"
    
    # MongoDB Settings
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "student_db"
    
    # JWT Settings
    jwt_secret_key: str = "your-secret-key"  # Change in production!
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS Settings
    allowed_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()