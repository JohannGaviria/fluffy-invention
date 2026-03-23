"""This module contains the API routes for the admin context."""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.contexts.admin.application.use_cases.assign_doctor_schedules_use_case import (
    AssignDoctorSchedulesUseCase,
)
from src.contexts.admin.domain.exceptions.exception import (
    DoctorNotFoundException,
    DoctorScheduleAlreadyExistsException,
    InactiveDoctorException,
)
from src.contexts.admin.presentation.api.compositions.use_cases_composition import (
    get_assign_doctor_schedules_use_case,
)
from src.contexts.admin.presentation.api.schemas.schema import (
    AssignDoctorSchedulesRequest,
)
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    MissingFieldException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger
from src.shared.presentation.api.compositions.infrastructure_composition import (
    get_logger,
)
from src.shared.presentation.api.compositions.security_composition import (
    get_current_user_admin,
)
from src.shared.presentation.api.schemas.schemas import ErrorsResponse, SuccessResponse

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post(
    path="/doctors/{doctor_id}/availability",
    summary="Assign schedules to a doctor",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorsResponse,
            "description": "Not found - Doctor not found.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorsResponse,
            "description": "Bad request - Invalid input data or doctor is inactive.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorsResponse,
            "description": "Internal server error - Database connection error or unexpected error.",
        },
    },
)
async def assign_doctor_schedules(
    request: AssignDoctorSchedulesRequest,
    doctor_id: UUID,
    use_case: AssignDoctorSchedulesUseCase = Depends(
        get_assign_doctor_schedules_use_case
    ),
    logger: Logger = Depends(get_logger),
    current_user: TokenPayloadVO = Depends(get_current_user_admin),
) -> JSONResponse:
    """Assign schedules to a doctor.

    This endpoint allows an admin to assign weekly schedules to a doctor.
    The request body should contain a mapping of days of the week to lists of schedule slots,
    along with the timezone for the schedules. The doctor_id is provided as a path parameter.

    Args:
        request (AssignDoctorSchedulesRequest): The request body containing
            schedules and timezone.
        doctor_id (UUID): The ID of the doctor to assign schedules to.
        use_case (AssignDoctorSchedulesUseCase): The use case for assigning doctor schedules.
        logger (Logger): The logger for logging errors.
        current_user (TokenPayloadVO): The current user token payload, used for authorization.

    Returns:
        JSONResponse: A response indicating success or failure of the operation.

    Raises:
        DoctorNotFoundException: If the doctor with the given ID does not exist.
        InactiveDoctorException: If the doctor is inactive and cannot be assigned schedules.
        DoctorScheduleAlreadyExistsException: If the doctor already has schedules assigned.
        MissingFieldException: If any required field is missing in the request.
        DatabaseConnectionException: If there is a database connection error during the operation.
        UnexpectedDatabaseException: If there is an unexpected database error during the operation.
        Exception: If any other unexpected error occurs during the execution of the use case,
            it will be logged and re-raised.
    """
    try:
        await use_case.execute(request.to_command(doctor_id))
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(
                SuccessResponse(message="Doctor schedules assigned successfully"),
                exclude_none=True,
            ),
        )
    except DoctorNotFoundException as e:
        logger.warning("Doctor not found", doctor_id=str(doctor_id), error=str(e))
        raise
    except InactiveDoctorException as e:
        logger.warning("Doctor is inactive", doctor_id=str(doctor_id), error=str(e))
        raise
    except DoctorScheduleAlreadyExistsException as e:
        logger.warning(
            "Doctor already has schedules assigned",
            doctor_id=str(doctor_id),
            error=str(e),
        )
        raise
    except MissingFieldException as e:
        logger.warning("Missing field in registration request", error=str(e))
        raise
    except (DatabaseConnectionException, UnexpectedDatabaseException) as e:
        logger.error("Database error during registration", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error during registration", error=str(e))
        raise
