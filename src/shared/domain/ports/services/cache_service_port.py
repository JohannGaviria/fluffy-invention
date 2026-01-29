"""This module contains the interface for the Cache Service Port."""

from abc import ABC, abstractmethod


class CacheServicePort(ABC):
    """Abstract interface for Cache Service operations."""

    @abstractmethod
    def get(self, key: str) -> dict | None:
        """Get a value from the cache by its key.

        Args:
            key (str): The key of the value to retrieve.

        Returns:
            dict | None: The value associated with the key, or None if not found.
        """
        pass

    @abstractmethod
    def set(self, key: str, ttl: int, value: dict | None) -> None:
        """Set a value in the cache with a time-to-live (TTL).

        Args:
            key (str): The key under which the value is stored.
            ttl (int): Time-to-live in seconds.
            value (dict | None): The value to store in the cache.

        Returns:
            None
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a value from the cache by its key.

        Args:
            key (str): The key of the value to delete.

        Returns:
            None
        """
        pass
