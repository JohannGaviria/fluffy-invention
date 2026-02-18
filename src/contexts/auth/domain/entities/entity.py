"""This module contains the entities definition for the authentication domain."""

from dataclasses import dataclass
from datetime import UTC, date, datetime
from enum import Enum
from uuid import UUID, uuid4

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.shared.domain.entities.entity import BaseEntity
from src.shared.domain.exceptions.exception import MissingFieldException


class RolesEnum(str, Enum):
    """Roles available for users in the authentication domain.

    Attributes:
        PATIENT (str): Role for patients.
        DOCTOR (str): Role for doctors.
        RECEPTIONIST (str): Role for receptionists.
        ADMIN (str): Role for administrators.
    """

    PATIENT = ("patient",)
    DOCTOR = ("doctor",)
    RECEPTIONIST = ("receptionist",)
    ADMIN = "admin"


@dataclass
class UserEntity(BaseEntity):
    """User entity representing a user in the authentication domain.

    Attributes:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (EmailVO): Email value object of the user.
        password_hash (PasswordHashVO): Password hash value object of the user.
        role (RolesEnum): Role of the user.
        is_active (bool): Indicates if the user is active.
    """

    first_name: str
    last_name: str
    email: EmailVO
    password_hash: PasswordHashVO
    role: RolesEnum
    is_active: bool

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: EmailVO,
        password_hash: PasswordHashVO,
        role: RolesEnum,
    ) -> "UserEntity":
        """Factory method to create a new UserEntity.

        Args:
            first_name (str): first name of the user.
            last_name (str): last name of the user.
            email (EmailVO): email of the user.
            password_hash (PasswordHashVO): password hash of the user.
            role (RolesEnum): role of the user.

        Returns:
            UserEntity: A new instance of UserEntity.
        """
        REQUIRED_FIELDS = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password_hash": password_hash,
            "role": role,
        }

        for field, value in REQUIRED_FIELDS.items():
            if not value:
                raise MissingFieldException(field, "is required")

        now = datetime.now(UTC)
        return cls(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
            role=role,
            is_active=False,
            created_at=now,
            updated_at=now,
        )


@dataclass
class PatientEntity(BaseEntity):
    """Patient entity representing a patient in the authentication domain.

    Attributes:
        user_id (UUID): ID of the associated user.
        document (str): Document number of the patient.
        phone (str): Phone number of the patient.
        birth_date (date): Birth date of the patient.
    """

    user_id: UUID
    document: str
    phone: str
    birth_date: date

    @classmethod
    def create(
        cls,
        user_id: UUID,
        document: str,
        phone: str,
        birth_date: date,
    ) -> "PatientEntity":
        """Factory method to create a new PatientEntity.

        Args:
            user_id (UUID): ID of the associated user.
            document (str): Document number of the patient.
            phone (str): Phone number of the patient.
            birth_date (date): Birth date of the patient.

        Returns:
            PatientEntity: A new instance of PatientEntity.
        """
        REQUIRED_FIELDS = {
            "user_id": user_id,
            "document": document,
            "phone": phone,
            "birth_date": birth_date,
        }

        for field, value in REQUIRED_FIELDS.items():
            if not value:
                raise MissingFieldException(field, "is required")

        now = datetime.now(UTC)
        return cls(
            id=uuid4(),
            user_id=user_id,
            document=document,
            phone=phone,
            birth_date=birth_date,
            created_at=now,
            updated_at=now,
        )


@dataclass
class DoctorEntity(BaseEntity):
    """Doctor entity representing a doctor in the authentication domain.

    Attributes:
        user_id (UUID): ID of the associated user.
        specialty_id (UUID): ID of the specialty.
        license_number (str): License number of the doctor.
        experience_years (int): Years of experience.
        is_active (bool): Indicates if the doctor is active.
        qualifications (str | None): Qualifications of the doctor.
        bio (str | None): Bio of the doctor.
    """

    user_id: UUID
    license_number: str
    experience_years: int
    is_active: bool
    specialty_id: UUID | None
    qualifications: str | None
    bio: str | None

    @classmethod
    def create(
        cls,
        user_id: UUID,
        license_number: str,
        experience_years: int,
        is_active: bool = True,
        specialty_id: UUID | None = None,
        qualifications: str | None = None,
        bio: str | None = None,
    ) -> "DoctorEntity":
        """Factory method to create a new DoctorEntity.

        Args:
            user_id (UUID): ID of the associated user.
            license_number (str): License number of the doctor.
            experience_years (int): Years of experience.
            is_active (bool): Indicates if the doctor is active.
            specialty_id (UUID | None): ID of the specialty.
            qualifications (str | None): Qualifications of the doctor.
            bio (str | None): Bio of the doctor.

        Returns:
            DoctorEntity: A new instance of DoctorEntity.
        """
        REQUIRED_FIELDS = {
            "user_id": user_id,
            "license_number": license_number,
            "experience_years": experience_years,
        }

        for field, value in REQUIRED_FIELDS.items():
            if not value:
                raise MissingFieldException(field, "is required")

        now = datetime.now(UTC)
        return cls(
            id=uuid4(),
            user_id=user_id,
            specialty_id=specialty_id,
            license_number=license_number,
            experience_years=experience_years,
            qualifications=qualifications,
            bio=bio,
            is_active=is_active,
            created_at=now,
            updated_at=now,
        )
