"""This module contains the TemplateNameCreateAdminVO value object."""

from dataclasses import dataclass

from src.shared.domain.value_objects.template_name_vo import TemplateNameVO


@dataclass(frozen=True)
class TemplateNameCreateAdminVO(TemplateNameVO):
    """Value object for the template name used to create the first admin."""

    @classmethod
    def create(cls) -> "TemplateNameCreateAdminVO":
        """Creates a TemplateNameCreateAdminVO instance with the predefined template name.

        Returns:
            TemplateNameCreateAdminVO: Instance with template name for creating the first admin.
        """
        return cls(name="auth_create_first_admin.html")
