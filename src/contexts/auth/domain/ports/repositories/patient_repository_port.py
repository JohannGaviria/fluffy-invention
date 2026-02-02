"""This module contains the interface for the Patient Repository Port."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.auth.domain.entities.entity import PatientEntity


class PatientRepositoryPort(ABC):
    """Abstract interface for Patient Repository operations."""

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> PatientEntity | None:
        """Finds a PatientEntity by user ID.

        Args:
            user_id (UUID): The user ID to search for.

        Returns:
            PatientEntity | None: The found patient entity or None if not found.
        """
        pass

    @abstractmethod
    def find_by_document(self, document: str) -> PatientEntity | None:
        """Finds a PatientEntity by document identifier.

        Args:
            document (str): The document identifier to search for.

        Returns:
            PatientEntity | None: The found patient entity or None if not found.
        """
        pass

    @abstractmethod
    def find_by_phone(self, phone: str) -> PatientEntity | None:
        """Finds a PatientEntity by phone number.

        Args:
            phone (str): The phone number to search for.

        Returns:
            PatientEntity | None: The found patient entity or None if not found.
        """
        pass

    @abstractmethod
    def save(self, entity: PatientEntity) -> None:
        """Saves a PatientEntity to the repository.

        Args:
            entity (PatientEntity): The patient entity to save.

        Returns:
            None
        """
        pass
