"""This module contains the PasswordServiceAdapter class implementation."""

import random
import secrets
import string

from src.contexts.auth.domain.ports.password_service_port import PasswordServicePort
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class PasswordServiceAdapter(PasswordServicePort):
    """Adapter for password service."""

    def generate(self) -> PasswordVO:
        """Generate a random password.

        Returns:
            PasswordVO: The generated password value object.
        """
        characters = (
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits
            + string.punctuation
        )
        return PasswordVO(
            "".join(secrets.choice(characters) for _ in range(random.randint(8, 12)))
        )
