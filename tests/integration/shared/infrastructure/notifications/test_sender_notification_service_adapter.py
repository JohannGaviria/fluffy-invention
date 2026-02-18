"""Integration tests for SenderNotificationServiceAdapter."""

from unittest.mock import MagicMock

import pytest

from src.shared.domain.value_objects.send_notification_vo import SendNotificationVO
from src.shared.infrastructure.logging.logger import Logger
from src.shared.infrastructure.notifications.sender_notification_service_adapter import (
    SenderNotificationServiceAdapter,
)


class TestSendNotificationServiceAdapter:
    @pytest.fixture
    def smtp_server_mock(self):
        smtp_mock = MagicMock()
        smtp_mock.sendmail = MagicMock()
        smtp_mock.starttls = MagicMock()
        smtp_mock.login = MagicMock()
        smtp_mock.quit = MagicMock()
        return smtp_mock

    @pytest.fixture
    def logger_mock(self):
        return MagicMock(spec=Logger)

    @pytest.fixture
    def sender_notification_service_adapter(
        self, smtp_server_mock, logger_mock, monkeypatch
    ):
        monkeypatch.setattr("smtplib.SMTP", lambda *args, **kwargs: smtp_server_mock)
        return SenderNotificationServiceAdapter(
            smtp_server="smtp.example.com",
            smtp_port=587,
            user_email="test@example.com",
            user_password="password",
            logger=logger_mock,
        )

    def test_send_notification_success(
        self, sender_notification_service_adapter, smtp_server_mock, logger_mock
    ):
        """Should send a notification successfully."""
        notification = SendNotificationVO(
            recipient="recipient@example.com",
            subject="Test Subject",
            body="<p>This is a test email.</p>",
        )

        sender_notification_service_adapter.send(notification)

        smtp_server_mock.sendmail.assert_called_once()
        logger_mock.info.assert_called_once_with("Notification sent successfully.")

    def test_send_notification_failure(
        self, sender_notification_service_adapter, smtp_server_mock, logger_mock
    ):
        """Should log an error when sending a notification fails."""
        smtp_server_mock.sendmail.side_effect = Exception("SMTP error")

        notification = SendNotificationVO(
            recipient="recipient@example.com",
            subject="Test Subject",
            body="<p>This is a test email.</p>",
        )

        with pytest.raises(Exception, match="SMTP error"):
            sender_notification_service_adapter.send(notification)

        logger_mock.error.assert_called_once_with(
            "Failed to send notification", error="SMTP error"
        )
