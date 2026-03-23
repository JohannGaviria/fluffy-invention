"""This module contains the main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.contexts.admin.infrastructure.persistence.documents.doctor_schedules_document import (
    DoctorSchedulesDocument,
)
from src.contexts.admin.presentation.api.exceptions.exceptions_handlers import (
    register_admin_exceptions_handlers,
)
from src.contexts.admin.presentation.api.routes.router import router as admin_router
from src.contexts.auth.presentation.api.exceptions.exceptions_handlers import (
    register_auth_exceptions_handlers,
)
from src.contexts.auth.presentation.api.routes.router import router
from src.shared.infrastructure.db.mongo import MongoDatabase
from src.shared.presentation.api.exceptions.exceptions_handlers import (
    register_exceptions_handlers,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    await MongoDatabase.init_beanie(document_models=[DoctorSchedulesDocument])
    yield
    MongoDatabase.close_client()


app = FastAPI(
    title=settings.APP_NAME,
    summary=settings.APP_SUMMARY,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Include API routers
app.include_router(router)
app.include_router(admin_router)

# Register exception handlers
register_auth_exceptions_handlers(app)
register_admin_exceptions_handlers(app)
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
