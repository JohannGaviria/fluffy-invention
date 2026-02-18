"""Unit tests for RegisterUserUseCase."""

from unittest.mock import Mock

import pytest

from src.contexts.auth.application.dto.command import (
    DoctorProfileCommand,
    PatientProfileCommand,
    RegisterUserCommand,
)
from src.contexts.auth.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from src.contexts.auth.domain.exceptions.exception import (
    DoctorLicenseNumberAlreadyRegisteredException,
    DoctorProfileAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCorporateEmailException,
    PatientDocumentAlreadyRegisteredException,
    PatientPhoneAlreadyRegisteredException,
    PatientProfileAlreadyExistsException,
    UnauthorizedUserRegistrationException,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.exceptions.exception import MissingFieldException


class TestRegisterUserUseCase:
    """Unit tests for RegisterUserUseCase."""

    def setup_method(self):
        """Setup mock dependencies for the use case."""
        self.user_repository_port = Mock()
        self.patient_repository_port = Mock()
        self.doctor_repository_port = Mock()
        self.password_service_port = Mock()
        self.password_hash_service_port = Mock()
        self.activation_code_service_port = Mock()
        self.cache_service_port = Mock()
        self.staff_email_policy_service_port = Mock()
        self.authorization_policy_service_port = Mock()
        self.template_renderer_service_port = Mock()
        self.sender_notification_service_port = Mock()

        self.use_case = RegisterUserUseCase(
            user_repository_port=self.user_repository_port,
            patient_repository_port=self.patient_repository_port,
            doctor_repository_port=self.doctor_repository_port,
            password_service_port=self.password_service_port,
            password_hash_service_port=self.password_hash_service_port,
            activation_code_service_port=self.activation_code_service_port,
            cache_service_port=self.cache_service_port,
            staff_email_policy_service_port=self.staff_email_policy_service_port,
            authorization_policy_service_port=self.authorization_policy_service_port,
            template_renderer_service_port=self.template_renderer_service_port,
            sender_notification_service_port=self.sender_notification_service_port,
        )

    def test_register_user_unauthorized_role(self):
        """Should raise UnauthorizedUserRegistrationException for unauthorized role."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role="unauthorized_role",
            profile=None,
            role_recorder="admin",
        )

        self.authorization_policy_service_port.can_register.return_value = False

        with pytest.raises(UnauthorizedUserRegistrationException):
            self.use_case.execute(command)

    def test_register_user_invalid_email(self):
        """Should raise InvalidCorporateEmailException for invalid email."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role="admin",
            profile=None,
            role_recorder="admin",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = False

        with pytest.raises(InvalidCorporateEmailException):
            self.use_case.execute(command)

    def test_register_user_email_already_exists(self):
        """Should raise EmailAlreadyExistsException if email is already registered."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role="admin",
            profile=None,
            role_recorder="admin",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = Mock()

        with pytest.raises(EmailAlreadyExistsException):
            self.use_case.execute(command)

    def test_register_user_patient_profile_creation(self):
        """Should create a patient profile successfully."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role="patient",
            profile=PatientProfileCommand(
                document="123456789",
                phone="1234567890",
                birth_date="1990-01-01",
            ),
            role_recorder="admin",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None
        self.patient_repository_port.find_by_user_id.return_value = None
        self.patient_repository_port.find_by_document.return_value = None
        self.patient_repository_port.find_by_phone.return_value = None

        temp_password = Mock()
        temp_password.value = "Temp_Password!23"
        self.password_service_port.generate.return_value = temp_password
        self.password_hash_service_port.hashed.return_value = "hashed_password"

        saved_user = Mock()
        saved_user.id = 1
        saved_user.email = EmailVO("john.doe@example.com")
        saved_user.first_name = "John"
        saved_user.last_name = "Doe"
        self.user_repository_port.save.return_value = saved_user

        self.activation_code_service_port.generate.return_value = "123456"

        self.use_case.execute(command)

        self.patient_repository_port.save.assert_called_once()

    def test_register_user_doctor_profile_creation(self):
        """Should create a doctor profile successfully."""
        command = RegisterUserCommand(
            first_name="Gregory",
            last_name="House",
            email="house.md@example.com",
            role="doctor",
            profile=DoctorProfileCommand(
                license_number="LIC-12345",
                experience_years=10,
                is_active=True,
                specialty_id=1,
                qualifications="MD, PhD",
                bio="Diagnostic specialist",
            ),
            role_recorder="doctor",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None

        self.doctor_repository_port.find_by_user_id.return_value = None
        self.doctor_repository_port.find_by_license_number.return_value = None

        temp_password = Mock()
        temp_password.value = "Temp_Password!23"
        self.password_service_port.generate.return_value = temp_password
        self.password_hash_service_port.hashed.return_value = "hashed_password"

        saved_user = Mock()
        saved_user.id = 99
        saved_user.email = EmailVO("house.md@example.com")
        saved_user.first_name = "Gregory"
        saved_user.last_name = "House"
        self.user_repository_port.save.return_value = saved_user

        self.activation_code_service_port.generate.return_value = "654321"

        self.use_case.execute(command)

        self.doctor_repository_port.save.assert_called_once()
        self.cache_service_port.set.assert_called_once()
        self.sender_notification_service_port.send.assert_called_once()

    def test_register_user_activation_code_and_email(self):
        """Should generate activation code and send email notification."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role="admin",
            profile=None,
            role_recorder="admin",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None

        temp_password = Mock()
        temp_password.value = "Temp_Password!23"
        self.password_service_port.generate.return_value = temp_password
        self.password_hash_service_port.hashed.return_value = "hashed_password"

        saved_user = Mock()
        saved_user.id = 1
        saved_user.email = EmailVO("john.doe@example.com")
        saved_user.first_name = "John"
        saved_user.last_name = "Doe"
        self.user_repository_port.save.return_value = saved_user

        self.activation_code_service_port.generate.return_value = "123456"

        self.use_case.execute(command)

        self.cache_service_port.set.assert_called_once()
        self.sender_notification_service_port.send.assert_called_once()

    def test_register_user_patient_profile_already_exists(self):
        """Should register user patient profile exists."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            role="patient",
            profile=PatientProfileCommand("123", "555", "1990-01-01"),
            role_recorder="patient",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None

        saved_user = Mock(id=1)
        self.user_repository_port.save.return_value = saved_user
        self.patient_repository_port.find_by_user_id.return_value = Mock()

        with pytest.raises(PatientProfileAlreadyExistsException):
            self.use_case.execute(command)

    def test_register_user_patient_document_already_registered(self):
        """Should register user patient document already registered."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            role="patient",
            profile=PatientProfileCommand("123", "555", "1990-01-01"),
            role_recorder="patient",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None

        saved_user = Mock(id=1)
        self.user_repository_port.save.return_value = saved_user
        self.patient_repository_port.find_by_user_id.return_value = None
        self.patient_repository_port.find_by_document.return_value = Mock()

        with pytest.raises(PatientDocumentAlreadyRegisteredException):
            self.use_case.execute(command)

    def test_register_user_patient_phone_already_registered(self):
        """Should register user patient phone already registered."""
        command = RegisterUserCommand(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            role="patient",
            profile=PatientProfileCommand("123", "555", "1990-01-01"),
            role_recorder="patient",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None

        saved_user = Mock(id=1)
        self.user_repository_port.save.return_value = saved_user
        self.patient_repository_port.find_by_user_id.return_value = None
        self.patient_repository_port.find_by_document.return_value = None
        self.patient_repository_port.find_by_phone.return_value = Mock()

        with pytest.raises(PatientPhoneAlreadyRegisteredException):
            self.use_case.execute(command)

    def test_register_user_doctor_profile_already_exists(self):
        """Should register user doctor profile already exists."""
        command = RegisterUserCommand(
            first_name="Greg",
            last_name="House",
            email="house@example.com",
            role="doctor",
            profile=DoctorProfileCommand("LIC1", 10, 1, "MD", "Bio"),
            role_recorder="doctor",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None

        saved_user = Mock(id=1)
        self.user_repository_port.save.return_value = saved_user
        self.doctor_repository_port.find_by_user_id.return_value = Mock()

        with pytest.raises(DoctorProfileAlreadyExistsException):
            self.use_case.execute(command)

    def test_register_user_doctor_license_already_registered(self):
        """Should register user doctor license already registered."""
        command = RegisterUserCommand(
            first_name="Greg",
            last_name="House",
            email="house@example.com",
            role="doctor",
            profile=DoctorProfileCommand("LIC1", 10, 1, "MD", "Bio"),
            role_recorder="doctor",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None

        saved_user = Mock(id=1)
        self.user_repository_port.save.return_value = saved_user
        self.doctor_repository_port.find_by_user_id.return_value = None
        self.doctor_repository_port.find_by_license_number.return_value = Mock()

        with pytest.raises(DoctorLicenseNumberAlreadyRegisteredException):
            self.use_case.execute(command)

    def test_register_user_doctor_profile_missing(self):
        """Should register user doctor profile missing."""
        command = RegisterUserCommand(
            first_name="Greg",
            last_name="House",
            email="house@example.com",
            role="doctor",
            profile=None,
            role_recorder="doctor",
        )

        self.authorization_policy_service_port.can_register.return_value = True
        self.staff_email_policy_service_port.is_allowed.return_value = True
        self.user_repository_port.find_by_email.return_value = None
        self.password_service_port.generate.return_value = Mock(value="Temp123!")
        self.password_hash_service_port.hashed.return_value = "hashed"

        with pytest.raises(MissingFieldException):
            self.use_case.execute(command)
