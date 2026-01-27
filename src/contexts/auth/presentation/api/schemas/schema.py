"""This module contains schemas for authentication-related requests and responses."""

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from src.contexts.auth.application.dto.command import (
    DoctorProfileCommand,
    LoginCommand,
    PatientProfileCommand,
    RegisterUserCommand,
)
from src.contexts.auth.domain.entities.entity import RolesEnum


class BaseProfile(BaseModel):
    """Base schema for user profiles.

    Attributes:
        profile_type (str): The type of the profile (e.g., "patient", "doctor").
    """

    profile_type: str


class PatientProfileRequest(BaseProfile):
    """Request schema for patient profile.

    Attributes:
        document (str): The document number of the patient.
        phone (str): The phone number of the patient.
        birth_date (date): The birth date of the patient.
    """

    profile_type: Literal["patient"]
    document: str
    phone: str
    birth_date: date

    model_config = {
        "json_schema_extra": {
            "example": {
                "profile_type": "patient",
                "document": "123456789",
                "phone": "+1234567890",
                "birth_date": "1990-01-01",
            }
        }
    }

    def to_command(self) -> PatientProfileCommand:
        """Converts the request data to a PatientProfileCommand.

        Returns:
            PatientProfileCommand: The command object with the request data.
        """
        return PatientProfileCommand(
            document=self.document,
            phone=self.phone,
            birth_date=self.birth_date,
        )


class DoctorProfileRequest(BaseProfile):
    """Request schema for doctor profile.

    Attributes:
        specialty_id (UUID): The unique identifier for the doctor's specialty.
        license_number (str): The medical license number of the doctor.
        experience_years (int): The number of years of experience the doctor has.
        is_active (bool): Indicates if the doctor's profile is active.
        qualifications (str | None): The qualifications of the doctor.
        bio (str | None): A brief biography of the doctor.
    """

    profile_type: Literal["doctor"]
    specialty_id: UUID
    license_number: str
    experience_years: int
    is_active: bool
    qualifications: str | None = Field(default=None)
    bio: str | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "profile_type": "doctor",
                "specialty_id": "d290f1ee-6c54-4b018-9d5f-ff5af830be8a",
                "license_number": "MED123456",
                "experience_years": 5,
                "is_active": True,
                "qualifications": "Board Certified in Internal Medicine",
                "bio": "Experienced physician with a passion for patient care.",
            }
        }
    }

    def to_command(self) -> DoctorProfileCommand:
        """Converts the request data to a DoctorProfileCommand.

        Returns:
            DoctorProfileCommand: The command object with the request data.
        """
        return DoctorProfileCommand(
            specialty_id=self.specialty_id,
            license_number=self.license_number,
            experience_years=self.experience_years,
            is_active=self.is_active,
            qualifications=self.qualifications,
            bio=self.bio,
        )


class RegisterUserRequest(BaseModel):
    """Request schema for registering a new user.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        role (RolesEnum): The role assigned to the user.
        profile (PatientProfileRequest | DoctorProfileRequest | None): The profile information based on the user's role.
    """

    first_name: str
    last_name: str
    email: str
    role: RolesEnum
    profile: PatientProfileRequest | DoctorProfileRequest | None = Field(
        default=None, discriminator="profile_type"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "role": "patient",
                "profile": {
                    "profile_type": "patient",
                    "document": "123456789",
                    "phone": "+1234567890",
                    "birth_date": "1990-01-01",
                },
            }
        }
    }

    def to_command(self, role_recorder: RolesEnum) -> RegisterUserCommand:
        """Converts the request data to a RegisterUserCommand.

        Returns:
            RegisterUserCommand: The command object with the request data.
        """
        return RegisterUserCommand(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            role=self.role,
            role_recorder=role_recorder,
            profile=self.profile.to_command() if self.profile else None,
        )


class ActivateUserAccountRequest(BaseModel):
    """Request schema for activating a user account.

    Attributes:
        activation_code (str): The activation code sent to the user's email.
        email (str): The email address of the user.
    """

    activation_code: str
    email: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "activation_code": "HA23E0",
                "email": "john.doe@example.com",
            }
        }
    }


class LoginRequest(BaseModel):
    """Request schema for user login.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass!23",
            }
        }
    }

    def to_command(self) -> LoginCommand:
        """Converts the request data to a LoginCommand.

        Returns:
            LoginCommand: The command object with the request data.
        """
        return LoginCommand(
            email=self.email,
            password=self.password,
        )


class AccessTokenResponse(BaseModel):
    """Response schema for access token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token (e.g., Bearer).
        expires_at (str): The expiration datetime of the token.
        expires_in (int): The time in seconds until the token expires.
    """

    access_token: str
    token_type: str
    expires_at: datetime
    expires_in: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_at": "2026-01-25T05:39:54.815252Z",
                "expires_in": 3600,
            }
        }
    }

    @classmethod
    def from_response_dto(cls, dto: "AccessTokenResponse") -> "AccessTokenResponse":
        """Creates an AccessTokenResponse schema from a response DTO.

        Args:
            dto (AccessTokenResponse): The response DTO.

        Returns:
            AccessTokenResponse: The schema instance.
        """
        return cls(
            access_token=dto.access_token,
            token_type=dto.token_type,
            expires_at=dto.expires_at,
            expires_in=dto.expires_in,
        )
