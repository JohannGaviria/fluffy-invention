"""This module contains a CLI script to create the initial admin user."""

import sys

from src.config import settings
from src.contexts.auth.application.dto.command import CreateAdminCommand
from src.contexts.auth.application.use_cases.create_admin_use_case import (
    CreateAdminUseCase,
)
from src.contexts.auth.domain.exceptions.exception import (
    AdminUserAlreadyExistsException,
    EmailAlreadyExistsException,
)
from src.contexts.auth.domain.value_objects.template_context_create_admin_vo import (
    TemplateContextCreateAdminVO,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_user_repository_adapter import (
    SQLModelRepositoryAdapter,
)
from src.contexts.auth.infrastructure.policies.staff_email_policy_service_adapter import (
    StaffEmailPolicyServiceAdapter,
)
from src.contexts.auth.infrastructure.security.password_hash_service_adapter import (
    PasswordHashServiceAdapter,
)
from src.contexts.auth.infrastructure.security.password_service_adapter import (
    PasswordServiceAdapter,
)
from src.shared.infrastructure.db.database import get_session
from src.shared.infrastructure.logging.logger import get_logger
from src.shared.infrastructure.notifications.sender_notification_service_adapter import (
    SenderNotificationServiceAdapter,
)
from src.shared.infrastructure.notifications.template_renderer_service_adapter import (
    TemplateRendererServiceAdapter,
)

logger = get_logger(settings.LOG_LEVEL)


def create_initial_admin() -> None:
    """Create the initial admin user based on configuration settings.

    Raises:
        AdminUserAlreadyExistsException: If an admin user already exists.
        EmailAlreadyExistsException: If the email for the admin user already exists.
    """
    # Initialize services and repositories
    user_repository = SQLModelRepositoryAdapter(next(get_session()), logger)
    password_hash_service = PasswordHashServiceAdapter()
    password_service = PasswordServiceAdapter()
    sender_notification_service = SenderNotificationServiceAdapter(
        settings.SMTP_SERVER,
        settings.SMTP_PORT,
        settings.USER_EMAIL,
        settings.USER_PASSWORD,
        logger,
    )
    template_renderer_service = TemplateRendererServiceAdapter(
        settings.TEMPLATE_PATH, TemplateContextCreateAdminVO
    )
    staff_email_policy_service = StaffEmailPolicyServiceAdapter(
        settings.ALLOWED_STAFF_EMAIL_DOMAINS, settings.ALLOWED_STAFF_ROLES
    )

    # Create the use case and execute it
    use_case = CreateAdminUseCase(
        user_repository,
        password_hash_service,
        password_service,
        sender_notification_service,
        template_renderer_service,
        staff_email_policy_service,
    )
    command = CreateAdminCommand(
        settings.INITIAL_ADMIN_FIRST_NAME,
        settings.INITIAL_ADMIN_LAST_NAME,
        settings.INITIAL_ADMIN_EMAIL,
    )
    use_case.execute(command)

    logger.info("Initial admin created successfully.")


if __name__ == "__main__":
    try:
        create_initial_admin()
    except AdminUserAlreadyExistsException:
        logger.info("Admin user already exists. Skipping bootstrap.")
        sys.exit(0)

    except EmailAlreadyExistsException:
        logger.info("Admin email already exists. Skipping bootstrap.")
        sys.exit(0)

    except Exception as e:
        logger.error("Failed to create initial admin", error=str(e))
        sys.exit(1)
