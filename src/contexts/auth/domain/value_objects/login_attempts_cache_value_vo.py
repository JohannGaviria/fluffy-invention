"""This module contains the LoginAttemptsCacheValueVO value object definition."""

from dataclasses import dataclass
from typing import Any

from src.shared.domain.value_objects.cache_value_vo import CacheValueVO


@dataclass(frozen=True)
class LoginAttemptsCacheValueVO(CacheValueVO):
    """Value object representing login attempts in cache."""

    attempt: int

    def validate(self) -> None:
        """Validate the login attempts value.

        Raises:
            ValueError: If attempts are negative or exceed maximum limit.
        """
        if self.attempt < 0:
            raise ValueError("Attempts cannot be negative")

        if self.attempt > 100:
            raise ValueError("Attempts exceed maximum limit")

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            dict: Dictionary representation of the cache value.
        """
        return {"attempt": self.attempt}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LoginAttemptsCacheValueVO":
        """Create instance from dictionary.

        Args:
            data (dict[str, any]): Dictionary representation of the cache value.

        Returns:
            LoginAttemptsCacheValueVO: Instance of the cache value object.
        """
        return cls(attempt=data["attempt"])

    def increment(self) -> "LoginAttemptsCacheValueVO":
        """Return a new instance with incremented attempt count.

        Returns:
            LoginAttemptsCacheValueVO: New instance with incremented attempts.
        """
        return LoginAttemptsCacheValueVO(attempt=self.attempt + 1)

    @classmethod
    def initial(cls) -> "LoginAttemptsCacheValueVO":
        """Create an initial LoginAttemptsCacheValueVO with 0 attempts.

        Returns:
            LoginAttemptsCacheValueVO: Instance with 0 attempts.
        """
        return cls(attempt=0)
