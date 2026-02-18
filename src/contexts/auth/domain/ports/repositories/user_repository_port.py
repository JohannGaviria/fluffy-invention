"""This module contains the interface for the User Repository Port."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.auth.domain.entities.entity import RolesEnum, UserEntity
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO


class UserRepositoryPort(ABC):
    """Abstract interface for User Repository operations."""

    @abstractmethod
    def find_by_id(self, id: UUID) -> UserEntity | None:
        """Find a user by their user id.

        Args:
            id (UUID): The id to search for.

        Returns:
            UserEntity | None: The user entity if found, otherwise None
        """
        pass

    @abstractmethod
    def find_by_email(self, email: EmailVO) -> UserEntity | None:
        """Find a user by their email address.

        Args:
            email (EmailVO): The email value object to search for.

        Returns:
            UserEntity | None: The user entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def save(self, entity: UserEntity) -> UserEntity:
        """Save a user entity to the repository.

        Args:
            entity (UserEntity): The user entity to save.

        Returns:
            UserEntity: The saved user entity.
        """
        pass

    @abstractmethod
    def status_update(self, status: bool, user_id: UUID) -> None:
        """Update the status of a user.

        Args:
            status (bool): The new status to set.
            user_id (UUID): The unique identifier of the user.
        """
        pass

    @abstractmethod
    def find_by_role(self, role: RolesEnum) -> list[UserEntity]:
        """Find users by their role.

        Args:
            role (RolesEnum): The role to search for.

        Returns:
            list[UserEntity]: A list of user entities with the specified role.
        """
        pass

    @abstractmethod
    def update_password(self, user_id: UUID, new: PasswordHashVO) -> None:
        """Update the password of the user.

        Args:
            user_id (UUID): The unique identifier of the user.
            new (PasswordHashVO): The new password hash to update.

        Returns:
            None
        """
        pass
