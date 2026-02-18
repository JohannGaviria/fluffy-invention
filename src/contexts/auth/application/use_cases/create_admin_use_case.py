"""This module contains the use case for creating an admin user."""

from src.contexts.auth.application.dto.command import CreateAdminCommand
from src.contexts.auth.domain.entities.entity import RolesEnum, UserEntity
from src.contexts.auth.domain.exceptions.exception import (
    AdminUserAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCorporateEmailException,
)
from src.contexts.auth.domain.ports.repositories.user_repository_port import (
    UserRepositoryPort,
)
from src.contexts.auth.domain.ports.services.password_hash_service_port import (
    PasswordHashServicePort,
)
from src.contexts.auth.domain.ports.services.password_service_port import (
    PasswordServicePort,
)
from src.contexts.auth.domain.ports.services.staff_email_policy_service_port import (
    StaffEmailPolicyServicePort,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.template_context_create_admin_vo import (
    TemplateContextCreateAdminVO,
)
from src.contexts.auth.domain.value_objects.template_name_create_admin_vo import (
    TemplateNameCreateAdminVO,
)
from src.shared.domain.ports.services.sender_notification_service_port import (
    SenderNotificationServicePort,
)
from src.shared.domain.ports.services.template_renderer_service_port import (
    TemplateRendererServicePort,
)
from src.shared.domain.value_objects.send_notification_vo import SendNotificationVO
from src.shared.domain.value_objects.template_renderer_vo import TemplateRendererVO


class CreateAdminUseCase:
    """Use case for creating an admin user."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        password_hash_service_port: PasswordHashServicePort,
        password_service_port: PasswordServicePort,
        sender_notification_service_port: SenderNotificationServicePort,
        template_renderer_service_port: TemplateRendererServicePort[
            TemplateContextCreateAdminVO
        ],
        staff_email_policy_service_port: StaffEmailPolicyServicePort,
    ) -> None:
        """Initialize the CreateAdminUseCase with required ports.

        Args:
            user_repository_port (UserRepositoryPort): Port for user repository operations.
            password_hash_service_port (PasswordHashServicePort): Port for password hashing.
            password_service_port (PasswordServicePort): Port for password generation.
            sender_notification_service_port (SenderNotificationServicePort): Port for sending notifications.
            template_renderer_service_port (TemplateRendererServicePort[TemplateContextCreateAdminVO]): Port for rendering templates.
            staff_email_policy_service_port (StaffEmailPolicyServicePort): Port for staff email policy checks
        """
        self.user_repository_port = user_repository_port
        self.password_hash_service_port = password_hash_service_port
        self.password_service_port = password_service_port
        self.sender_notification_service_port = sender_notification_service_port
        self.template_renderer_service_port = template_renderer_service_port
        self.staff_email_policy_service_port = staff_email_policy_service_port

    def execute(self, command: CreateAdminCommand) -> None:
        """Execute the use case to create an admin user.

        Args:
            command (CreateAdminCommand): The command containing admin user details.

        Raises:
            AdminUserAlreadyExistsException: If an admin user already exists.
            EmailAlreadyExistsException: If the email for the admin user already exists.
        """
        # Check for existing admin users
        users = self.user_repository_port.find_by_role(RolesEnum.ADMIN)
        if users:
            raise AdminUserAlreadyExistsException()

        # Staff email policy check
        if not self.staff_email_policy_service_port.is_allowed(
            EmailVO(command.email), RolesEnum.ADMIN
        ):
            raise InvalidCorporateEmailException(command.email, RolesEnum.ADMIN)

        # Check for existing user
        existing_user = self.user_repository_port.find_by_email(EmailVO(command.email))
        if existing_user:
            raise EmailAlreadyExistsException(command.email)

        # Generate temporary password and hash it
        temporary_password = self.password_service_port.generate()
        password_hash = self.password_hash_service_port.hashed(temporary_password)

        # Create and save the admin user
        entity = UserEntity.create(
            first_name=command.first_name,
            last_name=command.last_name,
            email=EmailVO(command.email),
            password_hash=password_hash,
            role=RolesEnum.ADMIN,
        )
        entity.is_active = True
        user = self.user_repository_port.save(entity)

        # Send notification with account details
        template_name = TemplateNameCreateAdminVO.create()
        context = TemplateContextCreateAdminVO(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            temporary_password=temporary_password.value,
        )

        # Render template and send notification
        template_renderer = TemplateRendererVO(template_name, context)
        message = self.template_renderer_service_port.render(template_renderer)

        # Send notification
        notification = SendNotificationVO(
            recipient=user.email.value,
            subject="Your Admin Account Has Been Created",
            body=message,
        )
        self.sender_notification_service_port.send(notification)
