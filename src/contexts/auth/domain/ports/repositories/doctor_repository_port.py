"""This module contains the interface for the Doctor Repository Port."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.auth.domain.entities.entity import DoctorEntity


class DoctorRepositoryPort(ABC):
    """Abstract interface for Doctor Repository operations."""

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> DoctorEntity | None:
        """Finds a DoctorEntity by user ID.

        Args:
            user_id (UUID): The user ID to search for.

        Returns:
            DoctorEntity | None: The found doctor entity or None if not found.
        """

    @abstractmethod
    def find_by_license_number(self, license_number: str) -> DoctorEntity | None:
        """Finds a DoctorEntity by license number.

        Args:
            license_number (str): The license number to search for.

        Returns:
            DoctorEntity | None: The found doctor entity or None if not found.
        """
        pass

    @abstractmethod
    def save(self, entity: DoctorEntity) -> None:
        """Saves a DoctorEntity to the repository.

        Args:
            entity (DoctorEntity): The doctor entity to save.

        Returns:
            None
        """
        pass
