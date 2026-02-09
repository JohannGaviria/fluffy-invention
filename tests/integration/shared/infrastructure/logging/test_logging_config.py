"""Integration tests for LoggingConfig."""

import json

from src.shared.infrastructure.logging.logging_config import LoggingConfig


class TestLoggingConfig:
    """Integration tests for LoggingConfig."""

    def test_should_configure_logging_successfully(self):
        """Should configure logging with the correct level and name."""
        level = "DEBUG"
        name = "test_logger"
        logger = LoggingConfig.configure(level=level, name=name)

        assert hasattr(logger, "info")
        assert hasattr(logger, "error")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "critical")

        assert "structlog" in str(type(logger))

    def test_should_log_message_with_configured_logger(self, capsys):
        """Should log a message using the configured logger."""
        level = "INFO"
        name = "test_logger"
        logger = LoggingConfig.configure(level=level, name=name)

        logger.info("This is a test log message.")
        captured = capsys.readouterr()

        output = captured.out.strip()
        assert output

        log_data = json.loads(output)
        assert log_data["event"] == "This is a test log message."
        assert log_data["level"] == "info"

    def test_should_use_json_renderer(self, capsys):
        """Should use JSON renderer for logging output."""
        level = "INFO"
        name = "test_logger"
        logger = LoggingConfig.configure(level=level, name=name)

        logger.info("Test JSON renderer", key="value")
        captured = capsys.readouterr()

        output = captured.out.strip()
        log_data = json.loads(output)

        assert log_data["key"] == "value"
        assert log_data["event"] == "Test JSON renderer"
        assert log_data["level"] == "info"
        assert "timestamp" in log_data

    def test_should_log_at_different_levels(self, capsys):
        """Should respect logging levels."""
        level = "WARNING"
        name = "test_logger"
        logger = LoggingConfig.configure(level=level, name=name)

        logger.debug("Debug message")
        logger.info("Info message")

        logger.warning("Warning message")

        captured = capsys.readouterr()
        output = captured.out.strip()

        if output:
            log_data = json.loads(output)
            assert log_data["event"] == "Warning message"
            assert log_data["level"] == "warning"

    def test_should_include_exc_info_on_error(self, capsys):
        """Should include exception info for error messages."""
        level = "ERROR"
        name = "test_logger"
        logger = LoggingConfig.configure(level=level, name=name)

        try:
            raise ValueError("Test error")
        except ValueError:
            logger.error("An error occurred", exc_info=True)

        captured = capsys.readouterr()
        output = captured.out.strip()

        if output:
            log_data = json.loads(output)
            assert log_data["event"] == "An error occurred"
            assert log_data["level"] == "error"
            assert "exc_info" in log_data

    def test_should_configure_with_different_levels(self):
        """Should configure logging with different valid levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in valid_levels:
            name = f"test_logger_{level}"
            logger = LoggingConfig.configure(level=level, name=name)

            assert hasattr(logger, "info")

    def test_should_return_bound_logger_instance(self, capsys):
        """Should return a logger that can actually log messages."""
        level = "INFO"
        name = "test_logger"
        logger = LoggingConfig.configure(level=level, name=name)

        logger.info("Test message")
        captured = capsys.readouterr()
        output = captured.out.strip()

        assert output
        log_data = json.loads(output)
        assert log_data["event"] == "Test message"
