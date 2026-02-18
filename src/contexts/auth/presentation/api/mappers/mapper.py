"""This module contains the mapper for AccessTokenResponse."""

from src.contexts.auth.application.dto.response import (
    AccessTokenResponse as AccessTokenResponseDTO,
)
from src.contexts.auth.presentation.api.schemas.schema import (
    AccessTokenResponse as AccessTokenResponseSchema,
)


class AccessTokenResponseMapper:
    """Mapper class to convert AccessTokenResponse to AccessTokenResponse."""

    @staticmethod
    def response(dto: AccessTokenResponseDTO) -> AccessTokenResponseSchema:
        """Returns a AccessTokenResponseDTO object mapped from AccessTokenResponseSchema.

        Args:
            dto (AccessTokenResponseDTO): The response DTO containing token info.

        Returns:
            AccessTokenResponseSchema: The mapped access token response schema.
        """
        return AccessTokenResponseSchema(
            access_token=dto.access_token,
            token_type=dto.token_type,
            expires_in=dto.expires_in,
            expires_at=dto.expires_at,
        )
