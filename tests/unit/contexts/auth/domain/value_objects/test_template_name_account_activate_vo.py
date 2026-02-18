"""Unit tests for TemplateNameAccountActivateVO."""

from dataclasses import FrozenInstanceError

import pytest

from src.contexts.auth.domain.value_objects.template_name_account_activate_vo import (
    TemplateNameAccountActivateVO,
)


class TestTemplateNameAccountActivateVO:
    """Unit tests for TemplateNameAccountActivateVO."""

    def test_should_create_template_name_account_activate_vo_successfully(self):
        """Should create TemplateNameAccountActivateVO successfully."""
        vo = TemplateNameAccountActivateVO.create()
        assert vo.name == "auth_activation_code.html"

    def test_should_create_same_name_consistently(self):
        """Should create the same template name on multiple calls."""
        vo1 = TemplateNameAccountActivateVO.create()
        vo2 = TemplateNameAccountActivateVO.create()

        assert vo1.name == vo2.name

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = TemplateNameAccountActivateVO.create()

        with pytest.raises(FrozenInstanceError):
            vo.name = "new_template.html"

    def test_should_inherit_from_template_name_vo(self):
        """Should inherit validation from TemplateNameVO."""
        vo = TemplateNameAccountActivateVO.create()
        # The name should not be empty or whitespace (validated by parent class)
        assert vo.name
        assert vo.name.strip()
