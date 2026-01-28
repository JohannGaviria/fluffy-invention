"""This module contains the abstract base class for activation code services."""

from abc import ABC, abstractmethod


class ActivationCodeServicePort(ABC):
    """Abstract base class for activation code services."""

    @abstractmethod
    def generate(self) -> str:
        """Generate a new activation code.

        Returns:
            str: The generated activation code.
        """
        pass
