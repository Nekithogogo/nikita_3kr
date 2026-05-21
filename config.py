from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    MODE: str = "DEV"               # DEV / PROD
    DOCS_USER: str = "admin"
    DOCS_PASSWORD: str = "secret"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()