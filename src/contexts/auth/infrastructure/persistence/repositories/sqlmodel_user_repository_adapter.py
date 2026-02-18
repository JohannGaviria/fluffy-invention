"""This module contains the SQLModel repository adapter for User Repository Port."""

from uuid import UUID

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import Session, select

from src.contexts.auth.domain.entities.entity import RolesEnum, UserEntity
from src.contexts.auth.domain.ports.repositories.user_repository_port import (
    UserRepositoryPort,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.contexts.auth.infrastructure.persistence.mappers.mapper import UserMapper
from src.contexts.auth.infrastructure.persistence.models.model import UserModel
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger


class SQLModelRepositoryAdapter(UserRepositoryPort):
    """SQLModel repository adapter for User Repository Port."""

    def __init__(
        self,
        session: Session,
        logger: Logger,
    ) -> None:
        """Initialize the SQLModelRepositoryAdapter.

        Args:
            session (Session): Session object.
            logger (Logger): Logger object.
        """
        self.session = session
        self.logger = logger

    def find_by_id(self, id: UUID) -> UserEntity | None:
        """Retrieve user by id.

        Args:
            id (UUID): The id to search for.

        Returns:
            UserEntity | None: User entity if found, else None.
        """
        try:
            model = self.session.exec(
                select(UserModel).where(UserModel.id == id)
            ).first()
            return UserMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def find_by_email(self, email: EmailVO) -> UserEntity | None:
        """Retrieve user by email.

        Args:
            email (EmailVO): Email vo representing the user.

        Returns:
            UserEntity | None: User entity if found, else None.
        """
        try:
            model = self.session.exec(
                select(UserModel).where(UserModel.email == email.value)
            ).first()
            return UserMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def save(self, entity: UserEntity) -> UserEntity:
        """Save the given entity.

        Args:
            entity (UserEntity): User entity to save.

        Returns:
            UserEntity: User entity saved.
        """
        try:
            model = UserMapper.to_model(entity)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return UserMapper.to_entity(model)
        except OperationalError as e:
            self.session.rollback()
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(message="Unexpected database error.,", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.,") from e

    def status_update(self, status: bool, user_id: UUID) -> None:
        """Update the active status of a user.

        Args:
            status (bool): New active status.
            user_id (UUID): ID of the user to update.
        """
        try:
            model = self.session.exec(
                select(UserModel).where(UserModel.id == user_id)
            ).first()
            if model:
                model.is_active = status
                self.session.add(model)
                self.session.commit()
        except OperationalError as e:
            self.session.rollback()
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def find_by_role(self, role: RolesEnum) -> list[UserEntity]:
        """Find users by their role.

        Args:
            role (RolesEnum): The role to search for.

        Returns:
            list[UserEntity]: A list of user entities with the specified role.
        """
        try:
            models = self.session.exec(
                select(UserModel).where(UserModel.role == role)
            ).all()
            return [UserMapper.to_entity(model) for model in models]
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def update_password(self, user_id: UUID, new: PasswordHashVO) -> None:
        """Update the password of a user.

        Args:
            user_id (UUID): The unique identifier of the user.
            new (PasswordHashVO): The new password hash to update.

        Returns:
            None
        """
        try:
            model = self.session.exec(
                select(UserModel).where(UserModel.id == user_id)
            ).first()
            if model:
                model.password = str(new)
                self.session.add(model)
                self.session.commit()
        except OperationalError as e:
            self.session.rollback()
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error..") from e
