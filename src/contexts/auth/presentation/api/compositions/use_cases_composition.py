"""This module contains the use cases composition for FastAPI dependencies."""

from fastapi import Depends

from src.config import settings
from src.contexts.auth.application.use_cases.activate_account_use_case import (
    ActivateAccountUseCase,
)
from src.contexts.auth.application.use_cases.login_use_case import LoginUseCase
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.application.use_cases.update_user_password_use_case import (
    UpdateUserPasswordUseCase,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_doctor_repository_adapter import (
    SQLModelDoctorRepositoryAdapter,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_patient_repository_adapter import (
    SQLModelPatientRepositoryAdapter,
)
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_user_repository_adapter import (
    SQLModelRepositoryAdapter,
)
from src.contexts.auth.infrastructure.policies.authorization_policy_service_adapter import (
    AuthorizationPolicyServiceAdapter,
)
from src.contexts.auth.infrastructure.policies.staff_email_policy_service_adapter import (
    StaffEmailPolicyServiceAdapter,
)
from src.contexts.auth.infrastructure.security.activation_code_service_adapter import (
    ActivationCodeServiceAdapter,
)
from src.contexts.auth.infrastructure.security.password_hash_service_adapter import (
    PasswordHashServiceAdapter,
)
from src.contexts.auth.infrastructure.security.password_service_adapter import (
    PasswordServiceAdapter,
)
from src.contexts.auth.infrastructure.security.token_service_adapter import (
    PyJWTTokenServiceAdapter,
)
from src.contexts.auth.presentation.api.compositions.infrastructure_composition import (
    get_activation_code_cache_service,
    get_activation_code_service,
    get_authorization_policy_service,
    get_doctor_repository,
    get_login_attempts_cache_service,
    get_password_hash_service,
    get_password_service,
    get_patient_repository,
    get_staff_email_policy_service,
    get_template_renderer_activate_account_service_service,
    get_user_repository,
)
from src.shared.infrastructure.cache.redis_cache_service_adapter import (
    RedisCacheServiceAdapter,
)
from src.shared.infrastructure.notifications.sender_notification_service_adapter import (
    SenderNotificationServiceAdapter,
)
from src.shared.infrastructure.notifications.template_renderer_service_adapter import (
    TemplateRendererServiceAdapter,
)
from src.shared.presentation.api.compositions.infrastructure_composition import (
    get_sender_notification_service,
    get_token_service,
)


def get_register_user_use_case(
    user_repository: SQLModelRepositoryAdapter = Depends(get_user_repository),
    patient_repository: SQLModelPatientRepositoryAdapter = Depends(
        get_patient_repository
    ),
    doctor_repository: SQLModelDoctorRepositoryAdapter = Depends(get_doctor_repository),
    password_service: PasswordServiceAdapter = Depends(get_password_service),
    password_hash_service: PasswordHashServiceAdapter = Depends(
        get_password_hash_service
    ),
    activation_code_service: ActivationCodeServiceAdapter = Depends(
        get_activation_code_service
    ),
    cache_service: RedisCacheServiceAdapter = Depends(
        get_activation_code_cache_service
    ),
    staff_email_policy_service: StaffEmailPolicyServiceAdapter = Depends(
        get_staff_email_policy_service
    ),
    authorization_policy_service: AuthorizationPolicyServiceAdapter = Depends(
        get_authorization_policy_service
    ),
    template_renderer_service: TemplateRendererServiceAdapter = Depends(
        get_template_renderer_activate_account_service_service
    ),
    sender_notification_service: SenderNotificationServiceAdapter = Depends(
        get_sender_notification_service
    ),
) -> RegisterUserUseCase:
    """Get the RegisterUserUseCase instance.

    Args:
        user_repository (SQLModelRepositoryAdapter): The user repository.
        patient_repository (SQLModelPatientRepositoryAdapter): The patient repository.
        doctor_repository (SQLModelDoctorRepositoryAdapter): The doctor repository.
        password_service (PasswordServiceAdapter): The password service.
        password_hash_service (PasswordHashServiceAdapter): The password hash service.
        activation_code_service (ActivationCodeServiceAdapter): The activation code service.
        cache_service (RedisCacheServiceAdapter): The cache service.
        staff_email_policy_service (StaffEmailPolicyServiceAdapter): The staff email policy service.
        authorization_policy_service (AuthorizationPolicyServiceAdapter): The authorization policy service.
        template_renderer_service (TemplateRendererServiceAdapter): The template renderer service.
        sender_notification_service (SenderNotificationServiceAdapter): The sender notification service.

    Returns:
        RegisterUserUseCase: An instance of RegisterUserUseCase.
    """
    return RegisterUserUseCase(
        user_repository,
        patient_repository,
        doctor_repository,
        password_service,
        password_hash_service,
        activation_code_service,
        cache_service,
        staff_email_policy_service,
        authorization_policy_service,
        template_renderer_service,
        sender_notification_service,
    )


def get_activate_account_use_case(
    user_repository: SQLModelRepositoryAdapter = Depends(get_user_repository),
    cache_service: RedisCacheServiceAdapter = Depends(
        get_activation_code_cache_service
    ),
) -> ActivateAccountUseCase:
    """Get the ActivateAccountUseCase instance.

    Args:
        user_repository (SQLModelRepositoryAdapter): The user repository.
        cache_service (RedisCacheServiceAdapter): The cache service.

    Returns:
        ActivateAccountUseCase: An instance of ActivateAccountUseCase.
    """
    return ActivateAccountUseCase(user_repository, cache_service)


def get_login_use_case(
    user_repository: SQLModelRepositoryAdapter = Depends(get_user_repository),
    password_hash_service: PasswordHashServiceAdapter = Depends(
        get_password_hash_service
    ),
    token_service: PyJWTTokenServiceAdapter = Depends(get_token_service),
    cache_service: RedisCacheServiceAdapter = Depends(get_login_attempts_cache_service),
) -> LoginUseCase:
    """Get the LoginUseCase instance.

    Args:
        user_repository (SQLModelRepositoryAdapter): The user repository.
        password_hash_service (PasswordHashServiceAdapter): The password hash service.
        token_service (TokenServicePort): The token service.
        cache_service (RedisCacheServiceAdapter): The cache service.

    Returns:
        LoginUseCase: An instance of LoginUseCase.
    """
    return LoginUseCase(
        user_repository,
        password_hash_service,
        token_service,
        cache_service,
        settings.ACCESS_TOKEN_EXPIRES_IN,
        settings.LOGIN_ATTEMPTS_LIMIT,
        settings.LOGIN_WAITING_TIME,
    )


def get_update_user_password_use_case(
    user_repository: SQLModelRepositoryAdapter = Depends(get_user_repository),
    password_service: PasswordServiceAdapter = Depends(get_password_service),
    password_hash_service: PasswordHashServiceAdapter = Depends(
        get_password_hash_service
    ),
) -> UpdateUserPasswordUseCase:
    """Get the UpdateUserPasswordUseCase instance.

    Args:
        user_repository (SQLModelRepositoryAdapter): The user repository.
        password_service (PasswordServiceAdapter): The password service.
        password_hash_service (PasswordHashServiceAdapter): The password hash service.

    Returns:
        UpdateUserPasswordUseCase: An instance of UpdateUserPasswordUseCase
    """
    return UpdateUserPasswordUseCase(
        user_repository,
        password_service,
        password_hash_service,
    )
