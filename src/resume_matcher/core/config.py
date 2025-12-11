from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/resume_matcher"

    # OpenAI
    OPENAI_API_KEY: str = "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"

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