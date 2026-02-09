"""Unit tests for ActivationCodeCacheKeyVO."""

from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from src.contexts.auth.domain.value_objects.activation_code_cache_key_vo import (
    ActivationCodeCacheKeyVO,
)


class TestActivationCodeCacheKeyVO:
    """Unit tests for ActivationCodeCacheKeyVO."""

    def test_should_create_from_user_id_successfully(self):
        """Should create ActivationCodeCacheKeyVO from user_id successfully."""
        user_id = uuid4()
        cache_key = ActivationCodeCacheKeyVO.from_user_id(user_id)

        expected_key = f"cache:auth:activation_code:{str(user_id)}"
        assert cache_key.key == expected_key

    def test_should_create_different_keys_for_different_users(self):
        """Should create different cache keys for different user IDs."""
        user_id_1 = uuid4()
        user_id_2 = uuid4()

        cache_key_1 = ActivationCodeCacheKeyVO.from_user_id(user_id_1)
        cache_key_2 = ActivationCodeCacheKeyVO.from_user_id(user_id_2)

        assert cache_key_1.key != cache_key_2.key

    def test_should_create_same_key_for_same_user(self):
        """Should create the same cache key for the same user ID."""
        user_id = uuid4()

        cache_key_1 = ActivationCodeCacheKeyVO.from_user_id(user_id)
        cache_key_2 = ActivationCodeCacheKeyVO.from_user_id(user_id)

        assert cache_key_1.key == cache_key_2.key

    def test_should_have_correct_prefix(self):
        """Should have the correct cache key prefix."""
        user_id = uuid4()
        cache_key = ActivationCodeCacheKeyVO.from_user_id(user_id)

        assert cache_key.key.startswith("cache:auth:activation_code:")

    def test_should_include_user_id_in_key(self):
        """Should include the user ID in the cache key."""
        user_id = uuid4()
        cache_key = ActivationCodeCacheKeyVO.from_user_id(user_id)

        assert str(user_id) in cache_key.key

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        user_id = uuid4()
        cache_key = ActivationCodeCacheKeyVO.from_user_id(user_id)

        with pytest.raises(FrozenInstanceError):
            cache_key.key = "new_key"
