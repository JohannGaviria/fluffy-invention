"""This module contains dependency injection functions for the authentication context."""

from fastapi import Depends
from sqlmodel import Session

from src.config import settings
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
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
