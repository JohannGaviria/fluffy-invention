"""Unit tests for CreateAdminUseCase."""

from unittest.mock import Mock

import pytest

from src.contexts.auth.application.dto.command import CreateAdminCommand
from src.contexts.auth.application.use_cases.create_admin_use_case import (
    CreateAdminUseCase,
)
from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.exceptions.exception import (
    AdminUserAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCorporateEmailException,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO


class TestCreateAdminUseCase:
    """Unit tests for CreateAdminUseCase."""

    def setup_method(self):
        """Setup mock dependencies for the use case."""
        self.user_repository_port = Mock()
        self.password_hash_service_port = Mock()
        self.password_service_port = Mock()
        self.sender_notification_service_port = Mock()
        self.template_renderer_service_port = Mock()
        self.staff_email_policy_service_port = Mock()

        self.use_case = CreateAdminUseCase(
            user_repository_port=self.user_repository_port,
            password_hash_service_port=self.password_hash_service_port,
            password_service_port=self.password_service_port,
            sender_notification_service_port=self.sender_notification_service_port,
            template_renderer_service_port=self.template_renderer_service_port,
            staff_email_policy_service_port=self.staff_email_policy_service_port,
        )

    def test_create_admin_user_successfully(self):
        """Should create admin user successfully."""
        command = CreateAdminCommand(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
        )
        self.user_repository_port.find_by_role.return_value = []
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None
        self.password_service_port.generate.return_value = Mock(value="temp_password")
        self.password_hash_service_port.hashed.return_value = "hashed_password"

        self.use_case.execute(command)

        self.user_repository_port.find_by_role.assert_called_once_with(RolesEnum.ADMIN)
        self.staff_email_policy_service_port.is_allowed.assert_called_once_with(
            EmailVO(command.email), RolesEnum.ADMIN
        )
        self.user_repository_port.find_by_email.assert_called_once_with(
            EmailVO(command.email)
        )
        self.user_repository_port.save.assert_called_once()
        self.sender_notification_service_port.send.assert_called_once()

    def test_create_admin_user_already_exists(self):
        """Should raise AdminUserAlreadyExistsException if admin user exists."""
        command = CreateAdminCommand(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
        )
        self.user_repository_port.find_by_role.return_value = [Mock()]

        with pytest.raises(AdminUserAlreadyExistsException):
            self.use_case.execute(command)

    def test_create_admin_user_invalid_email(self):
        """Should raise InvalidCorporateEmailException for invalid email."""
        command = CreateAdminCommand(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
        )
        self.user_repository_port.find_by_role.return_value = []
        self.staff_email_policy_service_port.is_allowed.return_value = False

        with pytest.raises(InvalidCorporateEmailException):
            self.use_case.execute(command)

    def test_create_admin_user_email_already_exists(self):
        """Should raise EmailAlreadyExistsException if email already exists."""
        command = CreateAdminCommand(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
        )
        self.user_repository_port.find_by_role.return_value = []
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = Mock()

        with pytest.raises(EmailAlreadyExistsException):
            self.use_case.execute(command)
