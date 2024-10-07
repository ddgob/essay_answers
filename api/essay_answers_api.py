"""
This module defines a simple Flask API for processing essays and 
queries using an object-oriented approach.

It includes endpoints: 
    - (/answers)
    - (/answers_based_on_subtitles)
    - (/answers_span)

All of them accept a POST request containing an essay and a list of 
queries, then returns a JSON response with answers for each query.
"""

from typing import List, Dict, Any, Union
import logging
from logging import Logger

from flask import Flask, request, jsonify, Response, make_response

from answer_service import AnswerService, AnswerServiceSpan

format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=format)

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
        self.api.add_url_rule(
            '/answers_based_on_subtitles',
            view_func=self.get_answers_based_on_subtitle,
            methods=['POST']
        )
        self.api.add_url_rule(
            '/answers_span',
            view_func=self.get_answers_span,
            methods=['POST']
        )

        self.logger: Logger = logging.getLogger(__name__)
        self.logger.info("API initialized.")

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

        self.logger.info("Validating if essay is a string...")

        if not isinstance(essay, str):
            json: Response = jsonify({"error": "Essay must be a string."})
            self.logger.error("Essay is not a string.")
            return make_response(json, 400)

        self.logger.info("Essay is a string.")

        return None

    def validate_empty_essay(self, essay: str) -> Union[None, Response]:
        """
        Validates the essay content.
        Checks if the essay is non-empty string.
        """

        self.logger.info("Validating if essay is empty...")

        if not essay.strip():
            json: Response = jsonify({"error": "Essay cannot be empty."})
            self.logger.error("Essay is empty.")
            return make_response(json, 400)

        self.logger.info("Essay is not empty.")

        return None

    def validate_essay(self, essay: str) -> Union[None, Response]:
        """
        Validates the essay content.
        Checks if the essay is a non-empty string.
        """

        self.logger.info("Validating essay...")

        response = self.validate_string_essay(essay)
        if response:
            return response

        response = self.validate_empty_essay(essay)
        if response:
            return response

        self.logger.info("Essay is valid.")

        return None

    def validate_empty_queries(self, queries: List[str]) -> Union[None, Response]:
        """
        Validates the queries list.
        Ensures that the list is not empty.
        """

        self.logger.info("Validating if queries list is empty...")

        if not queries:
            json: Response = jsonify({"error": "Queries list cannot be empty."})
            self.logger.error("Queries list is empty.")
            return make_response(json, 400)

        self.logger.info("Queries list is not empty.")

        return None

    def validate_string_queries(self, queries: List[str]) -> Union[None, Response]:
        """
        Validates the queries list.
        Ensures that the list contains only strings.
        """

        self.logger.info("Validating if queries are strings...")

        if not all(isinstance(query, str) for query in queries):
            json: Response = jsonify({"error": "Queries must be a list of strings."})
            self.logger.error("Queries are not strings.")
            return make_response(json, 400)

        self.logger.info("Queries are strings.")

        return None

    def validate_queries(self, queries: List[str]) -> Union[None, Response]:
        """
        Validates the queries list.
        Ensures that the list is not empty and contains only strings.
        """

        self.logger.info("Validating queries...")

        response = self.validate_empty_queries(queries)
        if response:
            return response

        response = self.validate_string_queries(queries)
        if response:
            return response

        self.logger.info("Queries are valid.")

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

        self.logger.info("Processing POST request to /answers...")

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

        self.logger.info("Finished processing POST request to /answers sucessfully.")

        return jsonify({"answers": answers})

    def get_answers_based_on_subtitle(self) -> Response:
        """
        Handles POST requests to the /answers_based_on_subtitles 
        endpoint.

        This function processes a POST request that contains an essay 
        and a list of queries. It validates that the essay is not empty 
        or a string of whitespaces. If the essay is empty or contains 
        only whitespace, it returns a 400 Bad Request response with 
        an error message. Otherwise, it returns a JSON response with 
        a list of answers, where each answer corresponds to a query,
        using subtitles from the essay.

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

        self.logger.info("Processing POST request to /answers_based_on_subtitles...")

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
        answers: List[str] = answer_service.answer_questions_based_on_subtitle(
            essay,
            queries
        )

        log: str = ("Finished processing POST request to /answers_based_on_subtitles "
                    "sucessfully."
                    )
        self.logger.info(log)

        return jsonify({"answers": answers})

    def get_answers_span(self) -> Response:
        """
        Handles POST requests to the /answers_span endpoint.

        This function processes a POST request that contains an essay 
        and a list of queries. It validates that the essay is not empty 
        or a string of whitespaces. If the essay is empty or contains 
        only whitespace, it returns a 400 Bad Request response with 
        an error message. Otherwise, it returns a JSON response with 
        a list of answers, where each answer corresponds to a query,
        using subtitles from the essay.

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

        self.logger.info("Processing POST request to /answers_span...")

        data: Dict[str, Any] = request.get_json()
        essay: str = data.get('essay', '')
        queries: List[str] = data.get('queries', [])

        response = self.validate_essay(essay)
        if response:
            return response

        response = self.validate_queries(queries)
        if response:
            return response

        answer_service_span: AnswerServiceSpan = AnswerServiceSpan()
        answers: List[str] = answer_service_span.answer_questions_span(
            essay,
            queries
        )

        log: str = "Finished processing POST request to /answers_span sucessfully."
        self.logger.info(log)

        return jsonify({"answers": answers})
