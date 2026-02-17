"""Unit tests for PasswordRecoveryCacheValueVO."""

from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_recovery_cache_value_vo import (
    PasswordRecoveryCacheValueVO,
)


class TestPasswordRecoveryCacheValueVO:
    """Unit tests for PasswordRecoveryCacheValueVO."""

    def _make_vo(
        self,
        user_id=None,
        email=None,
        recovery_code="ABC123",
    ) -> PasswordRecoveryCacheValueVO:
        """Helper to build a valid PasswordRecoveryCacheValueVO."""
        return PasswordRecoveryCacheValueVO(
            user_id=user_id or uuid4(),
            email=email or EmailVO("user@example.com"),
            recovery_code=recovery_code,
        )

    # ──────────────────────────── creation ──────────────────────────────

    def test_should_create_successfully_with_valid_data(self):
        """Should create PasswordRecoveryCacheValueVO with valid data."""
        user_id = uuid4()
        email = EmailVO("user@example.com")
        vo = PasswordRecoveryCacheValueVO(
            user_id=user_id, email=email, recovery_code="ABC123"
        )

        assert vo.user_id == user_id
        assert vo.email == email
        assert vo.recovery_code == "ABC123"

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = self._make_vo()

        with pytest.raises(FrozenInstanceError):
            vo.recovery_code = "NEW123"

    # ──────────────────────────── validate ──────────────────────────────
    # validate() is called automatically in __post_init__, so invalid
    # instances raise ValueError at construction time.

    def test_validate_raises_when_user_id_is_none(self):
        """Should raise ValueError at construction when user_id is None."""
        with pytest.raises(ValueError, match="user_id cannot be empty"):
            PasswordRecoveryCacheValueVO(
                user_id=None,
                email=EmailVO("user@example.com"),
                recovery_code="ABC123",
            )

    def test_validate_raises_when_email_is_none(self):
        """Should raise ValueError at construction when email is None."""
        with pytest.raises(ValueError, match="email cannot be empty"):
            PasswordRecoveryCacheValueVO(
                user_id=uuid4(),
                email=None,
                recovery_code="ABC123",
            )

    def test_validate_raises_when_recovery_code_is_empty(self):
        """Should raise ValueError at construction when recovery_code is empty."""
        with pytest.raises(ValueError, match="Code cannot be empty"):
            PasswordRecoveryCacheValueVO(
                user_id=uuid4(),
                email=EmailVO("user@example.com"),
                recovery_code="",
            )

    def test_validate_raises_when_recovery_code_is_whitespace(self):
        """Should raise ValueError at construction when recovery_code is only whitespace."""
        with pytest.raises(ValueError, match="Code cannot be empty"):
            PasswordRecoveryCacheValueVO(
                user_id=uuid4(),
                email=EmailVO("user@example.com"),
                recovery_code="   ",
            )

    def test_validate_raises_when_recovery_code_exceeds_six_chars(self):
        """Should raise ValueError at construction when recovery_code is longer than 6 chars."""
        with pytest.raises(ValueError, match="Recovery code too long"):
            PasswordRecoveryCacheValueVO(
                user_id=uuid4(),
                email=EmailVO("user@example.com"),
                recovery_code="ABCDEFG",
            )

    def test_validate_passes_with_exactly_six_chars(self):
        """Should not raise for a recovery_code of exactly 6 characters."""
        vo = self._make_vo(recovery_code="ABC123")
        vo.validate()  # should not raise

    def test_validate_passes_with_less_than_six_chars(self):
        """Should not raise for a recovery_code shorter than 6 characters."""
        vo = self._make_vo(recovery_code="AB1")
        vo.validate()  # should not raise

    # ──────────────────────────── to_dict ───────────────────────────────

    def test_to_dict_returns_correct_structure(self):
        """Should return a dict with user_id, email, and recovery_code."""
        user_id = uuid4()
        email = EmailVO("user@example.com")
        vo = PasswordRecoveryCacheValueVO(
            user_id=user_id, email=email, recovery_code="XYZ789"
        )

        result = vo.to_dict()

        assert result == {
            "user_id": str(user_id),
            "email": "user@example.com",
            "recovery_code": "XYZ789",
        }

    def test_to_dict_user_id_is_string(self):
        """user_id in dict must be a string."""
        vo = self._make_vo()
        result = vo.to_dict()
        assert isinstance(result["user_id"], str)

    def test_to_dict_email_is_string(self):
        """Email in dict must be the plain string value."""
        vo = self._make_vo(email=EmailVO("check@example.com"))
        result = vo.to_dict()
        assert result["email"] == "check@example.com"

    # ──────────────────────────── from_dict ─────────────────────────────

    def test_from_dict_creates_instance_correctly(self):
        """Should recreate a PasswordRecoveryCacheValueVO from its dict form."""
        user_id = uuid4()
        data = {
            "user_id": str(user_id),
            "email": "user@example.com",
            "recovery_code": "ABC123",
        }

        vo = PasswordRecoveryCacheValueVO.from_dict(data)

        assert vo.user_id == user_id
        assert vo.email == EmailVO("user@example.com")
        assert vo.recovery_code == "ABC123"

    def test_from_dict_roundtrip_preserves_data(self):
        """to_dict → from_dict should be a lossless round-trip."""
        original = self._make_vo()
        restored = PasswordRecoveryCacheValueVO.from_dict(original.to_dict())

        assert restored.user_id == original.user_id
        assert restored.email == original.email
        assert restored.recovery_code == original.recovery_code
