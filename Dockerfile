FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# configure Poetry
ENV POETRY_VERSION=1.6.1

# installing Poetry
RUN pip install poetry==${POETRY_VERSION} && poetry install --no-root --no-directory
COPY toktik_converter/ ./toktik_converter/
RUN poetry install --no-dev

# insalling ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# run the application
CMD ["poetry", "run", "celery", "-A", "toktik_converter.tasks.app", "worker", "-l", "INFO"]
