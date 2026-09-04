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

`.github/workflows/ci.yml`, em três jobs:

1. **quality** — `ruff check`, `ruff format --check`, `mypy`, `pytest` (Python 3.13).
2. **docker-build** — `docker build` **sem push**, em todo PR e branch de feature. É o gate:
   Dockerfile quebrado reprova antes do merge, não depois. Não faz login no GHCR e não
   recebe `packages: write`.
3. **docker-publish** — build **+ push** no GHCR, só em push na branch default. É o único
   job com `packages: write`.

Os dois jobs de imagem são mutuamente exclusivos: em PR o `docker-publish` aparece como
`skipped`, e na branch default é o `docker-build` que fica `skipped`.

`concurrency` com `cancel-in-progress` derruba execuções antigas da mesma ref.

### Runner: repo privado gerado a partir deste template precisa configurar

Este template é **público**, e em repositório público o GitHub Actions em runner hospedado
é gratuito. **O repo que você gera a partir dele é privado**, onde os minutos são cota paga
— e a cota da organização está esgotada. Por isso o `runs-on` é parametrizado por variável
de repositório, com default hospedado:

```yaml
runs-on: ${{ fromJSON(vars.CI_RUNNER || '"ubuntu-latest"') }}
```

Antes do primeiro push no repo novo, defina as duas variáveis (Settings → Secrets and
variables → Actions → Variables), ou por CLI:

```bash
gh variable set CI_RUNNER        --body '["self-hosted","desenrolai"]'
gh variable set CI_RUNNER_DOCKER --body '["self-hosted","docker-builder"]'
```

- O valor é **JSON**, não texto solto. `'["self-hosted","desenrolai"]'` vira dois labels;
  a string `self-hosted,desenrolai` viraria **um** label só, que nenhum runner atende, e o
  job ficaria em `queued` para sempre.
- `CI_RUNNER_DOCKER` é separado porque o build de imagem exige o runner com Docker
  (`docker-builder`); os demais jobs rodam no pool geral.
- Sem as variáveis, tudo continua em `ubuntu-latest` — este template continua verde assim.

**Sintoma de não configurar:** o job termina em **~2 segundos**, com **zero steps
executados** e conclusão **`failure`** — sem nenhum log de erro que oriente.

Cuidado: *zero steps sozinho não é a assinatura.* Um job legitimamente **`skipped`**
também reporta zero steps — e este workflow tem um por design: em PR, o `docker-publish`
aparece `skipped`, e isso é o comportamento correto. **O que separa os dois é a
conclusão:**

| Conclusão | Steps | Significado |
|---|---|---|
| `failure` em ~2s | 0 | **Billing** — cota de Actions esgotada/bloqueada, ou runner inexistente |
| `skipped` | 0 | O `if:` do job não bateu. Está tudo certo. |
| `queued` que nunca sai | — | `CI_RUNNER` com label que nenhum runner atende (ex.: valor não-JSON) |

Não perca tempo procurando erro de sintaxe: com `failure` em ~2s, confira a variável e o
billing da organização.

## Dependências

`uv.lock` é a fonte da verdade — commite-o. Para atualizar:

```bash
uv lock --upgrade
uv sync --all-groups
```
