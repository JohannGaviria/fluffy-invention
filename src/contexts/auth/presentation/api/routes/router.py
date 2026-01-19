"""This module contains the API routes for authentication-related operations."""

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.domain.exceptions.exception import (
    ActivationCodeExpiredException,
    EmailAlreadyExistsException,
    InvalidActivationCodeException,
    InvalidCorporateEmailException,
    InvalidEmailException,
    InvalidPasswordException,
    InvalidPasswordHashException,
    UnauthorizedUserRegistrationException,
    UserNotFoundException,
)
from src.contexts.auth.presentation.api.dependencies.dependency import (
    get_activate_account_use_case,
    get_logger,
    get_register_user_use_case,
)
from src.contexts.auth.presentation.api.schemas.schema import (
    ActivateUserAccountRequest,
    RegisterUserRequest,
)
from src.shared.domain.exception import (
    DatabaseConnectionException,
    MissingFieldException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger
from src.shared.presentation.api.schemas import ErrorsResponse, SuccessResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    path="/register",
    summary="Register a new user",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorsResponse,
            "description": "Bad Request - Invalid input data.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorsResponse,
            "description": "Forbidden - Unauthorized registration attempt.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorsResponse,
            "description": "Unprocessable Entity - Missing or invalid fields.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorsResponse,
            "description": "Internal Server Error - Database or server error.",
        },
    },
)
async def register_user(
    request: RegisterUserRequest,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
    logger: Logger = Depends(get_logger),
) -> JSONResponse:
    """Register a new user.

    This endpoint allows for the registration of a new user by accepting
    user details in the request body. It handles various exceptions that may
    arise during the registration process and returns appropriate HTTP responses.

    Args:
        request (RegisterUserRequest): The user registration request data.
        use_case (RegisterUserUseCase): The use case for registering a user.
        logger (Logger): The logger instance for logging events.

    Returns:
        JSONResponse: A JSON response indicating success or failure of the registration.

    Raises:
        HTTPException: Raised for various error conditions during registration.
        EmailAlreadyExistsException: If the email is already registered.
        InvalidCorporateEmailException: If the corporate email is invalid.
        InvalidEmailException: If the email format is invalid.
        InvalidPasswordException: If the password does not meet criteria.
        InvalidPasswordHashException: If there is an error hashing the password.
        UnauthorizedUserRegistrationException: If the user is not authorized to register.
        MissingFieldException: If required fields are missing in the request.
        DatabaseConnectionException: If there is a database connection error.
        UnexpectedDatabaseException: For any unexpected database errors.
    """
    try:
        use_case.execute(request.to_command())
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(
                SuccessResponse(message="User registered successfully"),
                exclude_none=True,
            ),
        )
    except (
        EmailAlreadyExistsException,
        InvalidCorporateEmailException,
        InvalidEmailException,
        InvalidPasswordException,
        InvalidPasswordHashException,
    ) as e:
        logger.warning("Registration error", error=str(e))
        raise
    except UnauthorizedUserRegistrationException as e:
        logger.warning("Unauthorized registration attempt", error=str(e))
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


@router.post(
    path="/activate",
    summary="",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorsResponse,
            "description": "Bad Request - Invalid input data.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorsResponse,
            "description": "Not Found - User not found.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorsResponse,
            "description": "Internal Server Error - Database or server error.",
        },
    },
)
async def activate_account(
    request: ActivateUserAccountRequest,
    use_case: ActivateAccountUseCase = Depends(get_activate_account_use_case),
    logger: Logger = Depends(get_logger),
) -> JSONResponse:
    """Activate a user account.

    This endpoint activates a user account using an activation code and email
    provided in the request body. It handles various exceptions that may arise
    during the activation process and returns appropriate HTTP responses.

    Args:
        request (ActivateUserAccountRequest): The account activation request data.
        use_case (ActivateAccountUseCase): The use case for activating a user account.
        logger (Logger): The logger instance for logging events.

    Returns:
        JSONResponse: A JSON response indicating success or failure of the activation.

    Raises:
        HTTPException: Raised for various error conditions during activation.
        ActivationCodeExpiredException: If the activation code has expired.
        InvalidActivationCodeException: If the activation code is invalid.
        UserNotFoundException: If the user is not found.
        DatabaseConnectionException: If there is a database connection error.
        UnexpectedDatabaseException: For any unexpected database errors.
    """
    try:
        use_case.execute(request.activation_code, request.email)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                SuccessResponse(message="User account activated successfully"),
                exclude_none=True,
            ),
        )
    except (ActivationCodeExpiredException, InvalidActivationCodeException) as e:
        logger.warning("Account activation error", error=str(e))
        raise
    except UserNotFoundException as e:
        logger.warning("User not found during account activation", error=str(e))
        raise
    except (DatabaseConnectionException, UnexpectedDatabaseException) as e:
        logger.error("Database error during account activation", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error during account activation", error=str(e))
        raise
