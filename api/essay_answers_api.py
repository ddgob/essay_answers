"""
This module defines a simple Flask API for processing essays and 
queries using an object-oriented approach.

It includes an endpoint (/answers) that accepts a POST request
containing an essay and a list of queries, then returns a JSON response
with answers for each query.
"""

from typing import List, Dict, Any, Union

from flask import Flask, request, jsonify, Response, make_response

from answer_service import AnswerService

class EssayAnswersAPI:
    """
    A class-based API for processing essays and queries.

    This class encapsulates a Flask application that provides an 
    endpoint (/answers) to process POST requests containing an essay and
    a list of queries. It handles request validation and returns JSON 
    responses with answers or error messages based on the input.
    """

    def __init__(self) -> None:
        self.api: Flask = Flask(__name__)
        self.api.add_url_rule('/answers', view_func=self.get_answers, methods=['POST'])

    def get_instance(self) -> Flask:
        """
        Returns the Flask app instance.
        """
        return self.api

    def validate_string_essay(self, essay: str) -> Union[None, Response]:
        """
        Validates the essay content.
        Checks if the essay is a string.
        """

        if not isinstance(essay, str):
            json: Response = jsonify({"error": "Essay must be a string."})
            return make_response(json, 400)

        return None

    def validate_empty_essay(self, essay: str) -> Union[None, Response]:
        """
        Validates the essay content.
        Checks if the essay is non-empty string.
        """

        if not essay.strip():
            json: Response = jsonify({"error": "Essay cannot be empty."})
            return make_response(json, 400)

        return None

    def validate_essay(self, essay: str) -> Union[None, Response]:
        """
        Validates the essay content.
        Checks if the essay is a non-empty string.
        """

        response = self.validate_string_essay(essay)
        if response:
            return response

        response = self.validate_empty_essay(essay)
        if response:
            return response

        return None

    def validate_empty_queries(self, queries: List[str]) -> Union[None, Response]:
        """
        Validates the queries list.
        Ensures that the list is not empty.
        """

        if not queries:
            json: Response = jsonify({"error": "Queries list cannot be empty."})
            return make_response(json, 400)

        return None

    def validate_string_queries(self, queries: List[str]) -> Union[None, Response]:
        """
        Validates the queries list.
        Ensures that the list contains only strings.
        """

        if not all(isinstance(query, str) for query in queries):
            json: Response = jsonify({"error": "Queries must be a list of strings."})
            return make_response(json, 400)

        return None

    def validate_queries(self, queries: List[str]) -> Union[None, Response]:
        """
        Validates the queries list.
        Ensures that the list is not empty and contains only strings.
        """
        response = self.validate_empty_queries(queries)
        if response:
            return response

        response = self.validate_string_queries(queries)
        if response:
            return response

        return None

    def get_answers(self) -> Response:
        """
        Handles POST requests to the /answers endpoint.

        This function processes a POST request that contains an essay 
        and a list of queries. It validates that the essay is not empty 
        or a string of whitespaces. If the essay is empty or contains 
        only whitespace, it returns a 400 Bad Request response with 
        an error message. Otherwise, it returns a JSON response with 
        a list of answers, where each answer corresponds to a query.

        Expected JSON input format:
        {
            "essay": "This is an example essay.",
            "queries": ["What is courage?", "What is bravery?"]
        }

        If the 'essay' field is empty or contains only whitespace:
        {
            "error": "Essay cannot be empty."
        }

        Returns:
            Response: A JSON object containing either a list of answers 
            or an error message. Example success response:
            {
                "answers": ["Answer number 1", "Answer number 2", ...]
            }
        """

        data: Dict[str, Any] = request.get_json()
        essay: str = data.get('essay', '')
        queries: List[str] = data.get('queries', [])

        response = self.validate_essay(essay)
        if response:
            return response

        response = self.validate_queries(queries)
        if response:
            return response

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions(essay, queries)

        return jsonify({"answers": answers})
