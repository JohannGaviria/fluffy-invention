"""This module contains the StaffEmailPolicyServiceAdapter class implementation."""

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.ports.staff_email_policy_service_port import (
    StaffEmailPolicyServicePort,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO


class StaffEmailPolicyServiceAdapter(StaffEmailPolicyServicePort):
    """Adapter for staff email policy service."""

    def __init__(
        self,
        allowed_domains: str,
        allowed_roles: RolesEnum,
    ) -> None:
        """Initialize the adapter with allowed domains and roles.

        Args:
            allowed_domains (str): The domains allowed for staff emails.
            allowed_roles (RolesEnum): The roles allowed to use staff emails.
        """
        self.allowed_domains = allowed_domains
        self.allowed_roles = allowed_roles

    def is_allowed(self, email: EmailVO, role: RolesEnum) -> bool:
        """Check if the email is allowed for the given role.

        Args:
            email (EmailVO): The email value object.
            role (RolesEnum): The role to check against.

        Returns:
            bool: True if the email is allowed for the role, False otherwise.
        """
        allowed_domains = [
            domains.strip() for domains in self.allowed_domains.split(",")
        ]
        allowed_roles = [roles.strip() for roles in self.allowed_roles.split(",")]

        if role not in allowed_roles:
            return True

        return email.domain in allowed_domains
