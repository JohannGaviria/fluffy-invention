"""This module contains the SQLModel repository adapter for Patient Repository Port."""

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import Session

from src.contexts.auth.domain.entities.entity import PatientEntity
from src.contexts.auth.domain.ports.repositories.patient_repository_port import (
    PatientRepositoryPort,
)
from src.contexts.auth.infrastructure.persistence.mappers.mapper import PatientMapper
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
