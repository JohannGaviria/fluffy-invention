"""This module contains the main FastAPI application."""

from fastapi import FastAPI

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


@app.get("/")
async def root():
    """Root endpoint providing basic application info."""
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "environment": settings.ENVIRONMENT,
    }
