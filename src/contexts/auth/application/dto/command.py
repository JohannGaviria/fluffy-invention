"""This module contains the DTO for the RegisterUserCommand."""

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class PatientProfileCommand:
    """Profile command DTO for patient information.

    Attributes:
        document (str): The document number of the patient.
        phone (str): The phone number of the patient.
        birth_date (date): The birth date of the patient.
    """

    document: str
    phone: str
    birth_date: date


@dataclass
class DoctorProfileCommand:
    """Command DTO for doctor profile information.

    Attributes:
        specialty_id (UUID): The ID of the doctor's specialty.
        license_number (str): The doctor's license number.
        experience_years (int): The number of years of experience the doctor has.
        is_active (bool): Indicates if the doctor is currently active.
        qualifications (str | None): The qualifications of the doctor.
        bio (str | None): A brief biography of the doctor.
    """

    specialty_id: UUID
    license_number: str
    experience_years: int
    is_active: bool
    qualifications: str | None = None
    bio: str | None = None


@dataclass
class RegisterUserCommand:
    """Command DTO for registering a new user.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        role (str): The role assigned to the user.
        role_recorder (str): The role of the user performing the registration.
    """

    first_name: str
    last_name: str
    email: str
    role: str
    role_recorder: str
    profile: PatientProfileCommand | DoctorProfileCommand | None = None


@dataclass
class LoginCommand:
    """Command DTO for login of user.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    email: str
    password: str


@dataclass
class CreateAdminCommand:
    """Command DTO for registering a new user.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
    """

    first_name: str
    last_name: str
    email: str
