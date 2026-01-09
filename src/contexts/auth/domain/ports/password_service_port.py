"""This module contains the interface for the Password Service Port."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class PasswordServicePort(ABC):
    """Abstract interface for Password Service operations."""

    @abstractmethod
    def verify(self, password: PasswordVO) -> bool:
        """Verify the given password.

        Args:
            password (PasswordVO): The password value object to verify.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        pass
