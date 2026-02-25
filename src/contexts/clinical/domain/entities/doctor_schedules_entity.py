"""This module contains the entity for the DoctorSchedules."""

from dataclasses import dataclass
from uuid import UUID

from src.contexts.clinical.domain.value_objects.schedule_vo import ScheduleVO
from src.shared.domain.entities.entity import BaseEntity


@dataclass
class DoctorSchedulesEntity(BaseEntity):
    """Entity for the DoctorSchedules.

    Attributes:
        doctor_id (UUID): The unique identifier of the doctor.
        schedule (ScheduleVO): The schedule of the doctor.
        timezone (str): The timezone of the doctor.
    """

    doctor_id: UUID
    schedule: ScheduleVO
    timezone: str
