"""This module contains the PasswordServiceAdapter class implementation."""

import random
import secrets
import string

from src.contexts.auth.domain.ports.services.password_service_port import (
    PasswordServicePort,
)
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class PasswordServiceAdapter(PasswordServicePort):
    """Adapter for password service."""

    def generate(self) -> PasswordVO:
        """Generate a random password.

        Returns:
            PasswordVO: The generated password value object.
        """
        length = random.randint(8, 12)

        required_chars = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(string.punctuation),
        ]

        # Ensure the password meets the required length
        remaining_length = length - len(required_chars)

        all_characters = (
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits
            + string.punctuation
        )

        # Fill the rest of the password length with random choices
        remaining_chars = [
            secrets.choice(all_characters) for _ in range(remaining_length)
        ]

        # Combine and shuffle the characters to form the final password
        password_chars = required_chars + remaining_chars
        random.shuffle(password_chars)

        return PasswordVO("".join(password_chars))
