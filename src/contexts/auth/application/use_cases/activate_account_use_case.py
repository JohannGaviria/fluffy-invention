"""This module contains the ActivateAccountUseCase for activating user accounts."""

from src.contexts.auth.domain.exceptions.exception import (
    ActivationCodeExpiredException,
    InvalidActivationCodeException,
    UserNotFoundException,
)
from src.contexts.auth.domain.ports.repositories.user_repository_port import (
    UserRepositoryPort,
)
from src.contexts.auth.domain.value_objects.activation_code_cache_key_vo import (
    ActivationCodeCacheKeyVO,
)
from src.contexts.auth.domain.value_objects.activation_code_cache_value_vo import (
    ActivationCodeCacheValueVO,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.ports.services.cache_service_port import CacheServicePort


class ActivateAccountUseCase:
    """Use case for activating a user account."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        cache_service_port: CacheServicePort[ActivationCodeCacheValueVO],
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
        key = ActivationCodeCacheKeyVO.from_user_id(user.id)
        cached_value = self.cache_service_port.get(key)
        if not cached_value:
            raise ActivationCodeExpiredException()

        # Check if the activation code matches
        if not activation_code == cached_value.code:
            raise InvalidActivationCodeException()

        # Activate the user account
        self.user_repository_port.status_update(True, user.id)

        # Remove the activation code from cache
        self.cache_service_port.delete(key)
