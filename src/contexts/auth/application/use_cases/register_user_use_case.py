"""This module contains the use case for registering a new user."""

from src.contexts.auth.application.dto.command import RegisterUserCommand
from src.contexts.auth.domain.entities.entity import RolesEnum, UserEntity
from src.contexts.auth.domain.exceptions.exception import (
    EmailAlreadyExistsException,
    InvalidCorporateEmailException,
    UnauthorizedUserRegistrationException,
)
from src.contexts.auth.domain.ports.activation_code_service_port import (
    ActivationCodeServicePort,
)
from src.contexts.auth.domain.ports.authorization_policy_service_port import (
    AuthorizationPolicyServicePort,
)
from src.contexts.auth.domain.ports.password_hash_service_port import (
    PasswordHashServicePort,
)
from src.contexts.auth.domain.ports.password_service_port import PasswordServicePort
from src.contexts.auth.domain.ports.staff_email_policy_service_port import (
    StaffEmailPolicyServicePort,
)
from src.contexts.auth.domain.ports.user_repository_port import UserRepositoryPort
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.cache_service_port import CacheServicePort
from src.shared.domain.event_bus_service_port import EventBusServicePort


class RegisterUserUseCase:
    """Use case for registering a new user."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        password_service_port: PasswordServicePort,
        password_hash_service_port: PasswordHashServicePort,
        activation_code_service_port: ActivationCodeServicePort,
        cache_service_port: CacheServicePort,
        staff_email_policy_service_port: StaffEmailPolicyServicePort,
        authorization_policy_service_port: AuthorizationPolicyServicePort,
        event_bus_service_port: EventBusServicePort,
    ) -> None:
        """Initialize the RegisterUserUseCase with required ports.

        Args:
            user_repository_port (UserRepositoryPort): Port for user repository operations.
            password_service_port (PasswordServicePort): Port for password generation.
            password_hash_service_port (PasswordHashServicePort): Port for password hashing.
            activation_code_service_port (ActivationCodeServicePort): Port for activation code generation.
            cache_service_port (CacheServicePort): Port for caching services.
            staff_email_policy_service_port (StaffEmailPolicyServicePort): Port for staff email policy checks.
            authorization_policy_service_port (AuthorizationPolicyServicePort): Port for authorization policy checks.
            event_bus_service_port (EventBusServicePort): Port for event bus operations.
        """
        self.user_repository_port = user_repository_port
        self.password_service_port = password_service_port
        self.password_hash_service_port = password_hash_service_port
        self.activation_code_service_port = activation_code_service_port
        self.cache_service_port = cache_service_port
        self.staff_email_policy_service_port = staff_email_policy_service_port
        self.authorization_policy_service_port = authorization_policy_service_port
        self.event_bus_service_port = event_bus_service_port

    def execute(self, command: RegisterUserCommand) -> None:
        """Register a new user based on the provided command.

        Args:
            command (RegisterUserCommand): The command containing user registration details.

        Raises:
            UnauthorizedUserRegistrationException: If the role is not authorized to register.
            InvalidCorporateEmailException: If the email is not valid for the specified role.
            EmailAlreadyExistsException: If the email is already registered.
        """
        # Authorization check
        if not self.authorization_policy_service_port.can_register(
            RolesEnum(command.role_recorder)
        ):
            raise UnauthorizedUserRegistrationException(command.role_recorder)

        # Staff email policy check
        if not self.staff_email_policy_service_port.is_allowed(
            EmailVO(command.email), RolesEnum(command.role)
        ):
            raise InvalidCorporateEmailException(command.email, command.role)

        # Check for existing user
        existing_user = self.user_repository_port.find_by_email(EmailVO(command.email))
        if not existing_user:
            raise EmailAlreadyExistsException(command.email)

        # Generate temporary password and hash it
        temporary_password = self.password_service_port.generate()
        password_hash = self.password_hash_service_port.hashed(temporary_password)

        # Create and save the new user entity
        entity = UserEntity.create(
            first_name=command.first_name,
            last_name=command.last_name,
            email=EmailVO(command.email),
            password_hash=password_hash,
            role=RolesEnum(command.role),
        )
        user = self.user_repository_port.save(entity)

        # Generate activation code and cache it
        cache_key = f"cache:auth:activation_code:{str(user.id)}"
        activation_code = self.activation_code_service_port.generate()
        ttl = 15 * 60
        cache_payload = {
            "user_id": str(user.id),
            "email": str(user.email),
            "code": activation_code,
        }
        self.cache_service_port.set(cache_key, ttl, cache_payload)

        # Publish activation code created event
        event_key = "event.auth.activation_code.created"
        event_payload = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "temporary_password": temporary_password,
            "code": activation_code,
        }
        self.event_bus_service_port.publisher(event_key, event_payload)
