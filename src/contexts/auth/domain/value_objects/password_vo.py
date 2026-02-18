"""This module contains the Password Value Object used in the authentication context."""

from dataclasses import dataclass

from src.contexts.auth.domain.exceptions.exception import InvalidPasswordException
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class PasswordVO(BaseValueObject):
    """Value Object representing a password.

    Attributes:
        password (str): The password string.

    Raises:
        InvalidPasswordException: If the password does not meet the security criteria.
    """

    password: str

    def validate(self) -> None:
        """Validate the password according to defined security rules.

        Raises:
            InvalidPasswordException: If the password does not meet the security criteria.
        """
        errors = []
        SPECIAL_CHARS = "!@#$%^&*()-_=+[]{}|;:,.<>?/\\"
        if len(self.password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not any(c.isupper() for c in self.password):
            errors.append("Password must contain at least one uppercase character.")
        if not any(c.islower() for c in self.password):
            errors.append("Password must contain at least one lowercase character.")
        if not any(c.isdigit() for c in self.password):
            errors.append("Password must contain at least one numeric character.")
        if not any(c in SPECIAL_CHARS for c in self.password):
            errors.append("Password must contain at least one special character.")

        if errors:
            raise InvalidPasswordException(errors)

    @property
    def value(self) -> str:
        """Return the password as a string.

        Returns:
            str: The password as a string.
        """
        return self.password

    def __str__(self) -> str:
        """Return the string representation of the password.

        Returns:
            str: The password as a string.
        """
        return self.password

    def __repr__(self) -> str:
        """Return the official string representation of the PasswordVO.

        Returns:
            str: The official string representation.
        """
        return f"PasswordVO({self.password})"
