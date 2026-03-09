"""This module contains the SQLModel repository adapter for Doctor Repository Port."""

from uuid import UUID

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import Session, select

from src.contexts.auth.domain.entities.entity import DoctorEntity
from src.contexts.auth.domain.ports.repositories.doctor_repository_port import (
    DoctorRepositoryPort,
)
from src.contexts.auth.infrastructure.persistence.mappers.mapper import DoctorMapper
from src.contexts.auth.infrastructure.persistence.models.model import DoctorModel
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger


class SQLModelDoctorRepositoryAdapter(DoctorRepositoryPort):
    """SQLModel repository adapter for Doctor Repository Port."""

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

    def find_by_id(self, id: UUID) -> DoctorEntity | None:
        """Find a doctor by ID.

        Args:
            id (UUID): ID of the doctor to find.

        Returns:
            DoctorEntity | None: The found doctor entity or None if not found.
        """
        try:
            model = self.session.exec(
                select(DoctorModel).where(DoctorModel.id == id)
            ).first()
            return DoctorMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def find_by_user_id(self, user_id: UUID) -> DoctorEntity | None:
        """Find a doctor by user ID.

        Args:
            user_id (UUID): User ID to search for.

        Returns:
            DoctorEntity | None: The found doctor entity or None if not found.
        """
        try:
            model = self.session.exec(
                select(DoctorModel).where(DoctorModel.user_id == user_id)
            ).first()
            return DoctorMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def find_by_license_number(self, license_number: str) -> DoctorEntity | None:
        """Find a doctor by license number.

        Args:
            license_number (str): License number to search for.

        Returns:
            DoctorEntity | None: The found doctor entity or None if not found.
        """
        try:
            model = self.session.exec(
                select(DoctorModel).where(DoctorModel.license_number == license_number)
            ).first()
            return DoctorMapper.to_entity(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def is_active(self, doctor_id: UUID) -> bool:
        """Check if a doctor is active.

        Args:
            doctor_id (UUID): Doctor ID to check.

        Returns:
            bool: True if the doctor is active, False otherwise.
        """
        try:
            model = self.session.exec(
                select(DoctorModel).where(DoctorModel.id == doctor_id)
            ).first()
            return model.is_active if model else False
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    def save(self, entity: DoctorEntity) -> None:
        """Save the given entity.

        Args:
            entity (DoctorEntity): Doctor entity to save.

        Returns:
            None.
        """
        try:
            model = DoctorMapper.to_model(entity)
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
