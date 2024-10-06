FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

WORKDIR /api

COPY . /api

RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --system --dev \
    && python /api/answer_service/sentence_embedding/build_sentence_embedding.py

EXPOSE 8000

CMD ["gunicorn", "api:essay_answers_api", "--timeout", "1000", "--bind", "0.0.0.0:8000"]

