"""Teste do endpoint de health batendo no app via TestClient."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_retorna_200_e_status_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_esta_no_schema_openapi() -> None:
    """O healthPath do forge.yaml precisa existir de fato no contrato do app."""
    schema = client.get("/openapi.json").json()

    assert "/health" in schema["paths"]


def test_rota_inexistente_retorna_404() -> None:
    assert client.get("/nao-existe").status_code == 404
