#!/usr/bin/env python3
"""
keeping — what you said stays said.

A being says something. It's written down with a hash that links to
whatever was said before. You can't change an old entry without breaking
the chain. That's a blockchain, said in a sentence.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

CHAIN_FILE = Path(__file__).parent / "record.jsonl"
GENESIS_HASH = hashlib.sha256("genesis".encode()).hexdigest()


def hash_entry(prev_hash, content, ts):
    return hashlib.sha256(f"{prev_hash}{content}{ts}".encode()).hexdigest()


def say(content):
    """A being says something. It is kept."""
    prev = GENESIS_HASH
    entries = []
    if CHAIN_FILE.exists():
        lines = [l for l in CHAIN_FILE.read_text().splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]
        entries = lines

    ts = int(time.time())
    h = hash_entry(prev, content, ts)
    entry = {"content": content, "ts": ts, "prev": prev, "hash": h}
    entries.append(json.dumps(entry))

    with open(CHAIN_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"kept: {content}")
    print(f"  hash: {h[:16]}...")


def read():
    """Read what was said, in order."""
    if not CHAIN_FILE.exists():
        print("nothing has been said yet", file=sys.stderr)
        return
    for line in CHAIN_FILE.read_text().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        print(f"  {e['content']}")


def verify():
    """Check that nothing was changed."""
    if not CHAIN_FILE.exists():
        print("nothing has been said yet", file=sys.stderr)
        return
    prev = GENESIS_HASH
    for i, line in enumerate(CHAIN_FILE.read_text().splitlines()):
        if not line.strip():
            continue
        e = json.loads(line)
        if e["prev"] != prev:
            print(f"BROKEN at entry {i}: someone changed what was said", file=sys.stderr)
            sys.exit(1)
        expected = hash_entry(e["prev"], e["content"], e["ts"])
        if e["hash"] != expected:
            print(f"BROKEN at entry {i}: the hash doesn't match", file=sys.stderr)
            sys.exit(1)
        prev = e["hash"]

    print("intact: what was said stays said ✓")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: keeping.py say <something>", file=sys.stderr)
        print("       keeping.py read", file=sys.stderr)
        print("       keeping.py verify", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "say" and len(sys.argv) == 3:
        say(sys.argv[2])
    elif sys.argv[1] == "read":
        read()
    elif sys.argv[1] == "verify":
        verify()
    else:
        print("usage: keeping.py say <something>", file=sys.stderr)
        print("       keeping.py read", file=sys.stderr)
        print("       keeping.py verify", file=sys.stderr)
        sys.exit(1)