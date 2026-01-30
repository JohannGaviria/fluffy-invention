"""This module contains the infrastructure composition for FastAPI dependencies."""

from fastapi import Depends
from sqlmodel import Session

from src.config import settings
from src.contexts.auth.domain.value_objects.activation_code_cache_value_vo import (
    ActivationCodeCacheValueVO,
)
from src.contexts.auth.domain.value_objects.login_attempts_cache_value_vo import (
    LoginAttemptsCacheValueVO,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_doctor_repository_adapter import (
    SQLModelDoctorRepositoryAdapter,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_patient_repository_adapter import (
    SQLModelPatientRepositoryAdapter,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_user_repository_adapter import (
    SQLModelRepositoryAdapter,
)
from src.contexts.auth.infrastructure.policies.authorization_policy_service_adapter import (
    AuthorizationPolicyServiceAdapter,
)
from src.contexts.auth.infrastructure.policies.staff_email_policy_service_adapter import (
    StaffEmailPolicyServiceAdapter,
)
from src.contexts.auth.infrastructure.security.activation_code_service_adapter import (
    ActivationCodeServiceAdapter,
)
from src.contexts.auth.infrastructure.security.password_hash_service_adapter import (
    PasswordHashServiceAdapter,
)
from src.contexts.auth.infrastructure.security.password_service_adapter import (
    PasswordServiceAdapter,
)
from src.shared.infrastructure.cache.redis_cache_service_adapter import (
    RedisCacheServiceAdapter,
)
from src.shared.infrastructure.cache.redis_client import RedisClient, get_redis_client
from src.shared.infrastructure.db.database import get_session
from src.shared.infrastructure.logging.logger import Logger
from src.shared.presentation.api.compositions.infrastructure_composition import (
    get_logger,
)


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


def get_patient_repository(
    session: Session = Depends(get_session), logger: Logger = Depends(get_logger)
) -> SQLModelPatientRepositoryAdapter:
    """Get the SQLModel patient repository adapter.

    Args:
        session (Session): The database session.
        logger (Logger): The logger instance.

    Returns:
        SQLModelPatientRepositoryAdapter: An instance of SQLModelPatientRepositoryAdapter.
    """
    return SQLModelPatientRepositoryAdapter(session, logger)


def get_doctor_repository(
    session: Session = Depends(get_session), logger: Logger = Depends(get_logger)
) -> SQLModelDoctorRepositoryAdapter:
    """Get the SQLModel doctor repository adapter.

    Args:
        session (Session): The database session.
        logger (Logger): The logger instance.

    Returns:
        SQLModelDoctorRepositoryAdapter: An instance of SQLModelDoctorRepositoryAdapter.
    """
    return SQLModelDoctorRepositoryAdapter(session, logger)


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


def get_staff_email_policy_service() -> StaffEmailPolicyServiceAdapter:
    """Get the staff email policy service adapter.

    Returns:
        StaffEmailPolicyServiceAdapter: An instance of StaffEmailPolicyServiceAdapter.
    """
    return StaffEmailPolicyServiceAdapter(
        settings.ALLOWED_STAFF_EMAIL_DOMAINS, settings.ALLOWED_STAFF_ROLES
    )


def get_activation_code_cache_service(
    redis_client: RedisClient = Depends(get_redis_client),
    logger: Logger = Depends(get_logger),
) -> RedisCacheServiceAdapter[ActivationCodeCacheValueVO]:
    """Get the Redis cache service adapter for activation codes.

    Args:
        redis_client (RedisClient): The Redis client instance.
        logger (Logger): The logger instance.

    Returns:
        RedisCacheServiceAdapter[ActivationCodeCacheValueVO]: Cache service for activation codes.
    """
    return RedisCacheServiceAdapter(redis_client, logger, ActivationCodeCacheValueVO)


def get_login_attempts_cache_service(
    redis_client: RedisClient = Depends(get_redis_client),
    logger: Logger = Depends(get_logger),
) -> RedisCacheServiceAdapter[LoginAttemptsCacheValueVO]:
    """Get the Redis cache service adapter for login attempts.

    Args:
        redis_client (RedisClient): The Redis client instance.
        logger (Logger): The logger instance.

    Returns:
        RedisCacheServiceAdapter[LoginAttemptsCacheValueVO]: Cache service for login attempts.
    """
    return RedisCacheServiceAdapter(redis_client, logger, LoginAttemptsCacheValueVO)
