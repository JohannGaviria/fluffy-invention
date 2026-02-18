"""Unit tests for AccessTokenVO."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta

import pytest

from src.contexts.auth.domain.value_objects.access_token_vo import AccessTokenVO


class TestAccessTokenVO:
    """Unit tests for AccessTokenVO."""

    def test_should_create_access_token_vo_successfully(self):
        """Should create AccessTokenVO successfully with valid data."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        token = AccessTokenVO(
            access_token="valid_token_123",
            token_type="Bearer",
            expires_at=expires_at,
            expires_in=3600,
        )
        assert token.access_token == "valid_token_123"
        assert token.token_type == "Bearer"
        assert token.expires_at == expires_at
        assert token.expires_in == 3600

    def test_should_raise_value_error_for_empty_access_token(self):
        """Should raise ValueError for empty access_token."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        with pytest.raises(ValueError) as exc_info:
            AccessTokenVO(
                access_token="",
                token_type="Bearer",
                expires_at=expires_at,
                expires_in=3600,
            )
        assert "access_token cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_access_token(self):
        """Should raise ValueError for access_token with only whitespace."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        with pytest.raises(ValueError) as exc_info:
            AccessTokenVO(
                access_token="   ",
                token_type="Bearer",
                expires_at=expires_at,
                expires_in=3600,
            )
        assert "access_token cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_invalid_token_type(self):
        """Should raise ValueError for invalid token_type."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        with pytest.raises(ValueError) as exc_info:
            AccessTokenVO(
                access_token="valid_token_123",
                token_type="InvalidType",
                expires_at=expires_at,
                expires_in=3600,
            )
        assert "Invalid token_type: InvalidType" in str(exc_info.value)

    def test_should_raise_value_error_for_negative_expires_in(self):
        """Should raise ValueError for negative expires_in."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        with pytest.raises(ValueError) as exc_info:
            AccessTokenVO(
                access_token="valid_token_123",
                token_type="Bearer",
                expires_at=expires_at,
                expires_in=-100,
            )
        assert "expires_in must be positive" in str(exc_info.value)

    def test_should_raise_value_error_for_zero_expires_in(self):
        """Should raise ValueError for zero expires_in."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        with pytest.raises(ValueError) as exc_info:
            AccessTokenVO(
                access_token="valid_token_123",
                token_type="Bearer",
                expires_at=expires_at,
                expires_in=0,
            )
        assert "expires_in must be positive" in str(exc_info.value)

    def test_should_raise_value_error_for_naive_datetime(self):
        """Should raise ValueError for timezone-naive expires_at."""
        expires_at = datetime.now()  # Naive datetime without timezone
        with pytest.raises(ValueError) as exc_info:
            AccessTokenVO(
                access_token="valid_token_123",
                token_type="Bearer",
                expires_at=expires_at,
                expires_in=3600,
            )
        assert "expires_at must be timezone-aware (UTC)" in str(exc_info.value)

    def test_should_raise_value_error_for_past_expires_at(self):
        """Should raise ValueError for expires_at in the past."""
        expires_at = datetime.now(UTC) - timedelta(hours=1)
        with pytest.raises(ValueError) as exc_info:
            AccessTokenVO(
                access_token="valid_token_123",
                token_type="Bearer",
                expires_at=expires_at,
                expires_in=3600,
            )
        assert "expires_at must be in the future" in str(exc_info.value)

    def test_should_convert_to_dict_successfully(self):
        """Should convert AccessTokenVO to dictionary successfully."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        token = AccessTokenVO(
            access_token="valid_token_123",
            token_type="Bearer",
            expires_at=expires_at,
            expires_in=3600,
        )
        result = AccessTokenVO.to_dict(token)
        assert result == {
            "access_token": "valid_token_123",
            "token_type": "Bearer",
            "expires_at": expires_at,
            "expires_in": 3600,
        }

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        token = AccessTokenVO(
            access_token="valid_token_123",
            token_type="Bearer",
            expires_at=expires_at,
            expires_in=3600,
        )
        with pytest.raises(FrozenInstanceError):
            token.access_token = "new_token"
