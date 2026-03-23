"""This module contains the request schemas for the admin API."""

from datetime import time
from uuid import UUID

from pydantic import BaseModel

from src.contexts.admin.application.dto.command import (
    AssignDoctorSchedulesCommand,
    SchedulesSlotCommand,
)
from src.contexts.admin.domain.enums.days_of_week_enum import DaysOfWeekEnum


class SchedulesSlotRequest(BaseModel):
    """Request schema for a single schedule slot.

    Attributes:
        start_time (str): The start time of the slot in "HH:MM:SS" format.
        end_time (str): The end time of the slot in "HH:MM:SS" format.
        slot_duration_minutes (int): The duration of the slot in minutes.
        is_available (bool): Whether the slot is available for booking.
    """

    start_time: time
    end_time: time
    slot_duration_minutes: int
    is_available: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "slot_duration_minutes": 30,
                "is_available": True,
            }
        }
    }

    def to_command(self) -> SchedulesSlotCommand:
        """Convert the request data to a SchedulesSlotCommand.

        Returns:
            SchedulesSlotCommand: The command object containing the slot details.
        """
        return SchedulesSlotCommand(
            start_time=self.start_time,
            end_time=self.end_time,
            slot_duration_minutes=self.slot_duration_minutes,
            is_available=self.is_available,
        )


class AssignDoctorSchedulesRequest(BaseModel):
    """Request schema for assigning doctor schedules.

    Attributes:
        schedules (dict[DaysOfWeekEnum, list[SchedulesSlotRequest]]):
            A dictionary mapping days of the week to lists of schedule slots.
        timezone (str): The timezone for the schedules, e.g., "America/New_York".
    """

    schedules: dict[DaysOfWeekEnum, list[SchedulesSlotRequest]]
    timezone: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
                "schedules": {
                    "monday": [
                        {
                            "start_time": "09:00:00",
                            "end_time": "17:00:00",
                            "slot_duration_minutes": 30,
                            "is_available": True,
                        }
                    ],
                    "tuesday": [
                        {
                            "start_time": "09:00:00",
                            "end_time": "17:00:00",
                            "slot_duration_minutes": 30,
                            "is_available": True,
                        }
                    ],
                    "wednesday": [],
                    "thursday": [],
                    "friday": [],
                    "saturday": [],
                    "sunday": [],
                },
                "timezone": "America/New_York",
            }
        }
    }

    def to_command(self, doctor_id: UUID) -> AssignDoctorSchedulesCommand:
        """Convert the request data to an AssignDoctorSchedulesCommand.

        Args:
            doctor_id (UUID): The ID of the doctor to assign the schedules to.

        Returns:
            AssignDoctorSchedulesCommand: The command object containing the doctor ID,
                schedules, and timezone.
        """
        return AssignDoctorSchedulesCommand(
            doctor_id=doctor_id,
            schedules={
                day: [slot.to_command() for slot in slots]
                for day, slots in self.schedules.items()
            },
            timezone=self.timezone,
        )
