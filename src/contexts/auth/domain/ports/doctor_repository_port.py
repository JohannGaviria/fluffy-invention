"""This module contains the interface for the Doctor Repository Port."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.entities.entity import DoctorEntity


class DoctorRepositoryPort(ABC):
    """Abstract interface for Doctor Repository operations."""

    @abstractmethod
    def save(self, entity: DoctorEntity) -> None:
        """Saves a DoctorEntity to the repository.

        Args:
            entity (DoctorEntity): The doctor entity to save.

        Returns:
            None
        """
        pass
