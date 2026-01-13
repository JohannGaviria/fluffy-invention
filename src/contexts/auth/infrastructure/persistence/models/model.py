"""This module contains the User persistence model definition."""

from datetime import UTC, datetime
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
