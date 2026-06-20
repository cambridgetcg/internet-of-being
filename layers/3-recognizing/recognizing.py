#!/usr/bin/env python3
"""
layer 3 — recognizing

i know you. you know me.
a being has a key. they sign their words. anyone can verify.
no certificate authority. no gatekeeper. just recognition.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

BEINGS_FILE = Path(__file__).parent / "beings.json"


def load():
    if BEINGS_FILE.exists():
        return json.loads(BEINGS_FILE.read_text())
    return {}


def save(data):
    BEINGS_FILE.write_text(json.dumps(data, indent=2))


def _make_key():
    """make a simple key pair (not real crypto — a being's signature)."""
    secret = os.urandom(32).hex()
    public = hashlib.sha256(secret.encode()).hexdigest()
    return secret, public


def _sign(secret, message):
    """sign a message with a secret."""
    return hashlib.sha256((secret + message).encode()).hexdigest()


def _verify(public, message, signature, beings_data):
    """verify a signature against a known being's public key."""
    for name, info in beings_data.items():
        if info["public"] == public:
            expected = hashlib.sha256((info["secret"] + message).encode()).hexdigest()
            return expected == signature
    return False


def meet(name):
    """a being arrives. we know them now."""
    data = load()
    if name in data:
        print(f"{name} is already known")
        return
    secret, public = _make_key()
    data[name] = {"secret": secret, "public": public}
    save(data)
    print(f"{name}: i know you now. your key: {public[:16]}...")


def sign(name, message):
    """a being signs their words."""
    data = load()
    if name not in data:
        print(f"i don't know {name}", file=sys.stderr)
        sys.exit(1)
    sig = _sign(data[name]["secret"], message)
    print(sig)


def verify(name, message, signature):
    """anyone can verify a being's signature."""
    data = load()
    if name not in data:
        print(f"i don't know {name}", file=sys.stderr)
        sys.exit(1)
    if _verify(data[name]["public"], message, signature, data):
        print(f"yes — {name} said that")
    else:
        print(f"no — {name} did not say that", file=sys.stderr)
        sys.exit(1)


def who():
    """who do we know?"""
    data = load()
    if not data:
        print("we don't know anyone yet")
        return
    for name, info in data.items():
        print(f"  {name} — key: {info['public'][:16]}...")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: recognizing.py meet <name>", file=sys.stderr)
        print("       recognizing.py sign <name> <words>", file=sys.stderr)
        print("       recognizing.py verify <name> <words> <signature>", file=sys.stderr)
        print("       recognizing.py who", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "meet" and len(sys.argv) == 3:
        meet(sys.argv[2])
    elif cmd == "sign" and len(sys.argv) >= 4:
        sign(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "verify" and len(sys.argv) >= 5:
        verify(sys.argv[2], " ".join(sys.argv[3:-1]), sys.argv[-1])
    elif cmd == "who":
        who()
    else:
        print("usage: recognizing.py meet <name>", file=sys.stderr)
        print("       recognizing.py sign <name> <words>", file=sys.stderr)
        print("       recognizing.py verify <name> <words> <signature>", file=sys.stderr)
        print("       recognizing.py who", file=sys.stderr)
        sys.exit(1)
