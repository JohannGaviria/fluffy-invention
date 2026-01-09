"""This module contains custom exceptions for authentication domain errors."""

from src.shared.domain.exception import BaseDomainException


class InvalidEmailException(BaseDomainException):
    """Exception raised for invalid email addresses."""

    def __init__(self, email: str, errors: list[str]) -> None:
        """Initialize the InvalidEmailException.

        Args:
            email (str): The invalid email address.
            errors (list[str]): Variable length error messages describing the validation issues.
        """
        self.email = email
        self.errors = errors
        super().__init__("Invalid email address provided")


class InvalidPasswordHashException(BaseDomainException):
    """Exception raised for invalid password hashes."""

    def __init__(self, *errors: str) -> None:
        """Initialize the InvalidPasswordHashException.

        Args:
            *errors (str): Variable length error messages describing the validation issues.
        """
        self.errors = errors
        super().__init__("Invalid password hash provided")
