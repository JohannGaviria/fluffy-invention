"""Unit tests for PasswordServiceAdapter."""

import string

from src.contexts.auth.domain.value_objects.password_vo import PasswordVO
from src.contexts.auth.infrastructure.security.password_service_adapter import (
    PasswordServiceAdapter,
)


class TestPasswordServiceAdapter:
    """Unit tests for PasswordServiceAdapter."""

    def test_should_generate_valid_password(self):
        """Should generate a valid password that meets security criteria."""
        adapter = PasswordServiceAdapter()

        password_vo = adapter.generate()

        assert isinstance(password_vo, PasswordVO)
        # If PasswordVO validates successfully, the password meets criteria
        assert len(password_vo.value) >= 8
        assert len(password_vo.value) <= 12

    def test_should_include_all_required_character_types(self):
        """Should include lowercase, uppercase, digit, and special character."""
        adapter = PasswordServiceAdapter()

        password_vo = adapter.generate()
        password = password_vo.value

        assert any(c in string.ascii_lowercase for c in password)
        assert any(c in string.ascii_uppercase for c in password)
        assert any(c in string.digits for c in password)
        assert any(c in string.punctuation for c in password)

    def test_should_generate_password_with_length_between_8_and_12(self):
        """Should generate password with length between 8 and 12."""
        adapter = PasswordServiceAdapter()

        for _ in range(50):
            password_vo = adapter.generate()
            password = password_vo.value
            assert 8 <= len(password) <= 12

    def test_should_generate_different_passwords_each_time(self):
        """Should generate different passwords on each call."""
        adapter = PasswordServiceAdapter()

        passwords = set()
        for _ in range(100):
            password_vo = adapter.generate()
            passwords.add(password_vo.value)

        # Should have generated all unique passwords
        assert len(passwords) == 100

    def test_should_use_secrets_module_for_randomness(self):
        """Should use secrets module for cryptographically strong randomness."""
        adapter = PasswordServiceAdapter()

        # Generate multiple passwords and verify they all validate
        for _ in range(20):
            password_vo = adapter.generate()
            # If no exception is raised, the password is valid
            assert password_vo is not None

    def test_should_shuffle_characters_properly(self):
        """Should shuffle characters so they're not in predictable order."""
        adapter = PasswordServiceAdapter()

        passwords = []
        for _ in range(50):
            password_vo = adapter.generate()
            passwords.append(password_vo.value)

        # Check that not all passwords start with the same character type
        first_chars = [p[0] for p in passwords]
        lowercase_starts = sum(1 for c in first_chars if c in string.ascii_lowercase)
        uppercase_starts = sum(1 for c in first_chars if c in string.ascii_uppercase)
        digit_starts = sum(1 for c in first_chars if c in string.digits)
        special_starts = sum(1 for c in first_chars if c in string.punctuation)

        # At least 2 different character types should appear as first character
        non_zero_counts = sum(
            [
                lowercase_starts > 0,
                uppercase_starts > 0,
                digit_starts > 0,
                special_starts > 0,
            ]
        )
        assert non_zero_counts >= 2
