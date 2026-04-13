"""This module contains the interface for the Doctor Schedules Query Repository Port."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.clinical.domain.value_objects.doctor_availability_vo import (
    DoctorAvailabilityVO,
)


class DoctorSchedulesQueryRepositoryPort(ABC):
    """Abstract interface for Doctor Schedules Query Repository operations."""

    @abstractmethod
    async def find_by_doctor_id(self, doctor_id: UUID) -> DoctorAvailabilityVO:
        """Find the doctor's availability by their unique identifier.

        Args:
            doctor_id (UUID): The unique identifier of the doctor.

        Returns:
            DoctorAvailabilityVO: The availability information of the doctor.
        """
        pass
