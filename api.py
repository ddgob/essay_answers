from flask import Flask, request, jsonify, Response
from typing import List, Dict, Any

api = Flask(__name__)

@api.route('/answers', methods=['POST'])
def get_answers() -> Response:
    
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
