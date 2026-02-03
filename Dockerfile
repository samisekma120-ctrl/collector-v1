# syntax=docker/dockerfile:1.6

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# deps OS minimales (bcrypt/crypto peuvent nécessiter libffi/openssl selon wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# user non-root
RUN addgroup --system app && adduser --system --ingroup app app

# Copier uniquement les fichiers nécessaires à l'installation (cache Docker friendly)
COPY pyproject.toml README.md /app/
COPY app /app/app

# Installer l'app et ses dépendances prod depuis pyproject.toml
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir .

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
