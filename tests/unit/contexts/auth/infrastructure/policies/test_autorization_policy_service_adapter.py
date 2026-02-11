"""Unit tests for AuthorizationPolicyServiceAdapter."""

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.infrastructure.policies.authorization_policy_service_adapter import (
    AuthorizationPolicyServiceAdapter,
)


class TestAuthorizationPolicyServiceAdapter:
    """Unit tests for AuthorizationPolicyServiceAdapter."""

    def test_should_allow_admin_to_register(self):
        """Should allow ADMIN role to register users."""
        adapter = AuthorizationPolicyServiceAdapter()

        result = adapter.can_register(RolesEnum.ADMIN)

        assert result is True

    def test_should_not_allow_patient_to_register(self):
        """Should not allow PATIENT role to register users."""
        adapter = AuthorizationPolicyServiceAdapter()

        result = adapter.can_register(RolesEnum.PATIENT)

        assert result is False

    def test_should_not_allow_doctor_to_register(self):
        """Should not allow DOCTOR role to register users."""
        adapter = AuthorizationPolicyServiceAdapter()

        result = adapter.can_register(RolesEnum.DOCTOR)

        assert result is False

    def test_should_not_allow_receptionist_to_register(self):
        """Should not allow RECEPTIONIST role to register users."""
        adapter = AuthorizationPolicyServiceAdapter()

        result = adapter.can_register(RolesEnum.RECEPTIONIST)

        assert result is False
