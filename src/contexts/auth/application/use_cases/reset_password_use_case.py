"""This module contains the use case for resetting a user's password."""

from src.contexts.auth.application.dto.command import ResetPasswordCommand
from src.contexts.auth.domain.exceptions.exception import (
    ActivationCodeExpiredException,
    NewPasswordEqualsCurrentException,
    UserNotFoundException,
)
from src.contexts.auth.domain.ports.repositories.user_repository_port import (
    UserRepositoryPort,
)
from src.contexts.auth.domain.ports.services.password_hash_service_port import (
    PasswordHashServicePort,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_recovery_cache_key_vo import (
    PasswordRecoveryCacheKeyVO,
)
from src.contexts.auth.domain.value_objects.password_recovery_cache_value_vo import (
    PasswordRecoveryCacheValueVO,
)
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO
from src.shared.domain.ports.services.cache_service_port import CacheServicePort


class ResetPasswordUseCase:
    """Use case for resetting a user's password."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        password_hash_service_port: PasswordHashServicePort,
        cache_service_port: CacheServicePort[PasswordRecoveryCacheValueVO],
    ) -> None:
        """Initialize the ResetPasswordUseCase with the necessary ports.

        Args:
            user_repository_port (UserRepositoryPort): Port for user repository operations.
            password_hash_service_port (PAsswordHashServicePort): Port for password hash service operations.
            cache_service_port (CacheServicePort[PasswordRecoveryCacheValueVO]): Port for cache service operations.
        """
        self.user_repository_port = user_repository_port
        self.password_hash_service_port = password_hash_service_port
        self.cache_service_port = cache_service_port

    def execute(self, command: ResetPasswordCommand) -> None:
        """Execute the use case to reset a user's password.

        Args:
            command: Command containing the email, recovery code, and new password.

        Raises:
            UserNotFoundException: If the user is not found.
            ActivationCodeExpiredException: If the recovery code is invalid or expired.
            NewPasswordEqualsCurrentException: If the new password is the same as the current password.
        """
        # Find the user by email
        user = self.user_repository_port.find_by_email(EmailVO(command.email))
        if not user:
            raise UserNotFoundException("email")

        # Check if the recovery code is valid
        recovery_cache_key = PasswordRecoveryCacheKeyVO.from_email(
            EmailVO(command.email)
        )
        recovery_cache_value = self.cache_service_port.get(recovery_cache_key)

        if not recovery_cache_value:  # If the recovery code is not found in the cache
            raise ActivationCodeExpiredException()

        # If the recovery code is found in the cache,
        # verify if it matches the one provided in the command
        if recovery_cache_value.recovery_code != command.recovery_code:
            raise ActivationCodeExpiredException()

        # Verify if the new password is the same as the current password
        is_same_password = self.password_hash_service_port.verify(
            PasswordVO(command.new_password), user.password_hash
        )
        if is_same_password:
            raise NewPasswordEqualsCurrentException()

        # Hash the new password and store it
        new_password_hash = self.password_hash_service_port.hashed(
            PasswordVO(command.new_password)
        )
        self.user_repository_port.update_password(user.id, new_password_hash)

        # Delete the recovery code from the cache
        self.cache_service_port.delete(recovery_cache_key)
