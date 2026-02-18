"""This module contains the ActivationCodeCacheKeyVO value object definition."""

from dataclasses import dataclass
from uuid import UUID

from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO


@dataclass(frozen=True)
class ActivationCodeCacheKeyVO(CacheKeyVO):
    """Cache key for activation codes."""

    @classmethod
    def from_user_id(cls, user_id: UUID) -> "ActivationCodeCacheKeyVO":
        """Create cache key from user ID.

        Args:
            user_id (UUID): The user ID.

        Returns:
            ActivationCodeCacheKeyVO: The cache key.
        """
        key = f"cache:auth:activation_code:{str(user_id)}"
        return cls(key=key)
