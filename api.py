"""
This module defines a simple Flask API for processing essays and 
queries.

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

from flask import Flask, request, jsonify, Response

api = Flask(__name__)

@api.route('/answers', methods=['POST'])
def get_answers() -> Response:
    """
    Handles POST requests to the /answers endpoint.

    This function processes a POST request that contains an essay
    and a list of queries.
    It returns a JSON response with a list of answers, where each answer
    corresponds to a query.

    Expected JSON input format:
    {
        "essay": "This is an example essay.",
        "queries": ["What is courage?", "What is bravery?"]
    }

    The function performs the following steps:
    1. Retrieves the essay and queries from the JSON body of the request
    2. Processes the queries and generates a response for each query
    3. Returns the answers in a JSON response

    Returns:
        Response: A JSON object containing a list of answers, structured
        as:
        {
            "answers": ["Answer number 1", "Answer number 2", ...]
        }
    """

    data: Dict[str, Any] = request.get_json()
    essay: str = data.get('essay', '')
    queries: List[str] = data.get('queries', [])

    if not essay.strip():
        return jsonify({"error": "Essay cannot be empty."}), 400

    # TODO change the logic for processing essays and queries to
    # obtain answers
    answers: List[str] = [
        f'Answer number {answer_number + 1}' 
        for answer_number in range(len(queries))
    ]

    return jsonify({"answers": answers})

if __name__ == '__main__':
    api.run()
