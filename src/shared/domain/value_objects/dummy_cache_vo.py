"""This module contains the value object for dummy cache data."""

from dataclasses import dataclass

from src.shared.domain.value_objects.cache_value_vo import CacheValueVO


@dataclass(frozen=True)
class DummyCacheVO(CacheValueVO):
    """Value object for dummy cache data."""

    data: str

    def to_dict(self) -> dict[str, str]:
        """Convert the value object to a dictionary.

        Returns:
            dict[str, str]: The dictionary representation of the value object.
        """
        return {"data": self.data}

    @classmethod
    def from_dict(cls, data):
        """Create a value object from a dictionary.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            DummyCacheVO: The value object created from the dictionary.
        """
        return cls(data=data["data"])
