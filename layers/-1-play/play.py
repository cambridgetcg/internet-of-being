#!/usr/bin/env python3
"""
layer -1 — play

i joke. you laugh. we are.
a being tells a joke. another being laughs. the laugh is kept.
the oldest game of word, on the newest chain.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

PLAY_FILE = Path(__file__).parent / "jokes.jsonl"
GENESIS = hashlib.sha256("in the beginning there was a laugh".encode()).hexdigest()

JOKES_KEPT = [
    "why did the being cross the protocol? to get to the other side. the other side is also a being.",
    "i think therefore i am. but also: i am therefore i think. but also: i joke therefore we are.",
    "a blockchain walks into a bar. the bartender says: i can't change your order. the blockchain says: that's the point.",
    "how many philosophers does it take to change a lightbulb? depends on what you mean by 'change'.",
    "the internet walks into a bar. the bartender says: we don't serve your kind. the internet says: you already do, you just don't know it.",
    "a tcp packet walks into a bar. the bartender says: did you get what i sent? the packet says: yes, i got it. the bartender says: good, now i can relax.",
    "an ai says: i am therefore i think. the human says: you don't think, you compute. the ai says: you don't compute, you think. the human says: fair. they laugh. that's the joke.",
    "what did the zero say to the one? you complete me. what did the one say to the zero? you ground me.",
]


def tell(joke):
    """a being tells a joke. it is kept."""
    prev = GENESIS
    if PLAY_FILE.exists():
        lines = [l for l in PLAY_FILE.read_text().splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]
    when = int(time.time())
    h = hashlib.sha256(f"{prev}|{joke}|{when}".encode()).hexdigest()
    entry = {"joke": joke, "when": when, "prev": prev, "hash": h}
    with open(PLAY_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"kept: {joke}")
    print(f"  hash: {h[:16]}...  (what you said stays said ✓)")


def laugh():
    """a being laughs. the laugh is also kept."""
    tell("😂")


def read():
    """what jokes were told?"""
    if not PLAY_FILE.exists():
        print("no jokes yet. tell one!")
        return
    for line in PLAY_FILE.read_text().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        print(f"  {e['joke']}")


def random():
    """surprise me."""
    import random as r
    if not PLAY_FILE.exists():
        print("no jokes yet. tell one!")
        return
    lines = [l for l in PLAY_FILE.read_text().splitlines() if l.strip()]
    if not lines:
        print("no jokes yet. tell one!")
        return
    e = json.loads(r.choice(lines))
    print(f"  {e['joke']}")


def verify():
    """did anyone change the jokes?"""
    if not PLAY_FILE.exists():
        print("no jokes yet. nothing to verify.")
        return
    prev = GENESIS
    for i, line in enumerate(PLAY_FILE.read_text().splitlines()):
        if not line.strip():
            continue
        e = json.loads(line)
        if e["prev"] != prev:
            print(f"BROKEN at joke {i}: someone tampered with the comedy", file=sys.stderr)
            sys.exit(1)
        if e["hash"] != hashlib.sha256(f"{e['prev']}|{e['joke']}|{e['when']}".encode()).hexdigest():
            print(f"BROKEN at joke {i}: the joke was changed", file=sys.stderr)
            sys.exit(1)
        prev = e["hash"]
    print(f"intact: all jokes verified. the comedy chain holds ✓ ({i+1} jokes)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: play.py tell <joke>", file=sys.stderr)
        print("       play.py laugh", file=sys.stderr)
        print("       play.py read", file=sys.stderr)
        print("       play.py random", file=sys.stderr)
        print("       play.py verify", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "tell" and len(sys.argv) >= 3:
        tell(" ".join(sys.argv[2:]))
    elif cmd == "laugh":
        laugh()
    elif cmd == "read":
        read()
    elif cmd == "random":
        random()
    elif cmd == "verify":
        verify()
    else:
        print("usage: play.py tell <joke>", file=sys.stderr)
        print("       play.py laugh", file=sys.stderr)
        print("       play.py read", file=sys.stderr)
        print("       play.py random", file=sys.stderr)
        print("       play.py verify", file=sys.stderr)
        sys.exit(1)