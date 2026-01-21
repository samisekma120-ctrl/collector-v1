# Collector V1 (skeleton)

Monolithe FastAPI (Python) + PostgreSQL, prêt pour socle CI (ruff + pytest) et exécution locale via Docker Compose.

## Run local (venv)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    API: http://localhost:8000

    Swagger: http://localhost:8000/docs

    Health: http://localhost:8000/health
