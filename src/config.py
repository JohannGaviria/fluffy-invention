"""This module contains the application configuration settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # Application metadata
    APP_NAME: str = Field(..., validation_alias="APP_NAME")
    APP_SUMMARY: str = Field(..., validation_alias="APP_SUMMARY")
    APP_DESCRIPTION: str = Field(..., validation_alias="APP_DESCRIPTION")
    
    # Backend configuration
    DEBUG: str = Field(..., validation_alias="DEBUG")
    ENVIRONMENT: str = Field(..., validation_alias="ENVIRONMENT")
    BACKEND_PORT: int = Field(..., validation_alias="BACKEND_PORT")
    BACKEND_WORKERS: int = Field(..., validation_alias="BACKEND_WORKERS")

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    """Get cached application settings."""
    return Settings()


settings = get_settings()
