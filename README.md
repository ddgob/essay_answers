# essay_answers

## Project Summary

In this project we will be creating an application that receives and essay and some queries from the users and returns the answers to these queries. This service will be available to the user through an endpoint

## Project Design and Technical Decisions

### Class Architecture

The project follows a modular architecture with clearly defined class structures. Below is a simplified diagram illustrating how different components interact:

<div align="center">
	<img src="./diagram.png">
</div>

- **SentenceEmbedding**: This class represents a sentence and its corresponding embedding, providing methods for calculating cosine similarity and finding the most similar sentence.
- **TestPreProcessor**: This class preprocesses the essay by splitting it into paragraphs and sentences, identifying subtitles, and organizing text for further analysis.
- **Encoder**: This class is responsible for encoding essay sentences and queries into embeddings using a pre-trained SentenceTransformer model.
- **AnswerService**: The service class that handles the core logic of finding answers to the queries by comparing query embeddings with essay embeddings and subtitles.
- **EssayAnswersAPI**: This class encapsulates the API logic and provides the /answers endpoint for receiving essay and query input, coordinating the validation and answer generation process.

### Model Used for Creating Embeddings

The all-mpnet-base-v2 model from the SentenceTransformer library was chosen for generating embeddings due to its high performance in tasks like sentence similarity and question answering. This BERT-based model captures complex word relationships, producing compact embeddings that enable efficient and accurate query matching. The SentenceTransformer library's ease of use and the pre-trained model's efficiency make it ideal for this task.

### Similarity Measure Used for Comparing Embeddings

Cosign similarity was chosen due to its focus on the angle between vectors rather than their magnitude, optimizing for semantic similarity of the embeddings. In addition to that widespread use of BERT and cosign similarity alongside each other makes the cosign similarity the ideal measurement of similarity.

### Formatting and Style Guide

- The code adheres to the [PEP8](https://pep8.org/) guidelines for Python
- A maximum line length of **90 characters** was chosen for improved readability in modern editor environments (especially due to the fact that typing was used).
- Comments follow a **72-character** limit per line to ensure clarity in explanations without overly long lines.
- Classes, functions, and variables follow a clear and consistent naming convention that aims for readability and clarity.

### Error Handling

We use structured error handling, ensuring that all API endpoints return meaningful error messages when invalid input is received.

- **400 Bad Request**: This status is returned when the client sends malformed or invalid data, such as missing required fields, an empty essay, or improperly formatted queries..
- **500 Internal Server Error**: This status is returned for any unexpected issues that occur within the server or application logic, indicating that something went wrong on the server-side.

### Dependencies Management

- Dependencies are managed using `pipenv` for environment isolation and reproducibility.
- Docker is used for consistent environment management.

### Logging

The project implements logging in various components to provide detailed insights into the internal operations. Logging is used to track the following processes:

- Text preprocessing (splitting paragraphs, identifying subtitles, etc...).
- Sentence encoding and embedding generation.
- Query and essay comparison to find the most relevant answers.
- Validation and API requests handling in EssayAnswersAPI.

## Prerequisites

### Docker

Ensure you have Docker installed on your machine. Docker will handle the environment setup, including system dependencies and Python package installations.

### Dependencies

This project uses the following Python packages, which are automatically installed within the Docker container:

- `flask`
- `gunicorn`
- `pybind11`
- `sentence-transformers`
- `numpy==1.24`
- `mypy`
- `pytest`
- `flask-testing`
- `torch`
- `requests`
- `ipykernel`

The dependencies are managed using `pipenv`. You do not need to install these manually unless running the application outside of Docker.

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/ddgob/essay_answers
cd essay_answers
```

### Step 2: Build the Docker container

Build and run the application using Docker:

```bash
docker build -t essay_answers .
docker run -d -p 8000:8000 --name essay_answers_api essay_answers
```

This command will:

- Build the Docker image using the Dockerfile file.
- Install system dependencies (e.g., cmake, g++, etc.).
- Install Python dependencies using pipenv.
- Build necessary pybind11 module.
- Set up the container environment and expose port 8000.

### Step 3: Verify the container is running

You can verify that the container is running and the API is listening on http://0.0.0.0:8000.

```bash
docker ps
```

You should see the running container named something like essay_answers_api

## Usage

Once the container is up and running, you can start interacting with the API.

### Start Here

The best way to see and understand the usage of the API and it's features is to follow this [quick tutorial](./quick_tutorial.ipynb).

### Another (worse) Option

However, if you don't want to fully understand how the API works and not see it's features, here’s an example of how to send a POST request to the `/answers` endpoint.

#### Example Request:

```bash
curl -X POST http://127.0.0.1:8000/answers \
    -H "Content-Type: application/json" \
    -d '{
            "essay": "Introduction to Trees.\nTrees are green. Trees have leaves. Trees are tall.\nConclusion\nI love trees. I want to buy five trees.", 
            "queries": ["What is the color of trees?", "How tall are trees?", "How many trees do I want to buy?"]
        }'
```

**OBS:** make sure you have `curl` installed

#### Example Response:

```bash
{
  "answers": ["Trees are green", "Trees are tall", "I want to buy five trees"]
}
```

## API Reference

- POST `/answers`
    - **Description:** Returns the answers to the provided queries based on the given essay.
    - **Request Body:**
        - `essay` (string): The essay text.
        - `queries` (array of strings): A list of queries related to the essay.
    - **Request Body:**
        - `answers` (array of strings): A list of answers corresponding to the queries.


## Testing

To test the application, you can run the following command:

```bash
docker exec -it essay_answers_api python tests/run_checks.py
```

This will run pytest on all the tests implemented in `/tests` and also check the typing in the whole project using `mypy`.