"""Unit tests for UserMapper."""

from datetime import UTC, datetime
from uuid import uuid4

from src.contexts.auth.domain.entities.entity import RolesEnum, UserEntity
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.contexts.auth.infrastructure.persistence.mappers.mapper import UserMapper
from src.contexts.auth.infrastructure.persistence.models.model import UserModel


class TestUserMapper:
    """Unit tests for UserMapper."""

    def test_should_map_model_to_entity_successfully(self):
        """Should map UserModel to UserEntity successfully."""
        now = datetime.now(UTC)
        user_id = uuid4()

        model = UserModel(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K",
            role=RolesEnum.PATIENT,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        entity = UserMapper.to_entity(model)

        assert isinstance(entity, UserEntity)
        assert entity.id == user_id
        assert entity.first_name == "John"
        assert entity.last_name == "Doe"
        assert isinstance(entity.email, EmailVO)
        assert entity.email.value == "john@example.com"
        assert isinstance(entity.password_hash, PasswordHashVO)
        assert (
            entity.password_hash.value
            == "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )
        assert entity.role == RolesEnum.PATIENT
        assert entity.is_active is True
        assert entity.created_at == now
        assert entity.updated_at == now

    def test_should_map_entity_to_model_successfully(self):
        """Should map UserEntity to UserModel successfully."""
        now = datetime.now(UTC)
        user_id = uuid4()
        email = EmailVO("john@example.com")
        password_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        entity = UserEntity(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email=email,
            password_hash=password_hash,
            role=RolesEnum.PATIENT,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        model = UserMapper.to_model(entity)

        assert isinstance(model, UserModel)
        assert model.id == user_id
        assert model.first_name == "John"
        assert model.last_name == "Doe"
        assert model.email == "john@example.com"
        assert (
            model.password
            == "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )
        assert model.role == RolesEnum.PATIENT
        assert model.is_active is True
        assert model.created_at == now
        assert model.updated_at == now

    def test_should_map_different_roles_correctly(self):
        """Should map different user roles correctly."""
        now = datetime.now(UTC)
        roles = [
            RolesEnum.PATIENT,
            RolesEnum.DOCTOR,
            RolesEnum.RECEPTIONIST,
            RolesEnum.ADMIN,
        ]

        for role in roles:
            model = UserModel(
                id=uuid4(),
                first_name="Test",
                last_name="User",
                email="test@example.com",
                password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K",
                role=role,
                is_active=False,
                created_at=now,
                updated_at=now,
            )

            entity = UserMapper.to_entity(model)
            assert entity.role == role

            back_to_model = UserMapper.to_model(entity)
            assert back_to_model.role == role

    def test_should_preserve_is_active_state(self):
        """Should preserve is_active state during mapping."""
        now = datetime.now(UTC)

        for is_active in [True, False]:
            model = UserModel(
                id=uuid4(),
                first_name="Test",
                last_name="User",
                email="test@example.com",
                password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K",
                role=RolesEnum.PATIENT,
                is_active=is_active,
                created_at=now,
                updated_at=now,
            )

            entity = UserMapper.to_entity(model)
            assert entity.is_active == is_active
