"""Unit tests for PasswordHashServiceAdapter."""

from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO
from src.contexts.auth.infrastructure.security.password_hash_service_adapter import (
    PasswordHashServiceAdapter,
)


class TestPasswordHashServiceAdapter:
    """Unit tests for PasswordHashServiceAdapter."""

    def test_should_hash_password_successfully(self):
        """Should hash a password successfully."""
        adapter = PasswordHashServiceAdapter()
        password = PasswordVO("SecurePass123!")

        hashed = adapter.hashed(password)

        assert isinstance(hashed, PasswordHashVO)
        assert hashed.value.startswith("$2b$")
        assert len(hashed.value) == 60  # bcrypt hash length

    def test_should_generate_different_hashes_for_same_password(self):
        """Should generate different hashes for the same password (salt)."""
        adapter = PasswordHashServiceAdapter()
        password = PasswordVO("SecurePass123!")

        hash1 = adapter.hashed(password)
        hash2 = adapter.hashed(password)

        # Different hashes due to different salts
        assert hash1.value != hash2.value

    def test_should_verify_correct_password(self):
        """Should verify correct password successfully."""
        adapter = PasswordHashServiceAdapter()
        plain_password = PasswordVO("SecurePass123!")
        hashed_password = adapter.hashed(plain_password)

        result = adapter.verify(plain_password, hashed_password)

        assert result is True

    def test_should_not_verify_incorrect_password(self):
        """Should not verify incorrect password."""
        adapter = PasswordHashServiceAdapter()
        correct_password = PasswordVO("SecurePass123!")
        wrong_password = PasswordVO("WrongPass456!")
        hashed_password = adapter.hashed(correct_password)

        result = adapter.verify(wrong_password, hashed_password)

        assert result is False

    def test_should_verify_with_different_adapter_instances(self):
        """Should verify password with different adapter instances."""
        adapter1 = PasswordHashServiceAdapter()
        adapter2 = PasswordHashServiceAdapter()

        password = PasswordVO("SecurePass123!")
        hashed = adapter1.hashed(password)

        result = adapter2.verify(password, hashed)

        assert result is True

    def test_should_hash_different_passwords_to_different_hashes(self):
        """Should hash different passwords to different hashes."""
        adapter = PasswordHashServiceAdapter()
        password1 = PasswordVO("Password123!")
        password2 = PasswordVO("DifferentPass456!")

        hash1 = adapter.hashed(password1)
        hash2 = adapter.hashed(password2)

        assert hash1.value != hash2.value

    def test_should_not_verify_password_with_wrong_hash(self):
        """Should not verify password with completely wrong hash."""
        adapter = PasswordHashServiceAdapter()
        password = PasswordVO("SecurePass123!")
        wrong_hash = PasswordHashVO(
            "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"
        )

        result = adapter.verify(password, wrong_hash)

        assert result is False
