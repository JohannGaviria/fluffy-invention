"""Unit tests for DoctorMapper."""

from datetime import UTC, datetime
from uuid import uuid4

from src.contexts.auth.domain.entities.entity import DoctorEntity
from src.contexts.auth.infrastructure.persistence.mappers.mapper import DoctorMapper
from src.contexts.auth.infrastructure.persistence.models.model import DoctorModel


class TestDoctorMapper:
    """Unit tests for DoctorMapper."""

    def test_should_map_model_to_entity_successfully(self):
        """Should map DoctorModel to DoctorEntity successfully."""
        now = datetime.now(UTC)
        doctor_id = uuid4()
        user_id = uuid4()
        specialty_id = uuid4()

        model = DoctorModel(
            id=doctor_id,
            user_id=user_id,
            specialty_id=specialty_id,
            license_number="MED123456",
            experience_years=5,
            qualifications="Board Certified",
            bio="Experienced physician",
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        entity = DoctorMapper.to_entity(model)

        assert isinstance(entity, DoctorEntity)
        assert entity.id == doctor_id
        assert entity.user_id == user_id
        assert entity.specialty_id == specialty_id
        assert entity.license_number == "MED123456"
        assert entity.experience_years == 5
        assert entity.qualifications == "Board Certified"
        assert entity.bio == "Experienced physician"
        assert entity.is_active is True
        assert entity.created_at == now
        assert entity.updated_at == now

    def test_should_map_entity_to_model_successfully(self):
        """Should map DoctorEntity to DoctorModel successfully."""
        now = datetime.now(UTC)
        doctor_id = uuid4()
        user_id = uuid4()
        specialty_id = uuid4()

        entity = DoctorEntity(
            id=doctor_id,
            user_id=user_id,
            specialty_id=specialty_id,
            license_number="MED123456",
            experience_years=5,
            qualifications="Board Certified",
            bio="Experienced physician",
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        model = DoctorMapper.to_model(entity)

        assert isinstance(model, DoctorModel)
        assert model.id == doctor_id
        assert model.user_id == user_id
        assert model.specialty_id == specialty_id
        assert model.license_number == "MED123456"
        assert model.experience_years == 5
        assert model.qualifications == "Board Certified"
        assert model.bio == "Experienced physician"
        assert model.is_active is True
        assert model.created_at == now
        assert model.updated_at == now

    def test_should_handle_none_optional_fields(self):
        """Should handle None values in optional fields correctly."""
        now = datetime.now(UTC)

        model = DoctorModel(
            id=uuid4(),
            user_id=uuid4(),
            specialty_id=None,
            license_number="MED123456",
            experience_years=5,
            qualifications=None,
            bio=None,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        entity = DoctorMapper.to_entity(model)

        assert entity.specialty_id is None
        assert entity.qualifications is None
        assert entity.bio is None

        back_to_model = DoctorMapper.to_model(entity)
        assert back_to_model.specialty_id is None
        assert back_to_model.qualifications is None
        assert back_to_model.bio is None

    def test_should_preserve_is_active_state(self):
        """Should preserve is_active state during mapping."""
        now = datetime.now(UTC)

        for is_active in [True, False]:
            model = DoctorModel(
                id=uuid4(),
                user_id=uuid4(),
                specialty_id=None,
                license_number="MED123456",
                experience_years=5,
                qualifications=None,
                bio=None,
                is_active=is_active,
                created_at=now,
                updated_at=now,
            )

            entity = DoctorMapper.to_entity(model)
            assert entity.is_active == is_active

    def test_should_handle_zero_experience_years(self):
        """Should handle zero experience years correctly."""
        now = datetime.now(UTC)

        model = DoctorModel(
            id=uuid4(),
            user_id=uuid4(),
            specialty_id=None,
            license_number="MED123456",
            experience_years=0,
            qualifications=None,
            bio=None,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        entity = DoctorMapper.to_entity(model)
        assert entity.experience_years == 0

        back_to_model = DoctorMapper.to_model(entity)
        assert back_to_model.experience_years == 0

    def test_should_roundtrip_mapping_preserve_data(self):
        """Should preserve all data through roundtrip mapping."""
        now = datetime.now(UTC)
        specialty_id = uuid4()

        original_model = DoctorModel(
            id=uuid4(),
            user_id=uuid4(),
            specialty_id=specialty_id,
            license_number="LIC789",
            experience_years=10,
            qualifications="MD, PhD",
            bio="Specialist",
            is_active=False,
            created_at=now,
            updated_at=now,
        )

        entity = DoctorMapper.to_entity(original_model)
        final_model = DoctorMapper.to_model(entity)

        assert final_model.id == original_model.id
        assert final_model.user_id == original_model.user_id
        assert final_model.specialty_id == original_model.specialty_id
        assert final_model.license_number == original_model.license_number
        assert final_model.experience_years == original_model.experience_years
        assert final_model.qualifications == original_model.qualifications
        assert final_model.bio == original_model.bio
        assert final_model.is_active == original_model.is_active
