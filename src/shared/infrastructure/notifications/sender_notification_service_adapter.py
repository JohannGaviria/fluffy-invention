"""This module contains the adapter for sending notifications via SMTP email."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.shared.domain.ports.services.sender_notification_service_port import (
    SenderNotificationServicePort,
)
from src.shared.domain.value_objects.send_notification_vo import SendNotificationVO
from src.shared.infrastructure.logging.logger import Logger


class SenderNotificationServiceAdapter(SenderNotificationServicePort):
    """Adapter for sending notifications via SMTP email."""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        user_email: str,
        user_password: str,
        logger: Logger,
    ) -> None:
        """Initializes the notification sender with SMTP server details.

        Args:
            smtp_server (str): The SMTP server address.
            smtp_port (int): The SMTP server port.
            user_email (str): The email address to send from.
            user_password (str): The password for the email account.
            logger (Logger): Logger instance for logging.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.user_email = user_email
        self.user_password = user_password
        self.logger = logger

    def send(self, notification: SendNotificationVO) -> None:
        """Sends an email notification.

        Args:
            notification (SendNotificationVO): The notification to be sent.

        Raises:
            Exception: If sending the email fails.
        """
        message = MIMEMultipart()
        message["From"] = self.user_email
        message["To"] = notification.recipient
        message["Subject"] = notification.subject

        html = MIMEText(notification.body, "html")
        message.attach(html)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.user_email, self.user_password)
            server.sendmail(
                self.user_email, notification.recipient, message.as_string()
            )
            server.quit()
            self.logger.info("Notification sent successfully.")
        except Exception as e:
            self.logger.error("Failed to send notification", error=str(e))
            raise e
