"""This module contains the TemplateRendererVO value object."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from src.shared.domain.value_objects.template_context_vo import TemplateContextVO
from src.shared.domain.value_objects.template_name_vo import TemplateNameVO
from src.shared.domain.value_objects.value_object import BaseValueObject

TemplateRendererContextType = TypeVar(
    "TemplateRendererContextType", bound=TemplateContextVO
)


@dataclass(frozen=True)
class TemplateRendererVO(BaseValueObject, Generic[TemplateRendererContextType]):  # noqa: UP046
    """Value object for template rendering."""

    template_name: TemplateNameVO
    context: TemplateRendererContextType

    def validate(self) -> None:
        """Validates the TemplateRendererVO instance.

        Raises:
            ValueError: If the context is None.
        """
        if self.context is None:
            raise ValueError("Context cannot be None.")
