# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install --no-cache-dir -U pip

# --- Dev image ---
FROM base AS dev
COPY pyproject.toml README.md /app/
COPY app /app/app
COPY tests /app/tests
RUN pip install --no-cache-dir -e ".[dev]"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# --- Prod image ---
FROM base AS prod
COPY pyproject.toml README.md /app/
COPY app /app/app
RUN pip install --no-cache-dir -e .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
