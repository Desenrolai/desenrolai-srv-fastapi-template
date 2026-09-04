# srv-fastapi-template

GitHub Template — backend **Python 3.13 + FastAPI**, gerenciado com [uv](https://docs.astral.sh/uv/).

## Stack

| Ferramenta | Versão mínima | Papel |
|---|---|---|
| Python | 3.13 | runtime |
| `fastapi` | 0.141.1 | framework HTTP |
| `pydantic` | 2.13.5 | schema e validação (v2) |
| `uvicorn[standard]` | 0.52.4 | ASGI server |
| `ruff` | 0.16.6 | lint + format |
| `mypy` | 2.3.1 | tipagem estrita |
| `pytest` + `pytest-cov` | 9.1.1 / 7.1.0 | testes e cobertura |

## Rodar localmente

```bash
uv sync --all-groups
uv run uvicorn src.main:app --reload --port 8000
# GET http://localhost:8000/health → {"status":"ok"}
```

## Gate de qualidade

Os quatro comandos que o CI roda — rode-os antes de todo push:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy
uv run pytest
```

- `mypy` roda em **strict** e cobre `src` e `tests`.
- `ruff` inclui `I` (ordem de import) e `S` (flake8-bandit, segurança). `S101` é ignorado só em `tests/`.
- `pytest` falha abaixo de **90%** de cobertura (`--cov-fail-under`).

## Estrutura

```
src/
  __init__.py
  main.py          # app FastAPI — adicione seus routers aqui
tests/
  test_health.py   # bate no app via TestClient
```

## Docker

Multi-stage com uv, base `python:3.13-slim`, usuário não-root (uid 10001) e
`HEALTHCHECK` no mesmo path do `healthPath` do `forge.yaml`.

```bash
docker build -t srv-fastapi-template .
docker run -p 8000:8000 srv-fastapi-template
```

## CI

`.github/workflows/ci.yml`, em dois jobs:

1. **quality** — `ruff check`, `ruff format --check`, `mypy`, `pytest` (Python 3.13).
2. **docker** — constrói a imagem em toda branch/PR (gate) e **publica no GHCR só na branch default**.

`concurrency` com `cancel-in-progress` derruba execuções antigas da mesma ref;
`permissions` é `contents: read` por padrão, elevado a `packages: write` só no job que publica.

## Dependências

`uv.lock` é a fonte da verdade — commite-o. Para atualizar:

```bash
uv lock --upgrade
uv sync --all-groups
```
