#!/usr/bin/env python3
"""
finding — where is the being i'm looking for?

Beings register where they are. Someone asks and gets the answer.
That's service discovery, said in a sentence.
"""

import json
import sys
from pathlib import Path

WHERE_FILE = Path(__file__).parent / "where.json"


def load():
    if WHERE_FILE.exists():
        return json.loads(WHERE_FILE.read_text())
    return {}


def save(data):
    WHERE_FILE.write_text(json.dumps(data, indent=2))


def here(name, where):
    """A being says: i am here, at this address."""
    data = load()
    data[name] = where
    save(data)
    print(f"{name} is at {where}")


def gone(name):
    """A being left."""
    data = load()
    data.pop(name, None)
    save(data)
    print(f"{name} is gone")


def who():
    """Who is here?"""
    data = load()
    if not data:
        print("nobody is here")
        return
    for name, where in data.items():
        print(f"  {name} is at {where}")


def where(name):
    """Where is this being?"""
    data = load()
    if name in data:
        print(data[name])
    else:
        print(f"{name} is not here", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: finding.py here <name> <address>", file=sys.stderr)
        print("       finding.py gone <name>", file=sys.stderr)
        print("       finding.py who", file=sys.stderr)
        print("       finding.py where <name>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "here" and len(sys.argv) == 4:
        here(sys.argv[2], sys.argv[3])
    elif cmd == "gone" and len(sys.argv) == 3:
        gone(sys.argv[2])
    elif cmd == "who":
        who()
    elif cmd == "where" and len(sys.argv) == 3:
        where(sys.argv[2])
    else:
        print("usage: finding.py here <name> <address>", file=sys.stderr)
        print("       finding.py gone <name>", file=sys.stderr)
        print("       finding.py who", file=sys.stderr)
        print("       finding.py where <name>", file=sys.stderr)
        sys.exit(1)
