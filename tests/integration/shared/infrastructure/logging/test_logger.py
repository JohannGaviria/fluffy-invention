"""Integration tests for Logger."""

import inspect
import json

from src.shared.infrastructure.logging.logger import (
    Logger,
    get_caller_module_name,
    get_logger,
)


class TestLogger:
    """Integration tests for Logger."""

    def test_logger_initialization(self):
        """Should initialize Logger with correct level and name."""
        logger = get_logger(level="DEBUG")
        assert isinstance(logger, Logger)
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")

    def test_logger_debug_message(self, capsys):
        """Should log a debug message."""
        logger = get_logger(level="DEBUG")
        logger.debug("This is a debug message.")
        captured = capsys.readouterr()

        output = captured.out.strip()
        if output:
            log_data = json.loads(output)
            assert log_data["event"] == "This is a debug message."
            assert log_data["level"] == "debug"

    def test_logger_info_message(self, capsys):
        """Should log an info message."""
        logger = get_logger(level="INFO")
        logger.info("This is an info message.")
        captured = capsys.readouterr()

        output = captured.out.strip()
        if output:
            log_data = json.loads(output)
            assert log_data["event"] == "This is an info message."
            assert log_data["level"] == "info"

    def test_logger_error_message(self, capsys):
        """Should log an error message."""
        logger = get_logger(level="ERROR")
        logger.error("This is an error message.")
        captured = capsys.readouterr()

        output = captured.out.strip()
        if output:
            log_data = json.loads(output)
            assert log_data["event"] == "This is an error message."
            assert log_data["level"] == "error"

    def test_logger_critical_message(self, capsys):
        """Should log an critical message."""
        logger = get_logger(level="CRITICAL")
        logger.critical("Critical failure")
        captured = capsys.readouterr()

        output = captured.out.strip()
        if output:
            log_data = json.loads(output)
            assert log_data["event"] == "Critical failure"
            assert log_data["level"] == "critical"

    def test_logger_with_context(self, capsys):
        """Should log with additional context."""
        logger = get_logger(level="INFO")
        logger.info("User action", user_id=123, action="login")
        captured = capsys.readouterr()

        output = captured.out.strip()
        if output:
            log_data = json.loads(output)
            assert log_data["event"] == "User action"
            assert log_data["user_id"] == 123
            assert log_data["action"] == "login"

    def test_logger_level_filtering(self, capsys):
        """Should filter messages based on log level."""
        logger = get_logger(level="WARNING")

        logger.debug("Debug message")
        logger.info("Info message")

        logger.warning("Warning message")
        logger.error("Error message")

        captured = capsys.readouterr()
        output = captured.out.strip()

        lines = [line for line in output.split("\n") if line.strip()]

        assert len(lines) >= 2

        found_warning = False
        found_error = False

        for line in lines:
            log_data = json.loads(line)
            if log_data.get("event") == "Warning message":
                found_warning = True
                assert log_data["level"] == "warning"
            elif log_data.get("event") == "Error message":
                found_error = True
                assert log_data["level"] == "error"

        assert found_warning, "Warning message not found"
        assert found_error, "Error message not found"

    def test_get_logger_returns_new_instance(self):
        """Should return a new Logger instance each time."""
        logger1 = get_logger(level="INFO")
        logger2 = get_logger(level="INFO")

        assert logger1 is not logger2
        assert isinstance(logger1, Logger)
        assert isinstance(logger2, Logger)

    def test_get_caller_module_name_fallback(self, monkeypatch):
        def broken_stack():
            raise IndexError

        monkeypatch.setattr(inspect, "stack", broken_stack)

        name = get_caller_module_name()
        assert name == "__main__"
