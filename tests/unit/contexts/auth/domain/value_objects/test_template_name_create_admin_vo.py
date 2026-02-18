"""Unit tests for TemplateNameCreateAdminVO."""

from src.contexts.auth.domain.value_objects.template_name_create_admin_vo import (
    TemplateNameCreateAdminVO,
)


class TestTemplateNameCreateAdminVO:
    """Unit tests for TemplateNameCreateAdminVO."""

    def test_should_create_template_name_create_admin_vo(self):
        """Should create TemplateNameCreateAdminVO with predefined template name."""
        vo = TemplateNameCreateAdminVO.create()
        assert vo.name == "auth_create_first_admin.html"
