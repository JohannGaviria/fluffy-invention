"""This module contains unit test for BaseException."""

import pytest

from src.shared.domain.exceptions.exception import (
    BaseDomainException,
    DatabaseConnectionException,
    MissingFieldException,
    UnexpectedDatabaseException,
)


def test_should_domain_exception_is_exception():
    """Should raise an exception if domain exception is raised."""
    assert issubclass(BaseDomainException, Exception)


def test_should_database_connection_exception_message_and_attr():
    """Should raise an exception if database connection exception is raised."""
    msg = "could not connect"

    with pytest.raises(DatabaseConnectionException) as exc_info:
        raise DatabaseConnectionException(msg)

    exc = exc_info.value

    assert hasattr(exc, "message")
    assert exc.message == msg
    assert "Database connection error" in str(exc)


def test_should_unexpected_database_exception_message_and_attr():
    """Should raise an exception if unexpected database exception is raised."""
    msg = "timeout"

    with pytest.raises(UnexpectedDatabaseException) as exc_info:
        raise UnexpectedDatabaseException(msg)

    exc = exc_info.value

    assert hasattr(exc, "message")
    assert exc.message == msg
    assert "Unexpected database error" in str(exc)


def test_should_missing_field_exception_message_and_attr():
    """Should raise an exception if missing field exception is raised."""
    field = "field_1"
    error = "field_1 is required"

    with pytest.raises(MissingFieldException) as exc_info:
        raise MissingFieldException(field, error)

    exc = exc_info.value

    assert exc.field == field
    assert exc.error == error
    assert f"{field}: {error}" in str(exc)
