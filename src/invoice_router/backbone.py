from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.util import find_spec
from typing import Any


@dataclass(frozen=True)
class BackboneStatus:
    automation_kit_available: bool
    review_router_available: bool
    fixture_safe: bool = True
    live_services_used: bool = False
    synthetic_data_only: bool = True

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CapabilityMetadata:
    package: str = "invoice-router"
    capabilities: tuple[str, ...] = (
        "invoice-ingest-schema",
        "deterministic-extraction",
        "validation-report",
        "review-packet-queue",
        "accounting-preview",
        "local-api",
        "cli-surface",
        "replayable-artifacts",
    )

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["capabilities"] = list(self.capabilities)
        return payload


def get_backbone_status() -> BackboneStatus:
    automation_kit_available = (
        find_spec("automation_kit") is not None or find_spec("auto_kit") is not None
    )
    return BackboneStatus(
        automation_kit_available=automation_kit_available,
        review_router_available=find_spec("review_router") is not None,
    )


def get_health() -> dict[str, Any]:
    payload = get_backbone_status().as_dict()
    payload.update(CapabilityMetadata().as_dict())
    return payload
