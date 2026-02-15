"""Integration tests for create_first_admin_cli (CLI presentation layer)."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from src.contexts.auth.domain.exceptions.exception import (
    AdminUserAlreadyExistsException,
    EmailAlreadyExistsException,
)

_CLI_MODULE = "src.contexts.auth.presentation.cli.create_first_admin_cli"


def _patch_settings(**overrides):
    """Return a MagicMock that behaves like the settings object."""
    defaults = {
        "LOG_LEVEL": "DEBUG",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": 587,
        "USER_EMAIL": "sender@example.com",
        "USER_PASSWORD": "s3cr3t",
        "TEMPLATE_PATH": "src/shared/infrastructure/notifications/templates/",
        "ALLOWED_STAFF_EMAIL_DOMAINS": "example.com,healthcare.org",
        "ALLOWED_STAFF_ROLES": "admin,doctor,receptionist",
        "INITIAL_ADMIN_FIRST_NAME": "John",
        "INITIAL_ADMIN_LAST_NAME": "Doe",
        "INITIAL_ADMIN_EMAIL": "john.doe@example.com",
    }

    defaults.update(overrides)
    mock = MagicMock()
    for k, v in defaults.items():
        setattr(mock, k, v)
    return mock


def _run(**settings_overrides):
    """Execute create_initial_admin() with all infrastructure dependencies mocked.

    Returns a dict with the mocks so callers can assert on them.
    """
    import contextlib

    import src.contexts.auth.presentation.cli.create_first_admin_cli as cli_mod

    use_case_instance = MagicMock()
    use_case_cls = MagicMock(return_value=use_case_instance)
    logger_mock = MagicMock()

    patches = [
        patch(f"{_CLI_MODULE}.settings", _patch_settings(**settings_overrides)),
        patch(f"{_CLI_MODULE}.SQLModelRepositoryAdapter"),
        patch(f"{_CLI_MODULE}.PasswordHashServiceAdapter"),
        patch(f"{_CLI_MODULE}.PasswordServiceAdapter"),
        patch(f"{_CLI_MODULE}.SenderNotificationServiceAdapter"),
        patch(f"{_CLI_MODULE}.TemplateRendererServiceAdapter"),
        patch(f"{_CLI_MODULE}.StaffEmailPolicyServiceAdapter"),
        patch(f"{_CLI_MODULE}.CreateAdminUseCase", use_case_cls),
        patch(f"{_CLI_MODULE}.get_session", return_value=iter([MagicMock()])),
        patch(f"{_CLI_MODULE}.get_logger", return_value=logger_mock),
        patch(f"{_CLI_MODULE}.logger", logger_mock),
    ]

    with contextlib.ExitStack() as stack:
        applied = [stack.enter_context(p) for p in patches]
        cli_mod.create_initial_admin()

    return {
        "use_case_instance": use_case_instance,
        "use_case_cls": use_case_cls,
        "logger": logger_mock,
        "SenderNotificationServiceAdapter": applied[4],
        "StaffEmailPolicyServiceAdapter": applied[6],
        "SQLModelRepositoryAdapter": applied[1],
        "PasswordHashServiceAdapter": applied[2],
        "PasswordServiceAdapter": applied[3],
        "TemplateRendererServiceAdapter": applied[5],
    }


def _run_raising(exc):
    """Run create_initial_admin() configured so that execute() raises *exc*."""
    import contextlib

    import src.contexts.auth.presentation.cli.create_first_admin_cli as cli_mod

    use_case_instance = MagicMock()
    use_case_instance.execute.side_effect = exc
    logger_mock = MagicMock()

    patches = [
        patch(f"{_CLI_MODULE}.settings", _patch_settings()),
        patch(f"{_CLI_MODULE}.SQLModelRepositoryAdapter"),
        patch(f"{_CLI_MODULE}.PasswordHashServiceAdapter"),
        patch(f"{_CLI_MODULE}.PasswordServiceAdapter"),
        patch(f"{_CLI_MODULE}.SenderNotificationServiceAdapter"),
        patch(f"{_CLI_MODULE}.TemplateRendererServiceAdapter"),
        patch(f"{_CLI_MODULE}.StaffEmailPolicyServiceAdapter"),
        patch(f"{_CLI_MODULE}.CreateAdminUseCase", return_value=use_case_instance),
        patch(f"{_CLI_MODULE}.get_session", return_value=iter([MagicMock()])),
        patch(f"{_CLI_MODULE}.get_logger", return_value=logger_mock),
        patch(f"{_CLI_MODULE}.logger", logger_mock),
    ]

    with contextlib.ExitStack() as stack:
        for p in patches:
            stack.enter_context(p)
        cli_mod.create_initial_admin()


class TestCreateInitialAdminSuccess:
    """Tests for the successful execution of create_initial_admin()."""

    def test_use_case_execute_is_called_once(self):
        """execute() must be called exactly once."""
        mocks = _run()
        mocks["use_case_instance"].execute.assert_called_once()

    def test_logs_success_message(self):
        """Should log the success info message after admin creation."""
        mocks = _run()
        mocks["logger"].info.assert_called_with("Initial admin created successfully.")

    def test_command_first_name_matches_settings(self):
        """CreateAdminCommand.first_name must equal INITIAL_ADMIN_FIRST_NAME."""
        mocks = _run(INITIAL_ADMIN_FIRST_NAME="Alice")
        command = mocks["use_case_instance"].execute.call_args[0][0]
        assert command.first_name == "Alice"

    def test_command_last_name_matches_settings(self):
        """CreateAdminCommand.last_name must equal INITIAL_ADMIN_LAST_NAME."""
        mocks = _run(INITIAL_ADMIN_LAST_NAME="Wonder")
        command = mocks["use_case_instance"].execute.call_args[0][0]
        assert command.last_name == "Wonder"

    def test_command_email_matches_settings(self):
        """CreateAdminCommand.email must equal INITIAL_ADMIN_EMAIL."""
        mocks = _run(INITIAL_ADMIN_EMAIL="alice.wonder@example.com")
        command = mocks["use_case_instance"].execute.call_args[0][0]
        assert command.email == "alice.wonder@example.com"


class TestCreateInitialAdminInfrastructureWiring:
    """Verify every infrastructure adapter is instantiated exactly once."""

    def test_user_repository_is_instantiated(self):
        """SQLModelRepositoryAdapter must be instantiated once."""
        mocks = _run()
        mocks["SQLModelRepositoryAdapter"].assert_called_once()

    def test_password_hash_service_is_instantiated(self):
        """PasswordHashServiceAdapter must be instantiated once."""
        mocks = _run()
        mocks["PasswordHashServiceAdapter"].assert_called_once()

    def test_password_service_is_instantiated(self):
        """PasswordServiceAdapter must be instantiated once."""
        mocks = _run()
        mocks["PasswordServiceAdapter"].assert_called_once()

    def test_template_renderer_service_is_instantiated(self):
        """TemplateRendererServiceAdapter must be instantiated once."""
        mocks = _run()
        mocks["TemplateRendererServiceAdapter"].assert_called_once()

    def test_create_admin_use_case_is_instantiated_once(self):
        """CreateAdminUseCase must be instantiated once."""
        mocks = _run()
        mocks["use_case_cls"].assert_called_once()

    def test_sender_notification_service_receives_smtp_settings(self):
        """SenderNotificationServiceAdapter must receive the SMTP config values."""
        mocks = _run(
            SMTP_SERVER="mail.corp.com",
            SMTP_PORT=465,
            USER_EMAIL="admin@corp.com",
            USER_PASSWORD="pwd123",
        )
        mocks["SenderNotificationServiceAdapter"].assert_called_once_with(
            "mail.corp.com",
            465,
            "admin@corp.com",
            "pwd123",
            mocks["logger"],
        )

    def test_staff_email_policy_service_receives_domain_and_role_settings(self):
        """StaffEmailPolicyServiceAdapter must receive the allowed domain/role config."""
        mocks = _run(
            ALLOWED_STAFF_EMAIL_DOMAINS="corp.com",
            ALLOWED_STAFF_ROLES="admin",
        )
        mocks["StaffEmailPolicyServiceAdapter"].assert_called_once_with(
            "corp.com", "admin"
        )


class TestCreateInitialAdminExceptionPropagation:
    """Verify that exceptions from the use-case propagate out of create_initial_admin()."""

    def test_propagates_admin_already_exists_exception(self):
        """AdminUserAlreadyExistsException must propagate unchanged."""
        with pytest.raises(AdminUserAlreadyExistsException):
            _run_raising(AdminUserAlreadyExistsException())

    def test_propagates_email_already_exists_exception(self):
        """EmailAlreadyExistsException must propagate unchanged."""
        with pytest.raises(EmailAlreadyExistsException):
            _run_raising(EmailAlreadyExistsException("john.doe@example.com"))

    def test_propagates_generic_exception(self):
        """Any unexpected RuntimeError must propagate unchanged."""
        with pytest.raises(RuntimeError):
            _run_raising(RuntimeError("DB unreachable"))


class TestCliEntrypointExitCodes:
    """Simulate the __main__ try/except block and verify exit codes and log calls."""

    def _simulate_main(self, side_effect, logger_mock):
        """Reproduce the exact try/except/else structure from create_first_admin_cli and return the captured SystemExit."""
        import src.contexts.auth.presentation.cli.create_first_admin_cli as cli_mod

        with (
            patch(f"{_CLI_MODULE}.create_initial_admin", side_effect=side_effect),
            patch(f"{_CLI_MODULE}.logger", logger_mock),
        ):
            with pytest.raises(SystemExit) as exc_info:
                try:
                    cli_mod.create_initial_admin()
                except AdminUserAlreadyExistsException:
                    logger_mock.info("Admin user already exists. Skipping bootstrap.")
                    sys.exit(0)
                except EmailAlreadyExistsException:
                    logger_mock.info("Admin email already exists. Skipping bootstrap.")
                    sys.exit(0)
                except Exception as e:
                    logger_mock.error("Failed to create initial admin", error=str(e))
                    sys.exit(1)
                else:
                    sys.exit(0)
        return exc_info.value

    def test_exits_0_on_success(self):
        """Should exit 0 when create_initial_admin completes without errors."""
        exc = self._simulate_main(side_effect=None, logger_mock=MagicMock())
        assert exc.code == 0

    def test_exits_0_when_admin_already_exists(self):
        """Should exit 0 and skip when AdminUserAlreadyExistsException is raised."""
        logger_mock = MagicMock()
        exc = self._simulate_main(
            side_effect=AdminUserAlreadyExistsException(), logger_mock=logger_mock
        )
        assert exc.code == 0
        logger_mock.info.assert_called_with(
            "Admin user already exists. Skipping bootstrap."
        )

    def test_exits_0_when_email_already_exists(self):
        """Should exit 0 and skip when EmailAlreadyExistsException is raised."""
        logger_mock = MagicMock()
        exc = self._simulate_main(
            side_effect=EmailAlreadyExistsException("john@example.com"),
            logger_mock=logger_mock,
        )
        assert exc.code == 0
        logger_mock.info.assert_called_with(
            "Admin email already exists. Skipping bootstrap."
        )

    def test_exits_1_on_unexpected_exception(self):
        """Should exit 1 when an unexpected exception is raised."""
        exc = self._simulate_main(
            side_effect=RuntimeError("Something went wrong"), logger_mock=MagicMock()
        )
        assert exc.code == 1

    def test_logs_error_message_on_unexpected_exception(self):
        """Should log the error detail when a generic exception is raised."""
        logger_mock = MagicMock()
        self._simulate_main(
            side_effect=RuntimeError("DB unreachable"), logger_mock=logger_mock
        )
        logger_mock.error.assert_called_once_with(
            "Failed to create initial admin", error="DB unreachable"
        )

    def test_does_not_log_error_when_admin_already_exists(self):
        """logger.error must NOT be called for AdminUserAlreadyExistsException."""
        logger_mock = MagicMock()
        self._simulate_main(
            side_effect=AdminUserAlreadyExistsException(), logger_mock=logger_mock
        )
        logger_mock.error.assert_not_called()

    def test_does_not_log_error_when_email_already_exists(self):
        """logger.error must NOT be called for EmailAlreadyExistsException."""
        logger_mock = MagicMock()
        self._simulate_main(
            side_effect=EmailAlreadyExistsException("admin@example.com"),
            logger_mock=logger_mock,
        )
        logger_mock.error.assert_not_called()
