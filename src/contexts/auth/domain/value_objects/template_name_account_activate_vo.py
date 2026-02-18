"""This module contains the TemplateNameAccountActivateVO value object."""

from dataclasses import dataclass

from src.shared.domain.value_objects.template_name_vo import TemplateNameVO


@dataclass(frozen=True)
class TemplateNameAccountActivateVO(TemplateNameVO):
    """Value object for the template name used for account activation."""

    @classmethod
    def create(cls) -> "TemplateNameAccountActivateVO":
        """Creates a TemplateNameAccountActivateVO instance with the predefined template name.

        Returns:
            TemplateNameAccountActivateVO: Instance with template name for account activation.
        """
        return cls(name="auth_activation_code.html")
