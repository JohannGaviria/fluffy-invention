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


class InvalidPasswordException(BaseDomainException):
    """Exception raised for invalid passwords."""

    def __init__(self, errors: list[str]) -> None:
        """Initialize the InvalidPasswordException.

        Args:
            errors (list[str]): Variable length error messages describing the validation issues.
        """
        self.errors = errors
        super().__init__("The password does not meet the security criteria")


class EmailAlreadyExistsException(BaseDomainException):
    """Exception raised when an email already exists in the system."""

    def __init__(self, email: str) -> None:
        """Initialize the EmailAlreadyExistsException.

        Args:
            email (str): The email address that already exists.
        """
        self.email = email
        super().__init__(f"Email '{email}' already exists")


class InvalidCorporateEmailException(BaseDomainException):
    """Exception raised when a corporate email does not meet policy requirements."""

    def __init__(self, email: str, role: str) -> None:
        """Initialize the InvalidCorporateEmailException.

        Args:
            email (str): The corporate email address.
            role (str): The role associated with the email.
        """
        self.email = email
        self.role = role
        super().__init__(f"Corporate email '{email}' is not allowed for role '{role}'")


class UnauthorizedUserRegistrationException(BaseDomainException):
    """Exception raised when a user is not authorized to register new users."""

    def __init__(self, role: str) -> None:
        """Initialize the UnauthorizedUserRegistrationException.

        Args:
            role (str): The role of the user attempting the registration.
        """
        self.role = role
        super().__init__(
            f"User with role '{role}' is not authorized to register new users"
        )


class UserNotFoundException(BaseDomainException):
    """Exception raised when a user is not found in the system."""

    def __init__(self, field: str) -> None:
        """Initialize the UserNotFoundException.

        Args:
            field (str): The field used to search for the user.
        """
        self.field = field
        super().__init__(f"User not found with {field}")


class ActivationCodeExpiredException(BaseDomainException):
    """Exception raised when an activation code has expired."""

    def __init__(self) -> None:
        """Initialize the ActivationCodeExpiredException."""
        super().__init__("The activation code has expired")


class InvalidActivationCodeException(BaseDomainException):
    """Exception raised when an activation code is invalid."""

    def __init__(self) -> None:
        """Initialize the InvalidActivationCodeException."""
        super().__init__("The activation code is invalid")


class InvalidCredentialsException(BaseDomainException):
    """Exception raised for invalid credentials."""

    def __init__(self) -> None:
        """Initialize the InvalidCredentialsException.

        Args:
            errors (str): Variable length error messages describing the validation issues.
        """
        super().__init__("Invalid credentials provided")


class AccountTemporarilyBlockedException(BaseDomainException):
    """Exception raised for account temporarily blocked."""

    def __init__(self, error: str) -> None:
        """Initialize the AccountTemporarilyBlockedException.

        Args:
            error (str): Variable length error messages describing the validation issues.
        """
        self.error = error
        super().__init__("Account temporarily blocked provided")


class UserInactiveException(BaseDomainException):
    """Exception raised when a user account is inactive."""

    def __init__(self) -> None:
        """Initialize the UserInactiveException."""
        super().__init__("The user account is inactive")


class AdminUserAlreadyExistsException(BaseDomainException):
    """Exception raised when an admin user already exists in the system."""

    def __init__(self) -> None:
        """Initialize the AdminUserAlreadyExistsException."""
        super().__init__("An admin user already exists in the system")
