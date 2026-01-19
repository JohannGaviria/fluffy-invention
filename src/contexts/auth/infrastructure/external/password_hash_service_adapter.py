"""This module contains the Password Hash Service Adapter implementation."""

from passlib.context import CryptContext

from src.contexts.auth.domain.ports.password_hash_service_port import (
    PasswordHashServicePort,
)
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class PasswordHashServiceAdapter(PasswordHashServicePort):
    """Password Hash Service Adapter implementation using passlib."""

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hashed(self, password: PasswordVO) -> PasswordHashVO:
        """Hash the given plain password.

        Args:
            password (PasswordVO): The password to be hashed.

        Returns:
            PasswordHashVO: The hashed password.
        """
        return PasswordHashVO(self.context.hash(password.value))
