"""This module contains the composition functions for the admin context infrastructure dependencies."""

from fastapi import Depends
from sqlmodel import Session

from src.contexts.admin.infrastructure.persistence.repositories.beanie_doctor_schedules_repository_adapter import (
    BeanieDoctorSchedulesRepositoryAdapter,
)
from src.contexts.admin.infrastructure.persistence.repositories.sqlmodel_doctor_query_repository_adapter import (
    SQLModelDoctorQueryRepositoryAdapter,
)
from src.shared.domain.value_objects.dummy_cache_vo import DummyCacheVO
from src.shared.infrastructure.cache.redis_cache_service_adapter import (
    RedisCacheServiceAdapter,
)
from src.shared.infrastructure.cache.redis_client import RedisClient, get_redis_client
from src.shared.infrastructure.db.database import get_session
from src.shared.infrastructure.logging.logger import Logger
from src.shared.presentation.api.compositions.infrastructure_composition import (
    get_logger,
)


def get_doctor_query_repository(
    session: Session = Depends(get_session), logger: Logger = Depends(get_logger)
) -> SQLModelDoctorQueryRepositoryAdapter:
    """Get an instance of SQLModelDoctorQueryRepositoryAdapter with dependencies injected.

    Args:
        session (Session): The database session for querying doctors.
        logger (Logger): The logger for logging errors in the repository.

    Returns:
        SQLModelDoctorQueryRepositoryAdapter: An instance of the repository adapter
            with dependencies injected.
    """
    return SQLModelDoctorQueryRepositoryAdapter(session, logger)


def get_doctor_schedules_repository(
    logger: Logger = Depends(get_logger),
) -> BeanieDoctorSchedulesRepositoryAdapter:
    """Get an instance of BeanieDoctorSchedulesRepositoryAdapter with dependencies injected.

    Args:
        logger (Logger): The logger for logging errors in the repository.

    Returns:
        BeanieDoctorSchedulesRepositoryAdapter: An instance of the repository adapter
            with dependencies injected.
    """
    return BeanieDoctorSchedulesRepositoryAdapter(logger)


def get_appointment_availability_cache_service(
    redis_client: RedisClient = Depends(get_redis_client),
    logger: Logger = Depends(get_logger),
) -> RedisCacheServiceAdapter[DummyCacheVO]:
    """Get an instance of RedisCacheServiceAdapter for appointment availability caching.

    Args:
        redis_client (RedisClient): The Redis client for interacting with the Redis cache.
        logger (Logger): The logger for logging errors in the cache service.

    Returns:
        RedisCacheServiceAdapter[DummyCacheVO]: An instance of the cache service adapter
            with dependencies injected.
    """
    return RedisCacheServiceAdapter(redis_client, logger, value_class=DummyCacheVO)
