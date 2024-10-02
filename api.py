"""
This module defines a simple Flask API for processing essays and 
queries using an object-oriented approach.

It includes an endpoint (/answers) that accepts a POST request
containing an essay and a list of queries, then returns a JSON response
with answers for each query.

Example usage:
    Start the Flask server:
        $ gunicorn api:api

    Send a POST request to /answers:
        $ curl -X POST http://127.0.0.1:8000/answers \
            -H "Content-Type: application/json" \
            -d '{
                    "essay": "This is an essay.", 
                    "queries": ["What is courage?"]
                }'
"""

from typing import List, Dict, Any

from flask import Flask, request, jsonify, Response, make_response

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
        self.api.add_url_rule('/answers', view_func=self.get_answers,
                              methods=['POST']
                              )

    def get_instance(self) -> Flask:
        """
        Returns the Flask app instance.
        """
        return self.api

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

        if not essay.strip():
            error_message = "Essay cannot be empty."
            json: Response = jsonify({"error": error_message})
            return make_response(json, 400)

        answers: List[str] = [
            f'Answer number {answer_number + 1}' 
            for answer_number in range(len(queries))
        ]

        return jsonify({"answers": answers})


api: Flask = EssayAnswersAPI().get_instance()
