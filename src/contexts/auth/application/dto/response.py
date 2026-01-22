"""This module contains the AccessTokenResponse DTO definition."""

from dataclasses import dataclass
from datetime import datetime

from src.contexts.auth.domain.value_objects.access_token_vo import AccessTokenVO


@dataclass
class AccessTokenResponse:
    """Response DTO for access token response.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token.
        expires_at (datetime): The expiration timestamp of the token.
        expires_in (int): The duration in seconds until the token expires.
    """

    access_token: str
    token_type: str
    expires_at: datetime
    expires_in: int

    @classmethod
    def from_vo(cls, vo: AccessTokenVO):
        """Create an AccessTokenResponseDTO from an AccessTokenVO.

        Args:
            vo (AccessTokenVO): The access token value object to convert.

        Returns:
            AccessTokenResponseDTO: The resulting DTO.
        """
        return cls(
            access_token=vo.access_token,
            token_type=vo.token_type,
            expires_at=vo.expires_at,
            expires_in=vo.expires_in,
        )
