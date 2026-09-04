"""Hello-world FastAPI — substitua pelos seus routers."""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="srv-fastapi-template", version="0.1.0")


class HealthResponse(BaseModel):
    """Corpo de `GET /health` — o `healthPath` declarado no forge.yaml."""

    status: str


@app.get("/health")
def health() -> HealthResponse:
    return HealthResponse(status="ok")
