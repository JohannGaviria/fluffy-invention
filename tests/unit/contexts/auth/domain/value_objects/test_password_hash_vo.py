"""This module contains uni tests for the PasswordHashVO."""

import pytest

from src.contexts.auth.domain.exceptions.exception import InvalidPasswordHashException
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO


class TestPasswordHashVO:
    """Unit tests for PasswordHashVO."""

    def test_should_create_password_hash_vo(self):
        """Should create a password hash VO."""
        password_hash = "$2b$12$RX3OV/wuXSfqufXUX4zV0eBgkNzWtC/IpHMk2qzsSkop3qi4bgDnC"
        password_hash_vo = PasswordHashVO(password_hash)
        assert password_hash_vo.value == password_hash

    def test_should_password_hash_pass_validation(self):
        """Should password hash validation."""
        password_hash = "$2b$12$RX3OV/wuXSfqufXUX4zV0eBgkNzWtC/IpHMk2qzsSkop3qi4bgDnC"
        password_hash_vo = PasswordHashVO(password_hash)
        password_hash_vo.validate()
        assert password_hash_vo.value == password_hash

    @pytest.mark.parametrize(
        "password_hash",
        [
            "2b$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$3b$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2x$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2b$1$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2b$123$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2b$ab$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2b$12$abc",
            "$2b$12$abcdefghijklmnopqrstuvwxyzABCDE",
            "$2b$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./ABCDEFG",
            "$2b$12$abcDEF1234567890+INVALIDINVALIDINVALIDINVALIDINVALIDINVALID",
            "$2b$12$abcDEF1234567890=INVALIDINVALIDINVALIDINVALIDINVALIDINVALID",
            "$2b$12$abcDEF12345@67890INVALIDINVALIDINVALIDINVALIDINVALIDINVALID",
            "$2b12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$$2b$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2b$$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2b$12$passwordpasswordpasswordpasswordpasswordpasswordpassword",
            "$2b$12$-----------------------------------------------------",
            "$2b$12$＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
            "$2b$12$ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
            "$2b$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A ",
            "$2b$\n12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./A",
        ],
    )
    def test_should_raise_error_password_hash_invalid_format(self, password_hash):
        """Should raise InvalidPasswordHashException when password hash is invalid."""
        with pytest.raises(InvalidPasswordHashException):
            PasswordHashVO(password_hash)

    def test_should_get_password_hash(self):
        """Should get password hash."""
        password_hash = "$2b$12$RX3OV/wuXSfqufXUX4zV0eBgkNzWtC/IpHMk2qzsSkop3qi4bgDnC"
        password_hash_vo = PasswordHashVO(password_hash)
        assert password_hash_vo.password_hash == password_hash
        assert password_hash_vo.value == password_hash

    def test_should_return_str_repr(self):
        """Should return a string representation."""
        password_hash = "$2b$12$RX3OV/wuXSfqufXUX4zV0eBgkNzWtC/IpHMk2qzsSkop3qi4bgDnC"
        password_hash_vo = PasswordHashVO(password_hash)
        assert str(password_hash_vo) == password_hash
        assert repr(password_hash_vo) == f"PasswordHashVO({password_hash})"
