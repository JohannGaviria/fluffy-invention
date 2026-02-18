"""This module contains the abstract base class for staff email policy services."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.value_objects.email_vo import EmailVO


class StaffEmailPolicyServicePort(ABC):
    """Abstract base class for staff email policy services."""

    @abstractmethod
    def is_allowed(self, email: EmailVO, role: RolesEnum) -> bool:
        """Determine if the given email is allowed for the specified role.

        Args:
            email (EmailVO): The email to be checked.
            role (RolesEnum): The role to be associated with the email.

        Returns:
            bool: True if the email is allowed for the role, False otherwise.
        """
        pass
