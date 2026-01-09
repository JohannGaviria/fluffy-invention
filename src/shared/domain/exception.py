"""This module contains custom exceptions for the domain layer."""


class BaseDomainException(Exception):
    """Base class for domain-specific exceptions."""

    pass


class MissingFieldException(BaseDomainException):
    """Exception raised for missing required fields."""

    def __init__(self, field: str, error: str) -> None:
        """Initialize the MissingFieldException.

        Args:
            field (str): The name of the missing field.
            error (str): The error message associated with the missing field.
        """
        self.field = field
        self.error = error
        super().__init__(f"{field}: {error}")
