"""Unit tests for StaffEmailPolicyServiceAdapter."""

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.contexts.auth.infrastructure.policies.staff_email_policy_service_adapter import (
    StaffEmailPolicyServiceAdapter,
)


class TestStaffEmailPolicyServiceAdapter:
    """Unit tests for StaffEmailPolicyServiceAdapter."""

    def test_should_allow_corporate_email_for_admin(self):
        """Should allow corporate email for ADMIN role."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com,corp.com", allowed_roles="admin,receptionist"
        )
        email = EmailVO("user@company.com")

        result = adapter.is_allowed(email, RolesEnum.ADMIN)

        assert result is True

    def test_should_reject_non_corporate_email_for_admin(self):
        """Should reject non-corporate email for ADMIN role."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com,corp.com", allowed_roles="admin,receptionist"
        )
        email = EmailVO("user@personal.com")

        result = adapter.is_allowed(email, RolesEnum.ADMIN)

        assert result is False

    def test_should_allow_any_email_for_patient(self):
        """Should allow any email for PATIENT role (not in allowed_roles)."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com", allowed_roles="admin,receptionist"
        )
        email = EmailVO("patient@gmail.com")

        result = adapter.is_allowed(email, RolesEnum.PATIENT)

        assert result is True

    def test_should_allow_any_email_for_doctor(self):
        """Should allow any email for DOCTOR role (not in allowed_roles)."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com", allowed_roles="admin,receptionist"
        )
        email = EmailVO("doctor@yahoo.com")

        result = adapter.is_allowed(email, RolesEnum.DOCTOR)

        assert result is True

    def test_should_handle_multiple_allowed_domains(self):
        """Should handle multiple allowed domains correctly."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com,subsidiary.com,partner.org",
            allowed_roles="admin,receptionist",
        )

        valid_emails = [
            EmailVO("user@company.com"),
            EmailVO("admin@subsidiary.com"),
            EmailVO("staff@partner.org"),
        ]

        for email in valid_emails:
            result = adapter.is_allowed(email, RolesEnum.ADMIN)
            assert result is True

    def test_should_trim_whitespace_from_domains(self):
        """Should trim whitespace from domain configuration."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains=" company.com , corp.com ", allowed_roles="admin"
        )
        email = EmailVO("user@company.com")

        result = adapter.is_allowed(email, RolesEnum.ADMIN)

        assert result is True

    def test_should_trim_whitespace_from_roles(self):
        """Should trim whitespace from roles configuration."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com", allowed_roles=" admin , receptionist "
        )
        email = EmailVO("user@company.com")

        result = adapter.is_allowed(email, RolesEnum.ADMIN)

        assert result is True

    def test_should_be_case_sensitive_for_domains(self):
        """Should match domains exactly (case-sensitive from EmailVO)."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com", allowed_roles="admin"
        )
        # EmailVO converts domain to lowercase
        email = EmailVO("user@Company.Com")

        result = adapter.is_allowed(email, RolesEnum.ADMIN)

        assert result is True

    def test_should_reject_corporate_email_for_receptionist_with_wrong_domain(self):
        """Should reject corporate email with wrong domain for RECEPTIONIST."""
        adapter = StaffEmailPolicyServiceAdapter(
            allowed_domains="company.com", allowed_roles="admin,receptionist"
        )
        email = EmailVO("user@wrongdomain.com")

        result = adapter.is_allowed(email, RolesEnum.RECEPTIONIST)

        assert result is False
