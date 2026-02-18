"""This module contains the Database class for managing the SQLModel database connection and sessions."""

from threading import Lock

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, create_engine

from src.config import settings
from src.shared.infrastructure.logging.logger import get_logger

logger = get_logger(level=getattr(settings, "log_level", "INFO"))


class Database:
    """Database class for managing SQLModel database connections and sessions."""

    _engine = None
    _lock = Lock()

    @classmethod
    def get_engine(cls):
        """Get or create the SQLModel database engine.

        Returns:
            Engine: The SQLModel database engine.
        """
        with cls._lock:
            if cls._engine is None:
                logger.info(
                    message="Creating new database engine", url=settings.DATABASE_URL
                )
                cls._engine = create_engine(
                    settings.DATABASE_URL,
                    echo=False,
                    pool_pre_ping=True,
                    pool_size=10,
                    max_overflow=20,
                    pool_timeout=30,
                    pool_recycle=1800,
                )
            else:
                logger.debug(message="Reusing existing database engine")
        return cls._engine

    @classmethod
    def get_session(cls):
        """Get a new SQLModel database session.

        Returns:
            Session: A new SQLModel database session.
        """
        engine = cls.get_engine()
        logger.debug(message="Opening DB session")
        return Session(engine)

    @classmethod
    def health_check(cls) -> bool:
        """Perform a health check on the database connection.

        Returns:
            bool: True if the database connection is healthy, False otherwise.
        """
        try:
            engine = cls.get_engine()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(message="Database health check succeeded")
            return True
        except SQLAlchemyError as e:
            logger.error(message="Database health check failed", error=str(e))
            cls.close_engine()
            return False

    @classmethod
    def close_engine(cls):
        """Dispose of the SQLModel database engine."""
        if cls._engine:
            logger.info(message="Disposing database engine")
            cls._engine.dispose()
            cls._engine = None


def get_session():
    """Provide a transactional scope around a series of operations."""
    db = Database.get_session()
    try:
        yield db
    finally:
        db.close()
        logger.debug(message="DB session closed")
