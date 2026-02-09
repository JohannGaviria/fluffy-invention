import pytest
from faker import Faker


@pytest.fixture
def faker():
    """Fixture that provides a Faker instance."""
    return Faker()
