"""This module contains the SQLModel repository adapter for User Repository Port."""

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import Session, select

from src.contexts.auth.domain.entities.entity import UserEntity
from src.contexts.auth.domain.ports.user_repository_port import UserRepositoryPort
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.infrastructure.persistence.mappers.mapper import UserMapper
from src.contexts.auth.infrastructure.persistence.models.model import UserModel
from src.shared.domain.exception import (
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
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e
