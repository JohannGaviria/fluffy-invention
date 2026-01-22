"""This module contains the adapter for JWT token generation using the PyJWT library."""

from datetime import UTC, datetime, timedelta

import jwt

from src.contexts.auth.domain.ports.token_service_port import TokenServicePort
from src.contexts.auth.domain.value_objects.access_token_vo import AccessTokenVO
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO


class PyJWTTokenServiceAdapter(TokenServicePort):
    """Adapter for JWT token generation using PyJWT library."""

    def __init__(
        self,
        expires_in: int,
        secret_key: str,
        algorithm: str,
    ) -> None:
        """Initializes the PyJWTTokenServiceAdapter with configuration parameters.

        Args:
            expires_in (int): The token expiration time in minutes.
            secret_key (str): The secret key used to sign the token.
            algorithm (str): The algorithm used for token encoding.
        """
        self.expires_in = expires_in
        self.secret_key = secret_key
        self.algorithm = algorithm

    def access(self, payload: TokenPayloadVO) -> AccessTokenVO:
        """Generates a JWT access token.

        Args:
            payload (TokenPayloadVO): The payload to encode in the token.

        Returns:
            AccessTokenVO: The generated access token value object.
        """
        token = jwt.encode(payload.to_dict(), self.secret_key, self.algorithm)
        return AccessTokenVO(
            access_token=token,
            token_type="Bearer",
            expires_in=self.expires_in,
            expires_at=datetime.now(UTC) + timedelta(minutes=self.expires_in),
        )
