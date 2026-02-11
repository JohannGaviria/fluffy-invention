"""Unit tests for SQLModelPatientRepositoryAdapter."""

from datetime import UTC, date, datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.contexts.auth.domain.entities.entity import PatientEntity
from src.contexts.auth.infrastructure.persistence.models.model import PatientModel
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_patient_repository_adapter import (
    SQLModelPatientRepositoryAdapter,
)
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)


class TestSQLModelPatientRepositoryAdapter:
    """Unit tests for SQLModelPatientRepositoryAdapter."""

    @pytest.fixture
    def session_mock(self):
        """Create a mock SQLModel session."""
        session = MagicMock()
        session.exec = MagicMock()
        session.add = MagicMock()
        session.commit = MagicMock()
        session.rollback = MagicMock()
        return session

    @pytest.fixture
    def logger_mock(self):
        """Create a mock logger."""
        return MagicMock()

    @pytest.fixture
    def repository(self, session_mock, logger_mock):
        """Create repository instance with mocked dependencies."""
        return SQLModelPatientRepositoryAdapter(
            session=session_mock, logger=logger_mock
        )

    @pytest.fixture
    def patient_model(self):
        """Create a sample PatientModel."""
        return PatientModel(
            id=uuid4(),
            user_id=uuid4(),
            document="123456789",
            phone="+1234567890",
            birth_date=date(1990, 1, 1),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    @pytest.fixture
    def patient_entity(self):
        """Create a sample PatientEntity."""
        return PatientEntity(
            id=uuid4(),
            user_id=uuid4(),
            document="987654321",
            phone="+9876543210",
            birth_date=date(1995, 5, 5),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    # ========== FIND BY USER ID TESTS ==========

    def test_should_find_patient_by_user_id_successfully(
        self, repository, session_mock, patient_model
    ):
        """Should find patient by user_id successfully."""
        user_id = patient_model.user_id
        result_mock = MagicMock()
        result_mock.first.return_value = patient_model
        session_mock.exec.return_value = result_mock

        patient = repository.find_by_user_id(user_id)

        assert patient is not None
        assert isinstance(patient, PatientEntity)
        assert patient.user_id == user_id
        session_mock.exec.assert_called_once()

    def test_should_return_none_when_patient_not_found_by_user_id(
        self, repository, session_mock
    ):
        """Should return None when patient is not found by user_id."""
        user_id = uuid4()
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        patient = repository.find_by_user_id(user_id)

        assert patient is None

    def test_should_raise_database_connection_exception_on_operational_error_find_by_user_id(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when finding by user_id."""
        user_id = uuid4()
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.find_by_user_id(user_id)

        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_find_by_user_id(
        self, repository, session_mock, logger_mock
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when finding by user_id."""
        user_id = uuid4()
        session_mock.exec.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.find_by_user_id(user_id)

        logger_mock.error.assert_called_once()

    # ========== FIND BY DOCUMENT TESTS ==========

    def test_should_find_patient_by_document_successfully(
        self, repository, session_mock, patient_model
    ):
        """Should find patient by document successfully."""
        document = patient_model.document
        result_mock = MagicMock()
        result_mock.first.return_value = patient_model
        session_mock.exec.return_value = result_mock

        patient = repository.find_by_document(document)

        assert patient is not None
        assert isinstance(patient, PatientEntity)
        assert patient.document == document

    def test_should_return_none_when_patient_not_found_by_document(
        self, repository, session_mock
    ):
        """Should return None when patient is not found by document."""
        document = "999999999"
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        patient = repository.find_by_document(document)

        assert patient is None

    def test_should_raise_database_connection_exception_on_operational_error_find_by_document(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when finding by document."""
        document = "123456789"
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.find_by_document(document)

        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_find_by_document(
        self, repository, session_mock, logger_mock
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when finding by document."""
        document = "123456789"
        session_mock.exec.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.find_by_document(document)

        logger_mock.error.assert_called_once()

    # ========== FIND BY PHONE TESTS ==========

    def test_should_find_patient_by_phone_successfully(
        self, repository, session_mock, patient_model
    ):
        """Should find patient by phone successfully."""
        phone = patient_model.phone
        result_mock = MagicMock()
        result_mock.first.return_value = patient_model
        session_mock.exec.return_value = result_mock

        patient = repository.find_by_phone(phone)

        assert patient is not None
        assert isinstance(patient, PatientEntity)
        assert patient.phone == phone

    def test_should_return_none_when_patient_not_found_by_phone(
        self, repository, session_mock
    ):
        """Should return None when patient is not found by phone."""
        phone = "+0000000000"
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        patient = repository.find_by_phone(phone)

        assert patient is None

    def test_should_raise_database_connection_exception_on_operational_error_find_by_phone(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when finding by phone."""
        phone = "+1234567890"
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.find_by_phone(phone)

        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_find_by_phone(
        self, repository, session_mock, logger_mock
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when finding by phone."""
        phone = "+1234567890"
        session_mock.exec.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.find_by_phone(phone)

        logger_mock.error.assert_called_once()

    # ========== SAVE TESTS ==========

    def test_should_save_patient_successfully(
        self, repository, session_mock, patient_entity
    ):
        """Should save patient successfully."""
        repository.save(patient_entity)

        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()

    def test_should_raise_database_connection_exception_on_operational_error_save(
        self, repository, session_mock, logger_mock, patient_entity
    ):
        """Should raise DatabaseConnectionException on OperationalError when saving."""
        session_mock.add.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.save(patient_entity)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_save(
        self, repository, session_mock, logger_mock, patient_entity
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when saving."""
        session_mock.commit.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.save(patient_entity)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()
