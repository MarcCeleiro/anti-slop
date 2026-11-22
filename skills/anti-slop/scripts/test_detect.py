#!/usr/bin/env python3
"""Regression test for detect.py against evals/detect-fixtures.

positive/*: every rule listed in the file's `expect:` line must fire.
negative/*: no finding at medium severity or above may fire.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "..", "evals", "detect-fixtures")
DETECT = os.path.join(HERE, "detect.py")


def run(path, *extra):
    out = subprocess.run([sys.executable, "-I", DETECT, "--json", "--fail-on", "none", *extra, path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["findings"]


def main():
    failures = 0
    for name in sorted(os.listdir(os.path.join(FIX, "positive"))):
        p = os.path.join(FIX, "positive", name)
        with open(p, encoding="utf-8") as f:
            m = re.search(r"expect:(.*)", f.readline())
        expected = set(re.findall(r"[A-Z]{1,2}-\d{2}", m.group(1))) if m else set()
        got = {f["rule"] for f in run(p)}
        missing = expected - got
        status = "ok " if not missing else "FAIL"
        failures += bool(missing)
        print(f"{status} positive/{name}: {len(expected & got)}/{len(expected)} expected rules"
              + (f", missing {sorted(missing)}" if missing else "") + (f", extra {sorted(got - expected)}" if got - expected else ""))
    for name in sorted(os.listdir(os.path.join(FIX, "negative"))):
        p = os.path.join(FIX, "negative", name)
        bad = run(p, "--min-severity", "medium")
        status = "ok " if not bad else "FAIL"
        failures += bool(bad)
        print(f"{status} negative/{name}: {len(bad)} findings at medium or above")
        for f in bad:
            print(f"      {f['rule']} line {f['line']}: {f['message']} | {f['excerpt']}")
    print(f"\n{'all passed' if not failures else f'{failures} fixture(s) failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
