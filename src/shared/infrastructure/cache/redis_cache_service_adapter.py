"""This module contains the adapter for Redis cache service."""

import json
from typing import cast

from redis import RedisError

from src.shared.domain.cache_service_port import CacheServicePort
from src.shared.infrastructure.cache.redis_client import RedisClient
from src.shared.infrastructure.logging.logger import Logger


class RedisCacheServiceAdapter(CacheServicePort):
    """Adapter for Redis cache service."""

    def __init__(self, redis_client: RedisClient, logger: Logger) -> None:
        """Initializes the Redis cache service adapter.

        Args:
            redis_client (RedisClient): The Redis client instance.
            logger (Logger): Logger instance for logging.
        """
        self.redis_client = redis_client
        self.logger = logger

    def set(self, key: str, ttl: int, value: dict | None) -> None:
        """Sets a value in the cache with a time-to-live (TTL).

        Args:
            key (str): The key to set.
            ttl (int): The time-to-live in seconds.
            value (dict | None): The value to set.

        Raises:
            Exception: If setting the key fails.
            RedisError: If a Redis error occurs.
            TypeError: If the value cannot be serialized to JSON.
            ValueError: If the value cannot be serialized to JSON.
        """
        try:
            self.redis_client.get_client().setex(key, ttl, json.dumps(value))
        except (RedisError, Exception) as e:
            self.logger.error(message="Redis SET failed", error=str(e))
            raise e
        except (TypeError, ValueError) as e:
            self.logger.error(message="Redis SET failed", error=str(e))
            raise e

    def get(self, key: str) -> dict | None:
        """Gets a value from the cache by key.

        Args:
            key (str): The key to retrieve.

        Returns:
            dict | None: The value associated with the key, or None if not found.

        Raises:
            Exception: If retrieving the key fails.
            RedisError: If a Redis error occurs.
            json.JSONDecodeError: If the retrieved value cannot be decoded from JSON.
        """
        try:
            value = cast(str | None, self.redis_client.get_client().get(key))
            return json.loads(value) if value else None
        except (RedisError, Exception) as e:
            self.logger.error(message="Redis GET failed", key=key, error=str(e))
            raise e
        except json.JSONDecodeError as e:
            self.logger.error(
                message="JSON decode failed for cache GET", key=key, error=str(e)
            )
            raise e

    def delete(self, key: str) -> None:
        """Deletes a key from the cache.

        Args:
            key (str): The key to delete.

        Raises:
            Exception: If deleting the key fails.
            RedisError: If a Redis error occurs.
        """
        try:
            self.redis_client.get_client().delete(key)
        except (RedisError, Exception) as e:
            self.logger.error(message="Redis DELETE failed", key=key, error=str(e))
            raise e
