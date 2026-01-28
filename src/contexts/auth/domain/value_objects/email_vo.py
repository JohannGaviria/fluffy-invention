"""This module contains the Email Value Object used in the authentication context."""

import re
from dataclasses import dataclass

from src.contexts.auth.domain.exceptions.exception import InvalidEmailException
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class EmailVO(BaseValueObject):
    """Base Value Object representing an email address.

    Attributes:
        email (str): The email address string.

    Raises:
        InvalidEmailException: If the email format is invalid.
    """

    email: str

    def validate(self) -> None:
        """Validate the email address format.

        Raises:
            InvalidEmailException: If the email format is invalid.
        """
        errors = []
        EMAIL_PATTERN = (
            r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,6}$"
        )
        if any(w in self.email for w in (" ", "\t", "\n")):
            errors.append("Email must not contain whitespace.")
        if ".." in self.email:
            errors.append("Email must not contain consecutive dots.")
        if not re.match(EMAIL_PATTERN, self.email):
            errors.append("Invalid email format.")
        if len(self.email) > 255:
            errors.append("Email too long.")

        if errors:
            raise InvalidEmailException(self.email, errors)

    @property
    def value(self) -> str:
        """Return the email address.

        Returns:
            str: The email address.
        """
        return self.email

    @property
    def domain(self) -> str:
        """Return the domain part of the email address.

        Returns:
            str: The domain of the email address.
        """
        return self.email.split("@")[1].lower()

    def __str__(self) -> str:
        """Return the string representation of the email.

        Returns:
            str: The email address as a string.
        """
        return self.email

    def __repr__(self) -> str:
        """Return the official string representation of the EmailVo.

        Returns:
            str: The official string representation.
        """
        return f"EmailVO({self.email})"
