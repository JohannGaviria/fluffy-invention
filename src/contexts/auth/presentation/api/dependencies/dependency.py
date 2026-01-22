"""This module contains dependency injection functions for the authentication context."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlmodel import Session

from src.config import settings
from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.application.use_cases.login_use_case import LoginUseCase
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.contexts.auth.infrastructure.external.activation_code_service_adapter import (
    ActivationCodeServiceAdapter,
)
from src.contexts.auth.infrastructure.external.authorization_policy_service_adapter import (
    AuthorizationPolicyServiceAdapter,
)
from src.contexts.auth.infrastructure.external.password_hash_service_adapter import (
    PasswordHashServiceAdapter,
)
from src.contexts.auth.infrastructure.external.password_service_adapter import (
    PasswordServiceAdapter,
)
from src.contexts.auth.infrastructure.external.staff_email_policy_service_adapter import (
    StaffEmailPolicyServiceAdapter,
)
from src.contexts.auth.infrastructure.external.token_service_adapter import (
    PyJWTTokenServiceAdapter,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_user_repository_adapter import (
    SQLModelRepositoryAdapter,
)
from src.shared.infrastructure.cache.redis_cache_service_adapter import (
    RedisCacheServiceAdapter,
)
from src.shared.infrastructure.cache.redis_client import RedisClient, get_redis_client
from src.shared.infrastructure.db.database import get_session
from src.shared.infrastructure.logging.logger import Logger
from src.shared.infrastructure.notifications.sender_notification_service_adapter import (
    SenderNotificationServiceAdapter,
)
from src.shared.infrastructure.notifications.template_renderer_service_adapter import (
    TemplateRendererServiceAdapter,
)


def get_logger() -> Logger:
    """Get the logger instance.

    Returns:
        Logger: An instance of Logger.
    """
    return Logger(settings.LOG_LEVEL)


def get_user_repository(
    session: Session = Depends(get_session), logger: Logger = Depends(get_logger)
) -> SQLModelRepositoryAdapter:
    """Get the SQLModel user repository adapter.

    Args:
        session (Session): The database session.
        logger (Logger): The logger instance.

    Returns:
        SQLModelRepositoryAdapter: An instance of SQLModelRepositoryAdapter.
    """
    return SQLModelRepositoryAdapter(session, logger)


def get_activation_code_service() -> ActivationCodeServiceAdapter:
    """Get the activation code service adapter.

    Returns:
        ActivationCodeServiceAdapter: An instance of ActivationCodeServiceAdapter.
    """
    return ActivationCodeServiceAdapter()


def get_authorization_policy_service() -> AuthorizationPolicyServiceAdapter:
    """Get the authorization policy service adapter.

    Returns:
        AuthorizationPolicyServiceAdapter: An instance of AuthorizationPolicyServiceAdapter.
    """
    return AuthorizationPolicyServiceAdapter()


def get_password_service() -> PasswordServiceAdapter:
    """Get the password service adapter.

    Returns:
        PasswordServiceAdapter: An instance of PasswordServiceAdapter.
    """
    return PasswordServiceAdapter()


def get_password_hash_service() -> PasswordHashServiceAdapter:
    """Get the password hash service adapter.

    Returns:
        PasswordHashServiceAdapter: An instance of PasswordHashServiceAdapter.
    """
    return PasswordHashServiceAdapter()


def get_staff_email_policy_service() -> StaffEmailPolicyServiceAdapter:
    """Get the staff email policy service adapter.

    Returns:
        StaffEmailPolicyServiceAdapter: An instance of StaffEmailPolicyServiceAdapter.
    """
    return StaffEmailPolicyServiceAdapter(
        settings.ALLOWED_STAFF_EMAIL_DOMAINS, settings.ALLOWED_STAFF_ROLES
    )


def get_cache_service(
    redis_client: RedisClient = Depends(get_redis_client),
    logger: Logger = Depends(get_logger),
) -> RedisCacheServiceAdapter:
    """Get the Redis cache service adapter.

    Args:
        redis_client (RedisClient): The Redis client instance.
        logger (Logger): The logger instance.

    Returns:
        RedisCacheServiceAdapter: An instance of RedisCacheServiceAdapter.
    """
    return RedisCacheServiceAdapter(redis_client, logger)


def get_template_renderer_service() -> TemplateRendererServiceAdapter:
    """Get the template renderer service adapter.

    Returns:
        TemplateRendererServiceAdapter: An instance of TemplateRendererServiceAdapter.
    """
    return TemplateRendererServiceAdapter(settings.TEMPLATE_PATH)


def get_sender_notification_service(
    logger: Logger = Depends(get_logger),
) -> SenderNotificationServiceAdapter:
    """Get the sender notification service adapter.

    Args:
        logger (Logger): The logger instance.

    Returns:
        SenderNotificationServiceAdapter: An instance of SenderNotificationServiceAdapter.
    """
    return SenderNotificationServiceAdapter(
        settings.SMTP_SERVER,
        settings.SMTP_PORT,
        settings.USER_EMAIL,
        settings.USER_PASSWORD,
        logger,
    )


def get_register_user_use_case(
    user_repository: SQLModelRepositoryAdapter = Depends(get_user_repository),
    password_service: PasswordServiceAdapter = Depends(get_password_service),
    password_hash_service: PasswordHashServiceAdapter = Depends(
        get_password_hash_service
    ),
    activation_code_service: ActivationCodeServiceAdapter = Depends(
        get_activation_code_service
    ),
    cache_service: RedisCacheServiceAdapter = Depends(get_cache_service),
    staff_email_policy_service: StaffEmailPolicyServiceAdapter = Depends(
        get_staff_email_policy_service
    ),
    authorization_policy_service: AuthorizationPolicyServiceAdapter = Depends(
        get_authorization_policy_service
    ),
    template_renderer_service: TemplateRendererServiceAdapter = Depends(
        get_template_renderer_service
    ),
    sender_notification_service: SenderNotificationServiceAdapter = Depends(
        get_sender_notification_service
    ),
) -> RegisterUserUseCase:
    """Dependency injector for RegisterUserUseCase.

    Args:
        user_repository (SQLModelRepositoryAdapter): The user repository.
        password_service (PasswordServiceAdapter): The password service.
        password_hash_service (PasswordHashServiceAdapter): The password hash service.
        activation_code_service (ActivationCodeServiceAdapter): The activation code service.
        cache_service (RedisCacheServiceAdapter): The cache service.
        staff_email_policy_service (StaffEmailPolicyServiceAdapter): The staff email policy service.
        authorization_policy_service (AuthorizationPolicyServiceAdapter): The authorization policy service.
        template_renderer_service (TemplateRendererServiceAdapter): The template renderer service.
        sender_notification_service (SenderNotificationServiceAdapter): The sender notification service.

    Returns:
        RegisterUserUseCase: An instance of RegisterUserUseCase.
    """
    return RegisterUserUseCase(
        user_repository,
        password_service,
        password_hash_service,
        activation_code_service,
        cache_service,
        staff_email_policy_service,
        authorization_policy_service,
        template_renderer_service,
        sender_notification_service,
    )


def get_activate_account_use_case(
    user_repository: SQLModelRepositoryAdapter = Depends(get_user_repository),
    cache_service: RedisCacheServiceAdapter = Depends(get_cache_service),
) -> ActivateAccountUseCase:
    """Dependency injector for ActivateAccountUseCase.

    Args:
        user_repository (SQLModelRepositoryAdapter): The user repository.
        cache_service (RedisCacheServiceAdapter): The cache service.

    Returns:
        ActivateAccountUseCase: An instance of ActivateAccountUseCase.
    """
    return ActivateAccountUseCase(user_repository, cache_service)


def get_token_service() -> PyJWTTokenServiceAdapter:
    """Get the token service adapter.

    Returns:
        TokenServicePort: An instance of TokenServicePort.
    """
    return PyJWTTokenServiceAdapter(
        settings.ACCESS_TOKEN_EXPIRES_IN,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


def get_login_use_case(
    user_repository: SQLModelRepositoryAdapter = Depends(get_user_repository),
    password_hash_service: PasswordHashServiceAdapter = Depends(
        get_password_hash_service
    ),
    token_service: PyJWTTokenServiceAdapter = Depends(get_token_service),
    cache_service: RedisCacheServiceAdapter = Depends(get_cache_service),
) -> LoginUseCase:
    """Dependency injector for LoginUseCase.

    Args:
        user_repository (SQLModelRepositoryAdapter): The user repository.
        password_hash_service (PasswordHashServiceAdapter): The password hash service.
        token_service (TokenServicePort): The token service.
        cache_service (RedisCacheServiceAdapter): The cache service.

    Returns:
        LoginUseCase: An instance of LoginUseCase.
    """
    return LoginUseCase(
        user_repository,
        password_hash_service,
        token_service,
        cache_service,
        settings.ACCESS_TOKEN_EXPIRES_IN,
        settings.LOGIN_ATTEMPTS_LIMIT,
        settings.LOGIN_WAITING_TIME,
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    logger: Logger = Depends(get_logger),
    token_service: PyJWTTokenServiceAdapter = Depends(get_token_service),
) -> TokenPayloadVO:
    """Dependency injector to get the current user from the JWT token.

    Args:
        token (str): The JWT token from the request.
        logger (Logger): The logger instance.
        token_service (TokenServicePort): The token service.

    Returns:
        TokenPayloadVO: The token payload value object.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = token_service.decode(token)
        return TokenPayloadVO(
            user_id=payload.user_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            role=payload.role,
            expires_in=payload.expires_in,
            jti=payload.jti,
        )
    except PyJWTError as e:
        logger.warning("Invalid or expired token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from e
