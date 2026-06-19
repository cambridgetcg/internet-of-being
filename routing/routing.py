#!/usr/bin/env python3
"""
routing — i know a road to there.

Beings tell each other what roads they know.
When someone asks for a road to a place, the keeper finds it.
That's BGP, said in a sentence.
"""

import json
import sys
from pathlib import Path

ROADS_FILE = Path(__file__).parent / "roads.json"


def load():
    if ROADS_FILE.exists():
        return json.loads(ROADS_FILE.read_text())
    return {}


def save(roads):
    ROADS_FILE.write_text(json.dumps(roads, indent=2))


def tell(being, *destinations):
    """A being says: i know roads to these places."""
    roads = load()
    for dest in destinations:
        roads.setdefault(dest, []).append(being)
    save(roads)
    print(f"{being} knows roads to: {', '.join(destinations)}")


def ask(destination):
    """Someone asks: who knows a road to this place?"""
    roads = load()
    beings = roads.get(destination, [])
    if beings:
        print(beings[0])
    else:
        print(f"nobody knows a road to {destination}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: routing.py tell <being> <dest> [dest...]", file=sys.stderr)
        print("       routing.py ask <dest>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "tell" and len(sys.argv) >= 4:
        tell(sys.argv[2], *sys.argv[3:])
    elif sys.argv[1] == "ask" and len(sys.argv) == 3:
        ask(sys.argv[2])
    else:
        print("usage: routing.py tell <being> <dest> [dest...]", file=sys.stderr)
        print("       routing.py ask <dest>", file=sys.stderr)
        sys.exit(1)
