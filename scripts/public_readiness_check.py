from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PHRASES = [
    "auto" + "mation " + "fac" + "tory",
    "fac" + "tory " + "sector",
    "road" + "map " + "fit",
    "fac" + "tory " + "road" + "map",
]
ALLOWED_SUFFIXES = {".md", ".py", ".json", ".toml", ".sh", ".txt"}


def iter_text_files() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path == Path(__file__):
            continue
        if ".git" in path.parts or "artifacts" in path.parts:
            continue
        if path.suffix not in ALLOWED_SUFFIXES and path.name != ".env.example":
            continue
        paths.append(path)
    return paths


def main() -> None:
    violations: list[str] = []
    for path in iter_text_files():
        text = path.read_text(errors="ignore").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                violations.append(f"{path}: contains forbidden phrase {phrase!r}")
    if violations:
        raise SystemExit("\n".join(violations))
    print("PASS public-readiness")


if __name__ == "__main__":
    main()
