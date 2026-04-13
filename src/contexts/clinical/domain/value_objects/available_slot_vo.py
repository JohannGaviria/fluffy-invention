"""This module contains the AvailableSlotVO value object definition."""

from dataclasses import dataclass
from datetime import datetime

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class AvailableSlotVO(BaseValueObject):
    """Value object representing an available time slot for a clinical appointment.

    Attributes:
        start_datetime (datetime): The starting datetime of the available slot.
        end_datetime (datetime): The ending datetime of the available slot.
    """

    start_datetime: datetime
    end_datetime: datetime

    def validate(self) -> None:
        """Validate the available slot value object.

        Raises:
            ValueError: If start_datetime or end_datetime is not provided.
        """
        if self.start_datetime is None:
            raise ValueError("start_datetime is required")

        if self.end_datetime is None:
            raise ValueError("end_datetime is required")

    def covers(self, requested: datetime) -> bool:
        """Check if the requested datetime falls within the available slot.

        Args:
            requested (datetime): The datetime to check against the available slot.

        Returns:
            bool: True if the requested datetime is within the slot, False otherwise.
        """
        return self.start_datetime <= requested < self.end_datetime
