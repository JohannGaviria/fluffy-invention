"""This module contains the Password Hash Value Object used in the authentication context."""

import re
from dataclasses import dataclass

from src.contexts.auth.domain.exceptions.exception import InvalidPasswordHashException
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class PasswordHashVO(BaseValueObject):
    """Base Value Object representing a password hash.

    Attributes:
        password_hash (str): The hashed password string.

    Raises:
        InvalidPasswordHashException: If the password hash is invalid.
    """

    password_hash: str

    def validate(self) -> None:
        """Validate the password hash.

        Raises:
            InvalidPasswordHashException: If the password hash is invalid.
        """
        errors = []
        BCRYPT_PATTERN = r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$"

        if not self.password_hash:
            errors.append("Password hash cannot be empty.")
        if not re.match(BCRYPT_PATTERN, self.password_hash):
            errors.append("Invalid bcrypt hash format.")

        if errors:
            raise InvalidPasswordHashException(*errors)

    @property
    def value(self) -> str:
        """Return the password hash.

        Returns:
            str: The password hash.
        """
        return self.password_hash

    def __str__(self) -> str:
        """Return the string representation of the password hash.

        Returns:
            str: The password hash as a string.
        """
        return self.password_hash

    def __repr__(self) -> str:
        """Return the official string representation of the PasswordHashVO.

        Returns:
            str: The official string representation.
        """
        return f"PasswordHashVO({self.password_hash})"
