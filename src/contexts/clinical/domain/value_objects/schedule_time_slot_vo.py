"""This module contains the value object for the ScheduleTimeSlot."""

from dataclasses import dataclass
from datetime import time

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class ScheduleTimeSlotVO(BaseValueObject):
    """Value object for a time slot in the schedule."""

    start_time: time
    end_time: time
    slot_duration_minutes: int = 30
    is_available: bool = True

    def validate(self) -> None:
        """Validate the value object.

        Raises:
            ValueError: If the start time is after the end time or
                        if the slot duration is not positive.
        """
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time.")
        if self.slot_duration_minutes <= 0:
            raise ValueError("Slot duration must be positive.")
