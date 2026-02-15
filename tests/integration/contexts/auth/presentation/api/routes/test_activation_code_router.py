"""Integration tests for POST /api/auth/activate."""

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
    ActivationCodeExpiredException,
    InvalidActivationCodeException,
    UserNotFoundException,
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

ACTIVATE_REQUEST_BODY = {
    "activation_code": "ABC123",
    "email": "john.doe@example.com",
}


def _make_app(activate_uc: ActivateAccountUseCase | None = None) -> FastAPI:
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
    app.dependency_overrides[get_login_use_case] = lambda: MagicMock(spec=LoginUseCase)
    app.dependency_overrides[get_current_user] = lambda: TokenPayloadVO(
        user_id=uuid4(),
        role=RolesEnum.ADMIN,
        expires_in=3600,
        jti=uuid4(),
    )

    if activate_uc is not None:
        app.dependency_overrides[get_activate_account_use_case] = lambda: activate_uc

    app.dependency_overrides[get_logger] = lambda: MagicMock()
    return app


class TestActivateAccountRoute:
    """Integration tests for POST /api/auth/activate."""

    @pytest.fixture
    def activate_uc_mock(self):
        return MagicMock(spec=ActivateAccountUseCase)

    @pytest.fixture
    def client(self, activate_uc_mock):
        return TestClient(
            _make_app(activate_uc=activate_uc_mock), raise_server_exceptions=False
        )

    def test_activate_returns_200_on_success(self, client, activate_uc_mock):
        """Should return 200 when the account is activated successfully."""
        activate_uc_mock.execute.return_value = None

        response = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User account activated successfully"

    def test_activate_calls_use_case_with_correct_arguments(
        self, client, activate_uc_mock
    ):
        """Should forward activation_code and email to the use-case."""
        activate_uc_mock.execute.return_value = None

        client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY)

        activate_uc_mock.execute.assert_called_once_with(
            ACTIVATE_REQUEST_BODY["activation_code"],
            ACTIVATE_REQUEST_BODY["email"],
        )

    def test_activate_returns_400_when_code_is_expired(self, client, activate_uc_mock):
        """Should return 400 when the activation code has expired."""
        activate_uc_mock.execute.side_effect = ActivationCodeExpiredException()

        response = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["message"] == "Activation code has expired"

    def test_activate_returns_400_when_code_is_invalid(self, client, activate_uc_mock):
        """Should return 400 when the activation code is invalid."""
        activate_uc_mock.execute.side_effect = InvalidActivationCodeException()

        response = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["message"] == "Invalid activation code"

    def test_activate_returns_404_when_user_not_found(self, client, activate_uc_mock):
        """Should return 404 when the user is not found."""
        activate_uc_mock.execute.side_effect = UserNotFoundException(
            "email: john@example.com"
        )

        response = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["message"] == "User not found"

    def test_activate_returns_500_on_database_connection_error(
        self, client, activate_uc_mock
    ):
        """Should return 500 when a database connection error occurs."""
        activate_uc_mock.execute.side_effect = DatabaseConnectionException(
            "Connection refused"
        )

        response = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_activate_returns_500_on_unexpected_database_error(
        self, client, activate_uc_mock
    ):
        """Should return 500 when an unexpected database error occurs."""
        activate_uc_mock.execute.side_effect = UnexpectedDatabaseException("Unknown")

        response = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_activate_returns_422_when_activation_code_is_missing(self, client):
        """Should return 422 when activation_code is missing."""
        response = client.post("/api/auth/activate", json={"email": "john@example.com"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_activate_returns_422_when_email_is_missing(self, client):
        """Should return 422 when email is missing."""
        response = client.post("/api/auth/activate", json={"activation_code": "ABC123"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_activate_returns_422_when_body_is_empty(self, client):
        """Should return 422 when the request body is empty."""
        response = client.post("/api/auth/activate", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_activate_success_response_has_message_field(
        self, client, activate_uc_mock
    ):
        """Successful activation response must contain a 'message' field."""
        activate_uc_mock.execute.return_value = None

        data = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY).json()

        assert "message" in data

    def test_activate_error_response_has_message_and_details(
        self, client, activate_uc_mock
    ):
        """Error response must contain 'message' and 'details' as a list."""
        activate_uc_mock.execute.side_effect = ActivationCodeExpiredException()

        data = client.post("/api/auth/activate", json=ACTIVATE_REQUEST_BODY).json()

        assert "message" in data
        assert "details" in data
        assert isinstance(data["details"], list)

    def test_get_method_is_not_allowed(self, client):
        """GET on /api/auth/activate must return 405."""
        assert (
            client.get("/api/auth/activate").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_method_is_not_allowed(self, client):
        """DELETE on /api/auth/activate must return 405."""
        assert (
            client.delete("/api/auth/activate").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_post_without_body_returns_422(self, client):
        """POST without a body must return 422."""
        assert (
            client.post("/api/auth/activate").status_code
            == status.HTTP_422_UNPROCESSABLE_CONTENT
        )
