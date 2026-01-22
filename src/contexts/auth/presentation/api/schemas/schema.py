"""This module contains the schema for user registration requests."""

from datetime import datetime

from pydantic import BaseModel

from src.contexts.auth.application.dto.command import LoginCommand, RegisterUserCommand
from src.contexts.auth.domain.entities.entity import RolesEnum


class RegisterUserRequest(BaseModel):
    """Request schema for registering a new user.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        role (RolesEnum): The role assigned to the user.
        role_recorder (str): The identifier of the entity recording the role.
    """

    first_name: str
    last_name: str
    email: str
    role: RolesEnum
    role_recorder: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "role": "patient",
                "role_recorder": "admin",
            }
        }
    }

    def to_command(self) -> RegisterUserCommand:
        """Converts the request data to a RegisterUserCommand.

        Returns:
            RegisterUserCommand: The command object with the request data.
        """
        return RegisterUserCommand(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            role=self.role,
            role_recorder=self.role_recorder,
        )


class ActivateUserAccountRequest(BaseModel):
    """Request schema for activating a user account.

    Attributes:
        activation_code (str): The activation code sent to the user's email.
        email (str): The email address of the user.
    """

    activation_code: str
    email: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "activation_code": "HA23E0",
                "email": "john.doe@example.com",
            }
        }
    }


class LoginRequest(BaseModel):
    """Request schema for user login.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass!23",
            }
        }
    }

    def to_command(self) -> LoginCommand:
        """Converts the request data to a LoginCommand.

        Returns:
            LoginCommand: The command object with the request data.
        """
        return LoginCommand(
            email=self.email,
            password=self.password,
        )


class AccessTokenResponse(BaseModel):
    """Response schema for access token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token (e.g., Bearer).
        expires_at (str): The expiration datetime of the token.
        expires_in (int): The time in seconds until the token expires.
    """

    access_token: str
    token_type: str
    expires_at: datetime
    expires_in: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_at": "2026-01-25T05:39:54.815252Z",
                "expires_in": 3600,
            }
        }
    }

    @classmethod
    def from_response_dto(cls, dto: "AccessTokenResponse") -> "AccessTokenResponse":
        """Creates an AccessTokenResponse schema from a response DTO.

        Args:
            dto (AccessTokenResponse): The response DTO.

        Returns:
            AccessTokenResponse: The schema instance.
        """
        return cls(
            access_token=dto.access_token,
            token_type=dto.token_type,
            expires_at=dto.expires_at,
            expires_in=dto.expires_in,
        )
