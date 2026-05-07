from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from invoice_router.backbone import get_health
from invoice_router.exports import ExportPreviewBuilder
from invoice_router.extractor import InvoiceExtractor
from invoice_router.models import InvoiceIngest, QueueResolution
from invoice_router.review_queue import FileReviewQueue
from invoice_router.routing import InvoiceRouter
from invoice_router.scenario_registry import ScenarioRegistry
from invoice_router.validation import InvoiceValidator


class InvoiceRouterRuntime:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.registry = ScenarioRegistry(root)
        self.extractor = InvoiceExtractor()
        self.validator = InvoiceValidator()
        self.router = InvoiceRouter()
        self.exports = ExportPreviewBuilder()
        self.queue = FileReviewQueue(root / "artifacts" / "local" / "queue")
        self.run_root = root / "artifacts" / "local" / "runs"
        self.run_root.mkdir(parents=True, exist_ok=True)

    def list_scenarios(self) -> list[dict[str, str]]:
        return [
            {
                "name": record.name,
                "description": record.description,
                "expected_outcome": record.expected_outcome,
            }
            for record in self.registry.list_records()
        ]

    def validate(self, scenario_name: str, fixture_path: Path | None = None) -> dict[str, Any]:
        ingest = self._load_ingest(scenario_name, fixture_path)
        extraction = self.extractor.extract(ingest)
        report = self.validator.validate(ingest, extraction)
        findings = report.model_dump(mode="json")["findings"]
        return {
            "scenario_name": scenario_name,
            "valid": not any(finding["severity"] == "error" for finding in findings),
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
            "findings": findings,
            "expected": self.registry.load_expected(scenario_name),
        }

    def run(self, scenario_name: str, fixture_path: Path | None = None) -> dict[str, Any]:
        ingest = self._load_ingest(scenario_name, fixture_path)
        extraction = self.extractor.extract(ingest)
        report = self.validator.validate(ingest, extraction)
        routing = self.router.route(report, extraction.overall_confidence)
        packet = None
        if routing.review_packet_required:
            packet = self.queue.enqueue(
                scenario_name=ingest.scenario_name,
                routing=routing,
                reason_codes=routing.reasons,
                evidence_snippets=self._build_evidence_snippets(extraction, report),
            )
        previews = self.exports.build_previews(ingest, extraction, routing, report.duplicate_key)
        run_id = report.duplicate_key
        run_dir = self.run_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        handoff_note = self._handoff_note(
            ingest.scenario_name,
            routing.recommended_next_step,
            routing.review_packet_required,
            packet.packet_id if packet else None,
        )
        self._write_artifacts(
            run_dir,
            ingest,
            extraction.model_dump(mode="json"),
            report.model_dump(mode="json"),
            routing.model_dump(mode="json"),
            [preview.model_dump(mode="json") for preview in previews],
            handoff_note,
        )
        audit_log = {
            "run_id": run_id,
            "scenario_name": ingest.scenario_name,
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
            "health_contract": self.health(),
            "input_path": str(run_dir / "input.json"),
            "extraction_path": str(run_dir / "extraction.json"),
            "validation_path": str(run_dir / "validation.json"),
            "routing_path": str(run_dir / "routing.json"),
            "export_preview_path": str(run_dir / "export-preview.json"),
            "handoff_notes_path": str(run_dir / "handoff-notes.md"),
        }
        (run_dir / "audit-log.json").write_text(json.dumps(audit_log, indent=2) + "\n")
        return {
            "run_id": run_id,
            "scenario_name": ingest.scenario_name,
            "routing_outcome": routing.outcome,
            "review_packet_id": packet.packet_id if packet else None,
            "review_required": routing.review_packet_required,
            "export_targets": [preview.target for preview in previews],
            "duplicate_key": report.duplicate_key,
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
        }

    def replay(self, run_id: str) -> dict[str, Any]:
        run = self.get_run(run_id)
        scenario_name = str(run["input"]["scenario_name"])
        original_hashes = run["hashes"]
        rerun = self.run(scenario_name)
        replay_hashes = self.get_run(rerun["run_id"])["hashes"]
        return {
            "run_id": run_id,
            "replay_run_id": rerun["run_id"],
            "hash_match": original_hashes == replay_hashes,
            "original_hashes": original_hashes,
            "replay_hashes": replay_hashes,
            "fixture_safe": True,
            "live_services_used": False,
            "synthetic_data_only": True,
        }

    def queue_state(self) -> dict[str, list[dict[str, object]]]:
        return self.queue.list_all()

    def claim_packet(self, packet_id: str, reviewer: str) -> dict[str, Any]:
        return self.queue.claim(packet_id, reviewer).model_dump(mode="json")

    def resolve_packet(
        self,
        packet_id: str,
        reviewer: str,
        decision: str,
        note: str,
    ) -> dict[str, Any]:
        resolution = QueueResolution(decision=decision, note=note)
        return self.queue.resolve(packet_id, reviewer, resolution).model_dump(mode="json")

    def health(self) -> dict[str, Any]:
        payload = get_health()
        payload.update(
            {
                "status": "ok",
                "fixture_safe": True,
                "live_services_used": False,
                "synthetic_data_only": True,
            }
        )
        return payload

    def get_run(self, run_id: str) -> dict[str, Any]:
        run_dir = self.run_root / run_id
        return {
            "audit_log": json.loads((run_dir / "audit-log.json").read_text()),
            "input": json.loads((run_dir / "input.json").read_text()),
            "extraction": json.loads((run_dir / "extraction.json").read_text()),
            "validation": json.loads((run_dir / "validation.json").read_text()),
            "routing": json.loads((run_dir / "routing.json").read_text()),
            "export_preview": json.loads((run_dir / "export-preview.json").read_text()),
            "hashes": {
                "input": (run_dir / "input.json").read_text(),
                "extraction": (run_dir / "extraction.json").read_text(),
                "validation": (run_dir / "validation.json").read_text(),
                "routing": (run_dir / "routing.json").read_text(),
                "export_preview": (run_dir / "export-preview.json").read_text(),
            },
            "handoff_notes": (run_dir / "handoff-notes.md").read_text(),
        }

    def _load_ingest(self, scenario_name: str, fixture_path: Path | None) -> InvoiceIngest:
        if fixture_path is not None:
            return self.registry.load_ingest_from_path(fixture_path)
        return self.registry.load_ingest(scenario_name)

    def _build_evidence_snippets(self, extraction: Any, report: Any) -> list[str]:
        snippets = [f"overall_confidence={extraction.overall_confidence:.2f}"]
        snippets.extend(
            f"{finding.reason_code.value}: {finding.message}" for finding in report.findings
        )
        return snippets[:6]

    def _handoff_note(
        self,
        scenario_name: str,
        recommended_next_step: str,
        review_required: bool,
        packet_id: str | None,
    ) -> str:
        lines = [
            f"Scenario: {scenario_name}",
            f"Review required: {'yes' if review_required else 'no'}",
            f"Recommended next step: {recommended_next_step}",
        ]
        if packet_id is not None:
            lines.append(f"Review packet: {packet_id}")
        return "\n".join(lines) + "\n"

    def _write_artifacts(
        self,
        run_dir: Path,
        ingest: InvoiceIngest,
        extraction: dict[str, Any],
        validation: dict[str, Any],
        routing: dict[str, Any],
        previews: list[dict[str, Any]],
        handoff_note: str,
    ) -> None:
        (run_dir / "input.json").write_text(ingest.model_dump_json(indent=2) + "\n")
        (run_dir / "extraction.json").write_text(json.dumps(extraction, indent=2) + "\n")
        (run_dir / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")
        (run_dir / "routing.json").write_text(json.dumps(routing, indent=2) + "\n")
        (run_dir / "export-preview.json").write_text(json.dumps(previews, indent=2) + "\n")
        (run_dir / "handoff-notes.md").write_text(handoff_note)


def build_runtime(base_path: Path | None = None) -> InvoiceRouterRuntime:
    repo_root = Path(__file__).resolve().parents[2] if base_path is None else base_path
    return InvoiceRouterRuntime(repo_root)
