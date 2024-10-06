"""
This module contains unit tests for the Flask API's /answers endpoint, 
implemented using an object-oriented approach.

The tests validate the following behaviors:
1. The API returns the correct status codes for valid and invalid 
   requests.
2. The API returns the correct structure of JSON responses.
3. The API handles cases such as empty essays or queries correctly.
4. The number of answers returned matches the number of queries sent.

The tests use the pytest framework and Flask's test client to simulate 
HTTP requests and validate responses.

The tests are now encapsulated in a test class to follow object-oriented 
design principles.

Example usage:
    Run the tests using pytest:
    $ pipenv run pytest
"""

from typing import Dict, Any, List

from flask.testing import FlaskClient
from werkzeug.test import TestResponse # import for WSGI response typing
import pytest

class TestEssayAnswersAPI:
    """
    Unit tests for the EssayAnswersAPI's /answers endpoint.

    This class tests various scenarios to validate the behavior of the 
    API's /answers endpoint. It checks the response status codes, JSON 
    response structure, and the correct handling of edge cases such as 
    empty essays or queries.
    """

    def test_response_code(self, test_client: FlaskClient) -> None:
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

    def test_answers_key_in_response_body(self, test_client: FlaskClient) -> None:
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

    def test_number_answers_response_body(self, test_client: FlaskClient) -> None:
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

    def test_empty_queries_response_code(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns a 400 Bad Request status 
        when no queries are provided.
        """

        test_data: Dict[str, Any] = {
            "essay": "This is an essay. This is the second sentence",
            "queries": []
        }

        response: TestResponse = test_client.post('/answers', json=test_data)

        assert response.status_code == 400

    def test_empty_essay_response_code(self, test_client: FlaskClient) -> None:
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

    def test_empty_essay_response_body(self, test_client: FlaskClient) -> None:
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

    def test_empty_essay_and_queries_response_body(self,
                                                   test_client: FlaskClient) -> None:
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

    def test_empty_essay_and_queries_response_code(self,
                                                   test_client: FlaskClient) -> None:
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

    def test_whitespace_essay_response_body(self, test_client: FlaskClient) -> None:
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

    def test_whitespace_essay_response_code(self, test_client: FlaskClient) -> None:
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

    def test_validate_string_essay_invalid(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns a 400 Bad Request status 
        when the essay is not a string.
        """

        test_data: Dict[str, Any] = {
            "essay": 12345,
            "queries": ["What is courage?"]
        }

        response: TestResponse = test_client.post('/answers', json=test_data)

        assert response.status_code == 400

    def test_validate_string_essay_error_message(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns the correct error 
        message when the essay is not a string.
        """

        test_data: Dict[str, Any] = {
            "essay": 12345,
            "queries": ["What is courage?"]
        }

        response: TestResponse = test_client.post('/answers', json=test_data)
        data: Dict[str, Any] = response.get_json()

        assert data["error"] == "Essay must be a string."

    def test_validate_empty_essay_invalid(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns a 400 Bad Request status 
        when the essay is an empty string.
        """

        test_data: Dict[str, Any] = {
            "essay": "",
            "queries": ["What is courage?"]
        }

        response: TestResponse = test_client.post('/answers', json=test_data)

        assert response.status_code == 400

    def test_validate_empty_essay_error_message(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns the correct error 
        message when the essay is an empty string.
        """

        test_data: Dict[str, Any] = {
            "essay": "",
            "queries": ["What is courage?"]
        }

        response: TestResponse = test_client.post('/answers', json=test_data)
        data: Dict[str, Any] = response.get_json()

        assert data["error"] == "Essay cannot be empty."

    def test_validate_empty_queries_invalid(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns a 400 Bad Request status 
        when the queries list is empty.
        """

        test_data: Dict[str, Any] = {
            "essay": "This is an essay.",  
            "queries": []
        }

        response: TestResponse = test_client.post('/answers', json=test_data)

        assert response.status_code == 400

    def test_validate_empty_queries_error_message(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns the correct error 
        message when the queries list is empty.
        """

        test_data: Dict[str, Any] = {
            "essay": "This is an essay.",  
            "queries": []
        }

        response: TestResponse = test_client.post('/answers', json=test_data)
        data: Dict[str, Any] = response.get_json()

        assert data["error"] == "Queries list cannot be empty."

    def test_validate_string_queries_invalid(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns a 400 Bad Request status 
        when the queries list contains non-string values.
        """

        test_data: Dict[str, Any] = {
            "essay": "This is an essay.",  
            "queries": [123, True]
        }

        response: TestResponse = test_client.post('/answers', json=test_data)

        assert response.status_code == 400

    def test_validate_string_queries_error_message(self,
                                                   test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns the correct error 
        message when the queries list contains non-string values.
        """

        test_data: Dict[str, Any] = {
            "essay": "This is an essay.",  
            "queries": [123, True]
        }

        response: TestResponse = test_client.post('/answers', json=test_data)
        data: Dict[str, Any] = response.get_json()

        assert data["error"] == "Queries must be a list of strings."

    def test_full_essay_response_code(self, test_client: FlaskClient) -> None:
        """
        Test that the /answers endpoint returns a 200 OK status 
        when provided with a full essay and queries.
        """

        with open('./tests/docs/full_essay.txt', 'r', encoding='utf-8') as file:
            full_essay: str = file.read()

        full_essay_query_1: str = "What is courage?"
        full_essay_query_2: str = "What is bravery?"
        full_essay_query_3: str = ("An example of a character in the literature who"
                              " displays courage"
                              )
        full_essay_query_4: str = ("An example of a character in the literature who"
                              " exhibits bravery"
                              )
        full_essay_query_5: str = "What risks a courageous act entails?"
        full_essay_query_6: str = "What risks a brave act entails?"

        full_essay_queries: List[str] = [
            full_essay_query_1,
            full_essay_query_2,
            full_essay_query_3,
            full_essay_query_4,
            full_essay_query_5,
            full_essay_query_6
        ]

        test_data: Dict[str, Any] = {
            "essay": full_essay,
            "queries": full_essay_queries
        }

        response: TestResponse = test_client.post('/answers', json=test_data)

        assert response.status_code == 200

    def test_full_essay_response_body(self, test_client: FlaskClient) -> None:
        """
        Test that the response from the /answers endpoint contains 
        the 'answers' key in the JSON response body when provided 
        with a full essay and queries.
        """

        with open('./tests/docs/full_essay.txt', 'r', encoding='utf-8') as file:
            full_essay: str = file.read()

        full_essay_query_1: str = "What is courage?"
        full_essay_query_2: str = "What is bravery?"
        full_essay_query_3: str = ("An example of a character in the literature who"
                              " displays courage"
                              )
        full_essay_query_4: str = ("An example of a character in the literature who"
                              " exhibits bravery"
                              )
        full_essay_query_5: str = "What risks a courageous act entails?"
        full_essay_query_6: str = "What risks a brave act entails?"

        full_essay_queries: List[str] = [
            full_essay_query_1,
            full_essay_query_2,
            full_essay_query_3,
            full_essay_query_4,
            full_essay_query_5,
            full_essay_query_6
        ]

        test_data: Dict[str, Any] = {
            "essay": full_essay,
            "queries": full_essay_queries
        }

        response: TestResponse = test_client.post('/answers', json=test_data)
        data: Dict[str, Any] = response.get_json()

        path_to_expected_answers: str = './tests/docs/expected_answers_full_essay.txt'
        with open(path_to_expected_answers, 'r', encoding='utf-8') as file:
            expected_answers: List[str] = file.read().splitlines()

        assert all(answer in data['answers'] for answer in expected_answers)

    def test_get_answers_based_on_subtitle_success(
        self,
        test_client: FlaskClient
    ) -> None:
        """
        Test /answers_based_on_subtitles endpoint for a successful 
        response.
        
        Asserts:
            A valid list of answers is returned based on subtitles.
        """

        essay: str = (
            "Title\nThis is the content under the title. And its a paragraph.\n"
            "Subtitle\nThis is the content under the subtitle. And its a paragraph.\n"
        )

        test_data: Dict[str, Any] = {
            "essay": essay,
            "queries": ["What is under the title?"]
        }

        response: TestResponse = test_client.post(
            '/answers_based_on_subtitles',
            json=test_data
        )

        data: Dict[str, Any] = response.get_json()
        assert data['answers'] == ["This is the content under the title"]

    def test_get_answers_based_on_subtitle_subtitles_only(
        self,
        test_client: FlaskClient
    ) -> None:
        """
        Test /answers_based_on_subtitles endpoint when an essay with 
        only subtitles is provided.

        Asserts:
            An empty list with no answers is returned.
        """

        test_data: Dict[str, Any] = {
            "essay": "Title\nThis is another subtitle.",
            "queries": ["What is under the title?"]
        }

        response: TestResponse = test_client.post(
            '/answers_based_on_subtitles',
            json=test_data
        )

        data: Dict[str, Any] = response.get_json()
        assert data['answers'] == []

    def test_get_answers_based_on_subtitle_empty_essay(
        self,
        test_client: FlaskClient
    ) -> None:
        """
        Test /answers_based_on_subtitles endpoint with empty essay.
        
        Asserts:
            Error message is returned for an empty essay.
        """

        test_data: Dict[str, Any] = {
            "essay": "",
            "queries": ["What is under the title?"]
        }

        response: TestResponse = test_client.post(
            '/answers_based_on_subtitles',
            json=test_data
        )

        data: Dict[str, Any] = response.get_json()
        assert data['error'] == 'Essay cannot be empty.'

    def test_get_answers_based_on_subtitle_empty_queries(
        self,
        test_client: FlaskClient
    ) -> None:
        """
        Test /answers_based_on_subtitles endpoint with empty queries.
        
        Asserts:
            Error message is returned for empty queries.
        """

        test_data: Dict[str, Any] = {
            "essay": "Title\nThis is the content under the title.",
            "queries": []
        }

        response: TestResponse = test_client.post(
            '/answers_based_on_subtitles',
            json=test_data
        )

        data: Dict[str, Any] = response.get_json()
        assert data['error'] == "Queries list cannot be empty."

    def test_get_answers_based_on_subtitle_non_string_queries(
        self,
        test_client: FlaskClient
    ) -> None:
        """
        Test /answers_based_on_subtitles with non-string queries.
        
        Asserts:
            Error message is returned for non-string queries.
        """

        test_data: Dict[str, Any] = {
            "essay": "Title\nThis is the content under the title.",
            "queries": [123, 456]
        }

        response: TestResponse = test_client.post(
            '/answers_based_on_subtitles',
            json=test_data
        )

        data: Dict[str, Any] = response.get_json()
        assert data['error'] == "Queries must be a list of strings."

    def test_answers_based_on_subtitle_full_essay_response_code(
        self,
        test_client: FlaskClient
    ) -> None:
        """
        Test that the /answers_based_on_subtitles endpoint returns a 
        200 OK status when provided with a full essay and queries.
        """

        with open('./tests/docs/full_essay.txt', 'r', encoding='utf-8') as file:
            full_essay: str = file.read()

        full_essay_query_1: str = "What is courage?"
        full_essay_query_2: str = "What is bravery?"
        full_essay_query_3: str = ("An example of a character in the literature who"
                              " displays courage"
                              )
        full_essay_query_4: str = ("An example of a character in the literature who"
                              " exhibits bravery"
                              )
        full_essay_query_5: str = "What risks a courageous act entails?"
        full_essay_query_6: str = "What risks a brave act entails?"

        full_essay_queries: List[str] = [
            full_essay_query_1,
            full_essay_query_2,
            full_essay_query_3,
            full_essay_query_4,
            full_essay_query_5,
            full_essay_query_6
        ]

        test_data: Dict[str, Any] = {
            "essay": full_essay,
            "queries": full_essay_queries
        }

        response: TestResponse = test_client.post(
            '/answers_based_on_subtitles',
            json=test_data
        )

        assert response.status_code == 200

    def test_answers_based_on_subtitle_full_essay_response_body(
        self,
        test_client: FlaskClient
    ) -> None:
        """
        Test that the response from the /answers_based_on_subtitles 
        endpoint contains the 'answers' key in the JSON response body 
        when provided with a full essay and queries.
        """

        with open('./tests/docs/full_essay.txt', 'r', encoding='utf-8') as file:
            full_essay: str = file.read()

        full_essay_query_1: str = "What is courage?"
        full_essay_query_2: str = "What is bravery?"
        full_essay_query_3: str = ("An example of a character in the literature who"
                              " displays courage"
                              )
        full_essay_query_4: str = ("An example of a character in the literature who"
                              " exhibits bravery"
                              )
        full_essay_query_5: str = "What risks a courageous act entails?"
        full_essay_query_6: str = "What risks a brave act entails?"

        full_essay_queries: List[str] = [
            full_essay_query_1,
            full_essay_query_2,
            full_essay_query_3,
            full_essay_query_4,
            full_essay_query_5,
            full_essay_query_6
        ]

        test_data: Dict[str, Any] = {
            "essay": full_essay,
            "queries": full_essay_queries
        }

        response: TestResponse = test_client.post(
            '/answers_based_on_subtitles',
            json=test_data
        )
        data: Dict[str, Any] = response.get_json()

        path_to_expected_answers: str = (
            './tests/docs/expected_answers_full_essay_based_on_subtitles.txt'
        )
        with open(path_to_expected_answers, 'r', encoding='utf-8') as file:
            expected_answers: List[str] = file.read().splitlines()

        for answer in data['answers']:
            print(answer)
            print("##################################################################")

        assert all(answer in data['answers'] for answer in expected_answers)

if __name__ == '__main__':
    pytest.main()
    """tester = TestEssayAnswersAPI()
    from tests import test_client
    tester.test_get_answers_based_on_subtitle_success(test_client)"""
