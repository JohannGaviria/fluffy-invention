"""This module contains the logging service implementation."""

import inspect

from src.shared.infrastructure.logging.logging_config import LoggingConfig


def get_caller_module_name(skip_frames: int = 2) -> str:
    """Get the name of the module that called the logger.

    Args:
        skip_frames (int): Number of frames to skip from the top of the stack.

    Returns:
        str: The name of the calling module, or "__main__" if not found.
    """
    try:
        # Get the current stack frames
        frames = inspect.stack()

        # Iterate through the stack frames,
        # skipping the specified number of frames
        for frame in frames[skip_frames:]:
            # get the module from the frame
            module = inspect.getmodule(frame[0])

            # if module is found, and it's not this module, return its name
            if module and module.__name__ != __name__:
                return module.__name__
    except (IndexError, AttributeError):
        pass

    # Fallback to __main__ if no other module is found
    return "__main__"


class Logger:
    """Service to handle logger."""

    def __init__(self, level: str):
        """Initialize the Logger instance.

        Args:
            level (str): The logging level.
        """
        name = get_caller_module_name()
        self.logger = LoggingConfig.configure(level=level, name=name)

    def debug(self, message: str, **kwargs):
        """Log a debug message with optional contextual information."""
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log an info message with optional contextual information."""
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log a warning message with optional contextual information."""
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log an error message with optional contextual information."""
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log a critical message with optional contextual information."""
        self.logger.critical(message, **kwargs)


def get_logger(level: str) -> Logger:
    """Provides a Logger instance.

    Args:
        level (str): The logging level.

    Returns:
        Logger: An instance of the logger.
    """
    return Logger(level)
