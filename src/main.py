"""This module contains the main FastAPI application."""

from fastapi import FastAPI

from src.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    summary=settings.APP_SUMMARY,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
)


@app.get("/")
async def root():
    """Root endpoint providing basic application info."""
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "environment": settings.ENVIRONMENT,
    }
