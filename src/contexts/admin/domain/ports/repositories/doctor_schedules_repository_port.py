"""This module contains the interface for the Doctor Schedules Repository Port."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.admin.domain.entities.doctor_schedules_entity import (
    DoctorSchedulesEntity,
)


class DoctorSchedulesRepositoryPort(ABC):
    """Abstract interface for Doctor Schedules Repository operations."""

    @abstractmethod
    async def doctor_schedule_exists(self, doctor_id: UUID) -> bool:
        """Check if a doctor schedule exists for the given doctor ID.

        Args:
            doctor_id (UUID): The ID of the doctor to check for existing schedules.

        Returns:
            bool: True if a schedule exists for the doctor, False otherwise.
        """
        pass

    @abstractmethod
    async def save(self, entity: DoctorSchedulesEntity) -> None:
        """Saves a DoctorSchedulesEntity to the repository.

        Args:
            entity (DoctorSchedulesEntity): the doctor schedules entity to save.

        Returns:
            None
        """
        pass
