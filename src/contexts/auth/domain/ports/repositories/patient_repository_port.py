"""This module contains the interface for the Patient Repository Port."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.entities.entity import PatientEntity


class PatientRepositoryPort(ABC):
    """Abstract interface for Patient Repository operations."""

    @abstractmethod
    def save(self, entity: PatientEntity) -> None:
        """Saves a PatientEntity to the repository.

        Args:
            entity (PatientEntity): The patient entity to save.

        Returns:
            None
        """
        pass
