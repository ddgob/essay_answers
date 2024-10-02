
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

    # TODO change the logic for processing essays and queries to
    # obtain answers
    answers: List[str] = [
        f'Answer number {answer_number + 1}' 
        for answer_number in range(len(queries))
    ]

    return jsonify({"answers": answers})

if __name__ == '__main__':
    api.run()
