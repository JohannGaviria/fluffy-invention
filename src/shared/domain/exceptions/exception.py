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


class DatabaseConnectionException(BaseDomainException):
    """Exception raised for database connection errors."""

    def __init__(self, message: str) -> None:
        """Initialize the DatabaseConnectionException.

        Args:
            message (str): The error message describing the database connection issue.
        """
        self.message = message
        super().__init__("Database connection error")


class UnexpectedDatabaseException(BaseDomainException):
    """Exception raised for unexpected database errors."""

    def __init__(self, message: str) -> None:
        """Initialize the UnexpectedDatabaseException.

        Args:
            message (str): The error message describing the unexpected database error.
        """
        self.message = message
        super().__init__("Unexpected database error")
