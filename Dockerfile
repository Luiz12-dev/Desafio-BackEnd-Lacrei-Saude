FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
