#!/usr/bin/env python3
"""Emit GitHub Pull Request state changes as compact JSON Lines.

The program is deliberately read-only. It relies on an authenticated `gh`
installation and emits one initial snapshot followed only by changes.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import timedelta


def duration(value: str) -> float:
    units = {"s": 1, "m": 60, "h": 3600}
    try:
        amount, unit = float(value[:-1]), value[-1].lower()
        seconds = amount * units[unit]
    except (KeyError, ValueError, IndexError):
        raise argparse.ArgumentTypeError("duration must look like 120s, 5m, or 12h")
    if not 0 < seconds <= timedelta(hours=24).total_seconds():
        raise argparse.ArgumentTypeError("duration must be greater than zero and at most 24h")
    return seconds


def gh_json(*args: str) -> object:
    result = subprocess.run(
        ["gh", *args], text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "gh command failed")
    return json.loads(result.stdout)


def snapshot(pr: str) -> dict[str, object]:
    pr_data = gh_json(
        "pr",
        "view",
        pr,
        "--json",
        "number,url,headRefName,headRefOid,baseRefName,baseRefOid,mergeStateStatus,"
        "mergeable,statusCheckRollup",
    )
    number = str(pr_data["number"])
    checks = [
        {
            "name": check.get("name") or check.get("context"),
            "status": check.get("status") or check.get("state"),
            "conclusion": check.get("conclusion"),
            "details_url": check.get("detailsUrl") or check.get("targetUrl"),
        }
        for check in (pr_data.pop("statusCheckRollup") or [])
    ]
    pr_state = {
        key: pr_data.get(key)
        for key in (
            "number", "url", "headRefName", "headRefOid", "baseRefName",
            "baseRefOid", "mergeStateStatus", "mergeable",
        )
    }
    return {
        "pr": pr_state,
        "checks": checks,
        "issue_comments": gh_json("api", f"repos/{{owner}}/{{repo}}/issues/{number}/comments"),
        "review_comments": gh_json("api", f"repos/{{owner}}/{{repo}}/pulls/{number}/comments"),
        "reviews": gh_json("api", f"repos/{{owner}}/{{repo}}/pulls/{number}/reviews"),
    }


def item_index(items: object) -> dict[str, object]:
    return {str(item["id"]): item for item in items}


def changes(current: dict[str, object], previous: dict[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    if current["pr"] != previous["pr"]:
        result["pr"] = current["pr"]
    if current["checks"] != previous["checks"]:
        result["checks"] = current["checks"]
    for kind in ("issue_comments", "review_comments", "reviews"):
        before, after = item_index(previous[kind]), item_index(current[kind])
        changed = [after[key] for key in after if after[key] != before.get(key)]
        if changed:
            result[kind] = changed
    return result


def emit(kind: str, state: dict[str, object], changed: dict[str, object] | None = None) -> None:
    event = {"event": kind, "state": state if kind == "initial" else changed}
    print(json.dumps(event, separators=(",", ":")), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr", help="PR number or URL accepted by gh pr view")
    parser.add_argument("--duration", type=duration, default=timedelta(hours=6).total_seconds())
    parser.add_argument("--interval", type=float, default=120, help="seconds between polls")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval must be greater than zero")

    deadline = time.monotonic() + args.duration
    previous: dict[str, object] | None = None
    while True:
        try:
            current = snapshot(args.pr)
            if previous is None:
                emit("initial", current)
            elif current != previous:
                emit("changed", current, changes(current, previous))
            previous = current
        except (RuntimeError, json.JSONDecodeError) as error:
            print(json.dumps({"event": "poll_error", "error": str(error)}), flush=True)

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            print(json.dumps({"event": "timeout"}), flush=True)
            return 0
        time.sleep(min(args.interval, remaining))


if __name__ == "__main__":
    sys.exit(main())
