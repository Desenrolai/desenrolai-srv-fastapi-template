# srv-fastapi-template

GitHub Template — backend Python 3.12 + FastAPI.

## Requisitos

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

## Rodar localmente

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]" || uv pip install fastapi "uvicorn[standard]"
uvicorn src.main:app --reload --port 8000
# GET http://localhost:8000/health → {"status":"ok"}
```

## Docker

```bash
docker build -t srv-fastapi-template .
docker run -p 8000:8000 srv-fastapi-template
```

## CI

Push para `main` → lint (ruff) + typecheck (mypy) + build + push GHCR.
