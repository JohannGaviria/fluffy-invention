"""This module contains the interface for the Cache Service Port."""

from abc import ABC, abstractmethod
from typing import Generic

from src.shared.domain.value_objects.cache_entry_vo import CacheEntryVO, CacheValueType
from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO


class CacheServicePort(ABC, Generic[CacheValueType]):  # noqa: UP046
    """Abstract interface for Cache Service operations."""

    @abstractmethod
    def get(self, key: CacheKeyVO) -> CacheValueType | None:
        """Get a value from the cache by its key.

        Args:
            key (CacheKeyVO): The key of the value to retrieve.

        Returns:
            CacheValueType | None: The value object associated with the key, or None if not found.
        """
        pass

    @abstractmethod
    def set(self, entry: CacheEntryVO[CacheValueType]) -> None:
        """Set a value in the cache with a time-to-live (TTL).

        Args:
            entry (CacheEntryVO[CacheValueType]): The cache entry containing key, value, and TTL.

        Returns:
            None
        """
        pass

    @abstractmethod
    def delete(self, key: CacheKeyVO) -> None:
        """Delete a value from the cache by its key.

        Args:
            key (CacheKeyVO): The key of the value to delete.

        Returns:
            None
        """
        pass
