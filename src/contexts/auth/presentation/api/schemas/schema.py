"""This module contains the schema for user registration requests."""

from pydantic import BaseModel

from src.contexts.auth.application.dto.command import RegisterUserCommand
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
