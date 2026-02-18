"""Integration tests for POST /api/auth/register."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.application.use_cases.login_use_case import LoginUseCase
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.exceptions.exception import (
    DoctorLicenseNumberAlreadyRegisteredException,
    DoctorProfileAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCorporateEmailException,
    PatientDocumentAlreadyRegisteredException,
    PatientPhoneAlreadyRegisteredException,
    PatientProfileAlreadyExistsException,
    UnauthorizedUserRegistrationException,
)
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.contexts.auth.presentation.api.exceptions.exceptions_handlers import (
    register_auth_exceptions_handlers,
)
from src.contexts.auth.presentation.api.routes.router import router
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)

ADMIN_TOKEN_PAYLOAD = TokenPayloadVO(
    user_id=uuid4(),
    role=RolesEnum.ADMIN,
    expires_in=3600,
    jti=uuid4(),
)

PATIENT_REQUEST_BODY = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "role": "patient",
    "profile": {
        "profile_type": "patient",
        "document": "123456789",
        "phone": "+1234567890",
        "birth_date": "1990-01-01",
    },
}

DOCTOR_REQUEST_BODY = {
    "first_name": "Gregory",
    "last_name": "House",
    "email": "house@example.com",
    "role": "doctor",
    "profile": {
        "profile_type": "doctor",
        "specialty_id": "d290f1ee-6c54-4b01-9d5f-ff5af830be8a",
        "license_number": "MED123456",
        "experience_years": 10,
        "is_active": True,
        "qualifications": "Board Certified",
        "bio": "Diagnostic specialist",
    },
}


def _make_app(
    register_uc: RegisterUserUseCase | None = None,
    current_user: TokenPayloadVO | None = None,
) -> FastAPI:
    app = FastAPI()
    register_auth_exceptions_handlers(app)
    app.include_router(router)

    from src.contexts.auth.presentation.api.compositions.use_cases_composition import (
        get_activate_account_use_case,
        get_login_use_case,
        get_register_user_use_case,
    )
    from src.shared.presentation.api.compositions.infrastructure_composition import (
        get_logger,
    )
    from src.shared.presentation.api.compositions.security_composition import (
        get_current_user,
    )

    # Always stub unused use-cases to avoid real dependency resolution
    app.dependency_overrides[get_activate_account_use_case] = lambda: MagicMock(
        spec=ActivateAccountUseCase
    )
    app.dependency_overrides[get_login_use_case] = lambda: MagicMock(spec=LoginUseCase)

    if register_uc is not None:
        app.dependency_overrides[get_register_user_use_case] = lambda: register_uc
    if current_user is not None:
        app.dependency_overrides[get_current_user] = lambda: current_user

    app.dependency_overrides[get_logger] = lambda: MagicMock()
    return app


class TestRegisterUserRoute:
    """Integration tests for POST /api/auth/register."""

    @pytest.fixture
    def register_uc_mock(self):
        return MagicMock(spec=RegisterUserUseCase)

    @pytest.fixture
    def client(self, register_uc_mock):
        app = _make_app(register_uc=register_uc_mock, current_user=ADMIN_TOKEN_PAYLOAD)
        return TestClient(app, raise_server_exceptions=False)

    def test_register_patient_returns_201(self, client, register_uc_mock):
        """Should return 201 when a patient is registered successfully."""
        register_uc_mock.execute.return_value = None

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "User registered successfully"
        register_uc_mock.execute.assert_called_once()

    def test_register_doctor_returns_201(self, client, register_uc_mock):
        """Should return 201 when a doctor is registered successfully."""
        register_uc_mock.execute.return_value = None

        response = client.post("/api/auth/register", json=DOCTOR_REQUEST_BODY)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "User registered successfully"

    def test_register_admin_without_profile_returns_201(self, client, register_uc_mock):
        """Should return 201 when an admin (no profile) is registered successfully."""
        register_uc_mock.execute.return_value = None
        body = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "role": "admin",
        }

        response = client.post("/api/auth/register", json=body)

        assert response.status_code == status.HTTP_201_CREATED

    def test_register_returns_409_when_email_already_exists(
        self, client, register_uc_mock
    ):
        """Should return 409 when the email already exists."""
        register_uc_mock.execute.side_effect = EmailAlreadyExistsException(
            "john.doe@example.com"
        )

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["message"] == "Email already exists"

    def test_register_returns_409_when_patient_document_already_registered(
        self, client, register_uc_mock
    ):
        """Should return 409 when the patient document is already registered."""
        register_uc_mock.execute.side_effect = (
            PatientDocumentAlreadyRegisteredException()
        )

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["message"] == "Patient document already registered"

    def test_register_returns_409_when_patient_phone_already_registered(
        self, client, register_uc_mock
    ):
        """Should return 409 when the patient phone is already registered."""
        register_uc_mock.execute.side_effect = PatientPhoneAlreadyRegisteredException()

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["message"] == "Patient phone number already registered"

    def test_register_returns_409_when_patient_profile_already_exists(
        self, client, register_uc_mock
    ):
        """Should return 409 when the patient profile already exists."""
        register_uc_mock.execute.side_effect = PatientProfileAlreadyExistsException()

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["message"] == "Patient profile already exists"

    def test_register_returns_409_when_doctor_license_already_registered(
        self, client, register_uc_mock
    ):
        """Should return 409 when the doctor license number is already registered."""
        register_uc_mock.execute.side_effect = (
            DoctorLicenseNumberAlreadyRegisteredException()
        )

        response = client.post("/api/auth/register", json=DOCTOR_REQUEST_BODY)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["message"] == "Doctor license number already registered"

    def test_register_returns_409_when_doctor_profile_already_exists(
        self, client, register_uc_mock
    ):
        """Should return 409 when the doctor profile already exists."""
        register_uc_mock.execute.side_effect = DoctorProfileAlreadyExistsException()

        response = client.post("/api/auth/register", json=DOCTOR_REQUEST_BODY)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["message"] == "Doctor profile already exists"

    def test_register_returns_400_when_invalid_corporate_email(
        self, client, register_uc_mock
    ):
        """Should return 400 when the email is not a valid corporate email."""
        register_uc_mock.execute.side_effect = InvalidCorporateEmailException(
            "john@gmail.com", "admin"
        )

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["message"] == "Invalid corporate email"

    def test_register_returns_403_when_unauthorized_role(
        self, client, register_uc_mock
    ):
        """Should return 403 when the requesting role cannot register users."""
        register_uc_mock.execute.side_effect = UnauthorizedUserRegistrationException(
            "patient"
        )

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["message"] == "Unauthorized user registration attempt"

    def test_register_returns_422_when_first_name_is_missing(self, client):
        """Should return 422 when first_name is missing."""
        body = {
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "role": "patient",
        }

        response = client.post("/api/auth/register", json=body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_register_returns_422_when_body_is_empty(self, client):
        """Should return 422 when the request body is empty."""
        response = client.post("/api/auth/register", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_register_returns_500_on_database_connection_error(
        self, client, register_uc_mock
    ):
        """Should return 500 when a database connection error occurs."""
        register_uc_mock.execute.side_effect = DatabaseConnectionException(
            "Connection refused"
        )

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_register_returns_500_on_unexpected_database_error(
        self, client, register_uc_mock
    ):
        """Should return 500 when an unexpected database error occurs."""
        register_uc_mock.execute.side_effect = UnexpectedDatabaseException("Unknown")

        response = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_register_success_response_contains_message(self, client, register_uc_mock):
        """Success response must contain a 'message' field."""
        register_uc_mock.execute.return_value = None

        data = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY).json()

        assert "message" in data

    def test_register_error_response_contains_message_and_details(
        self, client, register_uc_mock
    ):
        """Error response must contain 'message' and 'details' as a list."""
        register_uc_mock.execute.side_effect = EmailAlreadyExistsException(
            "john@example.com"
        )

        data = client.post("/api/auth/register", json=PATIENT_REQUEST_BODY).json()

        assert "message" in data
        assert "details" in data
        assert isinstance(data["details"], list)

    def test_get_method_is_not_allowed(self, client):
        """GET on /api/auth/register must return 405."""
        assert (
            client.get("/api/auth/register").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_method_is_not_allowed(self, client):
        """DELETE on /api/auth/register must return 405."""
        assert (
            client.delete("/api/auth/register").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_post_without_body_returns_422(self, client):
        """POST without a body must return 422."""
        assert (
            client.post("/api/auth/register").status_code
            == status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    def test_register_passes_role_recorder_from_jwt_to_command(self, register_uc_mock):
        """The current_user role from the JWT must be forwarded as role_recorder."""
        register_uc_mock.execute.return_value = None
        client = TestClient(
            _make_app(register_uc=register_uc_mock, current_user=ADMIN_TOKEN_PAYLOAD),
            raise_server_exceptions=False,
        )

        client.post("/api/auth/register", json=PATIENT_REQUEST_BODY)

        command = register_uc_mock.execute.call_args[0][0]
        assert command.role_recorder.value == "admin"
