from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str

    # Authentication settings
    BETTER_AUTH_SECRET: str

    # Application settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Frontend settings
    NEXT_PUBLIC_API_BASE_URL: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()