"""This module contains the infrastructure composition for FastAPI dependencies."""

from fastapi import Depends

from src.config import settings
from src.contexts.auth.infrastructure.security.token_service_adapter import (
    PyJWTTokenServiceAdapter,
)
from src.shared.infrastructure.logging.logger import Logger
from src.shared.infrastructure.notifications.sender_notification_service_adapter import (
    SenderNotificationServiceAdapter,
)


def get_logger() -> Logger:
    """Get the logger instance.

    Returns:
        Logger: An instance of Logger.
    """
    return Logger(settings.LOG_LEVEL)


# def get_template_renderer_service() -> TemplateRendererServiceAdapter:
#     """Get the template renderer service adapter.

#     Returns:
#         TemplateRendererServiceAdapter: An instance of TemplateRendererServiceAdapter.
#     """
#     return TemplateRendererServiceAdapter(settings.TEMPLATE_PATH)


def get_sender_notification_service(
    logger: Logger = Depends(get_logger),
) -> SenderNotificationServiceAdapter:
    """Get the sender notification service adapter.

    Args:
        logger (Logger): The logger instance.

    Returns:
        SenderNotificationServiceAdapter: An instance of SenderNotificationServiceAdapter.
    """
    return SenderNotificationServiceAdapter(
        settings.SMTP_SERVER,
        settings.SMTP_PORT,
        settings.USER_EMAIL,
        settings.USER_PASSWORD,
        logger,
    )


def get_token_service() -> PyJWTTokenServiceAdapter:
    """Get the token service adapter.

    Returns:
        TokenServicePort: An instance of TokenServicePort.
    """
    return PyJWTTokenServiceAdapter(
        settings.ACCESS_TOKEN_EXPIRES_IN,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    )
