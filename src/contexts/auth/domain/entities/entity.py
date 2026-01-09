"""This module contains the entities definition for the authentication domain."""

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.shared.domain.entity import BaseEntity
from src.shared.domain.exception import MissingFieldException


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
