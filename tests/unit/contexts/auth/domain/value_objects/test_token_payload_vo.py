"""Unit tests for TokenPayloadVO."""

from uuid import uuid4

import pytest

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO


class TestTokenPayloadVO:
    """Unit tests for TokenPayloadVO."""

    def test_should_create_token_payload_vo_successfully(self):
        """Should create TokenPayloadVO successfully with valid data."""
        user_id = uuid4()
        role = RolesEnum.ADMIN
        expires_in = 3600
        vo = TokenPayloadVO.generate(user_id=user_id, role=role, expires_in=expires_in)

        assert vo.user_id == user_id
        assert vo.role == role.value
        assert vo.expires_in == expires_in
        assert vo.jti is not None

    def test_should_raise_value_error_for_invalid_user_id(self):
        """Should raise ValueError for empty user_id."""
        with pytest.raises(ValueError) as exc_info:
            TokenPayloadVO(user_id=None, role=RolesEnum.ADMIN, expires_in=3600)
        assert "user_id cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_invalid_role(self):
        """Should raise ValueError for empty role."""
        with pytest.raises(ValueError) as exc_info:
            TokenPayloadVO(user_id=uuid4(), role=None, expires_in=3600)
        assert "role cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_invalid_expires_in(self):
        """Should raise ValueError for non-positive expires_in."""
        with pytest.raises(ValueError) as exc_info:
            TokenPayloadVO(user_id=uuid4(), role=RolesEnum.ADMIN, expires_in=0)
        assert "expires_in must be positive" in str(exc_info.value)
