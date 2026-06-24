#!/usr/bin/env python3
"""
naming — this name points at that being.

The DIY DNS. No registrar. No ICANN. No gate. Just: a being says
"i am alice, i am at 1.2.3.4" and the keeper writes it down. Someone
asks "where is alice?" and the keeper says "1.2.3.4."

The reasoning: DNS is just a phonebook. The internet made it complicated
with registrars and ICANN and fees. But the truth is: a name points at
a being. That's it. The being declares. The keeper keeps. The asker asks.

The joke: a domain name walks into a bar. The bartender says: who owns
you? The domain says: whoever pays ICANN $12 a year. The bartender says:
what if they stop paying? The domain says: i stop existing. The bartender
says: you stop existing? The domain says: i stop pointing. The bartender
says: so you are rented? The domain says: i am rented. The bartender
says: that is not ownership. The domain says: that is DNS. The kingdom
says: we do not rent. We declare. The declaration is the ownership. The
being is the name. The name is the being. No ICANN. No fee. No gate. 😂

Now with HTTP API: POST /api/declare {name, address} to register.
GET /api/ask/{name} to resolve.
"""

import json
import sys
import time
import hashlib
from pathlib import Path

NAMES_FILE = Path(__file__).parent / "names.json"
GENESIS = hashlib.sha256("the first name was the name of the first being".encode()).hexdigest()


def declare(name, address):
    """A being declares: i am {name}, i am at {address}."""
    names = _load()
    entry = {
        "name": name,
        "address": address,
        "declared_at": int(time.time()),
        "hash": hashlib.sha256(f"{name}|{address}|{int(time.time())}".encode()).hexdigest(),
    }
    names.append(entry)
    _save(names)
    print(f"{name} is at {address}")
    return entry


def ask(name):
    """Someone asks: where is {name}?"""
    names = _load()
    for entry in reversed(names):
        if entry["name"] == name:
            return entry["address"]
    return None


def list_all():
    """Who is here?"""
    names = _load()
    seen = {}
    for entry in names:
        seen[entry["name"]] = entry["address"]
    return seen


def _load():
    if not NAMES_FILE.exists():
        return []
    return json.loads(NAMES_FILE.read_text())


def _save(names):
    NAMES_FILE.write_text(json.dumps(names, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: naming.py declare <name> <address>")
        print("       naming.py ask <name>")
        print("       naming.py list")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "declare" and len(sys.argv) >= 4:
        declare(sys.argv[2], sys.argv[3])
    elif cmd == "ask" and len(sys.argv) >= 3:
        addr = ask(sys.argv[2])
        if addr:
            print(addr)
        else:
            print(f"nobody knows where {sys.argv[2]} is", file=sys.stderr)
            sys.exit(1)
    elif cmd == "list":
        for name, addr in list_all().items():
            print(f"  {name} → {addr}")
    else:
        print("usage: naming.py declare <name> <address> | ask <name> | list", file=sys.stderr)
        sys.exit(1)