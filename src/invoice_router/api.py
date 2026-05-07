from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from invoice_router.runtime import InvoiceRouterRuntime, build_runtime


class ScenarioRequest(BaseModel):
    scenario: str
    fixture_path: str | None = None


class ResolveRequest(BaseModel):
    packet_id: str
    reviewer: str
    decision: str
    note: str


class ClaimRequest(BaseModel):
    packet_id: str
    reviewer: str


@lru_cache(maxsize=1)
def get_runtime() -> InvoiceRouterRuntime:
    return build_runtime()


def register_routes(app: FastAPI) -> FastAPI:
    @app.get("/health")
    def health() -> dict[str, Any]:
        return get_runtime().health()

    @app.get("/scenarios")
    def scenarios() -> dict[str, Any]:
        runtime = get_runtime()
        return {
            "scenarios": runtime.list_scenarios(),
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
        }

    @app.post("/validate")
    def validate(payload: ScenarioRequest) -> dict[str, Any]:
        fixture_path = Path(payload.fixture_path) if payload.fixture_path else None
        return get_runtime().validate(payload.scenario, fixture_path)

    @app.post("/run")
    def run(payload: ScenarioRequest) -> dict[str, Any]:
        fixture_path = Path(payload.fixture_path) if payload.fixture_path else None
        return get_runtime().run(payload.scenario, fixture_path)

    @app.get("/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, Any]:
        try:
            result = get_runtime().get_run(run_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc
        return {
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
            **result,
        }

    @app.post("/queue/claim")
    def queue_claim(payload: ClaimRequest) -> dict[str, Any]:
        return {
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
            "packet": get_runtime().claim_packet(payload.packet_id, payload.reviewer),
        }

    @app.post("/queue/resolve")
    def queue_resolve(payload: ResolveRequest) -> dict[str, Any]:
        packet = get_runtime().resolve_packet(
            payload.packet_id,
            payload.reviewer,
            payload.decision,
            payload.note,
        )
        return {
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
            "packet": packet,
        }

    return app


def create_app() -> FastAPI:
    app = FastAPI(title="Invoice Router API", version="0.1.0")
    return register_routes(app)


app = create_app()
