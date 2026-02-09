"""Unit tests for TemplateContextCreateAdminVO."""

from dataclasses import FrozenInstanceError

import pytest

from src.contexts.auth.domain.value_objects.template_context_create_admin_vo import (
    TemplateContextCreateAdminVO,
)


class TestTemplateContextCreateAdminVO:
    """Unit tests for TemplateContextCreateAdminVO."""

    def test_should_create_template_context_create_admin_vo_successfully(self):
        """Should create TemplateContextCreateAdminVO successfully with valid data."""
        vo = TemplateContextCreateAdminVO(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            temporary_password="AdminPass123!",
        )
        assert vo.first_name == "Admin"
        assert vo.last_name == "User"
        assert vo.email == "admin@example.com"
        assert vo.temporary_password == "AdminPass123!"

    def test_should_raise_value_error_for_empty_first_name(self):
        """Should raise ValueError for empty first_name."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="",
                last_name="User",
                email="admin@example.com",
                temporary_password="AdminPass123!",
            )
        assert "First name cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_first_name(self):
        """Should raise ValueError for whitespace-only first_name."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="   ",
                last_name="User",
                email="admin@example.com",
                temporary_password="AdminPass123!",
            )
        assert "First name cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_empty_last_name(self):
        """Should raise ValueError for empty last_name."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="Admin",
                last_name="",
                email="admin@example.com",
                temporary_password="AdminPass123!",
            )
        assert "Last name cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_last_name(self):
        """Should raise ValueError for whitespace-only last_name."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="Admin",
                last_name="   ",
                email="admin@example.com",
                temporary_password="AdminPass123!",
            )
        assert "Last name cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_empty_email(self):
        """Should raise ValueError for empty email."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="Admin",
                last_name="User",
                email="",
                temporary_password="AdminPass123!",
            )
        assert "Email cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_email(self):
        """Should raise ValueError for whitespace-only email."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="Admin",
                last_name="User",
                email="   ",
                temporary_password="AdminPass123!",
            )
        assert "Email cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_empty_temporary_password(self):
        """Should raise ValueError for empty temporary_password."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                temporary_password="",
            )
        assert "Temporary password cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_temporary_password(self):
        """Should raise ValueError for whitespace-only temporary_password."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                temporary_password="   ",
            )
        assert "Temporary password cannot be empty" in str(exc_info.value)

    def test_should_convert_to_dict_successfully(self):
        """Should convert TemplateContextCreateAdminVO to dictionary successfully."""
        vo = TemplateContextCreateAdminVO(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            temporary_password="AdminPass123!",
        )
        result = vo.to_dict()
        assert result == {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "temporary_password": "AdminPass123!",
        }

    def test_should_create_from_dict_successfully(self):
        """Should create TemplateContextCreateAdminVO from dictionary successfully."""
        data = {
            "first_name": "Super",
            "last_name": "Admin",
            "email": "super@example.com",
            "temporary_password": "SuperPass123!",
        }
        vo = TemplateContextCreateAdminVO.from_dict(data)
        assert vo.first_name == "Super"
        assert vo.last_name == "Admin"
        assert vo.email == "super@example.com"
        assert vo.temporary_password == "SuperPass123!"

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = TemplateContextCreateAdminVO(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            temporary_password="AdminPass123!",
        )
        with pytest.raises(FrozenInstanceError):
            vo.first_name = "NewAdmin"

    def test_should_validate_on_creation_from_dict(self):
        """Should validate when creating from dictionary."""
        with pytest.raises(ValueError) as exc_info:
            TemplateContextCreateAdminVO.from_dict(
                {
                    "first_name": "",
                    "last_name": "User",
                    "email": "admin@example.com",
                    "temporary_password": "AdminPass123!",
                }
            )
        assert "First name cannot be empty" in str(exc_info.value)
