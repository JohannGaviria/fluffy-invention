"""This module contains the value object for representing a timezone."""

from dataclasses import dataclass
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class TimezoneVO(BaseValueObject):
    """Value Object representing a timezone."""

    timezone: str

    def __post_init__(self) -> None:
        """Post-initialization to validate the timezone value.

        Raises:
            ValueError: If the timezone is empty or invalid.
        """
        # Validate the timezone format using the ZoneInfo class.
        try:
            ZoneInfo(self.timezone)
        except ZoneInfoNotFoundError as err:
            raise ValueError(f"Invalid timezone: {self.timezone}") from err

    def validate(self) -> None:
        """Validate the timezone value.

        Raises:
            ValueError: If the timezone is empty or invalid.
        """
        if not self.timezone or not self.timezone.strip():
            raise ValueError("Timezone cannot be empty")
