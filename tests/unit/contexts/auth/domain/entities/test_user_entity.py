"""Unit tests for UserEntity."""

from datetime import UTC, datetime

import pytest

from src.contexts.auth.domain.entities.entity import RolesEnum, UserEntity
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.shared.domain.exceptions.exception import MissingFieldException


class TestUserEntity:
    """Unit tests for UserEntity."""

    def test_should_create_user_entity_successfully(self):
        """Should create UserEntity successfully with valid data."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        user = UserEntity.create(
            first_name="John",
            last_name="Doe",
            email=email,
            password_hash=password_hash,
            role=RolesEnum.PATIENT,
        )

        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == email
        assert user.password_hash == password_hash
        assert user.role == RolesEnum.PATIENT
        assert user.is_active is False
        assert user.id is not None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_should_create_user_with_different_roles(self):
        """Should create users with different roles."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        roles = [
            RolesEnum.PATIENT,
            RolesEnum.DOCTOR,
            RolesEnum.RECEPTIONIST,
            RolesEnum.ADMIN,
        ]

        for role in roles:
            user = UserEntity.create(
                first_name="John",
                last_name="Doe",
                email=email,
                password_hash=password_hash,
                role=role,
            )
            assert user.role == role

    def test_should_raise_missing_field_exception_for_empty_first_name(self):
        """Should raise MissingFieldException for empty first_name."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        with pytest.raises(MissingFieldException) as exc_info:
            UserEntity.create(
                first_name="",
                last_name="Doe",
                email=email,
                password_hash=password_hash,
                role=RolesEnum.PATIENT,
            )
        assert exc_info.value.field == "first_name"

    def test_should_raise_missing_field_exception_for_empty_last_name(self):
        """Should raise MissingFieldException for empty last_name."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        with pytest.raises(MissingFieldException) as exc_info:
            UserEntity.create(
                first_name="John",
                last_name="",
                email=email,
                password_hash=password_hash,
                role=RolesEnum.PATIENT,
            )
        assert exc_info.value.field == "last_name"

    def test_should_raise_missing_field_exception_for_none_email(self):
        """Should raise MissingFieldException for None email."""
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        with pytest.raises(MissingFieldException) as exc_info:
            UserEntity.create(
                first_name="John",
                last_name="Doe",
                email=None,
                password_hash=password_hash,
                role=RolesEnum.PATIENT,
            )
        assert exc_info.value.field == "email"

    def test_should_raise_missing_field_exception_for_none_password_hash(self):
        """Should raise MissingFieldException for None password_hash."""
        email = EmailVO("user@example.com")

        with pytest.raises(MissingFieldException) as exc_info:
            UserEntity.create(
                first_name="John",
                last_name="Doe",
                email=email,
                password_hash=None,
                role=RolesEnum.PATIENT,
            )
        assert exc_info.value.field == "password_hash"

    def test_should_raise_missing_field_exception_for_none_role(self):
        """Should raise MissingFieldException for None role."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        with pytest.raises(MissingFieldException) as exc_info:
            UserEntity.create(
                first_name="John",
                last_name="Doe",
                email=email,
                password_hash=password_hash,
                role=None,
            )
        assert exc_info.value.field == "role"

    def test_should_have_utc_timestamps(self):
        """Should have UTC timezone-aware timestamps."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        user = UserEntity.create(
            first_name="John",
            last_name="Doe",
            email=email,
            password_hash=password_hash,
            role=RolesEnum.PATIENT,
        )

        assert user.created_at.tzinfo == UTC
        assert user.updated_at.tzinfo == UTC

    def test_should_have_same_created_and_updated_timestamps(self):
        """Should have same created_at and updated_at on creation."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        user = UserEntity.create(
            first_name="John",
            last_name="Doe",
            email=email,
            password_hash=password_hash,
            role=RolesEnum.PATIENT,
        )

        assert user.created_at == user.updated_at

    def test_should_generate_unique_ids(self):
        """Should generate unique IDs for different users."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        user1 = UserEntity.create(
            first_name="John",
            last_name="Doe",
            email=email,
            password_hash=password_hash,
            role=RolesEnum.PATIENT,
        )

        user2 = UserEntity.create(
            first_name="Jane",
            last_name="Smith",
            email=email,
            password_hash=password_hash,
            role=RolesEnum.DOCTOR,
        )

        assert user1.id != user2.id

    def test_should_set_is_active_to_false_by_default(self):
        """Should set is_active to False by default on creation."""
        email = EmailVO("user@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        user = UserEntity.create(
            first_name="John",
            last_name="Doe",
            email=email,
            password_hash=password_hash,
            role=RolesEnum.PATIENT,
        )

        assert user.is_active is False
