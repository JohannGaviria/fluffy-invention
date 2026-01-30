"""This module contains the CacheTTLVO value object definition."""

from dataclasses import dataclass

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class CacheTTLVO(BaseValueObject):
    """Value object representing cache time-to-live (TTL) in seconds."""

    seconds: int

    def validate(self) -> None:
        """Validate the TTL value.

        Raises:
            ValueError: If TTL is negative or exceeds maximum allowed value.
        """
        if self.seconds < 0:
            raise ValueError("TTL must be positive")

        if self.seconds > 86400 * 30:
            raise ValueError("TTL too long (max 30 days)")

    @classmethod
    def from_minutes(cls, minutes: int) -> "CacheTTLVO":
        """Create CacheTTLVO from minutes.

        Args:
            minutes (int): Time to live in minutes.

        Returns:
            CacheTTLVO: Instance with TTL set in seconds.
        """
        return cls(seconds=minutes * 60)
