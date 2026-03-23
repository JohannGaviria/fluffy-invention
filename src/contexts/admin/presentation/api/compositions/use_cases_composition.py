"""This module contains the composition functions for the admin context use cases."""

from fastapi import Depends

from src.contexts.admin.application.use_cases.assign_doctor_schedules_use_case import (
    AssignDoctorSchedulesUseCase,
)
from src.contexts.admin.infrastructure.persistence.repositories.beanie_doctor_schedules_repository_adapter import (
    BeanieDoctorSchedulesRepositoryAdapter,
)
from src.contexts.admin.presentation.api.compositions.infrastructure_composition import (
    get_appointment_availability_cache_service,
    get_doctor_schedules_repository,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_doctor_repository_adapter import (
    SQLModelDoctorRepositoryAdapter,
)
from src.contexts.auth.presentation.api.compositions.infrastructure_composition import (
    get_doctor_repository,
)
from src.shared.infrastructure.cache.redis_cache_service_adapter import (
    RedisCacheServiceAdapter,
)


def get_assign_doctor_schedules_use_case(
    doctor_repository: SQLModelDoctorRepositoryAdapter = Depends(get_doctor_repository),
    doctor_schedules_repository: BeanieDoctorSchedulesRepositoryAdapter = Depends(
        get_doctor_schedules_repository
    ),
    cache_service: RedisCacheServiceAdapter = Depends(
        get_appointment_availability_cache_service
    ),
) -> AssignDoctorSchedulesUseCase:
    """Get an instance of AssignDoctorSchedulesUseCase with all dependencies injected.

    Args:
        doctor_repository (SQLModelDoctorRepositoryAdapter): The repository for doctor data.
        doctor_schedules_repository (BeanieDoctorSchedulesRepositoryAdapter):
            The repository for doctor schedules data
        cache_service (RedisCacheServiceAdapter): The cache service for managing appointment
            availability cache.

    Returns:
        AssignDoctorSchedulesUseCase: An instance of the use case with dependencies injected.
    """
    return AssignDoctorSchedulesUseCase(
        doctor_repository,
        doctor_schedules_repository,
        cache_service,
    )
