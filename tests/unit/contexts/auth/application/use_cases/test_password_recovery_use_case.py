"""Unit tests for PasswordRecoveryUseCase."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.contexts.auth.application.dto.command import PasswordRecoveryCommand
from src.contexts.auth.application.use_cases.password_recovery_use_case import (
    PasswordRecoveryUseCase,
)
from src.contexts.auth.domain.exceptions.exception import UserNotFoundException
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_recovery_cache_key_vo import (
    PasswordRecoveryCacheKeyVO,
)


class TestPasswordRecoveryUseCase:
    """Unit tests for PasswordRecoveryUseCase."""

    def setup_method(self):
        """Set up mock dependencies before each test."""
        self.user_repository_port = MagicMock()
        self.activation_code_service_port = MagicMock()
        self.cache_service_port = MagicMock()
        self.template_renderer_service_port = MagicMock()
        self.sender_notification_service_port = MagicMock()

        self.use_case = PasswordRecoveryUseCase(
            user_repository_port=self.user_repository_port,
            activation_code_service_port=self.activation_code_service_port,
            cache_service_port=self.cache_service_port,
            template_renderer_service_port=self.template_renderer_service_port,
            sender_notification_service_port=self.sender_notification_service_port,
        )

    def _make_command(
        self,
        email: str = "user@example.com",
        request_ip: str = "127.0.0.1",
        request_user_agent: str = "Mozilla/5.0",
    ) -> PasswordRecoveryCommand:
        """Return a PasswordRecoveryCommand with sensible defaults."""
        return PasswordRecoveryCommand(
            email=email,
            request_ip=request_ip,
            request_user_agent=request_user_agent,
        )

    def _make_user(self, email: str = "user@example.com"):
        """Return a mock user entity."""
        user = MagicMock()
        user.id = uuid4()
        user.email = EmailVO(email)
        user.first_name = "John"
        user.last_name = "Doe"
        return user

    # ──────────────────────── happy path ────────────────────────────────

    def test_execute_succeeds_when_user_exists(self):
        """Should complete without raising when the user is found."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html>body</html>"

        self.use_case.execute(self._make_command())  # must not raise

    def test_execute_looks_up_user_by_email(self):
        """Should call find_by_email with the EmailVO from the command."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html/>"

        command = self._make_command(email="user@example.com")
        self.use_case.execute(command)

        self.user_repository_port.find_by_email.assert_called_once_with(
            EmailVO("user@example.com")
        )

    def test_execute_generates_recovery_code(self):
        """Should call generate() on the activation code service."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "XY9876"
        self.template_renderer_service_port.render.return_value = "<html/>"

        self.use_case.execute(self._make_command())

        self.activation_code_service_port.generate.assert_called_once()

    def test_execute_stores_recovery_code_in_cache(self):
        """Should call cache_service_port.set with a CacheEntryVO."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html/>"

        self.use_case.execute(self._make_command())

        self.cache_service_port.set.assert_called_once()

    def test_execute_renders_email_template(self):
        """Should call template_renderer_service_port.render once."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html>content</html>"

        self.use_case.execute(self._make_command())

        self.template_renderer_service_port.render.assert_called_once()

    def test_execute_sends_notification_email(self):
        """Should call sender_notification_service_port.send once."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html/>"

        self.use_case.execute(self._make_command())

        self.sender_notification_service_port.send.assert_called_once()

    def test_execute_sends_email_to_user_email_address(self):
        """The notification recipient must match the user's email."""
        user = self._make_user(email="user@example.com")
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html/>"

        self.use_case.execute(self._make_command(email="user@example.com"))

        send_call_args = self.sender_notification_service_port.send.call_args[0][0]
        assert send_call_args.recipient == "user@example.com"

    # ──────────────────── existing active code handling ─────────────────

    def test_execute_deletes_existing_cache_entry_before_setting_new_one(self):
        """If an active code exists in cache, it should be deleted first."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = MagicMock()  # active code exists
        self.activation_code_service_port.generate.return_value = "NEW123"
        self.template_renderer_service_port.render.return_value = "<html/>"

        self.use_case.execute(self._make_command())

        # delete must be called before set
        expected_key = PasswordRecoveryCacheKeyVO.from_email(
            EmailVO("user@example.com")
        )
        self.cache_service_port.delete.assert_called_once_with(expected_key)
        self.cache_service_port.set.assert_called_once()

    def test_execute_does_not_delete_cache_when_no_active_code(self):
        """Should NOT call cache delete when there is no existing active code."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None  # no active code
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html/>"

        self.use_case.execute(self._make_command())

        self.cache_service_port.delete.assert_not_called()

    # ──────────────────────── user not found ────────────────────────────

    def test_execute_raises_user_not_found_when_user_does_not_exist(self):
        """Should raise UserNotFoundException when no user matches the email."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

    def test_execute_does_not_generate_code_when_user_not_found(self):
        """Should not reach the code-generation step when user is missing."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        self.activation_code_service_port.generate.assert_not_called()

    def test_execute_does_not_send_email_when_user_not_found(self):
        """Should not send any notification when user is missing."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        self.sender_notification_service_port.send.assert_not_called()

    def test_execute_does_not_write_cache_when_user_not_found(self):
        """Should not write to cache when user is missing."""
        self.user_repository_port.find_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        self.cache_service_port.set.assert_not_called()

    # ──────────────────────── email subject ─────────────────────────────

    def test_execute_sends_email_with_reset_password_subject(self):
        """The notification subject must be about password reset."""
        user = self._make_user()
        self.user_repository_port.find_by_email.return_value = user
        self.cache_service_port.get.return_value = None
        self.activation_code_service_port.generate.return_value = "ABC123"
        self.template_renderer_service_port.render.return_value = "<html/>"

        self.use_case.execute(self._make_command())

        notification = self.sender_notification_service_port.send.call_args[0][0]
        assert (
            "password" in notification.subject.lower()
            or "reset" in notification.subject.lower()
        )
