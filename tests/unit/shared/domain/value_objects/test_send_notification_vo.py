"""Unit tests for SendNotificationVO."""

import pytest

from src.shared.domain.value_objects.send_notification_vo import SendNotificationVO


class TestSendNotificationVO:
    """Unit tests for SendNotificationVO."""

    def test_should_create_send_notification_vo_successfully(self):
        """Should create SendNotificationVO successfully with valid data."""
        recipient = "test@example.com"
        subject = "Test Subject"
        body = "This is a test body."
        vo = SendNotificationVO(recipient=recipient, subject=subject, body=body)
        assert vo.recipient == recipient
        assert vo.subject == subject
        assert vo.body == body

    def test_should_create_with_spaces_around(self):
        """Should create SendNotificationVO successfully with spaces around content."""
        recipient = "  test@example.com  "
        subject = "  Test Subject  "
        body = "  This is a test body.  "
        vo = SendNotificationVO(recipient=recipient, subject=subject, body=body)
        assert vo.recipient == recipient
        assert vo.subject == subject
        assert vo.body == body

    def test_should_raise_value_error_for_empty_recipient(self):
        """Should raise ValueError for empty recipient."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(recipient="", subject="Test Subject", body="Test Body")
        assert "Recipient cannot be empty." in str(exc_info.value)

    def test_should_raise_value_error_for_empty_subject(self):
        """Should raise ValueError for empty subject."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(
                recipient="test@example.com", subject="", body="Test Body"
            )
        assert "Subject cannot be empty." in str(exc_info.value)

    def test_should_raise_value_error_for_empty_body(self):
        """Should raise ValueError for empty body."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(
                recipient="test@example.com", subject="Test Subject", body=""
            )
        assert "Body cannot be empty." in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_recipient(self):
        """Should raise ValueError for recipient with only whitespace."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(
                recipient="   ", subject="Test Subject", body="Test Body"
            )
        assert "Recipient cannot be empty." in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_subject(self):
        """Should raise ValueError for subject with only whitespace."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(
                recipient="test@example.com", subject="   ", body="Test Body"
            )
        assert "Subject cannot be empty." in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_body(self):
        """Should raise ValueError for body with only whitespace."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(
                recipient="test@example.com", subject="Test Subject", body="   "
            )
        assert "Body cannot be empty." in str(exc_info.value)

    def test_should_raise_value_error_for_tab_only_fields(self):
        """Should raise ValueError for fields with only tabs."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(recipient="\t\t", subject="Test", body="Test")
        assert "Recipient cannot be empty." in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(
                recipient="test@example.com", subject="\t\t", body="Test"
            )
        assert "Subject cannot be empty." in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(
                recipient="test@example.com", subject="Test", body="\t\t"
            )
        assert "Body cannot be empty." in str(exc_info.value)

    def test_should_raise_value_error_for_mixed_whitespace_fields(self):
        """Should raise ValueError for fields with mixed whitespace."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(recipient=" \t\n ", subject="Test", body="Test")
        assert "Recipient cannot be empty." in str(exc_info.value)

    def test_should_raise_first_error_found(self):
        """Should raise the first validation error encountered."""
        with pytest.raises(ValueError) as exc_info:
            SendNotificationVO(recipient="", subject="", body="")
        assert "Recipient cannot be empty." in str(exc_info.value)
