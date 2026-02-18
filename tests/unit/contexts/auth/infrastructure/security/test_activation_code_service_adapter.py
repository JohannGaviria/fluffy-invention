"""Unit tests for ActivationCodeServiceAdapter."""

import string

from src.contexts.auth.infrastructure.security.activation_code_service_adapter import (
    ActivationCodeServiceAdapter,
)


class TestActivationCodeServiceAdapter:
    """Unit tests for ActivationCodeServiceAdapter."""

    def test_should_generate_activation_code_with_default_length(self):
        """Should generate activation code with default length of 6."""
        adapter = ActivationCodeServiceAdapter()

        code = adapter.generate()

        assert len(code) == 6
        assert all(c in string.ascii_uppercase + string.digits for c in code)

    def test_should_generate_activation_code_with_custom_length(self):
        """Should generate activation code with custom length."""
        adapter = ActivationCodeServiceAdapter()

        code = adapter.generate(length=8)

        assert len(code) == 8
        assert all(c in string.ascii_uppercase + string.digits for c in code)

    def test_should_generate_different_codes_each_time(self):
        """Should generate different activation codes on each call."""
        adapter = ActivationCodeServiceAdapter()

        codes = set()
        for _ in range(100):
            code = adapter.generate()
            codes.add(code)

        # Should have generated mostly unique codes
        assert len(codes) > 90  # Allow for some collisions

    def test_should_only_use_uppercase_and_digits(self):
        """Should only use uppercase letters and digits."""
        adapter = ActivationCodeServiceAdapter()

        for _ in range(50):
            code = adapter.generate()
            assert all(c in string.ascii_uppercase + string.digits for c in code)
            assert not any(c in string.ascii_lowercase for c in code)

    def test_should_generate_code_with_length_1(self):
        """Should generate activation code with length 1."""
        adapter = ActivationCodeServiceAdapter()

        code = adapter.generate(length=1)

        assert len(code) == 1

    def test_should_generate_code_with_length_10(self):
        """Should generate activation code with length 10."""
        adapter = ActivationCodeServiceAdapter()

        code = adapter.generate(length=10)

        assert len(code) == 10
