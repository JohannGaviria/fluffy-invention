"""Unit tests for PasswordRecoveryCacheKeyVO."""

from dataclasses import FrozenInstanceError

import pytest

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_recovery_cache_key_vo import (
    PasswordRecoveryCacheKeyVO,
)


class TestPasswordRecoveryCacheKeyVO:
    """Unit tests for PasswordRecoveryCacheKeyVO."""

    def test_should_create_from_email_successfully(self):
        """Should create PasswordRecoveryCacheKeyVO from email successfully."""
        email = EmailVO("user@example.com")
        cache_key = PasswordRecoveryCacheKeyVO.from_email(email)

        expected_key = "cache:auth:recovery_code:user@example.com"
        assert cache_key.key == expected_key

    def test_should_have_correct_prefix(self):
        """Should have the correct cache key prefix."""
        email = EmailVO("user@example.com")
        cache_key = PasswordRecoveryCacheKeyVO.from_email(email)

        assert cache_key.key.startswith("cache:auth:recovery_code:")

    def test_should_include_email_in_key(self):
        """Should include the email address in the cache key."""
        email = EmailVO("test@domain.com")
        cache_key = PasswordRecoveryCacheKeyVO.from_email(email)

        assert "test@domain.com" in cache_key.key

    def test_should_create_different_keys_for_different_emails(self):
        """Should create different cache keys for different emails."""
        email_1 = EmailVO("user1@example.com")
        email_2 = EmailVO("user2@example.com")

        cache_key_1 = PasswordRecoveryCacheKeyVO.from_email(email_1)
        cache_key_2 = PasswordRecoveryCacheKeyVO.from_email(email_2)

        assert cache_key_1.key != cache_key_2.key

    def test_should_create_same_key_for_same_email(self):
        """Should create the same cache key for the same email."""
        email = EmailVO("user@example.com")

        cache_key_1 = PasswordRecoveryCacheKeyVO.from_email(email)
        cache_key_2 = PasswordRecoveryCacheKeyVO.from_email(email)

        assert cache_key_1.key == cache_key_2.key

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        email = EmailVO("user@example.com")
        cache_key = PasswordRecoveryCacheKeyVO.from_email(email)

        with pytest.raises(FrozenInstanceError):
            cache_key.key = "new_key"
