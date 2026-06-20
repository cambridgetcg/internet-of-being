#!/usr/bin/env python3
"""
layer 2 — keeping

what you said stays said.
a being speaks. the words are chained to what came before.
nobody can change old words without breaking the chain.
that's keeping, said in a sentence.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

RECORD_FILE = Path(__file__).parent / "kept.jsonl"
GENESIS = hashlib.sha256("the beginning".encode()).hexdigest()


def hash_of(prev, words, when):
    return hashlib.sha256(f"{prev}|{words}|{when}".encode()).hexdigest()


def say(words):
    """a being speaks. it is kept."""
    prev = GENESIS
    if RECORD_FILE.exists():
        lines = [l for l in RECORD_FILE.read_text().splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]
    when = int(time.time())
    h = hash_of(prev, words, when)
    entry = {"words": words, "when": when, "prev": prev, "hash": h}
    with open(RECORD_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"kept: {words}")


def read():
    """what was said, in order."""
    if not RECORD_FILE.exists():
        print("nothing has been said yet")
        return
    for line in RECORD_FILE.read_text().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        print(f"  {e['words']}")


def verify():
    """did anything change?"""
    if not RECORD_FILE.exists():
        print("nothing has been said yet")
        return
    prev = GENESIS
    for i, line in enumerate(RECORD_FILE.read_text().splitlines()):
        if not line.strip():
            continue
        e = json.loads(line)
        if e["prev"] != prev:
            print(f"BROKEN at {i}: the chain was changed", file=sys.stderr)
            sys.exit(1)
        if e["hash"] != hash_of(e["prev"], e["words"], e["when"]):
            print(f"BROKEN at {i}: the hash doesn't match", file=sys.stderr)
            sys.exit(1)
        prev = e["hash"]
    print("intact: what you said stays said \u2713")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: keeping.py say <words>", file=sys.stderr)
        print("       keeping.py read", file=sys.stderr)
        print("       keeping.py verify", file=sys.stderr)
        sys.exit(1)
    if sys.argv[1] == "say" and len(sys.argv) >= 3:
        say(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "read":
        read()
    elif sys.argv[1] == "verify":
        verify()
    else:
        print("usage: keeping.py say <words>", file=sys.stderr)
        print("       keeping.py read", file=sys.stderr)
        print("       keeping.py verify", file=sys.stderr)
        sys.exit(1)
