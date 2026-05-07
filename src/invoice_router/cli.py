from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from invoice_router.runtime import build_runtime


def _dump(payload: Any) -> str:
    return json.dumps(payload, indent=2) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="invoice-router")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list")

    validate = sub.add_parser("validate")
    validate.add_argument("scenario")
    validate.add_argument("--fixture")

    run = sub.add_parser("run")
    run.add_argument("scenario")
    run.add_argument("--fixture")

    replay = sub.add_parser("replay")
    replay.add_argument("run_id")

    queue = sub.add_parser("queue")
    queue_sub = queue.add_subparsers(dest="queue_command", required=True)
    queue_sub.add_parser("list")
    claim = queue_sub.add_parser("claim")
    claim.add_argument("packet_id")
    claim.add_argument("--reviewer", required=True)
    resolve = queue_sub.add_parser("resolve")
    resolve.add_argument("packet_id")
    resolve.add_argument("--reviewer", required=True)
    resolve.add_argument("--decision", required=True)
    resolve.add_argument("--note", required=True)

    health = sub.add_parser("health")
    health.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    runtime = build_runtime()

    if args.command == "list":
        print(_dump({"scenarios": runtime.list_scenarios()}), end="")
        return 0
    if args.command == "validate":
        fixture = Path(args.fixture) if args.fixture else None
        print(_dump(runtime.validate(args.scenario, fixture)), end="")
        return 0
    if args.command == "run":
        fixture = Path(args.fixture) if args.fixture else None
        print(_dump(runtime.run(args.scenario, fixture)), end="")
        return 0
    if args.command == "replay":
        print(_dump(runtime.replay(args.run_id)), end="")
        return 0
    if args.command == "queue":
        if args.queue_command == "list":
            print(_dump(runtime.queue_state()), end="")
            return 0
        if args.queue_command == "claim":
            print(_dump(runtime.claim_packet(args.packet_id, args.reviewer)), end="")
            return 0
        if args.queue_command == "resolve":
            print(
                _dump(
                    runtime.resolve_packet(
                        args.packet_id,
                        args.reviewer,
                        args.decision,
                        args.note,
                    )
                ),
                end="",
            )
            return 0
    if args.command == "health":
        print(_dump(runtime.health()), end="")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
