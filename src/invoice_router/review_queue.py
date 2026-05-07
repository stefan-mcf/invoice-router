from __future__ import annotations

import hashlib
import json
from pathlib import Path

from invoice_router.models import (
    QueueResolution,
    ReasonCode,
    ReviewPacket,
    ReviewPacketStatus,
    RoutingDecision,
)


class FileReviewQueue:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.pending_dir = root / "pending"
        self.claimed_dir = root / "claimed"
        self.resolved_dir = root / "resolved"
        self.dead_letter_dir = root / "dead-letter"
        for directory in [
            self.pending_dir,
            self.claimed_dir,
            self.resolved_dir,
            self.dead_letter_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    def enqueue(
        self,
        scenario_name: str,
        routing: RoutingDecision,
        reason_codes: list[ReasonCode],
        evidence_snippets: list[str],
    ) -> ReviewPacket:
        seed = json.dumps(
            {
                "scenario_name": scenario_name,
                "reasons": list(reason_codes),
                "evidence": evidence_snippets,
                "next_step": routing.recommended_next_step,
            },
            sort_keys=True,
        )
        packet_id = hashlib.sha256(seed.encode()).hexdigest()[:12]
        packet = ReviewPacket(
            packet_id=packet_id,
            scenario_name=scenario_name,
            status=ReviewPacketStatus.PENDING,
            reason_codes=reason_codes,
            reason_summary=routing.recommended_next_step,
            evidence_snippets=evidence_snippets,
            recommended_next_step=routing.recommended_next_step,
        )
        self._save(self.pending_dir, packet)
        return packet

    def list_all(self) -> dict[str, list[dict[str, object]]]:
        return {
            "pending": [
                packet.model_dump(mode="json")
                for packet in self._load_all(self.pending_dir)
            ],
            "claimed": [
                packet.model_dump(mode="json")
                for packet in self._load_all(self.claimed_dir)
            ],
            "resolved": [
                packet.model_dump(mode="json")
                for packet in self._load_all(self.resolved_dir)
            ],
            "dead_letter": [
                packet.model_dump(mode="json")
                for packet in self._load_all(self.dead_letter_dir)
            ],
        }

    def claim(self, packet_id: str, reviewer: str) -> ReviewPacket:
        packet = self._move(packet_id, self.pending_dir)
        packet.status = ReviewPacketStatus.CLAIMED
        packet.claimed_by = reviewer
        self._save(self.claimed_dir, packet)
        return packet

    def resolve(
        self,
        packet_id: str,
        reviewer: str,
        resolution: QueueResolution,
    ) -> ReviewPacket:
        packet = self._move(packet_id, self.claimed_dir)
        packet.claimed_by = reviewer
        packet.resolution_note = resolution.note
        packet.status = (
            ReviewPacketStatus.RESOLVED_APPROVED
            if resolution.decision == "approve"
            else ReviewPacketStatus.RESOLVED_REJECTED
        )
        self._save(self.resolved_dir, packet)
        return packet

    def dead_letter(self, packet_id: str, note: str) -> ReviewPacket:
        source = (
            self.claimed_dir
            if (self.claimed_dir / f"{packet_id}.json").exists()
            else self.pending_dir
        )
        packet = self._move(packet_id, source)
        packet.status = ReviewPacketStatus.DEAD_LETTER
        packet.resolution_note = note
        self._save(self.dead_letter_dir, packet)
        return packet

    def _load_all(self, directory: Path) -> list[ReviewPacket]:
        return [
            ReviewPacket.model_validate_json(path.read_text())
            for path in sorted(directory.glob("*.json"))
        ]

    def _save(self, directory: Path, packet: ReviewPacket) -> None:
        (directory / f"{packet.packet_id}.json").write_text(
            packet.model_dump_json(indent=2) + "\n"
        )

    def _move(self, packet_id: str, src_dir: Path) -> ReviewPacket:
        src = src_dir / f"{packet_id}.json"
        if not src.exists():
            raise FileNotFoundError(packet_id)
        packet = ReviewPacket.model_validate_json(src.read_text())
        src.unlink()
        return packet
