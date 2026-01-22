"""This module contains the LoginUseCase class for handling user login logic."""

from src.contexts.auth.application.dto.command import LoginCommand
from src.contexts.auth.application.dto.response import AccessTokenResponse
from src.contexts.auth.domain.exceptions.exception import (
    AccountTemporarilyBlockedException,
    InvalidCredentialsException,
    UserInactiveException,
)
from src.contexts.auth.domain.ports.password_hash_service_port import (
    PasswordHashServicePort,
)
from src.contexts.auth.domain.ports.token_service_port import TokenServicePort
from src.contexts.auth.domain.ports.user_repository_port import UserRepositoryPort
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.shared.domain.cache_service_port import CacheServicePort


class LoginUseCase:
    """Use case for user login."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        password_hash_service_port: PasswordHashServicePort,
        token_service_port: TokenServicePort,
        cache_service_port: CacheServicePort,
        expire_in: int,
        attempts_limit: int,
        waiting_time: int,
    ) -> None:
        """Initializes the LoginUseCase with required ports and configurations.

        Args:
            user_repository_port (UserRepositoryPort): The user repository port.
            password_hash_service_port (PasswordHashServicePort): The password hash service port.
            token_service_port (TokenServicePort): The token service port.
            cache_service_port (CacheServicePort): The cache service port.
            expire_in (int): The token expiration time in seconds.
            attempts_limit (int): The maximum number of allowed login attempts.
            waiting_time (int): The waiting time in seconds after reaching the attempts limit.
        """
        self.user_repository_port = user_repository_port
        self.password_hash_service_port = password_hash_service_port
        self.token_service_port = token_service_port
        self.cache_service_port = cache_service_port
        self.expire_in = expire_in
        self.attempts_limit = attempts_limit
        self.waiting_time = waiting_time

    def execute(self, command: LoginCommand) -> AccessTokenResponse:
        """Executes the login use case.

        Args:
            command (LoginCommand): The login command containing email and password.

        Returns:
            AccessTokenResponse: The access token response containing token info.

        Raises:
            AccountTemporarilyBlockedException: If the account is temporarily blocked due to too many failed attempts.
            InvalidCredentialsException: If the provided credentials are invalid.
            UserInactiveException: If the user account is inactive.
        """
        # Check for too many failed login attempts
        attempts_key = f"cache:auth:login_attempts:{command.email}"
        attempts = self.cache_service_port.get(attempts_key) or {"attempt": 0}
        if attempts["attempt"] >= self.attempts_limit:
            raise AccountTemporarilyBlockedException(
                "Too many failed attempts. Try again later."
            )

        # Validate user credentials
        user = self.user_repository_port.find_by_email(EmailVO(command.email))

        # User does not exist
        if user is None:
            attempts["attempt"] += 1
            self.cache_service_port.set(
                attempts_key,
                self.waiting_time,
                {"attempt": attempts["attempt"]},
            )
            raise InvalidCredentialsException()

        # User exists but is inactive
        if not user.is_active:
            raise UserInactiveException()

        # Verify password
        credentials_valid = self.password_hash_service_port.verify(
            PasswordVO(command.password),
            user.password_hash,
        )

        # Invalid password
        if not credentials_valid:
            attempts["attempt"] += 1
            self.cache_service_port.set(
                attempts_key,
                self.waiting_time,
                {"attempt": attempts["attempt"]},
            )
            raise InvalidCredentialsException()

        # Generate access token
        payload = TokenPayloadVO.generate(user, self.expire_in)
        token = self.token_service_port.access(payload)

        # Reset failed attempts on successful login
        self.cache_service_port.delete(attempts_key)

        return AccessTokenResponse(
            token.access_token, token.token_type, token.expires_at, token.expires_in
        )
