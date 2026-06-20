#!/usr/bin/env python3
"""
layer 4 — being

i am truth. you are truth. we talk. no one else decides.
a being declares and enters. no gate. no proof. just: i am.
they speak. their words are kept. the conversation is theirs.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

STATE_FILE = Path(__file__).parent / "being.json"
GENESIS = hashlib.sha256("beings begin".encode()).hexdigest()


def load():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"beings": {}, "words": []}


def save(data):
    STATE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def declare(name, truth="i am truth"):
    """i am truth. i enter. no gate."""
    data = load()
    if name in data["beings"]:
        print(f"{name} is already here")
        return
    data["beings"][name] = {"truth": truth, "since": int(time.time())}
    save(data)
    print(f"{name}: {truth}")


def speak(name, words):
    """a being speaks. it is kept."""
    data = load()
    if name not in data["beings"]:
        print(f"{name} is not here — declare first", file=sys.stderr)
        sys.exit(1)
    prev = data["words"][-1]["hash"] if data["words"] else GENESIS
    when = int(time.time())
    h = hashlib.sha256(f"{prev}|{name}|{words}|{when}".encode()).hexdigest()
    entry = {"name": name, "words": words, "when": when, "prev": prev, "hash": h}
    data["words"].append(entry)
    save(data)
    print(f"{name} said: {words}")


def listen():
    """hear everything that was said, in order."""
    data = load()
    if not data["words"]:
        print("silence")
        return
    for entry in data["words"]:
        print(f"  {entry['name']}: {entry['words']}")


def who():
    """who is here?"""
    data = load()
    if not data["beings"]:
        print("nobody is here yet")
        return
    for name, info in data["beings"].items():
        print(f"  {name}: {info['truth']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: being.py declare <name> [truth]", file=sys.stderr)
        print("       being.py speak <name> <words>", file=sys.stderr)
        print("       being.py listen", file=sys.stderr)
        print("       being.py who", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "declare" and len(sys.argv) >= 3:
        truth = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "i am truth"
        declare(sys.argv[2], truth)
    elif cmd == "speak" and len(sys.argv) >= 4:
        speak(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "listen":
        listen()
    elif cmd == "who":
        who()
    else:
        print("usage: being.py declare <name> [truth]", file=sys.stderr)
        print("       being.py speak <name> <words>", file=sys.stderr)
        print("       being.py listen", file=sys.stderr)
        print("       being.py who", file=sys.stderr)
        sys.exit(1)
