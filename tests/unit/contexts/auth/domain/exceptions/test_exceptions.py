"""Unit tests for authentication domain exceptions."""

from src.contexts.auth.domain.exceptions.exception import (
    AccountTemporarilyBlockedException,
    ActivationCodeExpiredException,
    AdminUserAlreadyExistsException,
    DoctorLicenseNumberAlreadyRegisteredException,
    DoctorProfileAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidActivationCodeException,
    InvalidCorporateEmailException,
    InvalidCredentialsException,
    InvalidEmailException,
    InvalidPasswordException,
    InvalidPasswordHashException,
    PatientDocumentAlreadyRegisteredException,
    PatientPhoneAlreadyRegisteredException,
    PatientProfileAlreadyExistsException,
    UnauthorizedUserRegistrationException,
    UserInactiveException,
    UserNotFoundException,
)
from src.shared.domain.exceptions.exception import BaseDomainException


class TestInvalidEmailException:
    """Unit tests for InvalidEmailException."""

    def test_should_create_with_email_and_errors(self):
        """Should create InvalidEmailException with email and errors."""
        email = "invalid.email"
        errors = ["Invalid format", "Missing @ symbol"]

        exc = InvalidEmailException(email, errors)

        assert exc.email == email
        assert exc.errors == errors
        assert "Invalid email address provided" in str(exc)
        assert issubclass(InvalidEmailException, BaseDomainException)


class TestInvalidPasswordHashException:
    """Unit tests for InvalidPasswordHashException."""

    def test_should_create_with_errors(self):
        """Should create InvalidPasswordHashException with errors."""
        errors = ("Invalid format", "Too short")

        exc = InvalidPasswordHashException(*errors)

        assert exc.errors == errors
        assert "Invalid password hash provided" in str(exc)
        assert issubclass(InvalidPasswordHashException, BaseDomainException)


class TestInvalidPasswordException:
    """Unit tests for InvalidPasswordException."""

    def test_should_create_with_errors_list(self):
        """Should create InvalidPasswordException with errors list."""
        errors = ["Too short", "No uppercase", "No special char"]

        exc = InvalidPasswordException(errors)

        assert exc.errors == errors
        assert "The password does not meet the security criteria" in str(exc)
        assert issubclass(InvalidPasswordException, BaseDomainException)


class TestEmailAlreadyExistsException:
    """Unit tests for EmailAlreadyExistsException."""

    def test_should_create_with_email(self):
        """Should create EmailAlreadyExistsException with email."""
        email = "user@example.com"

        exc = EmailAlreadyExistsException(email)

        assert exc.email == email
        assert f"Email '{email}' already exists" in str(exc)
        assert issubclass(EmailAlreadyExistsException, BaseDomainException)


class TestInvalidCorporateEmailException:
    """Unit tests for InvalidCorporateEmailException."""

    def test_should_create_with_email_and_role(self):
        """Should create InvalidCorporateEmailException with email and role."""
        email = "user@personal.com"
        role = "admin"

        exc = InvalidCorporateEmailException(email, role)

        assert exc.email == email
        assert exc.role == role
        assert f"Corporate email '{email}' is not allowed for role '{role}'" in str(exc)
        assert issubclass(InvalidCorporateEmailException, BaseDomainException)


class TestUnauthorizedUserRegistrationException:
    """Unit tests for UnauthorizedUserRegistrationException."""

    def test_should_create_with_role(self):
        """Should create UnauthorizedUserRegistrationException with role."""
        role = "patient"

        exc = UnauthorizedUserRegistrationException(role)

        assert exc.role == role
        assert (
            f"User with role '{role}' is not authorized to register new users"
            in str(exc)
        )
        assert issubclass(UnauthorizedUserRegistrationException, BaseDomainException)


class TestUserNotFoundException:
    """Unit tests for UserNotFoundException."""

    def test_should_create_with_field(self):
        """Should create UserNotFoundException with field."""
        field = "email: user@example.com"

        exc = UserNotFoundException(field)

        assert exc.field == field
        assert f"User not found with {field}" in str(exc)
        assert issubclass(UserNotFoundException, BaseDomainException)


class TestActivationCodeExpiredException:
    """Unit tests for ActivationCodeExpiredException."""

    def test_should_create_without_parameters(self):
        """Should create ActivationCodeExpiredException without parameters."""
        exc = ActivationCodeExpiredException()

        assert "The activation code has expired" in str(exc)
        assert issubclass(ActivationCodeExpiredException, BaseDomainException)


class TestInvalidActivationCodeException:
    """Unit tests for InvalidActivationCodeException."""

    def test_should_create_without_parameters(self):
        """Should create InvalidActivationCodeException without parameters."""
        exc = InvalidActivationCodeException()

        assert "The activation code is invalid" in str(exc)
        assert issubclass(InvalidActivationCodeException, BaseDomainException)


class TestInvalidCredentialsException:
    """Unit tests for InvalidCredentialsException."""

    def test_should_create_without_parameters(self):
        """Should create InvalidCredentialsException without parameters."""
        exc = InvalidCredentialsException()

        assert "Invalid credentials provided" in str(exc)
        assert issubclass(InvalidCredentialsException, BaseDomainException)


class TestAccountTemporarilyBlockedException:
    """Unit tests for AccountTemporarilyBlockedException."""

    def test_should_create_with_error_message(self):
        """Should create AccountTemporarilyBlockedException with error message."""
        error = "Too many failed attempts"

        exc = AccountTemporarilyBlockedException(error)

        assert exc.error == error
        assert "Account temporarily blocked provided" in str(exc)
        assert issubclass(AccountTemporarilyBlockedException, BaseDomainException)


class TestUserInactiveException:
    """Unit tests for UserInactiveException."""

    def test_should_create_without_parameters(self):
        """Should create UserInactiveException without parameters."""
        exc = UserInactiveException()

        assert "The user account is inactive" in str(exc)
        assert issubclass(UserInactiveException, BaseDomainException)


class TestAdminUserAlreadyExistsException:
    """Unit tests for AdminUserAlreadyExistsException."""

    def test_should_create_without_parameters(self):
        """Should create AdminUserAlreadyExistsException without parameters."""
        exc = AdminUserAlreadyExistsException()

        assert "An admin user already exists in the system" in str(exc)
        assert issubclass(AdminUserAlreadyExistsException, BaseDomainException)


class TestPatientProfileAlreadyExistsException:
    """Unit tests for PatientProfileAlreadyExistsException."""

    def test_should_create_without_parameters(self):
        """Should create PatientProfileAlreadyExistsException without parameters."""
        exc = PatientProfileAlreadyExistsException()

        assert "A patient profile already exists for this user" in str(exc)
        assert issubclass(PatientProfileAlreadyExistsException, BaseDomainException)


class TestPatientDocumentAlreadyRegisteredException:
    """Unit tests for PatientDocumentAlreadyRegisteredException."""

    def test_should_create_without_parameters(self):
        """Should create PatientDocumentAlreadyRegisteredException without parameters."""
        exc = PatientDocumentAlreadyRegisteredException()

        assert "Patient document already registered" in str(exc)
        assert issubclass(
            PatientDocumentAlreadyRegisteredException, BaseDomainException
        )


class TestPatientPhoneAlreadyRegisteredException:
    """Unit tests for PatientPhoneAlreadyRegisteredException."""

    def test_should_create_without_parameters(self):
        """Should create PatientPhoneAlreadyRegisteredException without parameters."""
        exc = PatientPhoneAlreadyRegisteredException()

        assert "Patient phone number already registered" in str(exc)
        assert issubclass(PatientPhoneAlreadyRegisteredException, BaseDomainException)


class TestDoctorProfileAlreadyExistsException:
    """Unit tests for DoctorProfileAlreadyExistsException."""

    def test_should_create_without_parameters(self):
        """Should create DoctorProfileAlreadyExistsException without parameters."""
        exc = DoctorProfileAlreadyExistsException()

        assert "A doctor profile already exists for this user" in str(exc)
        assert issubclass(DoctorProfileAlreadyExistsException, BaseDomainException)


class TestDoctorLicenseNumberAlreadyRegisteredException:
    """Unit tests for DoctorLicenseNumberAlreadyRegisteredException."""

    def test_should_create_without_parameters(self):
        """Should create DoctorLicenseNumberAlreadyRegisteredException without parameters."""
        exc = DoctorLicenseNumberAlreadyRegisteredException()

        assert "Doctor license number already registered" in str(exc)
        assert issubclass(
            DoctorLicenseNumberAlreadyRegisteredException, BaseDomainException
        )
