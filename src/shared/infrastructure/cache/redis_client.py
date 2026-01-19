"""This module contains the RedisClient class for managing Redis connections."""

import time
from threading import Lock

import redis

from src.config import settings
from src.shared.infrastructure.logging.logger import get_logger

logger = get_logger(level=getattr(settings, "log_level", "INFO"))


class RedisClient:
    """Redis client class for managing Redis connections with retry and health check."""

    _instance: redis.Redis | None = None
    _lock = Lock()

    MAX_RETRIES = 5
    RETRY_DELAY = 1.5

    @classmethod
    def get_client(cls) -> redis.Redis:
        """Get or create the Redis client instance.

        Returns:
            redis.Redis: The Redis client instance.
        """
        with cls._lock:
            if cls._instance is None:
                logger.info(message="Creating Redis client")
                cls._instance = cls._create_client()
            else:
                logger.debug(message="Redis client exists, performing health check")
                cls.health_check()
        return cls._instance

    @classmethod
    def _create_client(cls) -> redis.Redis:
        """Create a new Redis client with retry logic.

        Returns:
            redis.Redis: A new Redis client instance.

        Raises:
            redis.RedisError: If unable to connect to Redis after retries.
        """
        last_error = None

        for attempt in range(1, cls.MAX_RETRIES + 1):
            try:
                logger.debug(message="Attempting to connect to Redis", attempt=attempt)
                client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    health_check_interval=30,
                )
                client.ping()
                logger.info(message="Connected to Redis")
                return client

            except redis.RedisError as e:
                last_error = e
                logger.warning(
                    message="Redis connection attempt failed",
                    attempt=attempt,
                    error=str(e),
                )
                time.sleep(cls.RETRY_DELAY * attempt)

        logger.error(
            message="Failed to connect to Redis after retries", error=str(last_error)
        )
        raise redis.RedisError(f"Error connecting to Redis: {last_error}")

    @classmethod
    def health_check(cls) -> bool:
        """Perform a health check on the Redis client.

        Returns:
            bool: True if the Redis connection is healthy, False otherwise.
        """
        if cls._instance is None:
            logger.debug(message="No Redis instance, creating one during health check")
            cls._instance = cls._create_client()

        try:
            cls._instance.ping()
            logger.debug(message="Redis health check succeeded")
            return True
        except redis.RedisError as e:
            logger.warning(
                message="Redis health check failed, recreating client", error=str(e)
            )
            cls._instance = cls._create_client()
            return False

    @classmethod
    def close(cls) -> None:
        """Close the Redis client connection.

        Returns:
            None
        """
        with cls._lock:
            if cls._instance is not None:
                logger.info(message="Closing Redis client")
                cls._instance.close()
                cls._instance = None


def get_redis_client() -> RedisClient:
    """Dependency to get the Redis client instance.

    Returns:
        RedisClient: The Redis client instance.
    """
    return RedisClient()
