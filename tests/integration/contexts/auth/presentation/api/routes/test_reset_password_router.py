"""Integration tests for POST /api/auth/reset-password."""

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
from src.contexts.auth.application.use_cases.reset_password_use_case import (
    ResetPasswordUseCase,
)
from src.contexts.auth.application.use_cases.update_user_password_use_case import (
    UpdateUserPasswordUseCase,
)
from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.exceptions.exception import (
    ActivationCodeExpiredException,
    NewPasswordEqualsCurrentException,
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

RESET_PASSWORD_BODY = {
    "email": "user@example.com",
    "recovery_code": "ABC123",
    "new_password": "NewPass123!",
}


def _make_app(reset_uc: ResetPasswordUseCase | None = None) -> FastAPI:
    app = FastAPI()
    register_auth_exceptions_handlers(app)
    app.include_router(router)

    from src.contexts.auth.presentation.api.compositions.use_cases_composition import (
        get_activate_account_use_case,
        get_login_use_case,
        get_password_recovery_use_case,
        get_register_user_use_case,
        get_reset_password_use_case,
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
    app.dependency_overrides[get_password_recovery_use_case] = lambda: MagicMock(
        spec=PasswordRecoveryUseCase
    )
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

    if reset_uc is not None:
        app.dependency_overrides[get_reset_password_use_case] = lambda: reset_uc

    app.dependency_overrides[get_logger] = lambda: MagicMock()
    return app


class TestResetPasswordRoute:
    """Integration tests for POST /api/auth/reset-password."""

    @pytest.fixture
    def reset_uc_mock(self):
        return MagicMock(spec=ResetPasswordUseCase)

    @pytest.fixture
    def client(self, reset_uc_mock):
        return TestClient(
            _make_app(reset_uc=reset_uc_mock), raise_server_exceptions=False
        )

    # ──────────────────────── success path ──────────────────────────────

    def test_returns_200_on_success(self, client, reset_uc_mock):
        """Should return 200 when the password is reset successfully."""
        reset_uc_mock.execute.return_value = None

        response = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        assert response.status_code == status.HTTP_200_OK

    def test_success_response_contains_message(self, client, reset_uc_mock):
        """Successful response must contain a 'message' field."""
        reset_uc_mock.execute.return_value = None

        data = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY).json()

        assert "message" in data

    def test_success_message_mentions_password_reset(self, client, reset_uc_mock):
        """Success message should confirm the password was reset."""
        reset_uc_mock.execute.return_value = None

        data = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY).json()

        assert (
            "password" in data["message"].lower() or "reset" in data["message"].lower()
        )

    def test_use_case_execute_called_once(self, client, reset_uc_mock):
        """Should call use case execute exactly once."""
        reset_uc_mock.execute.return_value = None

        client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        reset_uc_mock.execute.assert_called_once()

    def test_command_contains_email_from_request(self, client, reset_uc_mock):
        """The command passed to the use case must contain the email from the request."""
        reset_uc_mock.execute.return_value = None

        client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        command = reset_uc_mock.execute.call_args[0][0]
        assert command.email == RESET_PASSWORD_BODY["email"]

    def test_command_contains_recovery_code_from_request(self, client, reset_uc_mock):
        """The command must contain the recovery_code from the request body."""
        reset_uc_mock.execute.return_value = None

        client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        command = reset_uc_mock.execute.call_args[0][0]
        assert command.recovery_code == RESET_PASSWORD_BODY["recovery_code"]

    def test_command_contains_new_password_from_request(self, client, reset_uc_mock):
        """The command must contain the new_password from the request body."""
        reset_uc_mock.execute.return_value = None

        client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        command = reset_uc_mock.execute.call_args[0][0]
        assert command.new_password == RESET_PASSWORD_BODY["new_password"]

    # ──────────────────────── error paths ───────────────────────────────

    def test_returns_404_when_user_not_found(self, client, reset_uc_mock):
        """Should return 404 when UserNotFoundException is raised."""
        reset_uc_mock.execute.side_effect = UserNotFoundException(
            "email: user@example.com"
        )

        response = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_404_response_message(self, client, reset_uc_mock):
        """404 response message should state 'User not found'."""
        reset_uc_mock.execute.side_effect = UserNotFoundException("email")

        data = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY).json()

        assert data["message"] == "User not found"

    def test_returns_400_when_activation_code_expired(self, client, reset_uc_mock):
        """Should return 400 when ActivationCodeExpiredException is raised."""
        reset_uc_mock.execute.side_effect = ActivationCodeExpiredException()

        response = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_400_response_message_for_expired_code(self, client, reset_uc_mock):
        """400 response message should indicate the activation code has expired."""
        reset_uc_mock.execute.side_effect = ActivationCodeExpiredException()

        data = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY).json()

        assert (
            "expired" in data["message"].lower()
            or "activation" in data["message"].lower()
        )

    def test_returns_422_when_new_password_equals_current(self, client, reset_uc_mock):
        """Should return 422 when NewPasswordEqualsCurrentException is raised."""
        reset_uc_mock.execute.side_effect = NewPasswordEqualsCurrentException()

        response = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_422_response_message_for_same_password(self, client, reset_uc_mock):
        """422 response message should state new and current passwords are the same."""
        reset_uc_mock.execute.side_effect = NewPasswordEqualsCurrentException()

        data = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY).json()

        assert (
            data["message"] == "The new password cannot be the same as the current one"
        )

    def test_returns_500_on_database_connection_error(self, client, reset_uc_mock):
        """Should return 500 when DatabaseConnectionException is raised."""
        reset_uc_mock.execute.side_effect = DatabaseConnectionException(
            "Connection refused"
        )

        response = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_returns_500_on_unexpected_database_error(self, client, reset_uc_mock):
        """Should return 500 when UnexpectedDatabaseException is raised."""
        reset_uc_mock.execute.side_effect = UnexpectedDatabaseException("Unknown")

        response = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    # ─────────────── request body validation (422) ───────────────────────

    def test_returns_422_when_email_is_missing(self, client):
        """Should return 422 when the email field is missing."""
        body = {k: v for k, v in RESET_PASSWORD_BODY.items() if k != "email"}

        response = client.put("/api/auth/reset-password", json=body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_recovery_code_is_missing(self, client):
        """Should return 422 when the recovery_code field is missing."""
        body = {k: v for k, v in RESET_PASSWORD_BODY.items() if k != "recovery_code"}

        response = client.put("/api/auth/reset-password", json=body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_new_password_is_missing(self, client):
        """Should return 422 when the new_password field is missing."""
        body = {k: v for k, v in RESET_PASSWORD_BODY.items() if k != "new_password"}

        response = client.put("/api/auth/reset-password", json=body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_body_is_empty(self, client):
        """Should return 422 when the request body is empty."""
        response = client.put("/api/auth/reset-password", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_body_is_absent(self, client):
        """Should return 422 when no request body is provided at all."""
        response = client.put("/api/auth/reset-password")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    # ─────────────────── error response structure ─────────────────────────

    def test_error_response_has_message_and_details(self, client, reset_uc_mock):
        """Error response must contain both 'message' and 'details' as a list."""
        reset_uc_mock.execute.side_effect = UserNotFoundException("email")

        data = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY).json()

        assert "message" in data
        assert "details" in data
        assert isinstance(data["details"], list)

    def test_error_details_is_non_empty_list(self, client, reset_uc_mock):
        """Error details list must contain at least one item."""
        reset_uc_mock.execute.side_effect = ActivationCodeExpiredException()

        data = client.put("/api/auth/reset-password", json=RESET_PASSWORD_BODY).json()

        assert len(data["details"]) > 0

    # ─────────────────── HTTP method restrictions ──────────────────────────

    def test_get_method_is_not_allowed(self, client):
        """GET on /api/auth/reset-password must return 405."""
        assert (
            client.get("/api/auth/reset-password").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_put_method_is_not_allowed(self, client):
        """POST on /api/auth/reset-password must return 405."""
        assert (
            client.post(
                "/api/auth/reset-password", json=RESET_PASSWORD_BODY
            ).status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_method_is_not_allowed(self, client):
        """DELETE on /api/auth/reset-password must return 405."""
        assert (
            client.delete("/api/auth/reset-password").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )
