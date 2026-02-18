"""Unit tests for PatientMapper."""

from datetime import UTC, date, datetime
from uuid import uuid4

from src.contexts.auth.domain.entities.entity import PatientEntity
from src.contexts.auth.infrastructure.persistence.mappers.mapper import PatientMapper
from src.contexts.auth.infrastructure.persistence.models.model import PatientModel


class TestPatientMapper:
    """Unit tests for PatientMapper."""

    def test_should_map_model_to_entity_successfully(self):
        """Should map PatientModel to PatientEntity successfully."""
        now = datetime.now(UTC)
        patient_id = uuid4()
        user_id = uuid4()
        birth_date = date(1990, 1, 1)

        model = PatientModel(
            id=patient_id,
            user_id=user_id,
            document="123456789",
            phone="+1234567890",
            birth_date=birth_date,
            created_at=now,
            updated_at=now,
        )

        entity = PatientMapper.to_entity(model)

        assert isinstance(entity, PatientEntity)
        assert entity.id == patient_id
        assert entity.user_id == user_id
        assert entity.document == "123456789"
        assert entity.phone == "+1234567890"
        assert entity.birth_date == birth_date
        assert entity.created_at == now
        assert entity.updated_at == now

    def test_should_map_entity_to_model_successfully(self):
        """Should map PatientEntity to PatientModel successfully."""
        now = datetime.now(UTC)
        patient_id = uuid4()
        user_id = uuid4()
        birth_date = date(1990, 1, 1)

        entity = PatientEntity(
            id=patient_id,
            user_id=user_id,
            document="123456789",
            phone="+1234567890",
            birth_date=birth_date,
            created_at=now,
            updated_at=now,
        )

        model = PatientMapper.to_model(entity)

        assert isinstance(model, PatientModel)
        assert model.id == patient_id
        assert model.user_id == user_id
        assert model.document == "123456789"
        assert model.phone == "+1234567890"
        assert model.birth_date == birth_date
        assert model.created_at == now
        assert model.updated_at == now

    def test_should_handle_different_birth_dates(self):
        """Should handle different birth dates correctly."""
        now = datetime.now(UTC)
        birth_dates = [
            date(1990, 1, 1),
            date(2000, 12, 31),
            date(1985, 6, 15),
        ]

        for birth_date in birth_dates:
            model = PatientModel(
                id=uuid4(),
                user_id=uuid4(),
                document="123456789",
                phone="+1234567890",
                birth_date=birth_date,
                created_at=now,
                updated_at=now,
            )

            entity = PatientMapper.to_entity(model)
            assert entity.birth_date == birth_date

            back_to_model = PatientMapper.to_model(entity)
            assert back_to_model.birth_date == birth_date

    def test_should_roundtrip_mapping_preserve_data(self):
        """Should preserve all data through roundtrip mapping."""
        now = datetime.now(UTC)
        original_model = PatientModel(
            id=uuid4(),
            user_id=uuid4(),
            document="987654321",
            phone="+9876543210",
            birth_date=date(1995, 5, 5),
            created_at=now,
            updated_at=now,
        )

        entity = PatientMapper.to_entity(original_model)
        final_model = PatientMapper.to_model(entity)

        assert final_model.id == original_model.id
        assert final_model.user_id == original_model.user_id
        assert final_model.document == original_model.document
        assert final_model.phone == original_model.phone
        assert final_model.birth_date == original_model.birth_date
