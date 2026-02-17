"""This module contains the use case for password recovery."""

from datetime import UTC, datetime

from src.contexts.auth.application.dto.command import PasswordRecoveryCommand
from src.contexts.auth.domain.exceptions.exception import UserNotFoundException
from src.contexts.auth.domain.ports.repositories.user_repository_port import (
    UserRepositoryPort,
)
from src.contexts.auth.domain.ports.services.activation_code_service_port import (
    ActivationCodeServicePort,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_recovery_cache_key_vo import (
    PasswordRecoveryCacheKeyVO,
)
from src.contexts.auth.domain.value_objects.password_recovery_cache_value_vo import (
    PasswordRecoveryCacheValueVO,
)
from src.contexts.auth.domain.value_objects.template_context_password_recovery_vo import (
    TemplateContextPasswordRecoveryVO,
)
from src.contexts.auth.domain.value_objects.template_name_password_recovery_vo import (
    TemplateNamePasswordRecoveryVO,
)
from src.shared.domain.ports.services.cache_service_port import CacheServicePort
from src.shared.domain.ports.services.sender_notification_service_port import (
    SenderNotificationServicePort,
)
from src.shared.domain.ports.services.template_renderer_service_port import (
    TemplateRendererServicePort,
)
from src.shared.domain.value_objects.cache_entry_vo import CacheEntryVO
from src.shared.domain.value_objects.cache_ttl_vo import CacheTTLVO
from src.shared.domain.value_objects.send_notification_vo import SendNotificationVO
from src.shared.domain.value_objects.template_renderer_vo import TemplateRendererVO


class PasswordRecoveryUseCase:
    """Use case for password recovery."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        activation_code_service_port: ActivationCodeServicePort,
        cache_service_port: CacheServicePort[PasswordRecoveryCacheValueVO],
        template_renderer_service_port: TemplateRendererServicePort,
        sender_notification_service_port: SenderNotificationServicePort,
    ) -> None:
        """Initialize the PasswordRecoveryUseCase with required ports.

        Args:
            user_repository_port (UserRepositoryPort): Port to interact with the user repository.
            activation_code_service_port (ActivationCodeServicePort): Port to interact with the activation code service.
            cache_service_port (CacheServicePort): Port to interact with the cache service.
            template_renderer_service_port (TemplateRendererServicePort): Port to interact with the template renderer service.
            sender_notification_service_port (SenderNotificationServicePort): Port to interact with the sender notification service.
        """
        self.user_repository_port = user_repository_port
        self.activation_code_service_port = activation_code_service_port
        self.cache_service_port = cache_service_port
        self.template_renderer_service_port = template_renderer_service_port
        self.sender_notification_service_port = sender_notification_service_port

    def execute(self, command: PasswordRecoveryCommand) -> None:
        """Execute the password recovery use case.

        Args:
            command (PasswordRecoveryCommand): Command to execute the use case.

        Raises:
            UserNotFoundException: If the user is not found.
        """
        user = self.user_repository_port.find_by_email(EmailVO(command.email))
        if not user:
            raise UserNotFoundException("email")

        password_recovery_cache_key = PasswordRecoveryCacheKeyVO.from_email(
            EmailVO(command.email)
        )

        active_code = self.cache_service_port.get(password_recovery_cache_key)
        if active_code:
            self.cache_service_port.delete(password_recovery_cache_key)

        recovery_code = self.activation_code_service_port.generate()

        value = PasswordRecoveryCacheValueVO(
            user_id=user.id, email=user.email, recovery_code=recovery_code
        )
        ttl = CacheTTLVO.from_minutes(45)
        entry = CacheEntryVO(key=password_recovery_cache_key, ttl=ttl, value=value)
        self.cache_service_port.set(entry)

        template_name = TemplateNamePasswordRecoveryVO.create()
        context = TemplateContextPasswordRecoveryVO(
            first_name=user.first_name,
            last_name=user.last_name,
            recovery_code=recovery_code,
            expiration_minutes=ttl.to_minutes(),
            request_datetime=datetime.now(UTC),
            request_ip=command.request_ip,
            request_user_agent=command.request_user_agent,
        )

        template = TemplateRendererVO(template_name=template_name, context=context)
        message = self.template_renderer_service_port.render(template)

        notification = SendNotificationVO(
            recipient=user.email.value, subject="Reset your password", body=message
        )
        self.sender_notification_service_port.send(notification)
