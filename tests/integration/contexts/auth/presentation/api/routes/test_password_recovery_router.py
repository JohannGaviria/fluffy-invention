"""Integration tests for POST /api/auth/password-recovery."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.application.use_cases.login_use_case import LoginUseCase
from src.contexts.auth.application.use_cases.password_recovery_use_case import (
    PasswordRecoveryUseCase,
)
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.exceptions.exception import UserNotFoundException
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.contexts.auth.presentation.api.exceptions.exceptions_handlers import (
    register_auth_exceptions_handlers,
)
from src.contexts.auth.presentation.api.routes.router import router
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)

PASSWORD_RECOVERY_BODY = {"email": "john.doe@example.com"}


def _make_app(recovery_uc: PasswordRecoveryUseCase | None = None) -> FastAPI:
    app = FastAPI()
    register_auth_exceptions_handlers(app)
    app.include_router(router)

    from src.contexts.auth.application.use_cases.update_user_password_use_case import (
        UpdateUserPasswordUseCase,
    )
    from src.contexts.auth.presentation.api.compositions.use_cases_composition import (
        get_activate_account_use_case,
        get_login_use_case,
        get_password_recovery_use_case,
        get_register_user_use_case,
        get_update_user_password_use_case,
    )
    from src.shared.presentation.api.compositions.infrastructure_composition import (
        get_logger,
    )
    from src.shared.presentation.api.compositions.security_composition import (
        get_current_user,
        request_details_dependency,
    )

    app.dependency_overrides[get_register_user_use_case] = lambda: MagicMock(
        spec=RegisterUserUseCase
    )
    app.dependency_overrides[get_activate_account_use_case] = lambda: MagicMock(
        spec=ActivateAccountUseCase
    )
    app.dependency_overrides[get_login_use_case] = lambda: MagicMock(spec=LoginUseCase)
    app.dependency_overrides[get_update_user_password_use_case] = lambda: MagicMock(
        spec=UpdateUserPasswordUseCase
    )
    app.dependency_overrides[get_current_user] = lambda: TokenPayloadVO(
        user_id=uuid4(),
        role=RolesEnum.ADMIN,
        expires_in=3600,
        jti=uuid4(),
    )
    app.dependency_overrides[request_details_dependency] = lambda: {
        "request_ip": "127.0.0.1",
        "request_user_agent": "test-agent",
    }

    if recovery_uc is not None:
        app.dependency_overrides[get_password_recovery_use_case] = lambda: recovery_uc

    app.dependency_overrides[get_logger] = lambda: MagicMock()
    return app


class TestPasswordRecoveryRoute:
    """Integration tests for POST /api/auth/password-recovery."""

    @pytest.fixture
    def recovery_uc_mock(self):
        return MagicMock(spec=PasswordRecoveryUseCase)

    @pytest.fixture
    def client(self, recovery_uc_mock):
        return TestClient(
            _make_app(recovery_uc=recovery_uc_mock), raise_server_exceptions=False
        )

    # ──────────────────────── success path ──────────────────────────────

    def test_returns_200_on_success(self, client, recovery_uc_mock):
        """Should return 200 when the recovery email is sent successfully."""
        recovery_uc_mock.execute.return_value = None

        response = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        )

        assert response.status_code == status.HTTP_200_OK

    def test_success_response_contains_message(self, client, recovery_uc_mock):
        """Successful response must contain a 'message' field."""
        recovery_uc_mock.execute.return_value = None

        data = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        ).json()

        assert "message" in data

    def test_success_message_mentions_password_recovery(self, client, recovery_uc_mock):
        """Success message should confirm the email was sent."""
        recovery_uc_mock.execute.return_value = None

        data = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        ).json()

        assert (
            "password" in data["message"].lower()
            or "recovery" in data["message"].lower()
        )

    def test_use_case_execute_called_once(self, client, recovery_uc_mock):
        """Should call use case execute exactly once."""
        recovery_uc_mock.execute.return_value = None

        client.post("/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY)

        recovery_uc_mock.execute.assert_called_once()

    def test_command_contains_email_from_request(self, client, recovery_uc_mock):
        """The command passed to the use case must contain the email from the request."""
        recovery_uc_mock.execute.return_value = None

        client.post("/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY)

        command = recovery_uc_mock.execute.call_args[0][0]
        assert command.email == PASSWORD_RECOVERY_BODY["email"]

    def test_command_contains_request_ip(self, client, recovery_uc_mock):
        """The command must forward the request IP injected by the dependency."""
        recovery_uc_mock.execute.return_value = None

        client.post("/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY)

        command = recovery_uc_mock.execute.call_args[0][0]
        assert command.request_ip == "127.0.0.1"

    def test_command_contains_request_user_agent(self, client, recovery_uc_mock):
        """The command must forward the user agent injected by the dependency."""
        recovery_uc_mock.execute.return_value = None

        client.post("/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY)

        command = recovery_uc_mock.execute.call_args[0][0]
        assert command.request_user_agent == "test-agent"

    # ──────────────────────── error paths ───────────────────────────────

    def test_returns_404_when_user_not_found(self, client, recovery_uc_mock):
        """Should return 404 when UserNotFoundException is raised."""
        recovery_uc_mock.execute.side_effect = UserNotFoundException(
            "email: john.doe@example.com"
        )

        response = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_404_response_message(self, client, recovery_uc_mock):
        """404 response message should state 'User not found'."""
        recovery_uc_mock.execute.side_effect = UserNotFoundException("email")

        data = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        ).json()

        assert data["message"] == "User not found"

    def test_returns_500_on_database_connection_error(self, client, recovery_uc_mock):
        """Should return 500 when DatabaseConnectionException is raised."""
        recovery_uc_mock.execute.side_effect = DatabaseConnectionException(
            "Connection refused"
        )

        response = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_returns_500_on_unexpected_database_error(self, client, recovery_uc_mock):
        """Should return 500 when UnexpectedDatabaseException is raised."""
        recovery_uc_mock.execute.side_effect = UnexpectedDatabaseException("Unknown")

        response = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    # ─────────────── request body validation (422) ───────────────────────

    def test_returns_422_when_email_is_missing(self, client):
        """Should return 422 when the email field is missing."""
        response = client.post("/api/auth/password-recovery", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_body_is_absent(self, client):
        """Should return 422 when no request body is provided at all."""
        response = client.post("/api/auth/password-recovery")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    # ─────────────────── error response structure ─────────────────────────

    def test_error_response_has_message_and_details(self, client, recovery_uc_mock):
        """Error response must contain both 'message' and 'details' as a list."""
        recovery_uc_mock.execute.side_effect = UserNotFoundException("email")

        data = client.post(
            "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
        ).json()

        assert "message" in data
        assert "details" in data
        assert isinstance(data["details"], list)

    # ─────────────────── HTTP method restrictions ──────────────────────────

    def test_get_method_is_not_allowed(self, client):
        """GET on /api/auth/password-recovery must return 405."""
        assert (
            client.get("/api/auth/password-recovery").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_put_method_is_not_allowed(self, client):
        """PUT on /api/auth/password-recovery must return 405."""
        assert (
            client.put(
                "/api/auth/password-recovery", json=PASSWORD_RECOVERY_BODY
            ).status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_method_is_not_allowed(self, client):
        """DELETE on /api/auth/password-recovery must return 405."""
        assert (
            client.delete("/api/auth/password-recovery").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )
