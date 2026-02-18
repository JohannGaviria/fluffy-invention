"""This module contains the API routes for authentication-related operations."""

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.application.use_cases.login_use_case import LoginUseCase
from src.contexts.auth.application.use_cases.password_recovery_use_case import (
    PasswordRecoveryUseCase,
)
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.application.use_cases.reset_password_use_case import (
    ResetPasswordUseCase,
)
from src.contexts.auth.application.use_cases.update_user_password_use_case import (
    UpdateUserPasswordUseCase,
)
from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.exceptions.exception import (
    AccountTemporarilyBlockedException,
    ActivationCodeExpiredException,
    CurrentPasswordIncorrectException,
    DoctorLicenseNumberAlreadyRegisteredException,
    DoctorProfileAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidActivationCodeException,
    InvalidCorporateEmailException,
    InvalidCredentialsException,
    InvalidEmailException,
    InvalidPasswordException,
    InvalidPasswordHashException,
    NewPasswordEqualsCurrentException,
    PatientDocumentAlreadyRegisteredException,
    PatientPhoneAlreadyRegisteredException,
    PatientProfileAlreadyExistsException,
    UnauthorizedUserRegistrationException,
    UserInactiveException,
    UserNotFoundException,
)
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.contexts.auth.presentation.api.compositions.use_cases_composition import (
    get_activate_account_use_case,
    get_login_use_case,
    get_password_recovery_use_case,
    get_register_user_use_case,
    get_reset_password_use_case,
    get_update_user_password_use_case,
)
from src.contexts.auth.presentation.api.mappers.mapper import AccessTokenResponseMapper
from src.contexts.auth.presentation.api.schemas.schema import (
    ActivateUserAccountRequest,
    LoginRequest,
    PasswordRecoveryRequest,
    RegisterUserRequest,
    ResetPasswordRequest,
    UpdateUserPasswordRequest,
)
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    MissingFieldException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger
from src.shared.presentation.api.compositions.security_composition import (
    get_current_user,
    get_logger,
    request_details_dependency,
)
from src.shared.presentation.api.schemas.schemas import ErrorsResponse, SuccessResponse

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
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
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
    current_user: TokenPayloadVO = Depends(get_current_user),
) -> JSONResponse:
    """Register a new user.

    This endpoint allows for the registration of a new user by accepting
    user details in the request body. It handles various exceptions that may
    arise during the registration process and returns appropriate HTTP responses.

    Args:
        request (RegisterUserRequest): The user registration request data.
        use_case (RegisterUserUseCase): The use case for registering a user.
        logger (Logger): The logger instance for logging events.
        current_user (TokenPayloadVO): The currently authenticated user performing the registration.

    Returns:
        JSONResponse: A JSON response indicating success or failure of the registration.

    Raises:
        HTTPException: Raised for various error conditions during registration.
        EmailAlreadyExistsException: If the email is already registered.
        InvalidCorporateEmailException: If the corporate email is invalid.
        InvalidEmailException: If the email format is invalid.
        InvalidPasswordException: If the password does not meet criteria.
        InvalidPasswordHashException: If there is an error hashing the password.
        PatientDocumentAlreadyRegisteredException: If the patient document is already registered.
        PatientPhoneAlreadyRegisteredException: If the patient phone number is already registered.
        PatientProfileAlreadyExistsException: If the patient profile already exists.
        DoctorLicenseNumberAlreadyRegisteredException: If the doctor license number is already registered.
        DoctorProfileAlreadyExistsException: If the doctor profile already exists.
        UnauthorizedUserRegistrationException: If the user is not authorized to register.
        MissingFieldException: If required fields are missing in the request.
        DatabaseConnectionException: If there is a database connection error.
        UnexpectedDatabaseException: For any unexpected database errors.
    """
    try:
        use_case.execute(request.to_command(RolesEnum(current_user.role)))
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
        PatientDocumentAlreadyRegisteredException,
        PatientPhoneAlreadyRegisteredException,
        PatientProfileAlreadyExistsException,
        DoctorLicenseNumberAlreadyRegisteredException,
        DoctorProfileAlreadyExistsException,
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


@router.post(
    path="/login",
    summary="User login",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorsResponse,
            "description": "Bad Request - Invalid input data.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorsResponse,
            "description": "Unauthorized - Invalid credentials.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorsResponse,
            "description": "Forbidden - Account temporarily blocked.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorsResponse,
            "description": "Internal Server Error - Database or server error.",
        },
    },
)
async def login_user(
    request: LoginRequest,
    use_case: LoginUseCase = Depends(get_login_use_case),
    logger: Logger = Depends(get_logger),
) -> JSONResponse:
    """Authenticate a user and provide an access token.

    This endpoint allows users to log in by providing their email and password.
    It handles various exceptions that may arise during the login process and
    returns appropriate HTTP responses.

    Args:
        request (RegisterUserRequest): The user login request data.
        use_case (LoginUseCase): The use case for user login.
        logger (Logger): The logger instance for logging events.

    Returns:
        JSONResponse: A JSON response containing the access token or indicating failure.

    Raises:
        HTTPException: Raised for various error conditions during login.
        InvalidCredentialsException: If the provided credentials are invalid.
        AccountTemporarilyBlockedException: If the account is temporarily blocked due to too many failed attempts.
        DatabaseConnectionException: If there is a database connection error.
        UnexpectedDatabaseException: For any unexpected database errors.
    """
    try:
        response = use_case.execute(request.to_command())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                SuccessResponse(
                    message="Login successful",
                    data=AccessTokenResponseMapper.response(response),
                )
            ),
        )
    except InvalidCredentialsException as e:
        logger.warning("Invalid login credentials", error=str(e))
        raise
    except AccountTemporarilyBlockedException as e:
        logger.warning("Account temporarily blocked", error=str(e))
        raise
    except UserInactiveException as e:
        logger.warning("Inactive user account", error=str(e))
        raise
    except (DatabaseConnectionException, UnexpectedDatabaseException) as e:
        logger.error("Database error during login", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error during login", error=str(e))
        raise


@router.put(
    path="/password",
    summary="Update user password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorsResponse,
            "description": "Bad Request - Invalid input data.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorsResponse,
            "description": "Unauthorized - Invalid credentials.",
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
async def update_password(
    request: UpdateUserPasswordRequest,
    current_user: TokenPayloadVO = Depends(get_current_user),
    use_case: UpdateUserPasswordUseCase = Depends(get_update_user_password_use_case),
    logger: Logger = Depends(get_logger),
) -> JSONResponse:
    """Update the password of the current user.

    This endpoint allows the currently authenticated user to update their password.
    It handles various exceptions that may arise during the password update process
    and returns appropriate HTTP responses.

    Args:
        request (UpdateUserPasswordRequest): The password update request data.
        current_user (TokenPayloadVO): The currently authenticated user.
        use_case (UpdateUserPasswordUseCase): The use case for updating the user password.
        logger (Logger): The logger instance for logging events.

    Returns:
        JSONResponse: A JSON response indicating success or failure of the password update.

    Raises:
        HTTPException: Raised for various error conditions during password update.
        NewPasswordEqualsCurrentException: If the new password is the same as the current password.
        CurrentPasswordIncorrectException: If the current password is incorrect.
        UserNotFoundException: If the user is not found.
        DatabaseConnectionException: If there is a database connection error.
        UnexpectedDatabaseException: For any unexpected database errors.
    """
    try:
        use_case.execute(request.to_command(current_user.user_id))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                SuccessResponse(
                    message="password updated successfully",
                ),
                exclude_none=True,
            ),
        )
    except NewPasswordEqualsCurrentException as e:
        logger.warning("New password equal current", error=str(e))
        raise
    except CurrentPasswordIncorrectException as e:
        logger.warning("Current password is incorrect", error=str(e))
        raise
    except UserNotFoundException as e:
        logger.warning("User not found", error=str(e))
        raise
    except (DatabaseConnectionException, UnexpectedDatabaseException) as e:
        logger.error("Database error during update password", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error during update password", error=str(e))
        raise


@router.post(
    path="/password-recovery",
    summary="Password recovery",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
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
async def password_recovery(
    request: PasswordRecoveryRequest,
    request_details: dict = Depends(request_details_dependency),
    use_case: PasswordRecoveryUseCase = Depends(get_password_recovery_use_case),
    logger: Logger = Depends(get_logger),
) -> JSONResponse:
    """Password recovery send email.

    This endpoint allows users to request a password recovery email. It handles the request
    by delegating to the appropriate use case and returns a success response if the email
    is sent successfully. If the user is not found, it raises a UserNotFoundException.

    Args:
        request (PasswordRecoveryRequest): The request data containing the email for password recovery.
        request_details (dict): The request details including IP and user agent.
        use_case (PasswordRecoveryUseCase): The use case for password recovery.
        logger (Logger): The logger instance for logging events.

    Returns:
        JSONResponse: A JSON response indicating success or failure of the password recovery request.

    Raises:
        HTTPException: Raised for various error conditions during password recovery.
        CurrentPasswordIncorrectException: If the current password is incorrect.
        UserNotFoundException: If the user is not found.
        DatabaseConnectionException: If there is a database connection error.
        UnexpectedDatabaseException: For any unexpected database errors.
    """
    try:
        use_case.execute(
            request.to_command(
                request_ip=request_details["request_ip"],
                request_user_agent=request_details["request_user_agent"],
            )
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                SuccessResponse(
                    message="password recovery email sent successfully",
                ),
                exclude_none=True,
            ),
        )
    except UserNotFoundException as e:
        logger.warning("User not found", error=str(e))
        raise
    except (DatabaseConnectionException, UnexpectedDatabaseException) as e:
        logger.error("Database error during update password", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error during update password", error=str(e))
        raise


@router.post(
    path="/reset-password",
    summary="Reset password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorsResponse,
            "description": "Not Found - User not found.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorsResponse,
            "description": "Bad Request - Invalid request data.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorsResponse,
            "description": "Internal Server Error - Database or server error.",
        },
    },
)
async def reset_password(
    request: ResetPasswordRequest,
    use_case: ResetPasswordUseCase = Depends(get_reset_password_use_case),
    logger: Logger = Depends(get_logger),
) -> JSONResponse:
    """Reset password.

    This endpoint allows a user to reset their password using a recovery code sent to their email.

    Args:
        request (ResetPasswordRequest): The request data containing the recovery code, new password, and email.
        use_case (ResetPasswordUseCase): The use case for resetting the password.
        logger (Logger): The logger instance for logging events.

    Returns:
        JSONResponse: A JSON response indicating success or failure of the password reset request.

    Raises:
        HTTPException: Raised for various error conditions during password reset.
        NewPasswordEqualsCurrentException: If the new password is the same as the current password.
        UserNotFoundException: If the user is not found.
        DatabaseConnectionException: If there is a database connection error.
        UnexpectedDatabaseException: For any unexpected database errors.
    """
    try:
        use_case.execute(request.to_command())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                SuccessResponse(
                    message="password reset successfully",
                ),
                exclude_none=True,
            ),
        )
    except NewPasswordEqualsCurrentException as e:
        logger.warning("New password equal current", error=str(e))
        raise
    except UserNotFoundException as e:
        logger.warning("User not found", error=str(e))
        raise
    except (DatabaseConnectionException, UnexpectedDatabaseException) as e:
        logger.error("Database error during update password", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error during update password", error=str(e))
        raise
