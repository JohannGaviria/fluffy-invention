"""This module contains the Value Objects for Access Token used in the authentication context."""

from dataclasses import dataclass
from datetime import UTC, datetime

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class AccessTokenVO(BaseValueObject):
    """Value Object representing an access token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token (e.g., Bearer).
        expires_at (datetime): The expiration datetime of the token.
        expires_in (int): The expiration time in seconds.

    Raises:
        ValueError: If any of the fields are invalid.
    """

    access_token: str
    token_type: str
    expires_at: datetime
    expires_in: int

    def validate(self) -> None:
        """Validate the access token.

        Raises:
            ValueError: If any of the fields are invalid.
        """
        if not self.access_token or not self.access_token.strip():
            raise ValueError("access_token cannot be empty")

        if self.token_type not in ["Bearer"]:
            raise ValueError(f"Invalid token_type: {self.token_type}")

        if self.expires_in <= 0:
            raise ValueError("expires_in must be positive")

        if self.expires_at.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware (UTC).")

        if self.expires_at <= datetime.now(UTC):
            raise ValueError("expires_at must be in the future")

    @classmethod
    def to_dict(cls, token: "AccessTokenVO") -> dict:
        """Convert AccessTokenVO to dictionary.

        Args:
            token (AccessTokenVO): The access token value object.

        Returns:
            dict: Dictionary representation of the access token.
        """
        return {
            "access_token": token.access_token,
            "token_type": token.token_type,
            "expires_at": token.expires_at,
            "expires_in": token.expires_in,
        }
