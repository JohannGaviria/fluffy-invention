"""This module contains the DoctorSchedulesMapper class for mapping."""

from src.contexts.admin.domain.entities.doctor_schedules_entity import (
    DoctorSchedulesEntity,
)
from src.contexts.admin.infrastructure.persistence.documents.doctor_schedules_document import (
    DoctorSchedulesDocument,
)


class DoctorSchedulesMapper:
    """Mapper class for converting between DoctorSchedulesEntity and DoctorSchedulesDocument."""

    @staticmethod
    def to_document(entity: DoctorSchedulesEntity) -> DoctorSchedulesDocument:
        """Map a DoctorSchedulesEntity to a DoctorSchedulesDocument.

        Args:
            entity (DoctorSchedulesEntity): The entity to map.

        Returns:
            DoctorSchedulesDocument: The mapped document.
        """
        return DoctorSchedulesDocument(
            doctor_id=entity.doctor_id,
            schedules=entity.schedules.to_dict(),
            timezone=entity.timezone.value(),
        )
