"""Unit tests for ActivateAccountUseCase."""

from unittest.mock import Mock

import pytest

from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.domain.exceptions.exception import (
    ActivationCodeExpiredException,
    InvalidActivationCodeException,
    UserNotFoundException,
)
from src.contexts.auth.domain.value_objects.activation_code_cache_key_vo import (
    ActivationCodeCacheKeyVO,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO


class TestActivateAccountUseCase:
    """Unit tests for ActivateAccountUseCase."""

    def setup_method(self):
        """Setup mock dependencies for the use case."""
        self.user_repository_port = Mock()
        self.cache_service_port = Mock()

        self.use_case = ActivateAccountUseCase(
            user_repository_port=self.user_repository_port,
            cache_service_port=self.cache_service_port,
        )

    def test_activate_account_successfully(self):
        """Should activate account successfully with valid data."""
        activation_code = "valid_code"
        email = "user@example.com"
        user = Mock()
        user.id = "user_id"
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = Mock(code=activation_code)

        self.use_case.execute(activation_code, email)

        self.user_repository_port.find_by_email.assert_called_once_with(EmailVO(email))
        self.cache_service_port.get.assert_called_once_with(
            ActivationCodeCacheKeyVO.from_user_id(user.id)
        )
        self.user_repository_port.status_update.assert_called_once_with(True, user.id)
        self.cache_service_port.delete.assert_called_once_with(
            ActivationCodeCacheKeyVO.from_user_id(user.id)
        )

    def test_activate_account_user_not_found(self):
        """Should raise UserNotFoundException if user is not found."""
        activation_code = "valid_code"
        email = "user@example.com"
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(activation_code, email)

    def test_activate_account_code_expired(self):
        """Should raise ActivationCodeExpiredException if code is expired."""
        activation_code = "valid_code"
        email = "user@example.com"
        user = Mock()
        user.id = "user_id"
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None

        with pytest.raises(ActivationCodeExpiredException):
            self.use_case.execute(activation_code, email)

    def test_activate_account_invalid_code(self):
        """Should raise InvalidActivationCodeException if code is invalid."""
        activation_code = "invalid_code"
        email = "user@example.com"
        user = Mock()
        user.id = "user_id"
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = Mock(code="valid_code")

        with pytest.raises(InvalidActivationCodeException):
            self.use_case.execute(activation_code, email)
