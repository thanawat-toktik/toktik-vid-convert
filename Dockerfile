FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# configure Poetry
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry

# installing Poetry
RUN pip install poetry==${POETRY_VERSION} && poetry install --no-root --no-directory
COPY toktik_converter/ ./toktik_converter/
RUN poetry install --no-dev

# run the application
CMD ["poetry", "run", "gunicorn", "toktik_converter.main:app", "uvicorn.workers.UvicornWorker"]