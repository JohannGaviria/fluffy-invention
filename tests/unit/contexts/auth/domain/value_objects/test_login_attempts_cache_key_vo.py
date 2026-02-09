"""Unit tests for LoginAttemptsCacheKeyVO."""

from dataclasses import FrozenInstanceError

import pytest

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.login_attempts_cache_key_vo import (
    LoginAttemptsCacheKeyVO,
)


class TestLoginAttemptsCacheKeyVO:
    """Unit tests for LoginAttemptsCacheKeyVO."""

    def test_should_create_from_email_successfully(self):
        """Should create LoginAttemptsCacheKeyVO from email successfully."""
        email = EmailVO(email="test@example.com")
        cache_key = LoginAttemptsCacheKeyVO.from_email(email)

        expected_key = "cache:auth:login_attempts:test@example.com"
        assert cache_key.key == expected_key

    def test_should_create_different_keys_for_different_emails(self):
        """Should create different cache keys for different emails."""
        email_1 = EmailVO(email="user1@example.com")
        email_2 = EmailVO(email="user2@example.com")

        cache_key_1 = LoginAttemptsCacheKeyVO.from_email(email_1)
        cache_key_2 = LoginAttemptsCacheKeyVO.from_email(email_2)

        assert cache_key_1.key != cache_key_2.key

    def test_should_create_same_key_for_same_email(self):
        """Should create the same cache key for the same email."""
        email = EmailVO(email="test@example.com")

        cache_key_1 = LoginAttemptsCacheKeyVO.from_email(email)
        cache_key_2 = LoginAttemptsCacheKeyVO.from_email(email)

        assert cache_key_1.key == cache_key_2.key

    def test_should_have_correct_prefix(self):
        """Should have the correct cache key prefix."""
        email = EmailVO(email="test@example.com")
        cache_key = LoginAttemptsCacheKeyVO.from_email(email)

        assert cache_key.key.startswith("cache:auth:login_attempts:")

    def test_should_include_email_in_key(self):
        """Should include the email address in the cache key."""
        email = EmailVO(email="test@example.com")
        cache_key = LoginAttemptsCacheKeyVO.from_email(email)

        assert "test@example.com" in cache_key.key

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        email = EmailVO(email="test@example.com")
        cache_key = LoginAttemptsCacheKeyVO.from_email(email)

        with pytest.raises(FrozenInstanceError):
            cache_key.key = "new_key"
