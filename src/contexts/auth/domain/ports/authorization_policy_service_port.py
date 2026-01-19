"""This module contains the abstract base class for authorization policy services."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.entities.entity import RolesEnum


class AuthorizationPolicyServicePort(ABC):
    """Abstract base class for authorization policy services."""

    @abstractmethod
    def can_register(self, role: RolesEnum) -> bool:
        """Register permission check for the given role.

        Args:
            role (RolesEnum): The role to be checked.

        Returns:
            bool: True if registration is permitted for the role, False otherwise.
        """
        pass
