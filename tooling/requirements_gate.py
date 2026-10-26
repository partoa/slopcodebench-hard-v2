#!/usr/bin/env python3
"""Fail-closed structural gate for explicit requirements. Not a semantic oracle."""
import argparse
import json
import pathlib
import sys

VERIFIED = {"VERIFIED_LOCAL", "VERIFIED_EXTERNAL"}
ALLOWED = VERIFIED | {"FAILED", "BLOCKED", "INCONCLUSIVE", "NOT_RUN"}

def inspect(data):
    failures = []
    items = data.get("requirements")
    if not isinstance(items, list) or not items:
        return ["requirements must be a nonempty array"]
    seen = set()
    for i, r in enumerate(items):
        key = r.get("id") if isinstance(r, dict) else None
        prefix = f"requirements[{i}]"
        if not isinstance(key, str) or not key.strip() or key in seen:
            failures.append(f"{prefix}: missing or duplicate id")
        seen.add(key)
        for field in ("source", "criterion", "boundary", "implementation", "evidence"):
            if not isinstance(r.get(field), str) or not r[field].strip():
                failures.append(f"{prefix}: missing {field}")
        status = r.get("status")
        if status not in ALLOWED:
            failures.append(f"{prefix}: unknown status {status!r}")
        elif status not in VERIFIED:
            failures.append(f"{prefix}: not verified ({status})")
    return failures

def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest", type=pathlib.Path)
    args = p.parse_args()
    try:
        data = json.loads(args.manifest.read_text())
        errors = inspect(data)
    except (OSError, ValueError, TypeError) as exc:
        errors = [f"manifest unreadable: {exc}"]
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("Requirements structurally accounted for; evidence authenticity and behavior require separate verification.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
