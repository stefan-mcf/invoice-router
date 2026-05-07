from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from invoice_router.models import InvoiceIngest


@dataclass(frozen=True)
class ScenarioRecord:
    name: str
    description: str
    expected_outcome: str
    fixture_path: Path
    expected_path: Path
    notes_path: Path


class ScenarioRegistry:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.input_dir = root / "fixtures" / "input"
        self.expected_dir = root / "fixtures" / "expected"
        self.notes_dir = root / "fixtures" / "notes"
        self.registry_path = root / "registry" / "scenario-registry.json"

    def list_records(self) -> list[ScenarioRecord]:
        entries = json.loads(self.registry_path.read_text())
        records: list[ScenarioRecord] = []
        for entry in entries["scenarios"]:
            name = str(entry["name"])
            records.append(
                ScenarioRecord(
                    name=name,
                    description=str(entry["description"]),
                    expected_outcome=str(entry["expected_outcome"]),
                    fixture_path=self.input_dir / f"{name}.json",
                    expected_path=self.expected_dir / f"{name}.json",
                    notes_path=self.notes_dir / f"{name}.md",
                )
            )
        return records

    def names(self) -> list[str]:
        return [record.name for record in self.list_records()]

    def get_record(self, name: str) -> ScenarioRecord:
        for record in self.list_records():
            if record.name == name:
                return record
        raise KeyError(name)

    def load_ingest(self, name: str) -> InvoiceIngest:
        record = self.get_record(name)
        return InvoiceIngest.model_validate_json(record.fixture_path.read_text())

    def load_ingest_from_path(self, path: Path) -> InvoiceIngest:
        return InvoiceIngest.model_validate_json(path.read_text())

    def load_expected(self, name: str) -> dict[str, Any]:
        record = self.get_record(name)
        return cast(dict[str, Any], json.loads(record.expected_path.read_text()))
