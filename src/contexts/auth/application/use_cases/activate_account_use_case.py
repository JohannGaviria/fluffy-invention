"""This module contains the ActivateAccountUseCase for activating user accounts."""

from src.contexts.auth.domain.exceptions.exception import (
    ActivationCodeExpiredException,
    InvalidActivationCodeException,
    UserNotFoundException,
)
from src.contexts.auth.domain.ports.user_repository_port import UserRepositoryPort
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.cache_service_port import CacheServicePort


class ActivateAccountUseCase:
    """Use case for activating a user account."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        cache_service_port: CacheServicePort,
    ) -> None:
        """Initialize the ActivateAccountUseCase with required ports.

        Args:
            user_repository_port (UserRepositoryPort): Port for user repository operations.
            cache_service_port (CacheServicePort): Port for caching services.
        """
        self.user_repository_port = user_repository_port
        self.cache_service_port = cache_service_port

    def execute(self, activation_code: str, email: str) -> None:
        """Activate a user account using the provided activation code and email.

        Args:
            activation_code (str): The activation code provided by the user.
            email (str): The email address of the user to activate.
        """
        # Retrieve the user by email
        user = self.user_repository_port.find_by_email(EmailVO(email))
        if not user:
            raise UserNotFoundException(email)

        # Validate the activation code from cache
        key = f"cache:auth:activation_code:{str(user.id)}"
        existing_cache = self.cache_service_port.get(key)
        if not existing_cache:
            raise ActivationCodeExpiredException()

        # Check if the activation code matches
        if activation_code != existing_cache["activation_code"]:
            raise InvalidActivationCodeException()

        # Activate the user account
        self.user_repository_port.status_update(True, user.id)
