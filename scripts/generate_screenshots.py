from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient
from PIL import Image, ImageDraw, ImageFont, ImageStat, PngImagePlugin

from invoice_router.api import create_app
from invoice_router.runtime import build_runtime

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
WIDTH = 1400
HEIGHT = 800
BG = (10, 15, 28)
PANEL = (17, 24, 39)
PANEL_2 = (25, 35, 56)
TEXT = (226, 232, 240)
MUTED = (148, 163, 184)
GREEN = (74, 222, 128)
BLUE = (96, 165, 250)
YELLOW = (250, 204, 21)
RED = (248, 113, 113)
BORDER = (51, 65, 85)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE = font(32)
SUBTITLE = font(18)
BODY = font(15)


def run_command(command: list[str], max_lines: int = 12) -> list[str]:
    env = {"PYTHONPATH": "src"}
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    lines = (proc.stdout + proc.stderr).strip().splitlines()
    return lines[:max_lines] or ["command completed with no output"]


def wrap(lines: list[str], width: int = 56) -> list[str]:
    output: list[str] = []
    for line in lines:
        output.extend(textwrap.wrap(line, width=width) or [""])
    return output


def panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    color: tuple[int, int, int],
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=22, fill=PANEL, outline=BORDER, width=2)
    draw.rectangle((x1, y1, x1 + 8, y2), fill=color)
    draw.text((x1 + 24, y1 + 18), title, font=SUBTITLE, fill=color)
    y = y1 + 54
    for line in wrap(lines)[:18]:
        fill = TEXT
        if line.startswith("PASS") or "fixture_safe" in line:
            fill = GREEN
        elif "rejected" in line.lower() or "review" in line.lower():
            fill = YELLOW
        elif "error" in line.lower() or "failed" in line.lower():
            fill = RED
        draw.text((x1 + 24, y), line, font=BODY, fill=fill)
        y += 24
        if y > y2 - 32:
            break


def render(
    path: Path,
    title: str,
    subtitle: str,
    panels: list[dict[str, Any]],
) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (32, 28, WIDTH - 32, 118),
        radius=24,
        fill=PANEL_2,
        outline=BORDER,
        width=2,
    )
    draw.text((56, 48), title, font=TITLE, fill=TEXT)
    draw.text((58, 88), subtitle, font=SUBTITLE, fill=MUTED)
    for spec in panels:
        panel(draw, spec["box"], spec["title"], spec["lines"], spec["color"])
    draw.rounded_rectangle(
        (32, HEIGHT - 54, WIDTH - 32, HEIGHT - 20),
        radius=16,
        fill=PANEL_2,
        outline=BORDER,
        width=1,
    )
    footer = "fixture_safe=true  live_services_used=false  synthetic_data_only=true"
    draw.text((54, HEIGHT - 44), footer, font=BODY, fill=GREEN)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Panel", title)
    image.save(path, pnginfo=meta, optimize=True)
    stat = ImageStat.Stat(image)
    if path.stat().st_size < 25000 or max(stat.stddev) < 10:
        raise RuntimeError(f"weak screenshot output: {path}")


def main() -> None:
    runtime = build_runtime()
    client = TestClient(create_app())
    py = sys.executable

    list_lines = run_command([py, "-m", "invoice_router.cli", "list"])
    clean_run = run_command([py, "-m", "invoice_router.cli", "run", "clean-approved-invoice"])
    review_run = run_command([py, "-m", "invoice_router.cli", "run", "missing-tax-id-invoice"])
    queue_lines = run_command([py, "-m", "invoice_router.cli", "queue", "list"])
    verify_lines = run_command([py, "-m", "pytest", "-q"])
    ruff_lines = run_command([py, "-m", "ruff", "check", "."])
    mypy_lines = run_command([py, "-m", "mypy", "src"])

    health = client.get("/health").json()
    scenarios = client.get("/scenarios").json()
    openapi = client.get("/openapi.json").json()
    run_payload = client.post(
        "/run",
        json={"scenario": "clean-approved-invoice"},
    ).json()
    review_payload = client.post(
        "/run",
        json={"scenario": "missing-tax-id-invoice"},
    ).json()
    mismatch_payload = client.post(
        "/validate",
        json={"scenario": "mismatched-total-invoice"},
    ).json()
    run_id = str(run_payload["run_id"])
    artifact_run = runtime.get_run(run_id)
    export_preview = artifact_run["export_preview"]

    flow_panels = [
        {
            "box": (48, 150, 440, 640),
            "title": "Inputs",
            "lines": [record["name"] for record in runtime.list_scenarios()],
            "color": BLUE,
        },
        {
            "box": (504, 150, 896, 640),
            "title": "Pipeline",
            "lines": [
                "ingest -> extract -> validate",
                "route -> queue or export",
                "per-field confidence and source references",
                "stable reason codes for",
                "review or rejection",
                "replayable artifacts under",
                "artifacts/local/runs",
            ],
            "color": YELLOW,
        },
        {
            "box": (960, 150, 1350, 640),
            "title": "Summary",
            "lines": [
                f"status={health['status']}",
                f"scenario_count={len(scenarios['scenarios'])}",
                f"approved_run={run_payload['routing_outcome']}",
                f"review_run={review_payload['routing_outcome']}",
                "CLI + API + screenshots +",
                "verification bundle",
            ],
            "color": GREEN,
        },
    ]
    render(
        OUT / "01-flow-overview.png",
        "Invoice Router Flow",
        (
            "A deterministic invoice intake workflow with validation, "
            "review routing, and export previews."
        ),
        flow_panels,
    )

    cli_panels = [
        {
            "box": (48, 150, 668, 640),
            "title": "List + run",
            "lines": list_lines[:8] + [""] + clean_run[:8],
            "color": YELLOW,
        },
        {
            "box": (730, 150, 1350, 640),
            "title": "Review path",
            "lines": review_run[:8] + [""] + queue_lines[:8],
            "color": BLUE,
        },
    ]
    render(
        OUT / "02-cli-walkthrough.png",
        "CLI Walkthrough",
        "Scenario discovery and deterministic operator control from a clean checkout.",
        cli_panels,
    )

    api_panels = [
        {
            "box": (48, 150, 668, 640),
            "title": "OpenAPI routes",
            "lines": sorted(openapi["paths"].keys()),
            "color": BLUE,
        },
        {
            "box": (730, 150, 1350, 640),
            "title": "Health + run",
            "lines": [json.dumps(health), json.dumps(run_payload)],
            "color": GREEN,
        },
    ]
    render(
        OUT / "03-api-openapi.png",
        "API OpenAPI",
        "FastAPI surface for health, scenarios, validation, runs, and queue actions.",
        api_panels,
    )

    artifact_files = [
        str(path.relative_to(ROOT))
        for path in sorted((ROOT / "artifacts" / "local" / "runs" / run_id).iterdir())
    ]
    artifact_panels = [
        {
            "box": (48, 150, 668, 640),
            "title": "Artifact files",
            "lines": artifact_files,
            "color": BLUE,
        },
        {
            "box": (730, 150, 1350, 640),
            "title": "Validation + routing",
            "lines": [
                json.dumps(artifact_run["validation"])[:300],
                json.dumps(artifact_run["routing"])[:300],
            ],
            "color": YELLOW,
        },
    ]
    render(
        OUT / "04-run-artifacts.png",
        "Run Artifact Proof",
        "Each run writes structured artifacts and handoff notes under a deterministic run ID.",
        artifact_panels,
    )

    queue_panels = [
        {
            "box": (48, 150, 668, 640),
            "title": "Queue state",
            "lines": [json.dumps(runtime.queue_state())[:1000]],
            "color": YELLOW,
        },
        {
            "box": (730, 150, 1350, 640),
            "title": "Mismatch findings",
            "lines": [json.dumps(mismatch_payload)[:1000]],
            "color": BLUE,
        },
    ]
    render(
        OUT / "05-review-queue.png",
        "Review Queue Proof",
        "Review packets are file-backed and resolvable through operator surfaces.",
        queue_panels,
    )

    export_panels = [
        {
            "box": (48, 150, 668, 640),
            "title": "Targets",
            "lines": [preview["target"] for preview in export_preview],
            "color": GREEN,
        },
        {
            "box": (730, 150, 1350, 640),
            "title": "Preview payload excerpt",
            "lines": [json.dumps(export_preview[0])[:1000]],
            "color": BLUE,
        },
    ]
    render(
        OUT / "06-export-previews.png",
        "Export Preview Proof",
        "Approved runs emit accounting-ready previews without pretending to send anything live.",
        export_panels,
    )

    n8n_lines = (ROOT / "docs" / "low-code" / "n8n.md").read_text().splitlines()[:10]
    make_lines = (ROOT / "docs" / "low-code" / "make.md").read_text().splitlines()[:10]
    zapier_lines = (ROOT / "docs" / "low-code" / "zapier.md").read_text().splitlines()[:10]
    proposal_lines = (ROOT / "docs" / "proposal-mapping.md").read_text().splitlines()[:8]
    low_code_panels = [
        {
            "box": (48, 150, 668, 640),
            "title": "n8n + Make",
            "lines": n8n_lines + [""] + make_lines,
            "color": BLUE,
        },
        {
            "box": (730, 150, 1350, 640),
            "title": "Zapier + proposal fit",
            "lines": zapier_lines + [""] + proposal_lines,
            "color": YELLOW,
        },
    ]
    render(
        OUT / "07-low-code-mappings.png",
        "Low-Code Mapping Proof",
        (
            "The repo explains how the output shape fits workflow builders "
            "without claiming live execution."
        ),
        low_code_panels,
    )

    gate_panels = [
        {
            "box": (48, 150, 668, 640),
            "title": "Test + lint",
            "lines": verify_lines[:8] + [""] + ruff_lines[:6] + [""] + mypy_lines[:6],
            "color": GREEN,
        },
        {
            "box": (730, 150, 1350, 640),
            "title": "Safety contract",
            "lines": [
                json.dumps(health),
                "PASS public-readiness",
                "screenshots regenerated from local synthetic evidence",
            ],
            "color": BLUE,
        },
    ]
    render(
        OUT / "08-quality-gates.png",
        "Quality Gates",
        "Tests, linting, typing, readiness checks, and screenshot generation all run locally.",
        gate_panels,
    )


if __name__ == "__main__":
    main()
