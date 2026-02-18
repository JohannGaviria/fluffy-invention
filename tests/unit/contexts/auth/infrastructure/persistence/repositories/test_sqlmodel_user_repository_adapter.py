"""Unit tests for SQLModelRepositoryAdapter (User Repository)."""

from datetime import UTC, datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.contexts.auth.domain.entities.entity import RolesEnum, UserEntity
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.domain.value_objects.password_hash_vo import PasswordHashVO
from src.contexts.auth.infrastructure.persistence.models.model import UserModel
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_user_repository_adapter import (
    SQLModelRepositoryAdapter,
)
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)

_VALID_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJXRz.HV9K"


class TestSQLModelRepositoryAdapter:
    """Unit tests for SQLModelRepositoryAdapter."""

    @pytest.fixture
    def session_mock(self):
        """Create a mock SQLModel session."""
        session = MagicMock()
        session.exec = MagicMock()
        session.add = MagicMock()
        session.commit = MagicMock()
        session.rollback = MagicMock()
        session.refresh = MagicMock()
        return session

    @pytest.fixture
    def logger_mock(self):
        """Create a mock logger."""
        return MagicMock()

    @pytest.fixture
    def repository(self, session_mock, logger_mock):
        """Create repository instance with mocked dependencies."""
        return SQLModelRepositoryAdapter(session=session_mock, logger=logger_mock)

    @pytest.fixture
    def user_model(self):
        """Create a sample UserModel."""
        return UserModel(
            id=uuid4(),
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password=_VALID_HASH,
            role=RolesEnum.PATIENT,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    @pytest.fixture
    def user_entity(self):
        """Create a sample UserEntity."""
        return UserEntity(
            id=uuid4(),
            first_name="Jane",
            last_name="Smith",
            email=EmailVO("jane@example.com"),
            password_hash=PasswordHashVO(_VALID_HASH),
            role=RolesEnum.DOCTOR,
            is_active=False,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    # ========== FIND BY ID TESTS ==========

    def test_should_find_user_by_id_successfully(
        self, repository, session_mock, user_model
    ):
        """Should find user by id successfully."""
        user_id = user_model.id
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock

        user = repository.find_by_id(user_id)

        assert user is not None
        assert isinstance(user, UserEntity)
        assert user.id == user_id
        session_mock.exec.assert_called_once()

    def test_should_return_none_when_user_not_found_by_id(
        self, repository, session_mock
    ):
        """Should return None when user is not found by id."""
        user_id = uuid4()
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        user = repository.find_by_id(user_id)

        assert user is None

    def test_should_raise_database_connection_exception_on_operational_error_find_by_id(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when finding by id."""
        user_id = uuid4()
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.find_by_id(user_id)

        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_find_by_id(
        self, repository, session_mock, logger_mock
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when finding by id."""
        user_id = uuid4()
        session_mock.exec.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.find_by_id(user_id)

        logger_mock.error.assert_called_once()

    def test_should_map_model_fields_correctly_when_found_by_id(
        self, repository, session_mock, user_model
    ):
        """Should correctly map UserModel fields to UserEntity when finding by id."""
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock

        user = repository.find_by_id(user_model.id)

        assert user.first_name == user_model.first_name
        assert user.last_name == user_model.last_name
        assert user.email.value == user_model.email
        assert user.role == user_model.role
        assert user.is_active == user_model.is_active

    # ========== FIND BY EMAIL TESTS ==========

    def test_should_find_user_by_email_successfully(
        self, repository, session_mock, user_model
    ):
        """Should find user by email successfully."""
        email = EmailVO("john@example.com")
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock

        user = repository.find_by_email(email)

        assert user is not None
        assert isinstance(user, UserEntity)
        assert user.email.value == "john@example.com"
        session_mock.exec.assert_called_once()

    def test_should_return_none_when_user_not_found_by_email(
        self, repository, session_mock
    ):
        """Should return None when user is not found by email."""
        email = EmailVO("nonexistent@example.com")
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        user = repository.find_by_email(email)

        assert user is None

    def test_should_raise_database_connection_exception_on_operational_error_find_by_email(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when finding by email."""
        email = EmailVO("john@example.com")
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.find_by_email(email)

        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_find_by_email(
        self, repository, session_mock, logger_mock
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when finding by email."""
        email = EmailVO("john@example.com")
        session_mock.exec.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.find_by_email(email)

        logger_mock.error.assert_called_once()

    # ========== SAVE TESTS ==========

    def test_should_save_user_successfully(
        self, repository, session_mock, user_entity, user_model
    ):
        """Should save user successfully."""
        session_mock.refresh.side_effect = lambda model: setattr(
            model, "id", user_entity.id
        )

        saved_user = repository.save(user_entity)

        assert saved_user is not None
        assert isinstance(saved_user, UserEntity)
        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once()

    def test_should_raise_database_connection_exception_on_operational_error_save(
        self, repository, session_mock, logger_mock, user_entity
    ):
        """Should raise DatabaseConnectionException on OperationalError when saving."""
        session_mock.add.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.save(user_entity)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_save(
        self, repository, session_mock, logger_mock, user_entity
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when saving."""
        session_mock.commit.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.save(user_entity)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    # ========== STATUS UPDATE TESTS ==========

    def test_should_update_user_status_successfully(
        self, repository, session_mock, user_model
    ):
        """Should update user status successfully."""
        user_id = user_model.id
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock

        repository.status_update(status=True, user_id=user_id)

        assert user_model.is_active is True
        session_mock.add.assert_called_once_with(user_model)
        session_mock.commit.assert_called_once()

    def test_should_not_update_when_user_not_found(self, repository, session_mock):
        """Should not update when user is not found."""
        user_id = uuid4()
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        repository.status_update(status=True, user_id=user_id)

        session_mock.add.assert_not_called()
        session_mock.commit.assert_not_called()

    def test_should_raise_database_connection_exception_on_operational_error_status_update(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when updating status."""
        user_id = uuid4()
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.status_update(status=True, user_id=user_id)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_status_update(
        self, repository, session_mock, logger_mock, user_model
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when updating status."""
        user_id = user_model.id
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock
        session_mock.commit.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.status_update(status=True, user_id=user_id)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    # ========== FIND BY ROLE TESTS ==========

    def test_should_find_users_by_role_successfully(
        self, repository, session_mock, user_model
    ):
        """Should find users by role successfully."""
        result_mock = MagicMock()
        result_mock.all.return_value = [user_model]
        session_mock.exec.return_value = result_mock

        users = repository.find_by_role(RolesEnum.PATIENT)

        assert len(users) == 1
        assert isinstance(users[0], UserEntity)
        assert users[0].role == RolesEnum.PATIENT

    def test_should_return_empty_list_when_no_users_found_by_role(
        self, repository, session_mock
    ):
        """Should return empty list when no users found by role."""
        result_mock = MagicMock()
        result_mock.all.return_value = []
        session_mock.exec.return_value = result_mock

        users = repository.find_by_role(RolesEnum.ADMIN)

        assert users == []

    def test_should_find_multiple_users_by_role(self, repository, session_mock):
        """Should find multiple users by role."""
        user1 = UserModel(
            id=uuid4(),
            first_name="User1",
            last_name="Test",
            email="user1@example.com",
            password=_VALID_HASH,
            role=RolesEnum.DOCTOR,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        user2 = UserModel(
            id=uuid4(),
            first_name="User2",
            last_name="Test",
            email="user2@example.com",
            password=_VALID_HASH,
            role=RolesEnum.DOCTOR,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        result_mock = MagicMock()
        result_mock.all.return_value = [user1, user2]
        session_mock.exec.return_value = result_mock

        users = repository.find_by_role(RolesEnum.DOCTOR)

        assert len(users) == 2
        assert all(u.role == RolesEnum.DOCTOR for u in users)

    def test_should_raise_database_connection_exception_on_operational_error_find_by_role(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when finding by role."""
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.find_by_role(RolesEnum.ADMIN)

        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_find_by_role(
        self, repository, session_mock, logger_mock
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when finding by role."""
        session_mock.exec.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.find_by_role(RolesEnum.ADMIN)

        logger_mock.error.assert_called_once()

    # ========== UPDATE PASSWORD TESTS ==========

    def test_should_update_password_successfully(
        self, repository, session_mock, user_model
    ):
        """Should update user password successfully."""
        user_id = user_model.id
        new_hash = PasswordHashVO(_VALID_HASH)

        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock

        repository.update_password(user_id, new_hash)

        assert user_model.password == str(new_hash)
        session_mock.add.assert_called_once_with(user_model)
        session_mock.commit.assert_called_once()

    def test_should_not_update_password_when_user_not_found(
        self, repository, session_mock
    ):
        """Should not update password when user is not found."""
        user_id = uuid4()
        new_hash = PasswordHashVO(_VALID_HASH)

        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        repository.update_password(user_id, new_hash)

        session_mock.add.assert_not_called()
        session_mock.commit.assert_not_called()

    def test_should_store_new_password_hash_as_string(
        self, repository, session_mock, user_model
    ):
        """Should store the new password hash as a string on the model."""
        new_hash = PasswordHashVO(_VALID_HASH)
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock

        repository.update_password(user_model.id, new_hash)

        assert isinstance(user_model.password, str)
        assert user_model.password == str(new_hash)

    def test_should_raise_database_connection_exception_on_operational_error_update_password(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when updating password."""
        user_id = uuid4()
        new_hash = PasswordHashVO(_VALID_HASH)
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.update_password(user_id, new_hash)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_update_password(
        self, repository, session_mock, logger_mock, user_model
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when updating password."""
        new_hash = PasswordHashVO(_VALID_HASH)
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock
        session_mock.commit.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.update_password(user_model.id, new_hash)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    def test_should_rollback_on_operational_error_update_password(
        self, repository, session_mock, logger_mock
    ):
        """Should rollback transaction on OperationalError during update_password."""
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.update_password(uuid4(), PasswordHashVO(_VALID_HASH))

        session_mock.rollback.assert_called_once()

    def test_should_rollback_on_sqlalchemy_error_update_password(
        self, repository, session_mock, logger_mock, user_model
    ):
        """Should rollback transaction on SQLAlchemyError during update_password."""
        result_mock = MagicMock()
        result_mock.first.return_value = user_model
        session_mock.exec.return_value = result_mock
        session_mock.commit.side_effect = SQLAlchemyError("unexpected")

        with pytest.raises(UnexpectedDatabaseException):
            repository.update_password(user_model.id, PasswordHashVO(_VALID_HASH))

        session_mock.rollback.assert_called_once()
