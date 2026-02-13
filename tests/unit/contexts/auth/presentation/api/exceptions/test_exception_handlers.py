"""Unit tests for auth exception handlers."""

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.contexts.auth.domain.exceptions.exception import (
    AccountTemporarilyBlockedException,
    ActivationCodeExpiredException,
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
from src.contexts.auth.presentation.api.exceptions.exceptions_handlers import (
    register_auth_exceptions_handlers,
)


def _make_app(*exceptions_and_messages) -> FastAPI:
    """Build a minimal FastAPI app that exposes one GET route per exception.

    ``exceptions_and_messages`` is a sequence of (path, exception_factory) tuples.
    """
    app = FastAPI()
    register_auth_exceptions_handlers(app)

    for path, exc_factory in exceptions_and_messages:

        @app.get(path)
        async def _route(exc_factory=exc_factory):  # default capture
            raise exc_factory()

    return app


# ──────────────────────────────────────────────────────────────────────────────
# Helpers / shared data
# ──────────────────────────────────────────────────────────────────────────────

VALID_EMAIL = "user@example.com"
VALID_ROLE = "admin"
VALID_ERRORS = ["error detail one", "error detail two"]


# ──────────────────────────────────────────────────────────────────────────────
# EmailAlreadyExistsException → 409 CONFLICT
# ──────────────────────────────────────────────────────────────────────────────


class TestEmailAlreadyExistsExceptionHandler:
    """Tests for EmailAlreadyExistsException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: EmailAlreadyExistsException(VALID_EMAIL)),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_409_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_409_CONFLICT

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Email already exists"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)
        assert len(data["details"]) > 0


# ──────────────────────────────────────────────────────────────────────────────
# InvalidEmailException → 400 BAD REQUEST
# ──────────────────────────────────────────────────────────────────────────────


class TestInvalidEmailExceptionHandler:
    """Tests for InvalidEmailException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: InvalidEmailException(VALID_EMAIL, VALID_ERRORS)),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_400_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Invalid email"

    def test_returns_errors_as_details(self, client):
        data = client.get("/test").json()
        assert data["details"] == VALID_ERRORS


# ──────────────────────────────────────────────────────────────────────────────
# InvalidPasswordException → 400 BAD REQUEST
# ──────────────────────────────────────────────────────────────────────────────


class TestInvalidPasswordExceptionHandler:
    """Tests for InvalidPasswordException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: InvalidPasswordException(VALID_ERRORS)),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_400_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Invalid password"

    def test_returns_errors_as_details(self, client):
        data = client.get("/test").json()
        assert data["details"] == VALID_ERRORS


# ──────────────────────────────────────────────────────────────────────────────
# InvalidPasswordHashException → 500 INTERNAL SERVER ERROR
# ──────────────────────────────────────────────────────────────────────────────


class TestInvalidPasswordHashExceptionHandler:
    """Tests for InvalidPasswordHashException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: InvalidPasswordHashException("hash error")),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_500_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Internal server error"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# InvalidCorporateEmailException → 400 BAD REQUEST
# ──────────────────────────────────────────────────────────────────────────────


class TestInvalidCorporateEmailExceptionHandler:
    """Tests for InvalidCorporateEmailException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            (
                "/test",
                lambda: InvalidCorporateEmailException(VALID_EMAIL, VALID_ROLE),
            ),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_400_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Invalid corporate email"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)
        assert len(data["details"]) > 0


# ──────────────────────────────────────────────────────────────────────────────
# UnauthorizedUserRegistrationException → 403 FORBIDDEN
# ──────────────────────────────────────────────────────────────────────────────


class TestUnauthorizedUserRegistrationExceptionHandler:
    """Tests for UnauthorizedUserRegistrationException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: UnauthorizedUserRegistrationException(VALID_ROLE)),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_403_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_403_FORBIDDEN

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Unauthorized user registration attempt"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# ActivationCodeExpiredException → 400 BAD REQUEST
# ──────────────────────────────────────────────────────────────────────────────


class TestActivationCodeExpiredExceptionHandler:
    """Tests for ActivationCodeExpiredException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: ActivationCodeExpiredException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_400_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Activation code has expired"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# InvalidActivationCodeException → 400 BAD REQUEST
# ──────────────────────────────────────────────────────────────────────────────


class TestInvalidActivationCodeExceptionHandler:
    """Tests for InvalidActivationCodeException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: InvalidActivationCodeException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_400_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Invalid activation code"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# UserNotFoundException → 404 NOT FOUND
# ──────────────────────────────────────────────────────────────────────────────


class TestUserNotFoundExceptionHandler:
    """Tests for UserNotFoundException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: UserNotFoundException("email: user@example.com")),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_404_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_404_NOT_FOUND

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "User not found"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# InvalidCredentialsException → 401 UNAUTHORIZED
# ──────────────────────────────────────────────────────────────────────────────


class TestInvalidCredentialsExceptionHandler:
    """Tests for InvalidCredentialsException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: InvalidCredentialsException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_401_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Invalid credentials"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# AccountTemporarilyBlockedException → 423 LOCKED
# ──────────────────────────────────────────────────────────────────────────────


class TestAccountTemporarilyBlockedExceptionHandler:
    """Tests for AccountTemporarilyBlockedException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: AccountTemporarilyBlockedException("Too many attempts")),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_423_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_423_LOCKED

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Account temporarily blocked"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# UserInactiveException → 403 FORBIDDEN
# ──────────────────────────────────────────────────────────────────────────────


class TestUserInactiveExceptionHandler:
    """Tests for UserInactiveException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: UserInactiveException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_403_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_403_FORBIDDEN

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "User account is inactive"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# PatientDocumentAlreadyRegisteredException → 409 CONFLICT
# ──────────────────────────────────────────────────────────────────────────────


class TestPatientDocumentAlreadyRegisteredExceptionHandler:
    """Tests for PatientDocumentAlreadyRegisteredException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: PatientDocumentAlreadyRegisteredException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_409_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_409_CONFLICT

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Patient document already registered"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# PatientPhoneAlreadyRegisteredException → 409 CONFLICT
# ──────────────────────────────────────────────────────────────────────────────


class TestPatientPhoneAlreadyRegisteredExceptionHandler:
    """Tests for PatientPhoneAlreadyRegisteredException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: PatientPhoneAlreadyRegisteredException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_409_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_409_CONFLICT

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Patient phone number already registered"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# PatientProfileAlreadyExistsException → 409 CONFLICT
# ──────────────────────────────────────────────────────────────────────────────


class TestPatientProfileAlreadyExistsExceptionHandler:
    """Tests for PatientProfileAlreadyExistsException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: PatientProfileAlreadyExistsException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_409_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_409_CONFLICT

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Patient profile already exists"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# DoctorLicenseNumberAlreadyRegisteredException → 409 CONFLICT
# ──────────────────────────────────────────────────────────────────────────────


class TestDoctorLicenseNumberAlreadyRegisteredExceptionHandler:
    """Tests for DoctorLicenseNumberAlreadyRegisteredException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: DoctorLicenseNumberAlreadyRegisteredException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_409_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_409_CONFLICT

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Doctor license number already registered"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# DoctorProfileAlreadyExistsException → 409 CONFLICT
# ──────────────────────────────────────────────────────────────────────────────


class TestDoctorProfileAlreadyExistsExceptionHandler:
    """Tests for DoctorProfileAlreadyExistsException handler."""

    @pytest.fixture
    def client(self):
        app = _make_app(
            ("/test", lambda: DoctorProfileAlreadyExistsException()),
        )
        return TestClient(app, raise_server_exceptions=False)

    def test_returns_409_status_code(self, client):
        assert client.get("/test").status_code == status.HTTP_409_CONFLICT

    def test_returns_correct_message(self, client):
        data = client.get("/test").json()
        assert data["message"] == "Doctor profile already exists"

    def test_returns_details_list(self, client):
        data = client.get("/test").json()
        assert isinstance(data["details"], list)


# ──────────────────────────────────────────────────────────────────────────────
# Response structure (transversal)
# ──────────────────────────────────────────────────────────────────────────────


class TestExceptionHandlerResponseStructure:
    """Ensure every handler returns the shared ErrorsResponse schema shape."""

    CASES = [
        ("/email-exists", lambda: EmailAlreadyExistsException(VALID_EMAIL)),
        ("/invalid-email", lambda: InvalidEmailException(VALID_EMAIL, VALID_ERRORS)),
        ("/invalid-pwd", lambda: InvalidPasswordException(VALID_ERRORS)),
        ("/invalid-hash", lambda: InvalidPasswordHashException("err")),
        (
            "/corp-email",
            lambda: InvalidCorporateEmailException(VALID_EMAIL, VALID_ROLE),
        ),
        ("/unauth-reg", lambda: UnauthorizedUserRegistrationException(VALID_ROLE)),
        ("/code-expired", lambda: ActivationCodeExpiredException()),
        ("/invalid-code", lambda: InvalidActivationCodeException()),
        ("/user-not-found", lambda: UserNotFoundException("email")),
        ("/invalid-creds", lambda: InvalidCredentialsException()),
        ("/acct-blocked", lambda: AccountTemporarilyBlockedException("Too many")),
        ("/user-inactive", lambda: UserInactiveException()),
        ("/patient-doc", lambda: PatientDocumentAlreadyRegisteredException()),
        ("/patient-phone", lambda: PatientPhoneAlreadyRegisteredException()),
        ("/patient-profile", lambda: PatientProfileAlreadyExistsException()),
        ("/doctor-license", lambda: DoctorLicenseNumberAlreadyRegisteredException()),
        ("/doctor-profile", lambda: DoctorProfileAlreadyExistsException()),
    ]

    @pytest.fixture
    def client(self):
        app = _make_app(*self.CASES)
        return TestClient(app, raise_server_exceptions=False)

    @pytest.mark.parametrize("path,_", CASES)
    def test_response_contains_message_key(self, client, path, _):
        data = client.get(path).json()
        assert "message" in data

    @pytest.mark.parametrize("path,_", CASES)
    def test_response_contains_details_key(self, client, path, _):
        data = client.get(path).json()
        assert "details" in data

    @pytest.mark.parametrize("path,_", CASES)
    def test_details_is_always_a_list(self, client, path, _):
        data = client.get(path).json()
        assert isinstance(data["details"], list)

    @pytest.mark.parametrize("path,_", CASES)
    def test_message_is_always_a_string(self, client, path, _):
        data = client.get(path).json()
        assert isinstance(data["message"], str)
        assert data["message"]  # not empty
