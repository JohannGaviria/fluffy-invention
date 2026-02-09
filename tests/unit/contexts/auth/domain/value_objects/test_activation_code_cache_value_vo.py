"""Unit tests for ActivationCodeCacheValueVO."""

from uuid import uuid4

import pytest

from src.contexts.auth.domain.value_objects.activation_code_cache_value_vo import (
    ActivationCodeCacheValueVO,
)
from src.contexts.auth.domain.value_objects.email_vo import EmailVO


class TestActivationCodeCacheValueVO:
    """Unit tests for ActivationCodeCacheValueVO."""

    def test_should_create_activation_code_cache_value_vo_successfully(self):
        """Should create ActivationCodeCacheValueVO successfully with valid data."""
        user_id = uuid4()
        email = EmailVO(email="test@example.com")
        code = "123456"
        vo = ActivationCodeCacheValueVO(user_id=user_id, email=email, code=code)

        assert vo.user_id == user_id
        assert vo.email == email
        assert vo.code == code

    def test_should_raise_value_error_for_empty_code(self):
        """Should raise ValueError for empty activation code."""
        user_id = uuid4()
        email = EmailVO(email="test@example.com")

        with pytest.raises(ValueError) as exc_info:
            ActivationCodeCacheValueVO(user_id=user_id, email=email, code="")
        assert "Activation code cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_long_code(self):
        """Should raise ValueError for activation code longer than 6 characters."""
        user_id = uuid4()
        email = EmailVO(email="test@example.com")

        with pytest.raises(ValueError) as exc_info:
            ActivationCodeCacheValueVO(user_id=user_id, email=email, code="1234567")
        assert "Activation code too long" in str(exc_info.value)
