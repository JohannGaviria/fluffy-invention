"""This module contains the value object for the ScheduleDay."""

from dataclasses import dataclass

from src.contexts.clinical.domain.value_objects.schedule_time_slot_vo import (
    ScheduleTimeSlotVO,
)
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class ScheduleDaysVO(BaseValueObject):
    """Value object for a list of ScheduleDaysVO objects."""

    slots: list[ScheduleTimeSlotVO]

    def validate(self) -> None:
        """Validate the value object.

        Raises:
            ValueError: If the slots are not a list of ScheduleDayVO objects.
        """
        if not isinstance(self.slots, list):
            raise ValueError("Slots must be a list of ScheduleDaysVO objects.")
