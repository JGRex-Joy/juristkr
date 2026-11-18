from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JURISTKR_",
        env_file=".env",
        extra="ignore",
    )

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "articles"


@lru_cache
def get_settings() -> Settings:
    return Settings()
