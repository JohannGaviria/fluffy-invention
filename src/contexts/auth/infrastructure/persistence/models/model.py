"""This module contains the User persistence model definition."""

from datetime import UTC, date, datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    """User persistence model.

    Attributes:
        id (UUID): Unique identifier for the user.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address.
        password (str): Hashed password for the user.
        role (str): Role of the user in the system.
        is_active (bool): Indicates if the user account is active.
        created_at (datetime): Timestamp of when the user was created.
        updated_at (datetime): Timestamp of the last update to the user.
    """

    __tablename__ = "users"
    id: UUID = Field(primary_key=True, index=True)
    first_name: str = Field(max_length=100, nullable=False)
    last_name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=255, nullable=False, unique=True, index=True)
    password: str = Field(max_length=255, nullable=False)
    role: str = Field(max_length=20, nullable=False, default="patient", index=True)
    is_active: bool = Field(default=False, nullable=False, index=True)
    created_at: datetime = Field(
        nullable=False, default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = Field(
        nullable=False, default_factory=lambda: datetime.now(UTC)
    )


# Apply migrations with: alembic revision --autogenerate -m "Add Patient and Doctor models"
class PatientModel(SQLModel, table=True):
    """Patient persistence model.

    Attributes:
        id (UUID): Unique identifier for the patient.
        user_id (UUID): Foreign key to the associated user.
        document (str): Patient's document number.
        phone (str): Patient's phone number.
        birth_date (date | None): Patient's birth date.
        created_at (datetime): Timestamp of when the patient was created.
        updated_at (datetime): Timestamp of the last update to the patient.
    """

    __tablename__ = "patients"
    id: UUID = Field(primary_key=True, index=True)
    user_id: UUID = Field(
        foreign_key="users.id", nullable=False, unique=True, index=True
    )
    document: str = Field(max_length=20, nullable=False, unique=True, index=True)
    phone: str = Field(max_length=20, nullable=False, index=True)
    birth_date: date = Field(nullable=False)
    created_at: datetime = Field(
        nullable=False, default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = Field(
        nullable=False, default_factory=lambda: datetime.now(UTC)
    )


class DoctorModel(SQLModel, table=True):
    """Doctor persistence model.

    Attributes:
        id (UUID): Unique identifier for the doctor.
        user_id (UUID): Foreign key to the associated user.
        specialty_id (UUID | None): Foreign key to the specialty.
        license_number (str): Doctor's license number.
        experience_years (int): Years of experience.
        qualifications (str | None): Doctor's qualifications.
        bio (str | None): Doctor's bio.
        is_active (bool): Indicates if the doctor is active.
        created_at (datetime): Timestamp of when the doctor was created.
        updated_at (datetime): Timestamp of the last update to the doctor.
    """

    __tablename__ = "doctors"
    id: UUID = Field(primary_key=True, index=True)
    user_id: UUID = Field(
        foreign_key="users.id", nullable=False, unique=True, index=True
    )
    specialty_id: UUID | None = Field(default=None, nullable=False, index=True)
    license_number: str = Field(max_length=50, nullable=False, unique=True, index=True)
    experience_years: int = Field(default=0, nullable=False)
    qualifications: str = Field(max_length=2000, nullable=True)
    bio: str = Field(max_length=1000, nullable=True)
    is_active: bool = Field(default=True, nullable=False, index=True)
    created_at: datetime = Field(
        nullable=False, default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = Field(
        nullable=False, default_factory=lambda: datetime.now(UTC)
    )
