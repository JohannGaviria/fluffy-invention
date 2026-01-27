"""This module contains the UserMapper class for mapping between UserModel and UserEntity."""

from src.contexts.auth.domain.entities.entity import (
    DoctorEntity,
    PatientEntity,
    RolesEnum,
    UserEntity,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.contexts.auth.infrastructure.persistence.models.model import (
    DoctorModel,
    PatientModel,
    UserModel,
)


class UserMapper:
    """Mapper class for converting between UserModel and UserEntity."""

    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        """Maps UserModel to UserEntity.

        Args:
            model (UserModel): The user model instance.

        Returns:
            UserEntity: The mapped user entity instance.
        """
        return UserEntity(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=EmailVO(model.email),
            password_hash=PasswordHashVO(model.password),
            role=RolesEnum(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: UserEntity) -> UserModel:
        """Maps UserEntity to UserModel.

        Args:
            entity (UserEntity): The user entity instance.

        Returns:
            UserModel: The mapped user model instance.
        """
        return UserModel(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email.value,
            password=entity.password_hash.value,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class PatientMapper:
    """Mapper class for converting between PatientModel and PatientEntity."""

    @staticmethod
    def to_model(entity: PatientEntity) -> PatientModel:
        """Maps PatientEntity to PatientModel.

        Args:
            entity (PatientEntity): The Patient entity instance.

        Returns:
            PatientModel: The mapped Patient model instance.
        """
        return PatientModel(
            id=entity.id,
            user_id=entity.user_id,
            document=entity.document,
            phone=entity.phone,
            birth_date=entity.birth_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class DoctorMapper:
    """Mapper class for converting between DoctorModel and DoctorEntity."""

    @staticmethod
    def to_model(entity: DoctorEntity) -> DoctorModel:
        """Maps DoctorEntity to DoctorModel.

        Args:
            entity (DoctorEntity): The Doctor entity instance.

        Returns:
            DoctorModel: The mapped Doctor model instance.
        """
        return DoctorModel(
            id=entity.id,
            user_id=entity.user_id,
            specialty_id=entity.specialty_id,
            license_number=entity.license_number,
            experience_years=entity.experience_years,
            qualifications=entity.qualifications,
            bio=entity.bio,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
