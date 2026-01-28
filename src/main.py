"""This module contains the main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.contexts.auth.presentation.api.exceptions.exceptions_handlers import (
    register_auth_exceptions_handlers,
)
from src.contexts.auth.presentation.api.routes.router import router
from src.shared.presentation.api.exceptions_handlers import register_exceptions_handlers

app = FastAPI(
    title=settings.APP_NAME,
    summary=settings.APP_SUMMARY,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
)

app.include_router(router)

register_auth_exceptions_handlers(app)
register_exceptions_handlers(app)


# Parse allowed origins for CORS from settings
allow_origins = [origin.strip() for origin in settings.CORS_ALLOW_ORIGINS.split(",")]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=(
        [origin.strip() for origin in settings.CORS_ALLOW_METHODS.split(",")]
    ),
    allow_headers=(
        [origin.strip() for origin in settings.CORS_ALLOW_HEADERS.split(",")]
    ),
)


@app.get("/")
async def root():
    """Root endpoint providing basic application info."""
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "environment": settings.ENVIRONMENT,
    }
