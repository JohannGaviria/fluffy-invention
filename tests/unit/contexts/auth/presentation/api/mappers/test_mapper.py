"""Unit tests for AccessTokenResponseMapper."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from src.contexts.auth.application.dto.response import (
    AccessTokenResponse as AccessTokenResponseDTO,
)
from src.contexts.auth.presentation.api.mappers.mapper import AccessTokenResponseMapper
from src.contexts.auth.presentation.api.schemas.schema import (
    AccessTokenResponse as AccessTokenResponseSchema,
)


class TestAccessTokenResponseMapper:
    """Unit tests for AccessTokenResponseMapper."""

    def _make_dto(
        self,
        access_token: str = "valid.jwt.token",
        token_type: str = "Bearer",
        expires_in: int = 3600,
        expires_at: datetime | None = None,
    ) -> AccessTokenResponseDTO:
        """Helper to build a AccessTokenResponseDTO."""
        if expires_at is None:
            expires_at = datetime(2009, 2, 13, 23, 31, 30, tzinfo=UTC)
        dto = MagicMock(spec=AccessTokenResponseDTO)
        dto.access_token = access_token
        dto.token_type = token_type
        dto.expires_in = expires_in
        dto.expires_at = expires_at
        return dto

    # ──────────────────────────── happy path ────────────────────────────

    def test_should_map_dto_to_schema_successfully(self):
        """Should map AccessTokenResponseDTO to AccessTokenResponseSchema."""
        expected_expires_at = datetime(2009, 2, 13, 23, 31, 30, tzinfo=UTC)
        dto = self._make_dto(expires_at=expected_expires_at)

        result = AccessTokenResponseMapper.response(dto)

        assert isinstance(result, AccessTokenResponseSchema)
        assert result.access_token == "valid.jwt.token"
        assert result.token_type == "Bearer"
        assert result.expires_in == 3600
        assert result.expires_at == expected_expires_at

    def test_should_preserve_access_token_value(self):
        """Should preserve the access_token value exactly."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.signature"
        dto = self._make_dto(access_token=token)

        result = AccessTokenResponseMapper.response(dto)

        assert result.access_token == token

    def test_should_preserve_token_type(self):
        """Should preserve the token_type value."""
        dto = self._make_dto(token_type="Bearer")

        result = AccessTokenResponseMapper.response(dto)

        assert result.token_type == "Bearer"

    def test_should_preserve_expires_in(self):
        """Should preserve the expires_in value."""
        dto = self._make_dto(expires_in=7200)

        result = AccessTokenResponseMapper.response(dto)

        assert result.expires_in == 7200

    def test_should_preserve_expires_at(self):
        """Should preserve the expires_at value."""
        expected = datetime(2286, 11, 20, 17, 46, 39, tzinfo=UTC)
        dto = self._make_dto(expires_at=expected)

        result = AccessTokenResponseMapper.response(dto)

        assert result.expires_at == expected

    def test_should_return_schema_instance(self):
        """Should always return an instance of AccessTokenResponseSchema."""
        dto = self._make_dto()

        result = AccessTokenResponseMapper.response(dto)

        assert type(result) is AccessTokenResponseSchema

    def test_should_be_callable_as_static_method(self):
        """Should be callable without instantiating the mapper class."""
        dto = self._make_dto()

        # Call directly on the class, not on an instance
        result = AccessTokenResponseMapper.response(dto)

        assert result is not None

    def test_should_map_different_dtos_independently(self):
        """Should map each DTO independently without shared state."""
        dto1 = self._make_dto(access_token="token_one", expires_in=3600)
        dto2 = self._make_dto(access_token="token_two", expires_in=7200)

        result1 = AccessTokenResponseMapper.response(dto1)
        result2 = AccessTokenResponseMapper.response(dto2)

        assert result1.access_token == "token_one"
        assert result1.expires_in == 3600
        assert result2.access_token == "token_two"
        assert result2.expires_in == 7200
        assert result1 is not result2

    def test_should_map_minimum_expires_in(self):
        """Should correctly map minimum expires_in value."""
        dto = self._make_dto(expires_in=1)

        result = AccessTokenResponseMapper.response(dto)

        assert result.expires_in == 1

    def test_should_map_epoch_expires_at(self):
        """Should correctly map epoch datetime as expires_at."""
        epoch = datetime(1970, 1, 1, 0, 0, 0, tzinfo=UTC)
        dto = self._make_dto(expires_at=epoch)

        result = AccessTokenResponseMapper.response(dto)

        assert result.expires_at == epoch

    def test_all_fields_transferred_correctly(self):
        """Should transfer all four fields correctly in a single assertion."""
        access_token = "abc.def.ghi"
        token_type = "Bearer"
        expires_in = 1800
        expires_at = datetime(2023, 11, 14, 22, 13, 20, tzinfo=UTC)

        dto = self._make_dto(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
            expires_at=expires_at,
        )

        result = AccessTokenResponseMapper.response(dto)

        assert result.access_token == access_token
        assert result.token_type == token_type
        assert result.expires_in == expires_in
        assert result.expires_at == expires_at
