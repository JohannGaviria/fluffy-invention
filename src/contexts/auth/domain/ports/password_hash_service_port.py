"""This module contains the interface for the Password Hash Service Port."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class PasswordHashServicePort(ABC):
    """Abstract interface for Password Hash Service operations."""

    @abstractmethod
    def hashed(self, plain: PasswordVO) -> PasswordHashVO:
        """Hash the given plain password.

        Args:
            plain (PasswordVO): The plain password value object to hash.

        Returns:
            PasswordHashVO: The hashed password value object.
        """
        pass
