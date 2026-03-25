"""This module contains the DoctorQueryRepositoryPort interface, which defines the contract for querying doctors."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.admin.domain.value_objects.doctor_summary_vo import DoctorSummaryVO


class DoctorQueryRepositoryPort(ABC):
    """Abstract base class for doctor query repository ports."""

    @abstractmethod
    def find_active_doctor(self, doctor_id: UUID) -> "DoctorSummaryVO | None":
        """Finds an active doctor by its ID.

        Args:
            doctor_id (UUID): The ID of the doctor to find.

        Returns:
            DoctorSummaryVO | None: The doctor summary if found, otherwise None.
        """
        pass
