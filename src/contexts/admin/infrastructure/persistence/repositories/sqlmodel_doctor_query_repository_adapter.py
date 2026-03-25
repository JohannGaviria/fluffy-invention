"""This module contains the SQLModelDoctorQueryRepositoryAdapter, which is an adapter for querying doctors using SQLModel."""

from uuid import UUID

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import Session, select

from src.contexts.admin.domain.ports.repositories.doctor_query_repository_port import (
    DoctorQueryRepositoryPort,
)
from src.contexts.admin.domain.value_objects.doctor_summary_vo import DoctorSummaryVO
from src.contexts.admin.infrastructure.persistence.mappers.doctor_query_mapper import (
    DoctorQueryMapper,
)
from src.contexts.auth.infrastructure.persistence.models.model import DoctorModel
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger


class SQLModelDoctorQueryRepositoryAdapter(DoctorQueryRepositoryPort):
    """Adapter for querying doctors using SQLModel."""

    def __init__(
        self,
        session: Session,
        logger: Logger,
    ) -> None:
        """Initialize the SQLModelDoctorQueryRepositoryAdapter.

        Args:
            session (Session): Session object.
            logger (Logger): Logger object.
        """
        self.session = session
        self.logger = logger

    def find_active_doctor(self, doctor_id: UUID) -> DoctorSummaryVO | None:
        """Find an active doctor by ID.

        Args:
            doctor_id (UUID): The ID of the doctor to find.

        Returns:
            DoctorSummaryVO | None: The doctor summary value object if found, otherwise None.
        """
        try:
            model = self.session.exec(
                select(DoctorModel).where(DoctorModel.id == doctor_id)
            ).first()
            return DoctorQueryMapper.to_vo(model) if model else None
        except OperationalError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except SQLAlchemyError as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e
