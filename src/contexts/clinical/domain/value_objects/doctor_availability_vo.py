"""This module contains the DoctorAvailabilityVO value object definition."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.contexts.clinical.domain.value_objects.available_slot_vo import AvailableSlotVO
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class DoctorAvailabilityVO(BaseValueObject):
    """Value object representing a doctor's availability.

    Attributes:
        doctor_id (UUID): The unique identifier of the doctor.
        available_slots (list[AvailableSlotVO]): A list of available time slots for the doctor.
    """

    doctor_id: UUID
    available_slots: list[AvailableSlotVO]

    def validate(self) -> None:
        """Validates the value object to ensure all required fields are present and valid.

        Raises:
            ValueError: If any required field is missing or invalid.
        """
        if self.doctor_id is None:
            raise ValueError("doctor_id is required")

        if self.available_slots is None:
            raise ValueError("available_slots is required")

    def has_availability_at(self, requested_datetime: datetime) -> bool:
        """Checks if the doctor is available at the requested datetime.

        Args:
            requested_datetime (datetime): The datetime to check for availability.

        Returns:
            bool: True if the doctor is available at the requested datetime, False otherwise.
        """
        return any(slot.covers(requested_datetime) for slot in self.available_slots)
