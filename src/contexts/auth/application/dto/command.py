"""This module contains the DTO for the RegisterUserCommand."""

from dataclasses import dataclass


@dataclass
class RegisterUserCommand:
    """Command DTO for registering a new user.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        role (str): The role assigned to the user.
        role_recorder (str): The role of the user performing the registration.
    """

    first_name: str
    last_name: str
    email: str
    role: str
    role_recorder: str


@dataclass
class LoginCommand:
    """Command DTO for login of user.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    email: str
    password: str
