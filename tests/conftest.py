from typing import Generator

import pytest
from flask.testing import FlaskClient

from answer_service import Encoder
from api import essay_answers_api


@pytest.fixture
def encoder() -> Encoder:
    """Fixture to initialize the Encoder object."""
    return Encoder()

@pytest.fixture
def test_client() -> Generator[FlaskClient, None, None]:
    """Set up a test client for Flask."""
    essay_answers_api.config['TESTING'] = True
    with essay_answers_api.test_client() as client:
        yield client
