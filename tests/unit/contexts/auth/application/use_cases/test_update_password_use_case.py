"""Unit tests for UpdateUserPasswordUseCase."""

from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.contexts.auth.application.dto.command import UpdateUserPasswordCommand
from src.contexts.auth.application.use_cases.update_user_password_use_case import (
    UpdateUserPasswordUseCase,
)
from src.contexts.auth.domain.exceptions.exception import (
    CurrentPasswordIncorrectException,
    NewPasswordEqualsCurrentException,
    UserNotFoundException,
)


class TestUpdateUserPasswordUseCase:
    """Unit tests for UpdateUserPasswordUseCase."""

    def setup_method(self):
        """Setup mock dependencies for the use case."""
        self.user_repository_port = Mock()
        self.password_service_port = Mock()
        self.password_hash_service_port = Mock()

        self.use_case = UpdateUserPasswordUseCase(
            user_repository_port=self.user_repository_port,
            password_service_port=self.password_service_port,
            password_hash_service_port=self.password_hash_service_port,
        )

    def _make_command(
        self,
        user_id=None,
        current_password="OldPassword123!",
        new_password="NewPassword456!",
    ) -> UpdateUserPasswordCommand:
        """Helper to build an UpdateUserPasswordCommand."""
        return UpdateUserPasswordCommand(
            user_id=user_id or uuid4(),
            current_password=current_password,
            new_password=new_password,
        )

    # ──────────────────────────── happy path ────────────────────────────

    def test_update_password_successfully(self):
        """Should update password successfully with valid credentials."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        # current password matches
        self.password_hash_service_port.verify.side_effect = [True, False]
        new_hash = Mock()
        self.password_hash_service_port.hashed.return_value = new_hash

        command = self._make_command(user_id=user.id)
        self.use_case.execute(command)

        self.user_repository_port.find_by_id.assert_called_once_with(command.user_id)
        self.user_repository_port.update_password.assert_called_once_with(
            user.id, new_hash
        )

    def test_update_password_calls_verify_twice(self):
        """Should call verify twice: once for current password, once to detect equality."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        self.password_hash_service_port.verify.side_effect = [True, False]
        self.password_hash_service_port.hashed.return_value = Mock()

        command = self._make_command(user_id=user.id)
        self.use_case.execute(command)

        assert self.password_hash_service_port.verify.call_count == 2

    def test_update_password_hashes_new_password(self):
        """Should hash the new password before storing it."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        self.password_hash_service_port.verify.side_effect = [True, False]
        new_hash = Mock()
        self.password_hash_service_port.hashed.return_value = new_hash

        command = self._make_command(user_id=user.id)
        self.use_case.execute(command)

        self.password_hash_service_port.hashed.assert_called_once()

    # ──────────────────────────── user not found ────────────────────────

    def test_raises_user_not_found_when_user_does_not_exist(self):
        """Should raise UserNotFoundException when user is not found by ID."""
        self.user_repository_port.find_by_id.return_value = None

        command = self._make_command()

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(command)

    def test_does_not_verify_password_when_user_not_found(self):
        """Should not verify password when user does not exist."""
        self.user_repository_port.find_by_id.return_value = None

        command = self._make_command()

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(command)

        self.password_hash_service_port.verify.assert_not_called()

    def test_user_not_found_exception_uses_id_field(self):
        """UserNotFoundException should be raised with 'id' as field."""
        self.user_repository_port.find_by_id.return_value = None

        command = self._make_command()

        with pytest.raises(UserNotFoundException) as exc_info:
            self.use_case.execute(command)

        assert exc_info.value.field == "id"

    # ──────────────────────────── wrong current password ────────────────

    def test_raises_current_password_incorrect_when_password_does_not_match(self):
        """Should raise CurrentPasswordIncorrectException when current password is wrong."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        self.password_hash_service_port.verify.return_value = False

        command = self._make_command(user_id=user.id)

        with pytest.raises(CurrentPasswordIncorrectException):
            self.use_case.execute(command)

    def test_does_not_update_password_when_current_is_incorrect(self):
        """Should not call update_password when current password is wrong."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        self.password_hash_service_port.verify.return_value = False

        command = self._make_command(user_id=user.id)

        with pytest.raises(CurrentPasswordIncorrectException):
            self.use_case.execute(command)

        self.user_repository_port.update_password.assert_not_called()

    # ──────────────────────────── same password ─────────────────────────

    def test_raises_new_password_equals_current_when_passwords_are_identical(self):
        """Should raise NewPasswordEqualsCurrentException when new == current."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        # Both calls to verify return True → current matches AND new equals current
        self.password_hash_service_port.verify.return_value = True

        command = self._make_command(user_id=user.id)

        with pytest.raises(NewPasswordEqualsCurrentException):
            self.use_case.execute(command)

    def test_does_not_update_password_when_new_equals_current(self):
        """Should not call update_password when new password equals current."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        self.password_hash_service_port.verify.return_value = True

        command = self._make_command(user_id=user.id)

        with pytest.raises(NewPasswordEqualsCurrentException):
            self.use_case.execute(command)

        self.user_repository_port.update_password.assert_not_called()

    def test_does_not_hash_new_password_when_new_equals_current(self):
        """Should not hash new password when it equals the current password."""
        user = Mock()
        user.id = uuid4()
        user.password_hash = Mock()

        self.user_repository_port.find_by_id.return_value = user
        self.password_hash_service_port.verify.return_value = True

        command = self._make_command(user_id=user.id)

        with pytest.raises(NewPasswordEqualsCurrentException):
            self.use_case.execute(command)

        self.password_hash_service_port.hashed.assert_not_called()

    # ──────────────────────── execution order ────────────────────────────

    def test_find_by_id_called_before_verify(self):
        """Should look up the user before any password verification."""
        call_order = []

        def track_find(*args, **kwargs):
            call_order.append("find_by_id")
            return None

        self.user_repository_port.find_by_id.side_effect = track_find

        command = self._make_command()

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(command)

        assert call_order == ["find_by_id"]
        self.password_hash_service_port.verify.assert_not_called()

    def test_password_not_updated_when_user_not_found(self):
        """Repository update_password must not be called when user is missing."""
        self.user_repository_port.find_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            self.use_case.execute(self._make_command())

        self.user_repository_port.update_password.assert_not_called()
