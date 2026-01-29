"""This module contains the Value Objects for Token Payload used in the authentication context."""

from dataclasses import dataclass
from uuid import UUID, uuid4

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class TokenPayloadVO(BaseValueObject):
    """Value Object representing the payload for a token.

    Attributes:
        user_id (UUID): The ID of the user.
        role (RolesEnum): The role of the user.
        expires_in (int): The expiration time in seconds.
        jti (UUID | None): The unique identifier for the token.

    Raises:
        ValueError: If any of the fields are invalid.
    """

    user_id: UUID
    role: RolesEnum
    expires_in: int
    jti: UUID | None = None

    def validate(self) -> None:
        """Validate the token payload.

        Raises:
            ValueError: If any of the fields are invalid.
        """
        if not self.user_id:
            raise ValueError("user_id cannot be empty")

        if not self.role or not self.role.strip():
            raise ValueError("role cannot be empty")

        if self.expires_in <= 0:
            raise ValueError("expires_in must be positive")

    @classmethod
    def generate(
        cls, user_id: UUID, role: RolesEnum, expires_in: int
    ) -> "TokenPayloadVO":
        """Generate a TokenPayloadVO from a UserEntity.

        Args:
            user_id (UUID): The ID of the user.
            role (RolesEnum): The role of the user.
            expires_in (int): Expiration time in seconds.

        Returns:
            TokenPayloadVO: The generated token payload value object.
        """
        return cls(
            jti=uuid4(),
            user_id=user_id,
            role=role.value,
            expires_in=expires_in,
        )

    def to_dict(self) -> dict:
        """Convert TokenPayloadVO to dictionary.

        Returns:
            dict: Dictionary representation of the token payload.
        """
        return {
            "sub": str(self.user_id),
            "role": self.role,
            "jti": str(self.jti),
            "expires_in": self.expires_in,
        }
