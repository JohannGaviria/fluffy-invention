"""This module contains uni tests for the PasswordVO."""

import pytest

from src.contexts.auth.domain.exceptions.exception import InvalidPasswordException
from src.contexts.auth.domain.value_objects.password_vo import PasswordVO


class TestPasswordVO:
    """Unit tests for PasswordVO."""

    def test_should_create_password_vo(self, faker):
        """Should create a password VO."""
        password = faker.password()
        password_vo = PasswordVO(password)
        assert password_vo.value == password

    def test_should_password_pass_validation(self, faker):
        """Should password validation."""
        password = faker.password()
        password_vo = PasswordVO(password)
        password_vo.validate()
        assert password_vo.value == password

    @pytest.mark.parametrize(
        "password",
        [
            "A1a!",
            "abc1!",
            "Z9*",
            "ABCDEFGH",
            "password1!",
            "abcde123!",
            "hello@123",
            "PASSWORD1!",
            "HELLO@123",
            "ABCDEF9$",
            "Password!",
            "Hello@World",
            "Admin$User",
            "Password1",
            "HelloWorld9",
            "AdminUser123",
            "password!",
            "hello@you",
            "test@me",
            "password1",
            "hello1234",
            "test9999",
            "12345678!",
            "9999@999",
            "1111$$$$",
            "PASSWORD!",
            "HELLO@YOU",
            "ADMIN$ROOT",
            "PASSWORD1",
            "HELLO1234",
            "ADMIN9999",
            "Password",
            "HelloWorld",
            "AdminUser",
            "password",
            "helloworld",
            "testcase",
            "aaaaaaaa",
            "11111111",
            "!!!!!!!!",
        ],
    )
    def test_should_raise_error_password_invalid_format(self, password):
        """Should raise InvalidPasswordException when password is invalid."""
        with pytest.raises(InvalidPasswordException):
            PasswordVO(password)

    def test_should_get_password(self, faker):
        """Should get password."""
        password = faker.password()
        password_vo = PasswordVO(password)
        assert password_vo.password == password
        assert password_vo.value == password

    def test_should_return_str_repr(self, faker):
        """Should return a string representation."""
        password = faker.password()
        password_vo = PasswordVO(password)
        assert str(password_vo) == password
        assert repr(password_vo) == f"PasswordVO({password})"
