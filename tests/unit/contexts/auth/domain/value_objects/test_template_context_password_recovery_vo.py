"""Unit tests for PasswordRecoveryCacheValueVO."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from typing import TypedDict, Unpack

import pytest

from src.contexts.auth.domain.value_objects.template_context_password_recovery_vo import (
    TemplateContextPasswordRecoveryVO,
)


class _PasswordRecoveryOverrides(TypedDict, total=False):
    """Overrides for default values for PasswordRecoveryCacheValueVO."""

    first_name: str
    last_name: str
    recovery_code: str
    expiration_minutes: int
    request_datetime: datetime
    request_ip: str
    request_user_agent: str


class TestTemplateContextPasswordRecoveryVO:
    """Unit tests for TemplateContextPasswordRecoveryVO."""

    def _make_vo(
        self,
        **overrides: Unpack[_PasswordRecoveryOverrides],
    ) -> TemplateContextPasswordRecoveryVO:
        """Make a TemplateContextPasswordRecoveryVO with default values."""
        defaults: _PasswordRecoveryOverrides = {
            "first_name": "John",
            "last_name": "Doe",
            "recovery_code": "ABC123",
            "expiration_minutes": 45,
            "request_datetime": datetime.now(UTC),
            "request_ip": "192.168.1.1",
            "request_user_agent": "Mozilla/5.0",
        }

        data: _PasswordRecoveryOverrides = {**defaults, **overrides}

        return TemplateContextPasswordRecoveryVO(
            first_name=data["first_name"],
            last_name=data["last_name"],
            recovery_code=data["recovery_code"],
            expiration_minutes=data["expiration_minutes"],
            request_datetime=data["request_datetime"],
            request_ip=data["request_ip"],
            request_user_agent=data["request_user_agent"],
        )

    # ────────────────────────── creation ────────────────────────────────

    def test_should_create_successfully_with_valid_data(self):
        """Should create TemplateContextPasswordRecoveryVO with all valid fields."""
        now = datetime.now(UTC)
        vo = TemplateContextPasswordRecoveryVO(
            first_name="Jane",
            last_name="Smith",
            recovery_code="XY1234",
            expiration_minutes=30,
            request_datetime=now,
            request_ip="10.0.0.1",
            request_user_agent="curl/7.0",
        )
        assert vo.first_name == "Jane"
        assert vo.last_name == "Smith"
        assert vo.recovery_code == "XY1234"
        assert vo.expiration_minutes == 30
        assert vo.request_datetime == now
        assert vo.request_ip == "10.0.0.1"
        assert vo.request_user_agent == "curl/7.0"

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = self._make_vo()
        with pytest.raises(FrozenInstanceError):
            vo.first_name = "Other"

    # ──────────────────────── validate – first_name ──────────────────────
    # validate() is called in __post_init__, so invalid values raise at
    # construction time; _make_vo() must NOT be used for invalid cases.

    def test_validate_raises_for_empty_first_name(self):
        """Should raise ValueError at construction when first_name is empty."""
        with pytest.raises(ValueError, match="First name cannot be empty"):
            self._make_vo(first_name="")

    def test_validate_raises_for_whitespace_first_name(self):
        """Should raise ValueError at construction when first_name is only whitespace."""
        with pytest.raises(ValueError, match="First name cannot be empty"):
            self._make_vo(first_name="   ")

    # ──────────────────────── validate – last_name ───────────────────────

    def test_validate_raises_for_empty_last_name(self):
        """Should raise ValueError at construction when last_name is empty."""
        with pytest.raises(ValueError, match="Last name cannot be empty"):
            self._make_vo(last_name="")

    def test_validate_raises_for_whitespace_last_name(self):
        """Should raise ValueError at construction when last_name is only whitespace."""
        with pytest.raises(ValueError, match="Last name cannot be empty"):
            self._make_vo(last_name="   ")

    # ──────────────────────── validate – recovery_code ───────────────────

    def test_validate_raises_for_empty_recovery_code(self):
        """Should raise ValueError at construction when recovery_code is empty."""
        with pytest.raises(ValueError, match="Recovery code cannot be empty"):
            self._make_vo(recovery_code="")

    # ──────────────────────── validate – expiration_minutes ──────────────

    def test_validate_raises_for_zero_expiration_minutes(self):
        """Should raise ValueError at construction when expiration_minutes is 0."""
        with pytest.raises(ValueError, match="Expiration minutes must be positive"):
            self._make_vo(expiration_minutes=0)

    def test_validate_raises_for_negative_expiration_minutes(self):
        """Should raise ValueError at construction when expiration_minutes is negative."""
        with pytest.raises(ValueError, match="Expiration minutes must be positive"):
            self._make_vo(expiration_minutes=-5)

    # ──────────────────────── validate – request_datetime ────────────────

    def test_validate_raises_for_none_request_datetime(self):
        """Should raise ValueError at construction when request_datetime is None."""
        with pytest.raises(ValueError, match="Request datetime cannot be empty"):
            self._make_vo(request_datetime=None)

    # ──────────────────────── validate – request_ip ───────────────────────

    def test_validate_raises_for_empty_request_ip(self):
        """Should raise ValueError at construction when request_ip is empty."""
        with pytest.raises(ValueError, match="Request IP cannot be empty"):
            self._make_vo(request_ip="")

    def test_validate_raises_for_whitespace_request_ip(self):
        """Should raise ValueError at construction when request_ip is only whitespace."""
        with pytest.raises(ValueError, match="Request IP cannot be empty"):
            self._make_vo(request_ip="   ")

    # ──────────────────────── validate – request_user_agent ──────────────

    def test_validate_raises_for_empty_request_user_agent(self):
        """Should raise ValueError at construction when request_user_agent is empty."""
        with pytest.raises(ValueError, match="Request user agent cannot be empty"):
            self._make_vo(request_user_agent="")

    def test_validate_raises_for_whitespace_request_user_agent(self):
        """Should raise ValueError at construction when request_user_agent is only whitespace."""
        with pytest.raises(ValueError, match="Request user agent cannot be empty"):
            self._make_vo(request_user_agent="   ")

    # ──────────────────────── validate – happy path ───────────────────────

    def test_validate_passes_with_all_valid_fields(self):
        """Should not raise when all fields are valid."""
        vo = self._make_vo()
        vo.validate()  # must not raise

    # ──────────────────────────── to_dict ────────────────────────────────

    def test_to_dict_returns_all_fields(self):
        """Should return a dict containing all context fields."""
        now = datetime.now(UTC)
        vo = TemplateContextPasswordRecoveryVO(
            first_name="John",
            last_name="Doe",
            recovery_code="ABC123",
            expiration_minutes=45,
            request_datetime=now,
            request_ip="127.0.0.1",
            request_user_agent="test-agent",
        )
        result = vo.to_dict()

        assert result["first_name"] == "John"
        assert result["last_name"] == "Doe"
        assert result["recovery_code"] == "ABC123"
        assert result["expiration_minutes"] == 45
        assert result["request_datetime"] == now
        assert result["request_ip"] == "127.0.0.1"
        assert result["request_user_agent"] == "test-agent"

    # ──────────────────────────── from_dict ──────────────────────────────

    def test_from_dict_creates_instance_correctly(self):
        """Should create a TemplateContextPasswordRecoveryVO from its dict."""
        now = datetime.now(UTC)
        data = {
            "first_name": "Alice",
            "last_name": "Wonder",
            "recovery_code": "ZZ9999",
            "expiration_minutes": 60,
            "request_datetime": now,
            "request_ip": "1.2.3.4",
            "request_user_agent": "PostmanRuntime",
        }
        vo = TemplateContextPasswordRecoveryVO.from_dict(data)

        assert vo.first_name == "Alice"
        assert vo.last_name == "Wonder"
        assert vo.recovery_code == "ZZ9999"
        assert vo.expiration_minutes == 60
        assert vo.request_datetime == now
        assert vo.request_ip == "1.2.3.4"
        assert vo.request_user_agent == "PostmanRuntime"

    def test_from_dict_roundtrip_preserves_data(self):
        """to_dict → from_dict should be lossless."""
        original = self._make_vo()
        restored = TemplateContextPasswordRecoveryVO.from_dict(original.to_dict())

        assert restored.first_name == original.first_name
        assert restored.last_name == original.last_name
        assert restored.recovery_code == original.recovery_code
        assert restored.expiration_minutes == original.expiration_minutes
        assert restored.request_datetime == original.request_datetime
        assert restored.request_ip == original.request_ip
        assert restored.request_user_agent == original.request_user_agent
