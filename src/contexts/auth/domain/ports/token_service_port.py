"""This module contains the abstract base class for the Token Service Port."""

from abc import ABC, abstractmethod

from src.contexts.auth.domain.value_objects.access_token_vo import AccessTokenVO
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO


class TokenServicePort(ABC):
    """Abstract base class for the Token Service Port."""

    @abstractmethod
    def access(self, payload: TokenPayloadVO) -> AccessTokenVO:
        """Generate an access token.

        Args:
            payload (TokenPayloadVO): The data to encode in the token.

        Returns:
            dict: access token and metadata.
        """
        pass
