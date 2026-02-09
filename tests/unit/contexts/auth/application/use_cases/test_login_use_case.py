"""Unit tests for LoginUseCase."""

from unittest.mock import Mock

import pytest

from src.contexts.auth.application.dto.command import LoginCommand
from src.contexts.auth.application.dto.response import AccessTokenResponse
from src.contexts.auth.application.use_cases.login_use_case import LoginUseCase
from src.contexts.auth.domain.exceptions.exception import (
    AccountTemporarilyBlockedException,
    InvalidCredentialsException,
    UserInactiveException,
)


class TestLoginUseCase:
    """Unit tests for LoginUseCase."""

    def setup_method(self):
        """Setup mock dependencies for the use case."""
        self.user_repository_port = Mock()
        self.password_hash_service_port = Mock()
        self.token_service_port = Mock()
        self.cache_service_port = Mock()

        self.use_case = LoginUseCase(
            user_repository_port=self.user_repository_port,
            password_hash_service_port=self.password_hash_service_port,
            token_service_port=self.token_service_port,
            cache_service_port=self.cache_service_port,
            expire_in=3600,
            attempts_limit=5,
            waiting_time=300,
        )

    def test_login_user_successfully(self):
        """Should login user successfully and return access token."""
        command = LoginCommand(email="user@example.com", password="PassSecure!23")

        self.cache_service_port.get.return_value = None

        user = Mock()
        user.is_active = True
        user.password_hash = "hashed_password"
        self.user_repository_port.find_by_email.return_value = user
        self.password_hash_service_port.verify.return_value = True
        self.token_service_port.access.return_value = Mock(
            access_token="token123",
            token_type="Bearer",
            expires_at=1234567890,
            expires_in=3600,
        )

        response = self.use_case.execute(command)

        assert isinstance(response, AccessTokenResponse)
        assert response.access_token == "token123"
        assert response.token_type == "Bearer"
        assert response.expires_at == 1234567890
        assert response.expires_in == 3600

        self.cache_service_port.delete.assert_called_once()

    def test_login_user_account_blocked(self):
        """Should raise AccountTemporarilyBlockedException if account is blocked."""
        command = LoginCommand(email="user@example.com", password="PassSecure!23")
        self.cache_service_port.get.return_value = Mock(attempt=5)

        with pytest.raises(AccountTemporarilyBlockedException):
            self.use_case.execute(command)

    def test_login_user_invalid_credentials(self):
        """Should raise InvalidCredentialsException for invalid credentials."""
        command = LoginCommand(email="user@example.com", password="wrongpassword")

        self.cache_service_port.get.return_value = None

        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(InvalidCredentialsException):
            self.use_case.execute(command)

    def test_login_user_inactive_account(self):
        """Should raise UserInactiveException if user account is inactive."""
        command = LoginCommand(email="user@example.com", password="PassSecure!23")

        self.cache_service_port.get.return_value = None

        user = Mock()
        user.is_active = False
        self.user_repository_port.find_by_email.return_value = user

        with pytest.raises(UserInactiveException):
            self.use_case.execute(command)

    def test_login_user_exceeds_attempts_limit(self):
        """Should raise AccountTemporarilyBlockedException when login attempts exceed limit."""
        command = LoginCommand(email="user@example.com", password="wrongpassword")

        attempts_vo = Mock(attempt=5)
        self.cache_service_port.get.return_value = attempts_vo

        with pytest.raises(AccountTemporarilyBlockedException):
            self.use_case.execute(command)

    def test_login_user_invalid_password(self):
        """Should raise InvalidCredentialsException for invalid password."""
        command = LoginCommand(email="user@example.com", password="Wrongpassword!23")

        self.cache_service_port.get.return_value = None

        user = Mock()
        user.is_active = True
        user.password_hash = "hashed_password"
        self.user_repository_port.find_by_email.return_value = user
        self.password_hash_service_port.verify.return_value = False

        with pytest.raises(InvalidCredentialsException):
            self.use_case.execute(command)
