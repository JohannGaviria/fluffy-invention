"""This module contains the security composition for FastAPI dependencies."""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError

from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.contexts.auth.infrastructure.security.token_service_adapter import (
    PyJWTTokenServiceAdapter,
)
from src.shared.infrastructure.logging.logger import Logger
from src.shared.presentation.api.compositions.infrastructure_composition import (
    get_logger,
    get_token_service,
)

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    logger: Logger = Depends(get_logger),
    token_service: PyJWTTokenServiceAdapter = Depends(get_token_service),
) -> TokenPayloadVO:
    """Dependency injector to get the current user from the JWT token.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials.
        logger (Logger): The logger instance.
        token_service (TokenServicePort): The token service.

    Returns:
        TokenPayloadVO: The token payload value object.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        token = credentials.credentials
        payload = token_service.decode(token)
        return TokenPayloadVO(
            user_id=payload.user_id,
            role=payload.role,
            expires_in=payload.expires_in,
            jti=payload.jti,
        )
    except PyJWTError as e:
        logger.warning("Invalid or expired token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from e


def request_details_dependency(request: Request) -> dict:
    """Dependency injector to get the request details.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        dict: The request details.
    """
    x_forwarded_for = request.headers.get("x-forwarded-for")
    request_ip = (
        x_forwarded_for.split(",")[0].strip()
        if x_forwarded_for
        else (request.client.host if request.client else None)
    )

    return {
        "request_ip": request_ip,
        "request_user_agent": request.headers.get("user-agent", "Unknown"),
    }
