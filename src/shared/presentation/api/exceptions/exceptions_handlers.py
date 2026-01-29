"""This module contains exception handlers for the FastAPI application."""

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)
from src.shared.presentation.api.schemas.schemas import ErrorsResponse


def register_exceptions_handlers(app: FastAPI) -> None:
    """Register exception handlers for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.exception_handler(DatabaseConnectionException)
    async def database_connection_exception_handler(
        request: Request, exc: DatabaseConnectionException
    ) -> JSONResponse:
        """Handle DatabaseConnectionException exceptions.

        Args:
            request (Request): The incoming request.
            exc (DatabaseConnectionException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            jsonable_encoder(
                ErrorsResponse(message="Database connection error", details=[str(exc)])
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(UnexpectedDatabaseException)
    async def unexpected_database_exception_handler(
        request: Request, exc: UnexpectedDatabaseException
    ) -> JSONResponse:
        """Handle UnexpectedDatabaseException exceptions.

        Args:
            request (Request): The incoming request.
            exc (UnexpectedDatabaseException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            jsonable_encoder(
                ErrorsResponse(message="Unexpected database error", details=[str(exc)])
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(Exception)
    async def application_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle generic Exception exceptions.

        Args:
            request (Request): The incoming request.
            exc (Exception): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            jsonable_encoder(
                ErrorsResponse(message="Internal server error", details=[str(exc)])
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
