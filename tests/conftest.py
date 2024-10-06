import pytest

from answer_service import Encoder

@pytest.fixture
def encoder() -> Encoder:
    """Fixture to initialize the Encoder object."""
    return Encoder()
