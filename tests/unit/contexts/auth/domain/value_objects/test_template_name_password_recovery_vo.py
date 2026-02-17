"""Unit tests for TemplateNamePasswordRecoveryVO."""

from dataclasses import FrozenInstanceError

import pytest

from src.contexts.auth.domain.value_objects.template_name_password_recovery_vo import (
    TemplateNamePasswordRecoveryVO,
)


class TestTemplateNamePasswordRecoveryVO:
    """Unit tests for TemplateNamePasswordRecoveryVO."""

    def test_should_create_with_predefined_template_name(self):
        """Should create with the predefined password-recovery template name."""
        vo = TemplateNamePasswordRecoveryVO.create()
        assert vo.name == "auth_password_recovery.html"

    def test_should_return_same_name_on_multiple_calls(self):
        """create() must always return the same template name."""
        vo1 = TemplateNamePasswordRecoveryVO.create()
        vo2 = TemplateNamePasswordRecoveryVO.create()
        assert vo1.name == vo2.name

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = TemplateNamePasswordRecoveryVO.create()
        with pytest.raises(FrozenInstanceError):
            vo.name = "other.html"

    def test_name_is_non_empty(self):
        """Template name must be non-empty."""
        vo = TemplateNamePasswordRecoveryVO.create()
        assert vo.name and vo.name.strip()
