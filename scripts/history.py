#!/usr/bin/env python3
"""Meat-proxy history: append results and show the trend.

A single score is a mood; the trend is a habit. Results are appended as JSONL to
~/.meat-proxy/history.jsonl (override with --file or MEAT_PROXY_HOME).

    python3 history.py append --index 60 --tier Passenger --session "cache cleanup"
    python3 history.py trend
    python3 history.py trend --json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_FILE = os.path.join(
    os.environ.get("MEAT_PROXY_HOME", os.path.expanduser("~/.meat-proxy")),
    "history.jsonl",
)


def _path(args):
    return args.file or DEFAULT_FILE


def _read(path):
    if not os.path.exists(path):
        return []
    records = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _append(args):
    path = _path(args)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "index": args.index,
        "tier": args.tier,
        "session": args.session or "",
    }
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    print(f"logged {args.index}/100 ({args.tier}) -> {path}")
    return 0


def _trend(args):
    records = _read(_path(args))
    if not records:
        print("No meat-proxy history yet. Run a session quiz first.")
        return 0

    indexes = [r["index"] for r in records]
    count = len(indexes)
    avg = sum(indexes) / count
    best = min(indexes)
    worst = max(indexes)
    rolling = indexes[-5:]
    rolling_avg = sum(rolling) / len(rolling)

    if count < 2:
        direction = "baseline"
    else:
        delta = rolling_avg - avg
        if delta <= -3:
            direction = "improving"
        elif delta >= 3:
            direction = "slipping"
        else:
            direction = "steady"

    recent = records[-5:]
    summary = {
        "sessions": count,
        "average": round(avg, 1),
        "best": best,
        "worst": worst,
        "rolling_average": round(rolling_avg, 1),
        "direction": direction,
        "recent": [
            {"session": r.get("session", ""), "index": r["index"], "tier": r.get("tier", "")}
            for r in recent
        ],
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    print(
        f"{count} sessions · avg {summary['average']} · "
        f"best {best} · worst {worst} · last 5 avg {summary['rolling_average']} "
        f"({direction})"
    )
    for r in recent:
        label = f" — {r['session']}" if r.get("session") else ""
        print(f"  {r['index']:>3}/100  {r.get('tier', ''):<16}{label}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Meat-proxy history and trend.")
    parser.add_argument("--file", help="history file (default ~/.meat-proxy/history.jsonl)")
    sub = parser.add_subparsers(dest="action", required=True)

    p_append = sub.add_parser("append", help="record a result")
    p_append.add_argument("--index", type=int, required=True)
    p_append.add_argument("--tier", required=True)
    p_append.add_argument("--session", default="")
    p_append.set_defaults(func=_append)

    p_trend = sub.add_parser("trend", help="show the trend")
    p_trend.add_argument("--json", action="store_true")
    p_trend.set_defaults(func=_trend)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
