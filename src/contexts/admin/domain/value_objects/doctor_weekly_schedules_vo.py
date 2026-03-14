"""This module contains the value object for representing a doctor's weekly schedules."""

from dataclasses import dataclass

from src.contexts.admin.domain.value_objects.schedules_slot_vo import SchedulesSlotVO
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class DoctorWeeklySchedulesVO(BaseValueObject):
    """Value Object representing a doctor's weekly schedules."""

    schedules: dict[str, list[SchedulesSlotVO]]

    def validate(self) -> None:
        """Validate the DoctorWeeklySchedulesVO fields.

        Raises:
            ValueError: If schedules is empty or contains invalid days or slots.
        """
        business_days = {
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        }

        if self.schedules is None:
            raise ValueError("Schedules cannot be empty")

        # Validate that the schedules dictionary contains valid days and slots.
        for day, slots in self.schedules.items():
            if day not in business_days:
                raise ValueError(f"Invalid day: {day}")

            if not isinstance(slots, list):
                raise ValueError(f"Slots for {day} must be a list")

            for slot in slots:
                slot.validate()

            self._validate_overlapping_slots(day, slots)

    def _validate_overlapping_slots(
        self, day: str, slots: list[SchedulesSlotVO]
    ) -> None:
        """Validate that there are no overlapping slots for a given day.

        Args:
            day (str): The day of the week for which to validate the slots.
            slots (list[SchedulesSlotVO]): The list of schedule slots to validate.

        Raises:
            ValueError: If overlapping slots are detected.
        """
        if len(slots) <= 1:
            return

        ordered_slots = sorted(slots, key=lambda s: s.start_time)

        # Check for overlapping slots by comparing the end time
        # of the current slot with the start time of the next slot.
        for i in range(len(ordered_slots) - 1):
            current_slot = ordered_slots[i]
            next_slot = ordered_slots[i + 1]

            # If the start time of the next slot is before the
            # end time of the current slot, then there is an overlap.
            if next_slot.start_time < current_slot.end_time:
                raise ValueError(
                    f"Overlapping slots detected on {day}: "
                    f"{current_slot.start_time}-{current_slot.end_time} "
                    f"overlaps with "
                    f"{next_slot.start_time}-{next_slot.end_time}"
                )
