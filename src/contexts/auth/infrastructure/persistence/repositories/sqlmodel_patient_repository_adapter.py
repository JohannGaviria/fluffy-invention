"""This module contains the SQLModel repository adapter for Patient Repository Port."""

from uuid import UUID

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import Session, select

from src.contexts.auth.domain.entities.entity import PatientEntity
from src.contexts.auth.domain.ports.repositories.patient_repository_port import (
    PatientRepositoryPort,
)
from src.contexts.auth.infrastructure.persistence.mappers.mapper import PatientMapper
from src.contexts.auth.infrastructure.persistence.models.model import PatientModel
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger


class SQLModelPatientRepositoryAdapter(PatientRepositoryPort):
    """SQLModel repository adapter for Patient Repository Port."""

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

    def find_by_user_id(self, user_id: UUID) -> PatientEntity | None:
        """Find a patient by user ID.

        Args:
            user_id (UUID): User ID to search for.

        Returns:
            PatientEntity | None: The found patient entity or None if not found.
        """
        try:
            model = self.session.exec(
                select(PatientModel).where(PatientModel.user_id == str(user_id))
            ).first()
            return PatientMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def find_by_document(self, document: str) -> PatientEntity | None:
        """Find a patient by document.

        Args:
            document (str): Document to search for.

        Returns:
            PatientEntity | None: The found patient entity or None if not found.
        """
        try:
            model = self.session.exec(
                select(PatientModel).where(PatientModel.document == document)
            ).first()
            return PatientMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def find_by_phone(self, phone: str) -> PatientEntity | None:
        """Find a patient by phone.

        Args:
            phone (str): Phone to search for.

        Returns:
            PatientEntity | None: The found patient entity or None if not found.
        """
        try:
            model = self.session.exec(
                select(PatientModel).where(PatientModel.phone == phone)
            ).first()
            return PatientMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def save(self, entity: PatientEntity) -> None:
        """Save the given entity.

        Args:
            entity (PatientEntity): Patient entity to save.

        Returns:
            None.
        """
        try:
            model = PatientMapper.to_model(entity)
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
