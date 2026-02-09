"""Unit tests for DoctorEntity."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.contexts.auth.domain.entities.entity import DoctorEntity
from src.shared.domain.exceptions.exception import MissingFieldException


class TestDoctorEntity:
    """Unit tests for DoctorEntity."""

    def test_should_create_doctor_entity_successfully(self):
        """Should create DoctorEntity successfully with valid data."""
        user_id = uuid4()
        specialty_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
            specialty_id=specialty_id,
            qualifications="Board Certified",
            bio="Experienced physician",
        )

        assert doctor.user_id == user_id
        assert doctor.license_number == "MED123456"
        assert doctor.experience_years == 5
        assert doctor.specialty_id == specialty_id
        assert doctor.qualifications == "Board Certified"
        assert doctor.bio == "Experienced physician"
        assert doctor.is_active is True
        assert doctor.id is not None
        assert isinstance(doctor.created_at, datetime)
        assert isinstance(doctor.updated_at, datetime)

    def test_should_create_doctor_with_minimal_data(self):
        """Should create DoctorEntity with only required fields."""
        user_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
        )

        assert doctor.user_id == user_id
        assert doctor.license_number == "MED123456"
        assert doctor.experience_years == 5
        assert doctor.specialty_id is None
        assert doctor.qualifications is None
        assert doctor.bio is None
        assert doctor.is_active is True

    def test_should_create_doctor_with_is_active_false(self):
        """Should create DoctorEntity with is_active set to False."""
        user_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
            is_active=False,
        )

        assert doctor.is_active is False

    def test_should_raise_missing_field_exception_for_none_user_id(self):
        """Should raise MissingFieldException for None user_id."""
        with pytest.raises(MissingFieldException) as exc_info:
            DoctorEntity.create(
                user_id=None,
                license_number="MED123456",
                experience_years=5,
            )
        assert exc_info.value.field == "user_id"

    def test_should_raise_missing_field_exception_for_empty_license_number(self):
        """Should raise MissingFieldException for empty license_number."""
        user_id = uuid4()

        with pytest.raises(MissingFieldException) as exc_info:
            DoctorEntity.create(
                user_id=user_id,
                license_number="",
                experience_years=5,
            )
        assert exc_info.value.field == "license_number"

    def test_should_raise_missing_field_exception_for_none_experience_years(self):
        """Should raise MissingFieldException for None experience_years."""
        user_id = uuid4()

        with pytest.raises(MissingFieldException) as exc_info:
            DoctorEntity.create(
                user_id=user_id,
                license_number="MED123456",
                experience_years=None,
            )
        assert exc_info.value.field == "experience_years"

    def test_should_have_utc_timestamps(self):
        """Should have UTC timezone-aware timestamps."""
        user_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
        )

        assert doctor.created_at.tzinfo == UTC
        assert doctor.updated_at.tzinfo == UTC

    def test_should_have_same_created_and_updated_timestamps(self):
        """Should have same created_at and updated_at on creation."""
        user_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
        )

        assert doctor.created_at == doctor.updated_at

    def test_should_generate_unique_ids(self):
        """Should generate unique IDs for different doctors."""
        user_id1 = uuid4()
        user_id2 = uuid4()

        doctor1 = DoctorEntity.create(
            user_id=user_id1,
            license_number="MED123456",
            experience_years=5,
        )

        doctor2 = DoctorEntity.create(
            user_id=user_id2,
            license_number="MED789012",
            experience_years=10,
        )

        assert doctor1.id != doctor2.id

    def test_should_accept_optional_specialty_id(self):
        """Should accept optional specialty_id."""
        user_id = uuid4()
        specialty_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
            specialty_id=specialty_id,
        )

        assert doctor.specialty_id == specialty_id

    def test_should_accept_optional_qualifications(self):
        """Should accept optional qualifications."""
        user_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
            qualifications="Board Certified in Internal Medicine",
        )

        assert doctor.qualifications == "Board Certified in Internal Medicine"

    def test_should_accept_optional_bio(self):
        """Should accept optional bio."""
        user_id = uuid4()

        doctor = DoctorEntity.create(
            user_id=user_id,
            license_number="MED123456",
            experience_years=5,
            bio="Passionate about patient care",
        )

        assert doctor.bio == "Passionate about patient care"
