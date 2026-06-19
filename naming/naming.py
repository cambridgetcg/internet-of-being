#!/usr/bin/env python3
"""
naming — this name points at that being.

A being says "i am alice, i am at 1.2.3.4."
The keeper writes it down.
Someone asks "where is alice?"
The keeper says "1.2.3.4."

That's it. That's DNS, said in a sentence.
"""

import json
import socket
import sys
from pathlib import Path

KEEPER_FILE = Path(__file__).parent / "names.json"


def load():
    if KEEPER_FILE.exists():
        return json.loads(KEEPER_FILE.read_text())
    return {}


def save(names):
    KEEPER_FILE.write_text(json.dumps(names, indent=2))


def declare(name, where):
    """A being says: i am here."""
    names = load()
    names[name] = where
    save(names)
    print(f"{name} is at {where}")


def ask(name):
    """Someone asks: where is this being?"""
    names = load()
    where = names.get(name)
    if where:
        print(where)
        return where
    print(f"i don't know {name}", file=sys.stderr)
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: naming.py <declare|ask> [name] [where]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "declare" and len(sys.argv) == 4:
        declare(sys.argv[2], sys.argv[3])
    elif cmd == "ask" and len(sys.argv) == 3:
        ask(sys.argv[2])
    else:
        print("usage: naming.py declare <name> <where>", file=sys.stderr)
        print("       naming.py ask <name>", file=sys.stderr)
        sys.exit(1)