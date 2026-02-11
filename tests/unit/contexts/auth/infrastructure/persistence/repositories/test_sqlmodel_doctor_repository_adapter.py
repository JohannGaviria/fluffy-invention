"""Unit tests for SQLModelDoctorRepositoryAdapter."""

from datetime import UTC, datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.contexts.auth.domain.entities.entity import DoctorEntity
from src.contexts.auth.infrastructure.persistence.models.model import DoctorModel
from src.contexts.auth.infrastructure.persistence.repositories.sqlmodel_doctor_repository_adapter import (
    SQLModelDoctorRepositoryAdapter,
)
from src.shared.domain.exceptions.exception import (
    DatabaseConnectionException,
    UnexpectedDatabaseException,
)


class TestSQLModelDoctorRepositoryAdapter:
    """Unit tests for SQLModelDoctorRepositoryAdapter."""

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
        return SQLModelDoctorRepositoryAdapter(session=session_mock, logger=logger_mock)

    @pytest.fixture
    def doctor_model(self):
        """Create a sample DoctorModel."""
        return DoctorModel(
            id=uuid4(),
            user_id=uuid4(),
            specialty_id=uuid4(),
            license_number="MED123456",
            experience_years=5,
            qualifications="Board Certified",
            bio="Experienced physician",
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    @pytest.fixture
    def doctor_entity(self):
        """Create a sample DoctorEntity."""
        return DoctorEntity(
            id=uuid4(),
            user_id=uuid4(),
            specialty_id=uuid4(),
            license_number="LIC789012",
            experience_years=10,
            qualifications="MD, PhD",
            bio="Specialist",
            is_active=False,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    # ========== FIND BY USER ID TESTS ==========

    def test_should_find_doctor_by_user_id_successfully(
        self, repository, session_mock, doctor_model
    ):
        """Should find doctor by user_id successfully."""
        user_id = doctor_model.user_id
        result_mock = MagicMock()
        result_mock.first.return_value = doctor_model
        session_mock.exec.return_value = result_mock

        doctor = repository.find_by_user_id(user_id)

        assert doctor is not None
        assert isinstance(doctor, DoctorEntity)
        assert doctor.user_id == user_id
        session_mock.exec.assert_called_once()

    def test_should_return_none_when_doctor_not_found_by_user_id(
        self, repository, session_mock
    ):
        """Should return None when doctor is not found by user_id."""
        user_id = uuid4()
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        doctor = repository.find_by_user_id(user_id)

        assert doctor is None

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

    # ========== FIND BY LICENSE NUMBER TESTS ==========

    def test_should_find_doctor_by_license_number_successfully(
        self, repository, session_mock, doctor_model
    ):
        """Should find doctor by license_number successfully."""
        license_number = doctor_model.license_number
        result_mock = MagicMock()
        result_mock.first.return_value = doctor_model
        session_mock.exec.return_value = result_mock

        doctor = repository.find_by_license_number(license_number)

        assert doctor is not None
        assert isinstance(doctor, DoctorEntity)
        assert doctor.license_number == license_number

    def test_should_return_none_when_doctor_not_found_by_license_number(
        self, repository, session_mock
    ):
        """Should return None when doctor is not found by license_number."""
        license_number = "NONEXISTENT"
        result_mock = MagicMock()
        result_mock.first.return_value = None
        session_mock.exec.return_value = result_mock

        doctor = repository.find_by_license_number(license_number)

        assert doctor is None

    def test_should_raise_database_connection_exception_on_operational_error_find_by_license_number(
        self, repository, session_mock, logger_mock
    ):
        """Should raise DatabaseConnectionException on OperationalError when finding by license_number."""
        license_number = "MED123456"
        session_mock.exec.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.find_by_license_number(license_number)

        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_find_by_license_number(
        self, repository, session_mock, logger_mock
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when finding by license_number."""
        license_number = "MED123456"
        session_mock.exec.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.find_by_license_number(license_number)

        logger_mock.error.assert_called_once()

    # ========== SAVE TESTS ==========

    def test_should_save_doctor_successfully(
        self, repository, session_mock, doctor_entity
    ):
        """Should save doctor successfully."""
        repository.save(doctor_entity)

        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()

    def test_should_raise_database_connection_exception_on_operational_error_save(
        self, repository, session_mock, logger_mock, doctor_entity
    ):
        """Should raise DatabaseConnectionException on OperationalError when saving."""
        session_mock.add.side_effect = OperationalError("conn error", None, None)

        with pytest.raises(DatabaseConnectionException):
            repository.save(doctor_entity)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    def test_should_raise_unexpected_database_exception_on_sqlalchemy_error_save(
        self, repository, session_mock, logger_mock, doctor_entity
    ):
        """Should raise UnexpectedDatabaseException on SQLAlchemyError when saving."""
        session_mock.commit.side_effect = SQLAlchemyError("db error")

        with pytest.raises(UnexpectedDatabaseException):
            repository.save(doctor_entity)

        session_mock.rollback.assert_called_once()
        logger_mock.error.assert_called_once()

    # ========== INTEGRATION TESTS ==========

    def test_should_handle_doctor_with_null_optional_fields(
        self, repository, session_mock
    ):
        """Should handle doctor with null optional fields."""
        doctor_model = DoctorModel(
            id=uuid4(),
            user_id=uuid4(),
            specialty_id=None,
            license_number="MED123456",
            experience_years=0,
            qualifications=None,
            bio=None,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        result_mock = MagicMock()
        result_mock.first.return_value = doctor_model
        session_mock.exec.return_value = result_mock

        doctor = repository.find_by_user_id(doctor_model.user_id)

        assert doctor is not None
        assert doctor.specialty_id is None
        assert doctor.qualifications is None
        assert doctor.bio is None
        assert doctor.experience_years == 0

    def test_should_save_doctor_with_all_fields(self, repository, session_mock):
        """Should save doctor with all fields populated."""
        doctor_entity = DoctorEntity(
            id=uuid4(),
            user_id=uuid4(),
            specialty_id=uuid4(),
            license_number="FULL123",
            experience_years=15,
            qualifications="MD, PhD, FAP",
            bio="Highly experienced specialist in cardiology",
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        repository.save(doctor_entity)

        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()
        # Verify the model created has all fields
        call_args = session_mock.add.call_args[0][0]
        assert call_args.license_number == "FULL123"
        assert call_args.experience_years == 15
        assert call_args.qualifications == "MD, PhD, FAP"
