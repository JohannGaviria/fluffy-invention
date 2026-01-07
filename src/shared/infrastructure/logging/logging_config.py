"""This module contains the logging configuration."""

import logging
import sys

import structlog


class LoggingConfig:
    """Logging configuration class."""

    @staticmethod
    def configure(level: str, name: str) -> structlog.BoundLogger:
        """Configures the logging settings.

        Args:
            level (str): The logging level.
            name (str): The name of the logger.

        Returns:
            logger (structlog.BoundLogger): Configured logger instance.
        """
        # Configure standard library logging
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=level,
        )

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                logging.getLevelName(level)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Return a logger bound with the module name
        return structlog.get_logger(name)
