"""This module contains the interface for the Password Service Port."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class PasswordServicePort(ABC):
    """Abstract interface for Password Service operations."""

    @abstractmethod
    def generate(self) -> PasswordVO:
        """Generate a temporary password.

        Returns:
            PasswordVO: The password value object to verify.
        """
        pass
