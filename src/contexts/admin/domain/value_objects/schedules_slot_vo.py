"""This module contains the value object for representing a schedule slot."""

from dataclasses import dataclass
from datetime import time

from src.shared.domain.exceptions.exception import MissingFieldException
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class SchedulesSlotVO(BaseValueObject):
    """Value Object representing a schedule slot."""

    start_time: time
    end_time: time
    slot_duration_minutes: int
    is_available: bool

    def validate(self) -> None:
        """Validate the SchedulesSlotVO fields.

        Raises:
            MissingFieldException: If any required field is missing.
            ValueError: If end_time is not greater than start_time or if the time range is
                not divisible by slot_duration_minutes.
        """
        REQUIRED_FIELDS = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "slot_duration_minutes": self.slot_duration_minutes,
            "is_available": self.is_available,
        }
        for field, value in REQUIRED_FIELDS.items():
            if value is None:
                raise MissingFieldException(field, "is required")

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")

        # Calculate the total minutes in the time range and
        # check if it's divisible by slot_duration_minutes
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute

        total_minutes = end_minutes - start_minutes

        if total_minutes % self.slot_duration_minutes != 0:
            raise ValueError("Time range must be divisible by slot duration")

    def to_dict(self) -> dict:
        """Convert the SchedulesSlotVO to a dictionary representation.

        Returns:
            dict: A dictionary containing the SchedulesSlotVO data.
        """
        return {
            "start_time": self.start_time.isoformat("minutes"),
            "end_time": self.end_time.isoformat("minutes"),
            "slot_duration_minutes": self.slot_duration_minutes,
            "is_available": self.is_available,
        }
