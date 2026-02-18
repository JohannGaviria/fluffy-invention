"""Unit tests for ResetPasswordUseCase."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.contexts.auth.application.dto.command import ResetPasswordCommand
from src.contexts.auth.application.use_cases.reset_password_use_case import (
    ResetPasswordUseCase,
)
from src.contexts.auth.domain.exceptions.exception import (
    ActivationCodeExpiredException,
    NewPasswordEqualsCurrentException,
    UserNotFoundException,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_recovery_cache_key_vo import (
    PasswordRecoveryCacheKeyVO,
)


class TestResetPasswordUseCase:
    """Unit tests for ResetPasswordUseCase."""

    def setup_method(self):
        """Set up mock dependencies before each test."""
        self.user_repository_port = MagicMock()
        self.password_hash_service_port = MagicMock()
        self.cache_service_port = MagicMock()

        self.use_case = ResetPasswordUseCase(
            user_repository_port=self.user_repository_port,
            password_hash_service_port=self.password_hash_service_port,
            cache_service_port=self.cache_service_port,
        )

    def _make_command(
        self,
        email: str = "user@example.com",
        recovery_code: str = "ABC123",
        new_password: str = "NewPass123!",
    ) -> ResetPasswordCommand:
        """Return a ResetPasswordCommand with sensible defaults."""
        return ResetPasswordCommand(
            email=email,
            recovery_code=recovery_code,
            new_password=new_password,
        )

    def _make_user(self, email: str = "user@example.com"):
        """Return a mock user entity."""
        user = MagicMock()
        user.id = uuid4()
        user.email = EmailVO(email)
        user.password_hash = MagicMock()
        return user

    def _make_cache_value(self, recovery_code: str = "ABC123"):
        """Return a mock cache value with the given recovery code."""
        cache_value = MagicMock()
        cache_value.recovery_code = recovery_code
        return cache_value

    # ──────────────────────── happy path ────────────────────────────────

    def test_execute_succeeds_with_valid_data(self):
        """Should complete without raising when all data is valid."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = False  # new != current
        self.password_hash_service_port.hashed.return_value = MagicMock()

        self.use_case.execute(
            self._make_command(recovery_code="ABC123")
        )  # must not raise

    def test_execute_looks_up_user_by_email(self):
        """Should call find_by_email with the EmailVO from the command."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = False
        self.password_hash_service_port.hashed.return_value = MagicMock()

        self.use_case.execute(self._make_command(email="user@example.com"))

        self.user_repository_port.find_by_email.assert_called_once_with(
            EmailVO("user@example.com")
        )

    def test_execute_checks_cache_with_correct_key(self):
        """Should call cache_service_port.get with the correct recovery cache key."""
        user = self._make_user(email="user@example.com")
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = False
        self.password_hash_service_port.hashed.return_value = MagicMock()

        self.use_case.execute(self._make_command(email="user@example.com"))

        expected_key = PasswordRecoveryCacheKeyVO.from_email(
            EmailVO("user@example.com")
        )
        self.cache_service_port.get.assert_called_once_with(expected_key)

    def test_execute_hashes_new_password(self):
        """Should hash the new password before storing it."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = False
        new_hash = MagicMock()
        self.password_hash_service_port.hashed.return_value = new_hash

        self.use_case.execute(self._make_command())

        self.password_hash_service_port.hashed.assert_called_once()

    def test_execute_updates_password_in_repository(self):
        """Should call update_password with the user id and new hash."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = False
        new_hash = MagicMock()
        self.password_hash_service_port.hashed.return_value = new_hash

        self.use_case.execute(self._make_command())

        self.user_repository_port.update_password.assert_called_once_with(
            user.id, new_hash
        )

    def test_execute_deletes_recovery_code_from_cache_after_reset(self):
        """Should delete the recovery cache entry after successfully updating the password."""
        user = self._make_user(email="user@example.com")
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = False
        self.password_hash_service_port.hashed.return_value = MagicMock()

        self.use_case.execute(self._make_command(email="user@example.com"))

        expected_key = PasswordRecoveryCacheKeyVO.from_email(
            EmailVO("user@example.com")
        )
        self.cache_service_port.delete.assert_called_once_with(expected_key)

    # ──────────────────────── user not found ────────────────────────────

    def test_raises_user_not_found_when_user_does_not_exist(self):
        """Should raise UserNotFoundException when no user matches the email."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

    def test_does_not_check_cache_when_user_not_found(self):
        """Should not access the cache when the user is missing."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        self.cache_service_port.get.assert_not_called()

    def test_does_not_update_password_when_user_not_found(self):
        """Should not call update_password when user is missing."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        self.user_repository_port.update_password.assert_not_called()

    def test_does_not_delete_cache_when_user_not_found(self):
        """Should not delete the cache entry when user is missing."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        self.cache_service_port.delete.assert_not_called()

    # ──────────────────────── expired / missing recovery code ───────────

    def test_raises_activation_code_expired_when_cache_is_empty(self):
        """Should raise ActivationCodeExpiredException when no recovery code is in cache."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None  # no entry in cache

        with pytest.raises(ActivationCodeExpiredException):
            self.use_case.execute(self._make_command())

    def test_does_not_update_password_when_cache_is_empty(self):
        """Should not update password when recovery code is not in cache."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None

        with pytest.raises(ActivationCodeExpiredException):
            self.use_case.execute(self._make_command())

        self.user_repository_port.update_password.assert_not_called()

    # ──────────────────────── wrong recovery code ────────────────────────

    def test_raises_activation_code_expired_when_code_does_not_match(self):
        """Should raise ActivationCodeExpiredException when recovery code does not match."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("CORRECT")

        with pytest.raises(ActivationCodeExpiredException):
            self.use_case.execute(self._make_command(recovery_code="WRONG1"))

    def test_does_not_update_password_when_code_does_not_match(self):
        """Should not update password when the recovery code is wrong."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("CORRECT")

        with pytest.raises(ActivationCodeExpiredException):
            self.use_case.execute(self._make_command(recovery_code="WRONG1"))

        self.user_repository_port.update_password.assert_not_called()

    # ──────────────────────── new password equals current ───────────────

    def test_raises_new_password_equals_current_when_passwords_are_same(self):
        """Should raise NewPasswordEqualsCurrentException when new password matches current."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = True  # same password

        with pytest.raises(NewPasswordEqualsCurrentException):
            self.use_case.execute(self._make_command())

    def test_does_not_update_password_when_new_equals_current(self):
        """Should not call update_password when new password equals current."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = True

        with pytest.raises(NewPasswordEqualsCurrentException):
            self.use_case.execute(self._make_command())

        self.user_repository_port.update_password.assert_not_called()

    def test_does_not_delete_cache_when_new_equals_current(self):
        """Should not delete the cache entry when new password equals current."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = True

        with pytest.raises(NewPasswordEqualsCurrentException):
            self.use_case.execute(self._make_command())

        self.cache_service_port.delete.assert_not_called()

    def test_does_not_hash_new_password_when_new_equals_current(self):
        """Should not hash the new password when it equals the current one."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = True

        with pytest.raises(NewPasswordEqualsCurrentException):
            self.use_case.execute(self._make_command())

        self.password_hash_service_port.hashed.assert_not_called()

    # ──────────────────────── execution order ────────────────────────────

    def test_find_by_email_is_called_before_cache_get(self):
        """Should look up the user before checking the cache."""
        call_order = []

        def track_find(*args, **kwargs):
            call_order.append("find_by_email")
            return None

        self.user_repository_port.find_by_email.side_effect = track_find

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        assert call_order == ["find_by_email"]
        self.cache_service_port.get.assert_not_called()

    def test_cache_delete_is_called_after_update_password(self):
        """The cache entry must be deleted after update_password is called."""
        call_order = []

        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = self._make_cache_value("ABC123")
        self.password_hash_service_port.verify.return_value = False
        self.password_hash_service_port.hashed.return_value = MagicMock()

        self.user_repository_port.update_password.side_effect = (
            lambda *a, **kw: call_order.append("update_password")
        )
        self.cache_service_port.delete.side_effect = lambda *a, **kw: call_order.append(
            "cache_delete"
        )

        self.use_case.execute(self._make_command())

        assert call_order == ["update_password", "cache_delete"]
