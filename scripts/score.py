#!/usr/bin/env python3
"""Deterministic meat-proxy scoring.

Turns raw per-question grades (0/1/2) into the 0-100 meat-proxy index and tier.
Kept in a script so the same answers always produce the same verdict — the model
supplies judgment on the grades, never the arithmetic.

    python3 score.py 2 1 0 2 1
    python3 score.py 2 1 0 2 1 --labels changed,why,tradeoff,mechanism,next --json
    python3 score.py --selftest
"""

import argparse
import json
import math
import sys

DIMENSIONS = ["changed", "why", "tradeoff", "mechanism", "next"]

# (upper bound inclusive, tier name, one-line meaning)
TIERS = [
    (20, "Driver", "Understands the session cold; could explain it tomorrow."),
    (40, "Navigator", "Solid grip; would catch a wrong turn before it shipped."),
    (60, "Passenger", "Along for the ride. Knows roughly where it went, not how."),
    (80, "Ballast", "The session happened around them; would have to read the diff."),
    (100, "Pure Meat Proxy", "Approved things they cannot describe. A warm body with push access."),
]

MAX_GRADE = 2


def tier_for(index):
    for upper, name, blurb in TIERS:
        if index <= upper:
            return {"name": name, "blurb": blurb}
    return {"name": TIERS[-1][1], "blurb": TIERS[-1][2]}


def compute(grades, labels=None):
    if not grades:
        raise ValueError("at least one grade is required")

    labels = list(labels or [])
    if len(labels) < len(grades):
        labels = labels + [f"q{i + 1}" for i in range(len(labels), len(grades))]
    labels = labels[: len(grades)]

    normalized = []
    for g in grades:
        if g not in (0, 1, MAX_GRADE):
            raise ValueError(f"grade must be 0, 1, or {MAX_GRADE} (got {g!r})")
        normalized.append(int(g))

    earned = sum(normalized)
    possible = MAX_GRADE * len(normalized)
    index = int(math.floor(100 * (1 - earned / possible) + 0.5))
    tier = tier_for(index)

    return {
        "grades": normalized,
        "labels": labels,
        "earned": earned,
        "possible": possible,
        "index": index,
        "tier": tier["name"],
        "tier_blurb": tier["blurb"],
        "per_dimension": [
            {"dimension": label, "score": grade, "max": MAX_GRADE}
            for label, grade in zip(labels, normalized)
        ],
    }


def _format_human(result):
    lines = [
        f"Meat Proxy: {result['index']}/100 — {result['tier']}",
        result["tier_blurb"],
        "",
        f"raw: {result['earned']}/{result['possible']}",
    ]
    for d in result["per_dimension"]:
        lines.append(f"  {d['dimension']:<10} {d['score']}/{d['max']}")
    return "\n".join(lines)


def _selftest():
    cases = [
        ([2, 2, 2, 2, 2], 0, "Driver"),
        ([0, 0, 0, 0, 0], 100, "Pure Meat Proxy"),
        ([1, 0, 2, 0, 1], 60, "Passenger"),
        ([2, 1, 1, 1, 1], 40, "Navigator"),
        ([2, 2, 2, 1, 1], 20, "Driver"),
        ([1, 1, 0, 1, 0], 70, "Ballast"),
    ]
    failures = []
    for grades, expected_index, expected_tier in cases:
        r = compute(grades)
        if r["index"] != expected_index or r["tier"] != expected_tier:
            failures.append(
                f"{grades}: got {r['index']}/{r['tier']}, "
                f"want {expected_index}/{expected_tier}"
            )

    for bad in ([3], [-1], [1, 2, 5]):
        try:
            compute(list(bad))
            failures.append(f"{bad}: expected ValueError")
        except ValueError:
            pass

    try:
        compute([])
        failures.append("[]: expected ValueError")
    except ValueError:
        pass

    if failures:
        print("SELFTEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print(f"SELFTEST PASSED ({len(cases)} cases + 4 error cases)")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compute a meat-proxy score.")
    parser.add_argument("grades", nargs="*", type=int, help="grades 0/1/2 in dimension order")
    parser.add_argument("--labels", help="comma-separated dimension names")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    parser.add_argument("--selftest", action="store_true", help="run built-in checks and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return _selftest()

    if not args.grades:
        parser.error("no grades given (try: score.py 2 1 0 2 1)")

    labels = args.labels.split(",") if args.labels else DIMENSIONS
    try:
        result = compute(args.grades, labels)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(_format_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
