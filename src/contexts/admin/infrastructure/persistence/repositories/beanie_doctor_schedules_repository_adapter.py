"""This module contains the BeanieDoctorSchedulesRepositoryAdapter, which is an adapter for the doctor schedules repository using Beanie ODM for MongoDB."""

from uuid import UUID

from src.contexts.admin.domain.entities.doctor_schedules_entity import (
    DoctorSchedulesEntity,
)
from src.contexts.admin.domain.ports.repositories.doctor_schedules_repository_port import (
    DoctorSchedulesRepositoryPort,
)
from src.contexts.admin.infrastructure.persistence.documents.doctor_schedules_document import (
    DoctorSchedulesDocument,
)
from src.contexts.admin.infrastructure.persistence.mappers.doctor_schedules_mapper import (
    DoctorSchedulesMapper,
)
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)
from src.shared.infrastructure.logging.logger import Logger


class BeanieDoctorSchedulesRepositoryAdapter(DoctorSchedulesRepositoryPort):
    """Adapter for the doctor schedules repository using Beanie ODM for MongoDB."""

    def __init__(self, logger: Logger) -> None:
        """Initialize the repository adapter.

        Args:
            logger (Logger): The logger for logging errors in the repository.
        """
        self.logger = logger

    async def doctor_schedule_exists(self, doctor_id: UUID) -> bool:
        """Check if a doctor schedule exists for the given doctor ID.

        Args:
            doctor_id (UUID): The ID of the doctor to check for existing schedules.

        Returns:
            bool: True if a schedule exists for the doctor, False otherwise.

        Raises:
            DatabaseConnectionException: If there is a connection error with the database.
            UnexpectedDatabaseException: If there is any other unexpected error during
                database operations.
        """
        try:
            document = await DoctorSchedulesDocument.find_one(
                DoctorSchedulesDocument.doctor_id == doctor_id
            )
            return True if document else False
        except ConnectionError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except Exception as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e

    async def save(self, entity: DoctorSchedulesEntity) -> None:
        """Save a DoctorSchedulesEntity to the database.

        Args:
            entity (DoctorSchedulesEntity): The entity to save.

        Raises:
            DatabaseConnectionException: If there is a connection error with the database.
            UnexpectedDatabaseException: If there is any other unexpected error during
                database operations.
        """
        try:
            document = DoctorSchedulesMapper.to_document(entity)
            await document.save()
        except ConnectionError as e:
            self.logger.error(message="Could not connect to database.", error=str(e))
            raise DatabaseConnectionException("Could not connect to database.") from e
        except Exception as e:
            self.logger.error(message="Unexpected database error.", error=str(e))
            raise UnexpectedDatabaseException("Unexpected database error.") from e
