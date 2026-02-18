"""Unit tests for PatientEntity."""

from datetime import UTC, date, datetime
from uuid import uuid4

import pytest

from src.contexts.auth.domain.entities.entity import PatientEntity
from src.shared.domain.exceptions.exception import MissingFieldException


class TestPatientEntity:
    """Unit tests for PatientEntity."""

    def test_should_create_patient_entity_successfully(self):
        """Should create PatientEntity successfully with valid data."""
        user_id = uuid4()
        birth_date = date(1990, 1, 1)

        patient = PatientEntity.create(
            user_id=user_id,
            document="123456789",
            phone="+1234567890",
            birth_date=birth_date,
        )

        assert patient.user_id == user_id
        assert patient.document == "123456789"
        assert patient.phone == "+1234567890"
        assert patient.birth_date == birth_date
        assert patient.id is not None
        assert isinstance(patient.created_at, datetime)
        assert isinstance(patient.updated_at, datetime)

    def test_should_raise_missing_field_exception_for_none_user_id(self):
        """Should raise MissingFieldException for None user_id."""
        birth_date = date(1990, 1, 1)

        with pytest.raises(MissingFieldException) as exc_info:
            PatientEntity.create(
                user_id=None,
                document="123456789",
                phone="+1234567890",
                birth_date=birth_date,
            )
        assert exc_info.value.field == "user_id"

    def test_should_raise_missing_field_exception_for_empty_document(self):
        """Should raise MissingFieldException for empty document."""
        user_id = uuid4()
        birth_date = date(1990, 1, 1)

        with pytest.raises(MissingFieldException) as exc_info:
            PatientEntity.create(
                user_id=user_id,
                document="",
                phone="+1234567890",
                birth_date=birth_date,
            )
        assert exc_info.value.field == "document"

    def test_should_raise_missing_field_exception_for_empty_phone(self):
        """Should raise MissingFieldException for empty phone."""
        user_id = uuid4()
        birth_date = date(1990, 1, 1)

        with pytest.raises(MissingFieldException) as exc_info:
            PatientEntity.create(
                user_id=user_id,
                document="123456789",
                phone="",
                birth_date=birth_date,
            )
        assert exc_info.value.field == "phone"

    def test_should_raise_missing_field_exception_for_none_birth_date(self):
        """Should raise MissingFieldException for None birth_date."""
        user_id = uuid4()

        with pytest.raises(MissingFieldException) as exc_info:
            PatientEntity.create(
                user_id=user_id,
                document="123456789",
                phone="+1234567890",
                birth_date=None,
            )
        assert exc_info.value.field == "birth_date"

    def test_should_have_utc_timestamps(self):
        """Should have UTC timezone-aware timestamps."""
        user_id = uuid4()
        birth_date = date(1990, 1, 1)

        patient = PatientEntity.create(
            user_id=user_id,
            document="123456789",
            phone="+1234567890",
            birth_date=birth_date,
        )

        assert patient.created_at.tzinfo == UTC
        assert patient.updated_at.tzinfo == UTC

    def test_should_have_same_created_and_updated_timestamps(self):
        """Should have same created_at and updated_at on creation."""
        user_id = uuid4()
        birth_date = date(1990, 1, 1)

        patient = PatientEntity.create(
            user_id=user_id,
            document="123456789",
            phone="+1234567890",
            birth_date=birth_date,
        )

        assert patient.created_at == patient.updated_at

    def test_should_generate_unique_ids(self):
        """Should generate unique IDs for different patients."""
        user_id1 = uuid4()
        user_id2 = uuid4()
        birth_date = date(1990, 1, 1)

        patient1 = PatientEntity.create(
            user_id=user_id1,
            document="123456789",
            phone="+1234567890",
            birth_date=birth_date,
        )

        patient2 = PatientEntity.create(
            user_id=user_id2,
            document="987654321",
            phone="+0987654321",
            birth_date=birth_date,
        )

        assert patient1.id != patient2.id

    def test_should_accept_different_birth_dates(self):
        """Should accept different birth dates."""
        user_id = uuid4()

        dates = [
            date(1990, 1, 1),
            date(2000, 12, 31),
            date(1985, 6, 15),
        ]

        for birth_date in dates:
            patient = PatientEntity.create(
                user_id=user_id,
                document="123456789",
                phone="+1234567890",
                birth_date=birth_date,
            )
            assert patient.birth_date == birth_date
