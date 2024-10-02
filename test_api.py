"""
This module contains unit tests for the Flask API's /answers endpoint.

The tests validate the following behaviors:
1. The API returns the correct status codes for valid and invalid 
   requests.
2. The API returns the correct structure of JSON responses.
3. The API handles cases such as empty essays or queries correctly.
4. The number of answers returned matches the number of queries sent.

The tests use the pytest framework and test Flask's test client to 
simulate HTTP requests and validate responses.

Example usage:
    Run the tests using pytest:
    $ pipenv run pytest
"""

from typing import Dict, Any, Generator

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse # import for WSGI response typing

from api import api

@pytest.fixture
def test_client() -> Generator[FlaskClient, None, None]:
    """Set up a test client for Flask."""
    api.config['TESTING'] = True
    with api.test_client() as client:
        yield client

def test_response_code(test_client: FlaskClient) -> None:
    """
    Test that the /answers endpoint returns a 200 OK status 
    when provided with a valid essay and queries.
    """

    test_data: Dict[str, Any] = {
        "essay": "This is an essay. This is the second sentence",
        "queries": ["What is courage?", "What is bravery?"]
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    assert response.status_code == 200

def test_answers_key_in_response_body(test_client: FlaskClient) -> None:
    """
    Test that the response from the /answers endpoint contains 
    the 'answers' key in the JSON response body when provided 
    with a valid essay and queries.
    """

    test_data: Dict[str, Any] = {
        "essay": "This is an essay. This is the second sentence",
        "queries": ["What is courage?", "What is bravery?"]
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    data: Dict[str, Any] = response.get_json()

    assert "answers" in data

def test_number_answers_response_body(test_client: FlaskClient) -> None:
    """
    Test that the number of answers in the response matches 
    the number of queries sent to the /answers endpoint.
    """

    test_data: Dict[str, Any] = {
        "essay": "This is an essay. This is the second sentence",
        "queries": ["What is courage?", "What is bravery?"]
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    data: Dict[str, Any] = response.get_json()

    assert len(data["answers"]) == len(test_data["queries"])

def test_empty_queries_response_body(test_client: FlaskClient) -> None:
    """
    Test that the response from the /answers endpoint contains 
    an empty list of answers when no queries are provided.
    """

    test_data: Dict[str, Any] = {
        "essay": "This is an essay. This is the second sentence",
        "queries": []
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    data: Dict[str, Any] = response.get_json()

    assert data["answers"] == []

def test_empty_essay_response_code(test_client: FlaskClient) -> None:
    """
    Test that the /answers endpoint returns a 400 Bad Request status 
    when the essay is an empty string.
    """

    test_data: Dict[str, Any] = {
        "essay": "",
        "queries": ["What is courage?", "What is bravery?"]
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    assert response.status_code == 400

def test_empty_essay_response_body(test_client: FlaskClient) -> None:
    """
    Test that the response from the /answers endpoint contains 
    the correct error message when the essay is an empty string.
    """

    test_data: Dict[str, Any] = {
        "essay": "",
        "queries": ["What is courage?", "What is bravery?"]
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    data: Dict[str, Any] = response.get_json()

    assert data["error"] == "Essay cannot be empty."

def test_empty_essay_and_queries_response_body(test_client: FlaskClient) -> None:
    """
    Test that the response from the /answers endpoint contains 
    the correct error message when both the essay is empty and 
    the queries list is empty.
    """

    test_data: Dict[str, Any] = {
        "essay": "",
        "queries": []
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    data: Dict[str, Any] = response.get_json()

    assert data["error"] == "Essay cannot be empty."

def test_empty_essay_and_queries_response_code(test_client: FlaskClient) -> None:
    """
    Test that the /answers endpoint returns a 400 Bad Request status 
    when both the essay and the queries list are empty.
    """

    test_data: Dict[str, Any] = {
        "essay": "",
        "queries": []
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    assert response.status_code == 400

def test_whitespace_essay_response_body(test_client: FlaskClient) -> None:
    """
    Test that the response from the /answers endpoint contains 
    the correct error message when the essay is a whitespace.
    """

    test_data: Dict[str, Any] = {
        "essay": " ",
        "queries": ["What is courage?", "What is bravery?"]
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    data: Dict[str, Any] = response.get_json()

    assert data["error"] == "Essay cannot be empty."

def test_whitespace_essay_response_code(test_client: FlaskClient) -> None:
    """
    Test that the /answers endpoint returns a 400 Bad Request status 
    when the essay is a whitespace.
    """

    test_data: Dict[str, Any] = {
        "essay": "",
        "queries": ["What is courage?", "What is bravery?"]
    }

    response: TestResponse = test_client.post('/answers', json=test_data)

    assert response.status_code == 400
