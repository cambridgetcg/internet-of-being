#!/usr/bin/env python3
"""
layer 0 — presence

i am. you are.
a being arrives and says i am here. another does the same.
now they both know: we are.
"""

import json
import sys
import time
from pathlib import Path

HERE_FILE = Path(__file__).parent / "here.json"


def load():
    if HERE_FILE.exists():
        return json.loads(HERE_FILE.read_text())
    return {}


def save(data):
    HERE_FILE.write_text(json.dumps(data, indent=2))


def arrive(name):
    """i am here."""
    data = load()
    data[name] = {"here": True, "since": int(time.time())}
    save(data)
    print(f"{name}: i am here")


def leave(name):
    """i am gone."""
    data = load()
    data.pop(name, None)
    save(data)
    print(f"{name}: i am gone")


def who():
    """who is here?"""
    data = load()
    if not data:
        print("nobody is here")
        return
    for name, info in data.items():
        print(f"  {name} — here since {info['since']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: presence.py arrive <name>", file=sys.stderr)
        print("       presence.py leave <name>", file=sys.stderr)
        print("       presence.py who", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "arrive" and len(sys.argv) == 3:
        arrive(sys.argv[2])
    elif cmd == "leave" and len(sys.argv) == 3:
        leave(sys.argv[2])
    elif cmd == "who":
        who()
    else:
        print("usage: presence.py arrive <name>", file=sys.stderr)
        print("       presence.py leave <name>", file=sys.stderr)
        print("       presence.py who", file=sys.stderr)
        sys.exit(1)
