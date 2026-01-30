"""This module contains the CacheKeyVO value object definition."""

import re
from dataclasses import dataclass

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class CacheKeyVO(BaseValueObject):
    """Value object representing a cache key."""

    key: str

    def validate(self) -> None:
        """Validate the cache key format.

        Raises:
            ValueError: If the cache key format is invalid.
        """
        # Regex pattern:
        # Example valid keys: cache:user:123, cache:session:abc:def
        CACHE_PATTERN = r"^cache:[a-zA-Z0-9_]+:[a-zA-Z0-9_]+(:[^:]+)?$"

        if not self.key and not self.key.strip():
            raise ValueError("Cache key cannot be empty")

        if not re.match(CACHE_PATTERN, self.key):
            raise ValueError("Invalid cache key format")

        if len(self.key) > 250:
            raise ValueError("Cache key too long (max 250 characters)")
