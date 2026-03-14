"""This module contains the entity representing a doctor's schedules."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.contexts.admin.domain.value_objects.doctor_weekly_schedules_vo import (
    DoctorWeeklySchedulesVO,
)
from src.contexts.admin.domain.value_objects.timezone_vo import TimezoneVO
from src.shared.domain.entities.entity import BaseEntity
from src.shared.domain.exceptions.exception import MissingFieldException


@dataclass
class DoctorSchedulesEntity(BaseEntity):
    """Entity representing a doctor's schedules.

    Attributes:
        doctor_id (UUID): The unique identifier of the doctor.
        schedules (DoctorWeeklySchedulesVO): The doctor's weekly schedules.
        timezone (TimezoneVO): The doctor's timezone.
    """

    doctor_id: UUID
    schedules: DoctorWeeklySchedulesVO
    timezone: TimezoneVO

    @classmethod
    def create(
        cls, doctor_id: UUID, schedules: DoctorWeeklySchedulesVO, timezone: TimezoneVO
    ) -> "DoctorSchedulesEntity":
        """Factory method to create a new DoctorSchedulesEntity instance.

        Args:
            doctor_id (UUID): The unique identifier of the doctor.
            schedules (DoctorWeeklySchedulesVO): The doctor's weekly schedules.
            timezone (TimezoneVO): The doctor's timezone.

        Returns:
            DoctorSchedulesEntity: A new instance of DoctorSchedulesEntity.

        Raises:
            MissingFieldException: If any required field is missing.
            ValueError: If schedules or timezone validation fails.
        """
        if doctor_id is None:
            raise MissingFieldException("doctor_id", "is required")

        if schedules is None:
            raise MissingFieldException("schedules", "is required")

        if timezone is None:
            raise MissingFieldException("timezone", "is required")

        schedules.validate()
        timezone.validate()

        now = datetime.now(UTC)
        return DoctorSchedulesEntity(
            id=uuid4(),
            doctor_id=doctor_id,
            schedules=schedules,
            timezone=timezone,
            created_at=now,
            updated_at=now,
        )
