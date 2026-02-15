"""This module contains the use case for update user password."""

from src.contexts.auth.application.dto.command import UpdateUserPasswordCommand
from src.contexts.auth.domain.exceptions.exception import (
    CurrentPasswordIncorrectException,
    NewPasswordEqualsCurrentException,
    UserNotFoundException,
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
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class UpdateUserPasswordUseCase:
    """Use case for update user password."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        password_service_port: PasswordServicePort,
        password_hash_service_port: PasswordHashServicePort,
    ) -> None:
        """Initialize the UpdateUserPasswordUseCase with required ports.

        Args:
            user_repository_port (UserRepositoryPort): Port for user repository operations.
            password_service_port (PasswordServicePort): Port for password generation.
            password_hash_service_port (PasswordHashServicePort): Port for password hashing.
        """
        self.user_repository_port = user_repository_port
        self.password_service_port = password_service_port
        self.password_hash_service_port = password_hash_service_port

    def execute(self, command: UpdateUserPasswordCommand) -> None:
        """Execute the use case for updating a user's password.

        Args:
            command (UpdateUserPasswordCommand): Command containing the user identifier, the current password, and the new password.

        Raises:
            UserNotFoundException: If no user is found with the given identifier.
            CurrentPasswordIncorrectException: If the provided current password does not match the stored password.
            NewPasswordEqualsCurrentException: If the new password is the same as the current password.
        """
        # Search for user by their ID
        user = self.user_repository_port.find_by_id(command.user_id)
        if not user:
            raise UserNotFoundException("id")

        # Check if the current password matches the stored password
        is_current_password = self.password_hash_service_port.verify(
            PasswordVO(command.current_password), user.password_hash
        )
        if not is_current_password:
            raise CurrentPasswordIncorrectException

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
