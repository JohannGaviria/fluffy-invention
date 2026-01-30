"""This module contains the adapter for Redis cache service using Value Objects."""

import json
from typing import Generic, cast

from redis import RedisError

from src.shared.domain.ports.services.cache_service_port import CacheServicePort
from src.shared.domain.value_objects.cache_entry_vo import CacheEntryVO, CacheValueType
from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO
from src.shared.infrastructure.cache.redis_client import RedisClient
from src.shared.infrastructure.logging.logger import Logger


class RedisCacheServiceAdapter(
    CacheServicePort[CacheValueType],
    Generic[CacheValueType],  # noqa: UP046
):
    """Adapter for Redis cache service using Value Objects.

    This adapter is generic and works with any CacheValueVO subclass.
    """

    def __init__(
        self,
        redis_client: RedisClient,
        logger: Logger,
        value_class: type[CacheValueType],
    ) -> None:
        """Initializes the Redis cache service adapter.

        Args:
            redis_client (RedisClient): The Redis client instance.
            logger (Logger): Logger instance for logging.
            value_class (Type[CacheValueType]): The class type for deserializing cache values.
                This is needed to call from_dict() with the correct type.
        """
        self.redis_client = redis_client
        self.logger = logger
        self.value_class = value_class

    def get(self, key: CacheKeyVO) -> CacheValueType | None:
        """Gets a value from the cache by key.

        Args:
            key (CacheKeyVO): The cache key value object.

        Returns:
            CacheValueType | None: The value object associated with the key, or None if not found.

        Raises:
            RedisError: If a Redis error occurs.
            json.JSONDecodeError: If the retrieved value cannot be decoded from JSON.
            Exception: For any other unexpected errors.
        """
        try:
            # Get raw value from Redis
            raw_value = cast(str | None, self.redis_client.get_client().get(key.key))

            if raw_value is None:
                self.logger.debug(message="Cache GET miss", key=key.key)
                return None

            # Deserialize JSON to dict
            value_dict = json.loads(raw_value)

            # Reconstruct VO using the value_class
            value_obj = self.value_class.from_dict(value_dict)

            self.logger.debug(message="Cache GET hit", key=key.key)
            return value_obj

        except json.JSONDecodeError as e:
            self.logger.error(
                message="JSON decode failed for cache GET", key=key.key, error=str(e)
            )
            raise
        except RedisError as e:
            self.logger.error(message="Redis GET failed", key=key.key, error=str(e))
            raise
        except Exception as e:
            self.logger.error(
                message="Unexpected error during cache GET", key=key.key, error=str(e)
            )
            raise

    def set(self, entry: CacheEntryVO[CacheValueType]) -> None:
        """Sets a value in the cache with a time-to-live (TTL).

        Args:
            entry (CacheEntryVO[CacheValueType]): The cache entry containing key, ttl, and value.

        Raises:
            RedisError: If a Redis error occurs.
            TypeError: If the value cannot be serialized to JSON.
            ValueError: If the value cannot be serialized to JSON.
            Exception: For any other unexpected errors.
        """
        try:
            # Serialize value to dict, then to JSON
            value_dict = entry.value.to_dict()
            json_value = json.dumps(value_dict)

            # Store in Redis with TTL
            self.redis_client.get_client().setex(
                entry.key.key, entry.ttl.seconds, json_value
            )

            self.logger.debug(
                message="Cache SET successful", key=entry.key.key, ttl=entry.ttl.seconds
            )

        except (TypeError, ValueError) as e:
            self.logger.error(
                message="Value serialization failed", key=entry.key.key, error=str(e)
            )
            raise
        except RedisError as e:
            self.logger.error(
                message="Redis SET failed", key=entry.key.key, error=str(e)
            )
            raise
        except Exception as e:
            self.logger.error(
                message="Unexpected error during cache SET",
                key=entry.key.key,
                error=str(e),
            )
            raise

    def delete(self, key: CacheKeyVO) -> None:
        """Deletes a key from the cache.

        Args:
            key (CacheKeyVO): The cache key value object.

        Raises:
            RedisError: If a Redis error occurs.
            Exception: For any other unexpected errors.
        """
        try:
            self.redis_client.get_client().delete(key.key)
            self.logger.debug(message="Cache DELETE successful", key=key.key)

        except RedisError as e:
            self.logger.error(message="Redis DELETE failed", key=key.key, error=str(e))
            raise
        except Exception as e:
            self.logger.error(
                message="Unexpected error during cache DELETE",
                key=key.key,
                error=str(e),
            )
            raise
