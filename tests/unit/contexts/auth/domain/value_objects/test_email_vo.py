"""This module contains unit tests for the EmailVO."""

import pytest

from src.contexts.auth.domain.exceptions.exception import InvalidEmailException
from src.contexts.auth.domain.value_objects.email_vo import EmailVO


class TestEmailVO:
    """Unit test for EmailVO."""

    def test_should_create_email_vo(self, faker):
        """Should create a EmailVO."""
        email = faker.email()
        email_vo = EmailVO(email)
        assert email_vo.value == email

    def test_should_email_pass_validation(self, faker):
        """Should email validation."""
        email = faker.email()
        email_vo = EmailVO(email)
        email_vo.validate()
        assert email_vo.value == email

    @pytest.mark.parametrize(
        "email",
        [
            "user @example.com",
            "user\texample@example.com",
            "user\n@example.com",
            " user@example.com",
            "user@example.com ",
            "user..name@example.com",
            "user@example..com",
            "..user@example.com",
            "userexample.com",
            "user@.com",
            "@example.com",
            "user@com",
            "user@.com.",
            "user@com.",
            "user@-example.com",
            "user@example",
            "user@.",
            "user@.domain.com",
        ],
    )
    def test_should_raise_error_email_invalid_format(self, email):
        """Should raise InvalidEmailException for invalid email format."""
        with pytest.raises(InvalidEmailException):
            EmailVO(email)

    def test_should_get_email(self, faker):
        """Should get email."""
        email = faker.email()
        email_vo = EmailVO(email)
        assert email_vo.email == email
        assert email_vo.value == email

    def test_should_return_str_repr(self, faker):
        """Should return a string representation."""
        email = faker.email()
        email_vo = EmailVO(email)
        assert str(email_vo) == email
        assert repr(email_vo) == f"EmailVO({email})"
