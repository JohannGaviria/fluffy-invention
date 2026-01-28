"""This module contains the use case for registering a new user."""

from src.contexts.auth.application.dto.command import (
    DoctorProfileCommand,
    PatientProfileCommand,
    RegisterUserCommand,
)
from src.contexts.auth.domain.entities.entity import (
    DoctorEntity,
    PatientEntity,
    RolesEnum,
    UserEntity,
)
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
from src.contexts.auth.domain.ports.doctor_repository_port import DoctorRepositoryPort
from src.contexts.auth.domain.ports.password_hash_service_port import (
    PasswordHashServicePort,
)
from src.contexts.auth.domain.ports.password_service_port import PasswordServicePort
from src.contexts.auth.domain.ports.patient_repository_port import PatientRepositoryPort
from src.contexts.auth.domain.ports.staff_email_policy_service_port import (
    StaffEmailPolicyServicePort,
)
from src.contexts.auth.domain.ports.user_repository_port import UserRepositoryPort
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.exceptions.exception import MissingFieldException
from src.shared.domain.ports.services.cache_service_port import CacheServicePort
from src.shared.domain.ports.services.sender_notification_service_port import (
    SenderNotificationServicePort,
)
from src.shared.domain.ports.services.template_renderer_service_port import (
    TemplateRendererServicePort,
)


class RegisterUserUseCase:
    """Use case for registering a new user."""

    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        patient_repository_port: PatientRepositoryPort,
        doctor_repository_port: DoctorRepositoryPort,
        password_service_port: PasswordServicePort,
        password_hash_service_port: PasswordHashServicePort,
        activation_code_service_port: ActivationCodeServicePort,
        cache_service_port: CacheServicePort,
        staff_email_policy_service_port: StaffEmailPolicyServicePort,
        authorization_policy_service_port: AuthorizationPolicyServicePort,
        template_renderer_service_port: TemplateRendererServicePort,
        sender_notification_service_port: SenderNotificationServicePort,
    ) -> None:
        """Initialize the RegisterUserUseCase with required ports.

        Args:
            user_repository_port (UserRepositoryPort): Port for user repository operations.
            patient_repository_port (PatientRepositoryPort): Port for patient repository operations.
            doctor_repository_port (DoctorRepositoryPort): Port for doctor repository operations.
            password_service_port (PasswordServicePort): Port for password generation.
            password_hash_service_port (PasswordHashServicePort): Port for password hashing.
            activation_code_service_port (ActivationCodeServicePort): Port for activation code generation.
            cache_service_port (CacheServicePort): Port for caching services.
            staff_email_policy_service_port (StaffEmailPolicyServicePort): Port for staff email policy checks.
            authorization_policy_service_port (AuthorizationPolicyServicePort): Port for authorization policy checks.
            template_renderer_service_port (TemplateRendererServicePort): Port for rendering templates.
            sender_notification_service_port (SenderNotificationServicePort): Port for sending notifications.
        """
        self.user_repository_port = user_repository_port
        self.patient_repository_port = patient_repository_port
        self.doctor_repository_port = doctor_repository_port
        self.password_service_port = password_service_port
        self.password_hash_service_port = password_hash_service_port
        self.activation_code_service_port = activation_code_service_port
        self.cache_service_port = cache_service_port
        self.staff_email_policy_service_port = staff_email_policy_service_port
        self.authorization_policy_service_port = authorization_policy_service_port
        self.template_renderer_service_port = template_renderer_service_port
        self.sender_notification_service_port = sender_notification_service_port

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
        if existing_user:
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

        if command.role == "patient":
            if not isinstance(command.profile, PatientProfileCommand):
                raise MissingFieldException(
                    "profile", "Patient profile is required for patient role"
                )
            patient_entity = PatientEntity.create(
                user_id=user.id,
                document=command.profile.document,
                phone=command.profile.phone,
                birth_date=command.profile.birth_date,
            )
            self.patient_repository_port.save(patient_entity)

        if command.role == "doctor":
            if not isinstance(command.profile, DoctorProfileCommand):
                raise MissingFieldException(
                    "profile", "Doctor profile is required for doctor role"
                )

            doctor_entity = DoctorEntity.create(
                user_id=user.id,
                license_number=command.profile.license_number,
                experience_years=command.profile.experience_years,
                specialty_id=command.profile.specialty_id,
                qualifications=command.profile.qualifications,
                bio=command.profile.bio,
            )
            self.doctor_repository_port.save(doctor_entity)

        # Generate activation code and cache it
        key = f"cache:auth:activation_code:{str(user.id)}"
        activation_code = self.activation_code_service_port.generate()
        ttl = 15 * 60
        payload = {
            "user_id": str(user.id),
            "email": str(user.email),
            "code": activation_code,
        }
        self.cache_service_port.set(key, ttl, payload)

        context = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "temporary_password": temporary_password,
            "activation_code": activation_code,
            "expiration_minutes": ttl // 60,
        }
        message = self.template_renderer_service_port.render(
            "auth_activation_code.html", context
        )
        self.sender_notification_service_port.send(
            user.email.value, "Activate your account", message
        )
