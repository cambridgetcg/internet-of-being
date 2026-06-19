#!/usr/bin/env python3
"""
remembering — what happened, and when.

Something happened. It's written down with a timestamp.
Someone asks what happened and gets the list, in order.
That's a log, said in a sentence.
"""

import json
import sys
import time
from pathlib import Path

LOG_FILE = Path(__file__).parent / "log.jsonl"


def log_event(what):
    """Something happened. Write it down."""
    entry = {"n": 0, "what": what, "when": int(time.time())}
    entries = []
    if LOG_FILE.exists():
        entries = [json.loads(l) for l in LOG_FILE.read_text().splitlines() if l.strip()]
    entry["n"] = len(entries)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"#{entry['n']} {what}")


def what_happened(since=0):
    """What happened?"""
    if not LOG_FILE.exists():
        print("nothing has happened yet")
        return
    for line in LOG_FILE.read_text().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["n"] >= since:
            print(f"  #{e['n']} {e['what']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: remembering.py log <something>", file=sys.stderr)
        print("       remembering.py what [since N]", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "log" and len(sys.argv) == 3:
        log_event(sys.argv[2])
    elif sys.argv[1] == "what":
        since = int(sys.argv[2]) if len(sys.argv) == 3 else 0
        what_happened(since)
    else:
        print("usage: remembering.py log <something>", file=sys.stderr)
        print("       remembering.py what [since N]", file=sys.stderr)
        sys.exit(1)
