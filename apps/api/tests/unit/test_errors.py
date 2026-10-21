from fastapi import FastAPI
from fastapi.testclient import TestClient

from tricolink.core.error_handlers import install_error_handlers
from tricolink.shared_kernel.errors import NotFoundError
from tricolink.shared_kernel.security_errors import AuthenticationError


def build_app() -> FastAPI:
    app = FastAPI()
    install_error_handlers(app)

    @app.get("/missing")
    async def missing() -> None:
        raise NotFoundError("Link not found")

    @app.get("/auth")
    async def auth() -> None:
        raise AuthenticationError()

    @app.get("/crash")
    async def crash() -> None:
        raise RuntimeError("secret details must not leak")

    @app.get("/number")
    async def number(value: int) -> dict[str, int]:
        return {"value": value}

    return app


def test_app_error_uses_standard_envelope() -> None:
    with TestClient(build_app()) as client:
        response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {"error": {"code": "not_found", "message": "Link not found"}}


def test_security_error_uses_standard_envelope() -> None:
    with TestClient(build_app()) as client:
        response = client.get("/auth")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "authentication_required"


def test_unhandled_error_does_not_leak_stack_trace() -> None:
    with TestClient(build_app(), raise_server_exceptions=False) as client:
        response = client.get("/crash")

    assert response.status_code == 500
    body = response.text
    assert "secret details" not in body
    assert "Traceback" not in body
    assert response.json() == {
        "error": {"code": "internal_error", "message": "Internal server error"}
    }


def test_validation_error_uses_standard_envelope() -> None:
    with TestClient(build_app()) as client:
        response = client.get("/number", params={"value": "not-an-int"})

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "validation_error"
    assert isinstance(payload["error"]["details"], list)


def test_unknown_route_uses_standard_envelope() -> None:
    with TestClient(build_app()) as client:
        response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
