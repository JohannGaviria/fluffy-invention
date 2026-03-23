"""This module contains exception handlers for admin-related exceptions in the FastAPI application."""

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.contexts.admin.domain.exceptions.exception import (
    DoctorNotFoundException,
    DoctorScheduleAlreadyExistsException,
    InactiveDoctorException,
)
from src.shared.presentation.api.schemas.schemas import ErrorsResponse


def register_admin_exceptions_handlers(app: FastAPI) -> None:
    """Register admin-related exception handlers for the FastAPI application."""

    @app.exception_handler(DoctorNotFoundException)
    async def doctor_not_found_exception_handler(
        request: Request, exc: DoctorNotFoundException
    ) -> JSONResponse:
        """Handle DoctorNotFoundException exceptions.

        Args:
            request (Request): The incoming request that caused the exception.
            exc (DoctorNotFoundException): The exception instance.

        Returns:
            JSONResponse: A JSON response with a 404 status code and error details.
        """
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(
                ErrorsResponse(message="Doctor not found", details=[str(exc)])
            ),
        )

    @app.exception_handler(InactiveDoctorException)
    async def inactive_doctor_exception_handler(
        request: Request, exc: InactiveDoctorException
    ) -> JSONResponse:
        """Handle InactiveDoctorException exceptions.

        Args:
            request (Request): The incoming request that caused the exception.
            exc (InactiveDoctorException): The exception instance.

        Returns:
            JSONResponse: A JSON response with a 400 status code and error details.
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                ErrorsResponse(message="Doctor is inactive", details=[str(exc)])
            ),
        )

    @app.exception_handler(DoctorScheduleAlreadyExistsException)
    async def doctor_schedule_already_exists_exception_handler(
        request: Request, exc: DoctorScheduleAlreadyExistsException
    ) -> JSONResponse:
        """Handle DoctorScheduleAlreadyExistsException exceptions.

        Args:
            request (Request): The incoming request that caused the exception.
            exc (DoctorScheduleAlreadyExistsException): The exception instance.

        Returns:
            JSONResponse: A JSON response with a 400 status code and error details.
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                ErrorsResponse(
                    message="Doctor already has schedules assigned", details=[str(exc)]
                )
            ),
        )
