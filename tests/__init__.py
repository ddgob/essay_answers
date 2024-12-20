"""
This module provides shared fixtures for unit testing the Flask API.

It includes:
- A pytest fixture named `test_client` that sets up a test client for
  the Flask API.
- The test client is configured for testing, allowing for simulated HTTP
  requests to the API endpoints without needing to run the server.

Example usage:
    Use the `test_client` fixture in your test functions to simulate
    requests to the API, as shown in the test files.

This module ensures that all tests can share a common test client 
configuration for consistency and ease of maintenance.
"""
