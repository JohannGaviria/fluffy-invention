"""This module contains the ActivationCodeServiceAdapter class implementation."""

import random
import string

from src.contexts.auth.domain.ports.activation_code_service_port import (
    ActivationCodeServicePort,
)


class ActivationCodeServiceAdapter(ActivationCodeServicePort):
    """Adapter for activation code service."""

    def generate(self, length: int = 6) -> str:
        """Generate a random activation code.

        Args:
            length (int): Length of the activation code. Defaults to 6.

        Returns:
            str: The generated activation code.
        """
        characters = string.ascii_uppercase + string.digits
        return "".join(random.choice(characters) for _ in range(length))
