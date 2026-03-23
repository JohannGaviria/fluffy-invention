"""This module contains the Beanie document model for doctor schedules."""

from typing import Annotated
from uuid import UUID

from beanie import Document, Indexed
from pydantic import BaseModel

from src.contexts.admin.domain.enums.days_of_week_enum import DaysOfWeekEnum


class SchedulesSlot(BaseModel):
    """Model representing a single schedule slot for a doctor.

    Attributes:
        start_time (str): The start time of the slot in "HH:MM:SS" format.
        end_time (str): The end time of the slot in "HH:MM:SS" format.
        slot_duration_minutes (int): The duration of the slot in minutes.
        is_available (bool): Whether the slot is available for booking.
    """

    start_time: str
    end_time: str
    slot_duration_minutes: int
    is_available: bool


class DoctorSchedulesDocument(Document):
    """Document representing a doctor's schedules.

    Attributes:
        doctor_id (UUID): The unique identifier of the doctor.
        schedules (dict[DaysOfWeekEnum, list[SchedulesSlot]]):
            A dictionary mapping days of the week to lists of schedule slots.
        timezone (str): The doctor's timezone.
    """

    doctor_id: Annotated[UUID, Indexed(unique=True)]
    schedules: dict[DaysOfWeekEnum, list[SchedulesSlot]]
    timezone: str

    class Settings:
        """Beanie document settings."""

        name = "doctor_schedules"
