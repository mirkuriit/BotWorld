FROM python:3.13-slim



env POSTGRES_USER=${POSTGRES_USER}
env POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
env POSTGRES_DB=${POSTGRES_DB}
env POSTGRES_PORT=${POSTGRES_PORT}
env POSTGRES_HOST=${POSTGRES_HOST_FOR_BACKEND}

POSTGRES_HOST=localhost
ENV FASTAPI_HOST=${FASTAPI_HOST}
ENV FASTAPI_PORT=${FASTAPI_PORT}

RUN pip install --no-cache-dir poetry

WORKDIR /botworld/botworld_api

COPY pyproject.toml poetry.lock README.md /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./botworld /app




CMD uvicorn app.src.main:app --host ${FASTAPI_HOST} --port ${FASTAPI_PORT}