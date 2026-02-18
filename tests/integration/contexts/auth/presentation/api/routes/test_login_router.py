"""Integration tests for POST /api/auth/login."""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.contexts.auth.application.dto.response import AccessTokenResponse
from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.application.use_cases.login_use_case import LoginUseCase
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.exceptions.exception import (
    AccountTemporarilyBlockedException,
    InvalidCredentialsException,
    UserInactiveException,
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

LOGIN_REQUEST_BODY = {
    "email": "john.doe@example.com",
    "password": "SecurePass!23",
}


def _build_access_token_response() -> AccessTokenResponse:
    """Build a sample AccessTokenResponse DTO."""
    return AccessTokenResponse(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
        token_type="Bearer",
        expires_at=datetime.now(UTC) + timedelta(hours=1),
        expires_in=3600,
    )


def _make_app(login_uc: LoginUseCase | None = None) -> FastAPI:
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

    # Stub unused use-cases and auth guard
    app.dependency_overrides[get_register_user_use_case] = lambda: MagicMock(
        spec=RegisterUserUseCase
    )
    app.dependency_overrides[get_activate_account_use_case] = lambda: MagicMock(
        spec=ActivateAccountUseCase
    )
    app.dependency_overrides[get_current_user] = lambda: TokenPayloadVO(
        user_id=uuid4(),
        role=RolesEnum.ADMIN,
        expires_in=3600,
        jti=uuid4(),
    )

    if login_uc is not None:
        app.dependency_overrides[get_login_use_case] = lambda: login_uc

    app.dependency_overrides[get_logger] = lambda: MagicMock()
    return app


class TestLoginUserRoute:
    """Integration tests for POST /api/auth/login."""

    @pytest.fixture
    def login_uc_mock(self):
        return MagicMock(spec=LoginUseCase)

    @pytest.fixture
    def client(self, login_uc_mock):
        return TestClient(
            _make_app(login_uc=login_uc_mock), raise_server_exceptions=False
        )

    def test_login_returns_200_on_success(self, client, login_uc_mock):
        """Should return 200 on successful login."""
        login_uc_mock.execute.return_value = _build_access_token_response()

        response = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Login successful"

    def test_login_response_contains_data_field(self, client, login_uc_mock):
        """Successful response must have a 'data' field."""
        login_uc_mock.execute.return_value = _build_access_token_response()

        data = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY).json()

        assert "data" in data

    def test_login_response_data_contains_access_token(self, client, login_uc_mock):
        """Response data must contain 'access_token'."""
        token_response = _build_access_token_response()
        login_uc_mock.execute.return_value = token_response

        data = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY).json()

        assert data["data"]["access_token"] == token_response.access_token

    def test_login_response_data_contains_token_type(self, client, login_uc_mock):
        """Response data must contain 'token_type' equal to Bearer."""
        login_uc_mock.execute.return_value = _build_access_token_response()

        data = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY).json()

        assert data["data"]["token_type"] == "Bearer"

    def test_login_response_data_contains_expires_in(self, client, login_uc_mock):
        """Response data must contain 'expires_in'."""
        login_uc_mock.execute.return_value = _build_access_token_response()

        data = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY).json()

        assert data["data"]["expires_in"] == 3600

    def test_login_response_data_contains_expires_at(self, client, login_uc_mock):
        """Response data must contain 'expires_at'."""
        login_uc_mock.execute.return_value = _build_access_token_response()

        data = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY).json()

        assert "expires_at" in data["data"]

    def test_login_returns_401_when_credentials_are_invalid(
        self, client, login_uc_mock
    ):
        """Should return 401 when the provided credentials are invalid."""
        login_uc_mock.execute.side_effect = InvalidCredentialsException()

        response = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["message"] == "Invalid credentials"

    def test_login_returns_403_when_account_is_inactive(self, client, login_uc_mock):
        """Should return 403 when the user account is inactive."""
        login_uc_mock.execute.side_effect = UserInactiveException()

        response = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["message"] == "User account is inactive"

    def test_login_returns_423_when_account_is_blocked(self, client, login_uc_mock):
        """Should return 423 when the account is temporarily blocked."""
        login_uc_mock.execute.side_effect = AccountTemporarilyBlockedException(
            "Too many failed attempts"
        )

        response = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY)

        assert response.status_code == status.HTTP_423_LOCKED
        assert response.json()["message"] == "Account temporarily blocked"

    def test_login_returns_500_on_database_connection_error(
        self, client, login_uc_mock
    ):
        """Should return 500 when a database connection error occurs."""
        login_uc_mock.execute.side_effect = DatabaseConnectionException(
            "Connection refused"
        )

        response = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_login_returns_500_on_unexpected_database_error(
        self, client, login_uc_mock
    ):
        """Should return 500 when an unexpected database error occurs."""
        login_uc_mock.execute.side_effect = UnexpectedDatabaseException("Unknown")

        response = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_login_returns_422_when_email_is_missing(self, client):
        """Should return 422 when the email field is missing."""
        response = client.post("/api/auth/login", json={"password": "SecurePass!23"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_login_returns_422_when_password_is_missing(self, client):
        """Should return 422 when the password field is missing."""
        response = client.post("/api/auth/login", json={"email": "john@example.com"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_login_returns_422_when_body_is_empty(self, client):
        """Should return 422 when the request body is empty."""
        response = client.post("/api/auth/login", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_login_success_response_has_message_field(self, client, login_uc_mock):
        """Successful login response must contain a 'message' field."""
        login_uc_mock.execute.return_value = _build_access_token_response()

        data = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY).json()

        assert "message" in data

    def test_login_error_response_has_message_and_details(self, client, login_uc_mock):
        """Error response must contain 'message' and 'details' as a list."""
        login_uc_mock.execute.side_effect = InvalidCredentialsException()

        data = client.post("/api/auth/login", json=LOGIN_REQUEST_BODY).json()

        assert "message" in data
        assert "details" in data
        assert isinstance(data["details"], list)

    def test_get_method_is_not_allowed(self, client):
        """GET on /api/auth/login must return 405."""
        assert (
            client.get("/api/auth/login").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_method_is_not_allowed(self, client):
        """DELETE on /api/auth/login must return 405."""
        assert (
            client.delete("/api/auth/login").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_post_without_body_returns_422(self, client):
        """POST without a body must return 422."""
        assert (
            client.post("/api/auth/login").status_code
            == status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    def test_login_passes_email_and_password_to_use_case(self, client, login_uc_mock):
        """The email and password must be forwarded exactly to the use-case."""
        login_uc_mock.execute.return_value = _build_access_token_response()

        client.post("/api/auth/login", json=LOGIN_REQUEST_BODY)

        command = login_uc_mock.execute.call_args[0][0]
        assert command.email == LOGIN_REQUEST_BODY["email"]
        assert command.password == LOGIN_REQUEST_BODY["password"]
