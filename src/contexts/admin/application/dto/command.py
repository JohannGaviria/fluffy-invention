"""This module contains the command classes for the admin context application layer."""

from dataclasses import dataclass
from datetime import time
from uuid import UUID

from src.contexts.admin.domain.enums.days_of_week_enum import DaysOfWeekEnum
from src.contexts.admin.domain.value_objects.doctor_weekly_schedules_vo import (
    DoctorWeeklySchedulesVO,
)
from src.contexts.admin.domain.value_objects.schedules_slot_vo import SchedulesSlotVO


@dataclass
class SchedulesSlotCommand:
    """Command for representing a schedule slot for a doctor.

    Attributes:
        start_time (time): The start time of the slot.
        end_time (time): The end time of the slot.
        slot_duration_minutes (int): The duration of the slot in minutes.
        is_available (bool): Whether the slot is available for booking.
    """

    start_time: time
    end_time: time
    slot_duration_minutes: int
    is_available: bool

    def to_vo(self) -> SchedulesSlotVO:
        """Convert the command data to a SchedulesSlotVO.

        Returns:
            SchedulesSlotVO: The value object containing the slot details.
        """
        return SchedulesSlotVO(
            start_time=self.start_time,
            end_time=self.end_time,
            slot_duration_minutes=self.slot_duration_minutes,
            is_available=self.is_available,
        )


@dataclass
class AssignDoctorSchedulesCommand:
    """Command for assigning schedules to a doctor.

    Attributes:
        doctor_id (UUID): The unique identifier of the doctor.
        schedules (dict[DaysOfWeekEnum, list[SchedulesSlotCommand]]): A dictionary mapping days of the week
            to lists of schedule slots.
        timezone (str): The timezone for the schedules, e.g., "America/New_York".
    """

    doctor_id: UUID
    schedules: dict[DaysOfWeekEnum, list[SchedulesSlotCommand]]
    timezone: str

    def to_vo(self) -> DoctorWeeklySchedulesVO:
        """Convert the command data to a DoctorWeeklySchedulesVO.

        Returns:
            DoctorWeeklySchedulesVO: The value object containing the doctor's weekly schedules.
        """
        return DoctorWeeklySchedulesVO(
            schedules={
                day: [slot.to_vo() for slot in slots]
                for day, slots in self.schedules.items()
            }
        )
