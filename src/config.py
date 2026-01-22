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
    LOG_LEVEL: str = Field(..., validation_alias="LOG_LEVEL")
    ALLOWED_STAFF_EMAIL_DOMAINS: str = Field(
        ..., validation_alias="ALLOWED_STAFF_EMAIL_DOMAINS"
    )
    ALLOWED_STAFF_ROLES: str = Field(..., validation_alias="ALLOWED_STAFF_ROLES")

    # Security configuration
    JWT_SECRET_KEY: str = Field(..., validation_alias="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(..., validation_alias="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRES_IN: int = Field(
        ..., validation_alias="ACCESS_TOKEN_EXPIRES_IN"
    )
    LOGIN_ATTEMPTS_LIMIT: int = Field(..., validation_alias="LOGIN_ATTEMPTS_LIMIT")
    LOGIN_WAITING_TIME: int = Field(..., validation_alias="LOGIN_WAITING_TIME")

    # Database configuration
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    DB_PORT: int = Field(..., validation_alias="DB_PORT")
    POSTGRES_USER: str = Field(..., validation_alias="POSTGRES_USER")
    POSTGRES_DB: str = Field(..., validation_alias="POSTGRES_DB")
    POSTGRES_PASSWORD: str = Field(..., validation_alias="POSTGRES_PASSWORD")

    # Redis configuration
    REDIS_PORT: int = Field(..., validation_alias="REDIS_PORT")
    REDIS_PASSWORD: str = Field(..., validation_alias="REDIS_PASSWORD")
    REDIS_HOST: str = Field(..., validation_alias="REDIS_HOST")
    REDIS_DB: int = Field(..., validation_alias="REDIS_DB")

    # Notification configuration
    SMTP_SERVER: str = Field(..., validation_alias="SMTP_SERVER")
    SMTP_PORT: int = Field(..., validation_alias="SMTP_PORT")
    USER_EMAIL: str = Field(..., validation_alias="USER_EMAIL")
    USER_PASSWORD: str = Field(..., validation_alias="USER_PASSWORD")
    TEMPLATE_PATH: str = Field(..., validation_alias="TEMPLATE_PATH")

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    """Get cached application settings."""
    return Settings()


settings = get_settings()
