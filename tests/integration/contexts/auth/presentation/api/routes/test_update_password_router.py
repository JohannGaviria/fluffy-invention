"""Integration tests for PUT /api/auth/password."""

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
from src.contexts.auth.application.use_cases.update_user_password_use_case import (
    UpdateUserPasswordUseCase,
)
from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.exceptions.exception import (
    CurrentPasswordIncorrectException,
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

UPDATE_PASSWORD_BODY = {
    "current_password": "OldPassword123!",
    "new_password": "NewPassword456!",
}

_CURRENT_USER = TokenPayloadVO(
    user_id=uuid4(),
    role=RolesEnum.PATIENT,
    expires_in=3600,
    jti=uuid4(),
)


def _make_app(update_uc: UpdateUserPasswordUseCase | None = None) -> FastAPI:
    app = FastAPI()
    register_auth_exceptions_handlers(app)
    app.include_router(router)

    from src.contexts.auth.presentation.api.compositions.use_cases_composition import (
        get_activate_account_use_case,
        get_login_use_case,
        get_register_user_use_case,
        get_update_user_password_use_case,
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
    app.dependency_overrides[get_login_use_case] = lambda: MagicMock(spec=LoginUseCase)
    app.dependency_overrides[get_current_user] = lambda: _CURRENT_USER

    if update_uc is not None:
        app.dependency_overrides[get_update_user_password_use_case] = lambda: update_uc

    app.dependency_overrides[get_logger] = lambda: MagicMock()
    return app


class TestUpdatePasswordRoute:
    """Integration tests for PUT /api/auth/password."""

    @pytest.fixture
    def update_uc_mock(self):
        return MagicMock(spec=UpdateUserPasswordUseCase)

    @pytest.fixture
    def client(self, update_uc_mock):
        return TestClient(
            _make_app(update_uc=update_uc_mock), raise_server_exceptions=False
        )

    # ──────────────────────── success path ──────────────────────────────

    def test_update_password_returns_200_on_success(self, client, update_uc_mock):
        """Should return 200 when password is updated successfully."""
        update_uc_mock.execute.return_value = None

        response = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        assert response.status_code == status.HTTP_200_OK

    def test_update_password_response_contains_message(self, client, update_uc_mock):
        """Successful response must contain a 'message' field."""
        update_uc_mock.execute.return_value = None

        data = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY).json()

        assert "message" in data

    def test_update_password_success_message_text(self, client, update_uc_mock):
        """Success message should confirm the password was updated."""
        update_uc_mock.execute.return_value = None

        data = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY).json()

        assert "password" in data["message"].lower()

    def test_update_password_calls_use_case_once(self, client, update_uc_mock):
        """Should invoke the use case execute method exactly once."""
        update_uc_mock.execute.return_value = None

        client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        update_uc_mock.execute.assert_called_once()

    def test_update_password_passes_current_user_id_to_command(
        self, client, update_uc_mock
    ):
        """Should forward the authenticated user_id from JWT to the command."""
        update_uc_mock.execute.return_value = None

        client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        command = update_uc_mock.execute.call_args[0][0]
        assert command.user_id == _CURRENT_USER.user_id

    def test_update_password_passes_current_password_to_command(
        self, client, update_uc_mock
    ):
        """Should forward the current_password from the request body to the command."""
        update_uc_mock.execute.return_value = None

        client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        command = update_uc_mock.execute.call_args[0][0]
        assert command.current_password == UPDATE_PASSWORD_BODY["current_password"]

    def test_update_password_passes_new_password_to_command(
        self, client, update_uc_mock
    ):
        """Should forward the new_password from the request body to the command."""
        update_uc_mock.execute.return_value = None

        client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        command = update_uc_mock.execute.call_args[0][0]
        assert command.new_password == UPDATE_PASSWORD_BODY["new_password"]

    # ──────────────── new password equals current (422) ─────────────────

    def test_update_password_returns_422_when_new_equals_current(
        self, client, update_uc_mock
    ):
        """Should return 422 when the new password equals the current password."""
        update_uc_mock.execute.side_effect = NewPasswordEqualsCurrentException()

        response = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_password_error_message_new_equals_current(
        self, client, update_uc_mock
    ):
        """Response message should indicate new and current passwords are the same."""
        update_uc_mock.execute.side_effect = NewPasswordEqualsCurrentException()

        data = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY).json()

        assert "message" in data
        assert (
            data["message"] == "The new password cannot be the same as the current one"
        )

    # ─────────────── current password incorrect (403) ───────────────────

    def test_update_password_returns_403_when_current_password_is_wrong(
        self, client, update_uc_mock
    ):
        """Should return 403 when the current password does not match."""
        update_uc_mock.execute.side_effect = CurrentPasswordIncorrectException()

        response = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_password_error_message_current_password_incorrect(
        self, client, update_uc_mock
    ):
        """Response message should describe the current password mismatch."""
        update_uc_mock.execute.side_effect = CurrentPasswordIncorrectException()

        data = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY).json()

        assert "message" in data
        assert (
            "current password" in data["message"].lower()
            or "does not match" in data["message"].lower()
        )

    # ─────────────────── user not found (404) ───────────────────────────

    def test_update_password_returns_404_when_user_not_found(
        self, client, update_uc_mock
    ):
        """Should return 404 when the user is not found."""
        update_uc_mock.execute.side_effect = UserNotFoundException("id")

        response = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_password_error_message_user_not_found(self, client, update_uc_mock):
        """Response message should indicate user was not found."""
        update_uc_mock.execute.side_effect = UserNotFoundException("id")

        data = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY).json()

        assert data["message"] == "User not found"

    # ─────────────────── database errors (500) ──────────────────────────

    def test_update_password_returns_500_on_database_connection_error(
        self, client, update_uc_mock
    ):
        """Should return 500 when a database connection error occurs."""
        update_uc_mock.execute.side_effect = DatabaseConnectionException(
            "Connection refused"
        )

        response = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_update_password_returns_500_on_unexpected_database_error(
        self, client, update_uc_mock
    ):
        """Should return 500 when an unexpected database error occurs."""
        update_uc_mock.execute.side_effect = UnexpectedDatabaseException("Unknown")

        response = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    # ────────────── request body validation (422) ───────────────────────

    def test_update_password_returns_422_when_current_password_is_missing(self, client):
        """Should return 422 when current_password field is missing."""
        response = client.put(
            "/api/auth/password", json={"new_password": "NewPassword456!"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_password_returns_422_when_new_password_is_missing(self, client):
        """Should return 422 when new_password field is missing."""
        response = client.put(
            "/api/auth/password", json={"current_password": "OldPassword123!"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_password_returns_422_when_body_is_empty(self, client):
        """Should return 422 when the request body is empty."""
        response = client.put("/api/auth/password", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_put_without_body_returns_422(self, client):
        """PUT without a body must return 422."""
        assert (
            client.put("/api/auth/password").status_code
            == status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    # ─────────────── error response structure ───────────────────────────

    def test_error_response_has_message_and_details(self, client, update_uc_mock):
        """Error response must contain 'message' and 'details' as a list."""
        update_uc_mock.execute.side_effect = UserNotFoundException("id")

        data = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY).json()

        assert "message" in data
        assert "details" in data
        assert isinstance(data["details"], list)

    def test_error_details_is_non_empty_list(self, client, update_uc_mock):
        """Error details list must contain at least one item."""
        update_uc_mock.execute.side_effect = CurrentPasswordIncorrectException()

        data = client.put("/api/auth/password", json=UPDATE_PASSWORD_BODY).json()

        assert len(data["details"]) > 0

    # ────────────────── HTTP method restrictions ─────────────────────────

    def test_get_method_is_not_allowed(self, client):
        """GET on /api/auth/password must return 405."""
        assert (
            client.get("/api/auth/password").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_post_method_is_not_allowed(self, client):
        """POST on /api/auth/password must return 405."""
        assert (
            client.post("/api/auth/password", json=UPDATE_PASSWORD_BODY).status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_method_is_not_allowed(self, client):
        """DELETE on /api/auth/password must return 405."""
        assert (
            client.delete("/api/auth/password").status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )
