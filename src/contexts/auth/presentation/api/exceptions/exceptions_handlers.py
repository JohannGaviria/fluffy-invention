"""This module contains authentication-related exception handlers for the FastAPI application."""

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.contexts.auth.domain.exceptions.exception import (
    EmailAlreadyExistsException,
    InvalidCorporateEmailException,
    InvalidEmailException,
    InvalidPasswordException,
    InvalidPasswordHashException,
    UnauthorizedUserRegistrationException,
)
from src.shared.presentation.api.schemas import ErrorsResponse


def register_auth_exceptions_handlers(app: FastAPI) -> None:
    """Register authentication-related exception handlers for the FastAPI application."""

    @app.exception_handler(EmailAlreadyExistsException)
    async def email_already_exception_handler(
        request: Request, exc: EmailAlreadyExistsException
    ) -> JSONResponse:
        """Handle EmailAlreadyExistsException exceptions.

        Args:
            request (Request): The incoming request.
            exc (EmailAlreadyExistsException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            content=jsonable_encoder(
                ErrorsResponse(
                    message="Email already exists",
                    details=[str(exc)],
                )
            ),
            status_code=status.HTTP_409_CONFLICT,
        )

    @app.exception_handler(InvalidEmailException)
    async def invalid_email_exception_handler(
        request: Request, exc: InvalidEmailException
    ) -> JSONResponse:
        """Handle InvalidEmailException exceptions.

        Args:
            request (Request): The incoming request.
            exc (InvalidEmailException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            content=jsonable_encoder(
                ErrorsResponse(
                    message="Invalid email",
                    details=exc.errors,
                )
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(InvalidPasswordException)
    async def invalid_password_exception_handler(
        request: Request, exc: InvalidPasswordException
    ) -> JSONResponse:
        """Handle InvalidPasswordException exceptions.

        Args:
            request (Request): The incoming request.
            exc (InvalidPasswordException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            content=jsonable_encoder(
                ErrorsResponse(
                    message="Invalid password",
                    details=exc.errors,
                )
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(InvalidPasswordHashException)
    async def invalid_password_hash_exception_handler(
        request: Request, exc: InvalidPasswordHashException
    ) -> JSONResponse:
        """Handle InvalidPasswordHashException exceptions.

        Args:
            request (Request): The incoming request.
            exc (InvalidPasswordHashException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            content=jsonable_encoder(
                ErrorsResponse(
                    message="Internal server error",
                    details=[str(exc)],
                )
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(InvalidCorporateEmailException)
    async def invalid_corporate_email_exception_handler(
        request: Request, exc: InvalidCorporateEmailException
    ) -> JSONResponse:
        """Handle InvalidCorporateEmailException exceptions.

        Args:
            request (Request): The incoming request.
            exc (InvalidCorporateEmailException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            content=jsonable_encoder(
                ErrorsResponse(
                    message="Invalid corporate email",
                    details=[str(exc)],
                )
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(UnauthorizedUserRegistrationException)
    async def unauthorized_user_registration_exception_handler(
        request: Request, exc: UnauthorizedUserRegistrationException
    ) -> JSONResponse:
        """Handle UnauthorizedUserRegistrationException exceptions.

        Args:
            request (Request): The incoming request.
            exc (UnauthorizedUserRegistrationException): The raised exception.

        Returns:
            JSONResponse: A JSON response with error details.
        """
        return JSONResponse(
            content=jsonable_encoder(
                ErrorsResponse(
                    message="Unauthorized user registration attempt",
                    details=[str(exc)],
                )
            ),
            status_code=status.HTTP_403_FORBIDDEN,
        )
