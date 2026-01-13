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
        allowed_domains: list[str],
        allowed_roles: list[RolesEnum],
    ) -> None:
        """Initialize the adapter with allowed domains and roles.

        Args:
            allowed_domains (list[str]): List of allowed email domains.
            allowed_roles (list[RolesEnum]): List of roles subject to email domain restrictions.
        """
        self.allowed_domains = {d.lower() for d in allowed_domains}
        self.allowed_roles = set(allowed_roles)

    def is_allowed(self, email: EmailVO, role: RolesEnum) -> bool:
        """Check if the email is allowed for the given role.

        Args:
            email (EmailVO): The email value object.
            role (RolesEnum): The role to check against.

        Returns:
            bool: True if the email is allowed for the role, False otherwise.
        """
        if role not in self.allowed_roles:
            return True

        return email.domain in self.allowed_domains
