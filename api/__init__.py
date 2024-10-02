"""
This module initializes and exposes the Flask API for processing essays
and queries.

It includes:
- The `EssayAnswersAPI` class that defines the API endpoints and their 
behaviors.
- An instance of the Flask application created from `EssayAnswersAPI`, 
exposed as `api` for use with Gunicorn or other WSGI servers.

The primary endpoint is `/answers`, which accepts POST requests 
containing an essay and a list of queries, returning a JSON response 
with answers.

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

from .api import EssayAnswersAPI

# Expose the API instance for use with gunicorn
api = EssayAnswersAPI().get_instance()
