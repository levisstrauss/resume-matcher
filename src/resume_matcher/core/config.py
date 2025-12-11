from pydantic_settings import BaseSettings
from functools import lru_cache

import os
from dotenv import load_dotenv


class Settings(BaseSettings):
    # Database
    database_url: Optional[str] = None

    # OpenAI
    OPENAI_API_KEY: str

    # App settings
    debug: bool = False
    app_name: str = "Resume Matcher"
    api_v1_prefix: str = "/api/v1"

    # Embedding settings
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()