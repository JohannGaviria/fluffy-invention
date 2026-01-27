"""This module contains the SQLModel repository adapter for Doctor Repository Port."""

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import Session

from src.contexts.auth.domain.entities.entity import DoctorEntity
from src.contexts.auth.domain.ports.doctor_repository_port import DoctorRepositoryPort
from src.contexts.auth.infrastructure.persistence.mappers.mapper import DoctorMapper
from src.shared.domain.exception import (
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
