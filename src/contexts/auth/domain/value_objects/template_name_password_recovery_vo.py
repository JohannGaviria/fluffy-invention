"""This module contains the TemplateNamePasswordRecoveryVO value object."""

from dataclasses import dataclass

from src.shared.domain.value_objects.template_name_vo import TemplateNameVO


@dataclass(frozen=True)
class TemplateNamePasswordRecoveryVO(TemplateNameVO):
    """Value object for the template name used in password recovery."""

    @classmethod
    def create(cls) -> "TemplateNamePasswordRecoveryVO":
        """Creates a TemplateNamePasswordRecoveryVO instance with the predefined template name.

        Returns:
            TemplateNamePasswordRecoveryVO: Instance with template name for password recovery.
        """
        name = "auth_password_recovery.html"
        return cls(name=name)
