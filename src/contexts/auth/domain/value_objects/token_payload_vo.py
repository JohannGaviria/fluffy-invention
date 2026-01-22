"""This module contains the Value Objects for Token Payload used in the authentication context."""

from dataclasses import dataclass
from uuid import uuid4

from src.contexts.auth.domain.entities.entity import UserEntity
from src.shared.domain.value_object import BaseValueObject


@dataclass(frozen=True)
class TokenPayloadVO(BaseValueObject):
    """Value Object representing the payload for a token.

    Attributes:
        user_id (str): The ID of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.
        role (str): Tje role of the user.
        expires_in (int): The expiration time in seconds.
        jti (str | None): The unique identifier for the token.

    Raises:
        ValueError: If any of the fields are invalid.
    """

    user_id: str
    first_name: str
    last_name: str
    email: str
    role: str
    expires_in: int
    jti: str | None = None

    def validate(self) -> None:
        """Validate the token payload.

        Raises:
            ValueError: If any of the fields are invalid.
        """
        if not self.user_id or not self.user_id.strip():
            raise ValueError("user_id cannot be empty")

        if not self.first_name or not self.first_name.strip():
            raise ValueError("first name cannot be empty")

        if not self.last_name or not self.last_name.strip():
            raise ValueError("last name cannot be empty")

        if not self.email or "@" not in self.email:
            raise ValueError(f"Invalid email format: {self.email}")

        if not self.role or not self.role.strip():
            raise ValueError("role cannot be empty")

        if self.expires_in <= 0:
            raise ValueError("expires_in must be positive")

    @classmethod
    def generate(cls, entity: UserEntity, expires_in: int) -> "TokenPayloadVO":
        """Generate a TokenPayloadVO from a UserEntity.

        Args:
            entity (UserEntity): The user entity.
            expires_in (int): Expiration time in seconds.

        Returns:
            TokenPayloadVO: The generated token payload value object.
        """
        return cls(
            jti=str(uuid4()),
            user_id=str(entity.id),
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email.value,
            role=entity.role,
            expires_in=expires_in,
        )

    def to_dict(self) -> dict:
        """Convert TokenPayloadVO to dictionary.

        Returns:
            dict: Dictionary representation of the token payload.
        """
        return {
            "sub": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "jti": self.jti,
            "expires_in": self.expires_in,
        }
