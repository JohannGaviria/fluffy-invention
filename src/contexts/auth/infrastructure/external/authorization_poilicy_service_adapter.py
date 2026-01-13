"""This module contains the AuthorizationPolicyServiceAdapter class implementation."""

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.ports.authorization_policy_service_port import (
    AuthorizationPolicyServicePort,
)


class AuthorizationPolicyServiceAdapter(AuthorizationPolicyServicePort):
    """Adapter for authorization policy service."""

    def can_register(self, role: RolesEnum) -> bool:
        """Check if the given role can register.

        Args:
            role (RolesEnum): The role to check.

        Returns:
            bool: True if the role can register, False otherwise.
        """
        return role == RolesEnum.ADMIN
