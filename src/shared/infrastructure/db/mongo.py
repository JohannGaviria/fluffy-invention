"""This module contains the Database class for managing the Beanie/Motor MongoDB connection."""

from threading import Lock

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import settings
from src.shared.infrastructure.logging.logger import get_logger

logger = get_logger(level=getattr(settings, "log_level", "INFO"))


class MongoDatabase:
    """Database class for managing MongoDB connections via Motor and Beanie."""

    _client: AsyncIOMotorClient | None = None
    _lock = Lock()

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        """Get or create the Motor async MongoDB client.

        Returns:
            AsyncIOMotorClient: The MongoDB client instance.
        """
        with cls._lock:
            if cls._client is None:
                logger.info(
                    message="Creating new MongoDB client", url=settings.MONGO_URL
                )
                cls._client = AsyncIOMotorClient(
                    settings.MONGO_URL,
                    maxPoolSize=10,
                    minPoolSize=1,
                    maxIdleTimeMS=1800000,
                    serverSelectionTimeoutMS=30000,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000,
                )
            else:
                logger.debug(message="Reusing existing MongoDB client")
        return cls._client

    @classmethod
    async def init_beanie(cls, document_models: list) -> None:
        """Initialize Beanie ODM with the given document models.

        Args:
            document_models: List of Beanie Document classes to register.
        """
        client = cls.get_client()
        logger.info(message="Initializing Beanie ODM", database=settings.MONGO_DB)
        await init_beanie(
            database=client[settings.MONGO_DB],
            document_models=document_models,
        )

    @classmethod
    async def health_check(cls) -> bool:
        """Perform a health check on the MongoDB connection.

        Returns:
            bool: True if the connection is healthy, False otherwise.
        """
        try:
            client = cls.get_client()
            await client.admin.command("ping")
            logger.info(message="MongoDB health check succeeded")
            return True
        except Exception as e:
            logger.error(message="MongoDB health check failed", error=str(e))
            cls.close_client()
            return False

    @classmethod
    def close_client(cls) -> None:
        """Close and dispose of the MongoDB client."""
        if cls._client is not None:
            logger.info(message="Closing MongoDB client")
            cls._client.close()
            cls._client = None
