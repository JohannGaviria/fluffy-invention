"""Unit tests for PyJWTTokenServiceAdapter."""

from datetime import UTC, datetime
from uuid import uuid4

import jwt
import pytest

from src.contexts.auth.domain.entities.entity import RolesEnum
from src.contexts.auth.domain.value_objects.access_token_vo import AccessTokenVO
from src.contexts.auth.domain.value_objects.token_payload_vo import TokenPayloadVO
from src.contexts.auth.infrastructure.security.token_service_adapter import (
    PyJWTTokenServiceAdapter,
)


class TestPyJWTTokenServiceAdapter:
    """Unit tests for PyJWTTokenServiceAdapter."""

    def test_should_generate_access_token_successfully(self):
        """Should generate access token successfully."""
        adapter = PyJWTTokenServiceAdapter(
            expires_in=60, secret_key="test_secret_key", algorithm="HS256"
        )
        user_id = uuid4()
        payload = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.PATIENT, expires_in=3600
        )

        token = adapter.access(payload)

        assert isinstance(token, AccessTokenVO)
        assert token.token_type == "Bearer"
        assert token.expires_in == 60
        assert token.access_token is not None
        assert len(token.access_token) > 0

    def test_should_decode_token_successfully(self):
        """Should decode token successfully."""
        adapter = PyJWTTokenServiceAdapter(
            expires_in=60, secret_key="test_secret_key", algorithm="HS256"
        )
        user_id = uuid4()
        payload = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.ADMIN, expires_in=3600
        )

        token = adapter.access(payload)
        decoded = adapter.decode(token.access_token)

        assert decoded.user_id == str(user_id)
        assert decoded.role == RolesEnum.ADMIN.value
        assert decoded.expires_in == 3600

    def test_should_set_correct_expiration_time(self):
        """Should set correct expiration time."""
        adapter = PyJWTTokenServiceAdapter(
            expires_in=30, secret_key="test_secret_key", algorithm="HS256"
        )
        user_id = uuid4()
        payload = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.DOCTOR, expires_in=1800
        )

        before = datetime.now(UTC)
        token = adapter.access(payload)
        after = datetime.now(UTC)

        # expires_at should be approximately 30 minutes from now
        assert token.expires_at > before
        assert token.expires_at > after

    def test_should_generate_valid_jwt_token(self):
        """Should generate a valid JWT token."""
        adapter = PyJWTTokenServiceAdapter(
            expires_in=60, secret_key="test_secret_key", algorithm="HS256"
        )
        user_id = uuid4()
        payload = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.RECEPTIONIST, expires_in=3600
        )

        token = adapter.access(payload)

        # Verify it's a valid JWT token by decoding it
        decoded = jwt.decode(
            token.access_token, "test_secret_key", algorithms=["HS256"]
        )
        assert decoded["sub"] == str(user_id)
        assert decoded["role"] == RolesEnum.RECEPTIONIST.value

    def test_should_fail_decode_with_wrong_secret(self):
        """Should fail to decode token with wrong secret key."""
        adapter = PyJWTTokenServiceAdapter(
            expires_in=60, secret_key="correct_secret", algorithm="HS256"
        )
        user_id = uuid4()
        payload = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.PATIENT, expires_in=3600
        )

        token = adapter.access(payload)

        wrong_adapter = PyJWTTokenServiceAdapter(
            expires_in=60, secret_key="wrong_secret", algorithm="HS256"
        )

        with pytest.raises(jwt.InvalidSignatureError):
            wrong_adapter.decode(token.access_token)

    def test_should_include_jti_in_token(self):
        """Should include jti (token ID) in the token."""
        adapter = PyJWTTokenServiceAdapter(
            expires_in=60, secret_key="test_secret_key", algorithm="HS256"
        )
        user_id = uuid4()
        payload = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.ADMIN, expires_in=3600
        )

        token = adapter.access(payload)
        decoded = adapter.decode(token.access_token)

        assert decoded.jti is not None

    def test_should_generate_different_tokens_for_same_payload(self):
        """Should generate different tokens for same payload (different jti)."""
        adapter = PyJWTTokenServiceAdapter(
            expires_in=60, secret_key="test_secret_key", algorithm="HS256"
        )
        user_id = uuid4()

        payload1 = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.PATIENT, expires_in=3600
        )
        payload2 = TokenPayloadVO.generate(
            user_id=user_id, role=RolesEnum.PATIENT, expires_in=3600
        )

        token1 = adapter.access(payload1)
        token2 = adapter.access(payload2)

        # Different tokens due to different jti
        assert token1.access_token != token2.access_token
