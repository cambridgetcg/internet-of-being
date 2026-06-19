#!/usr/bin/env python3
"""
trusting — who vouches for you?

A being vouches for another. When someone asks "is this being real?"
the keeper follows the chain of vouching from someone you trust to them.
That's PKI, said in a sentence.
"""

import json
import sys
from pathlib import Path

VOUCHES_FILE = Path(__file__).parent / "vouches.json"


def load():
    if VOUCHES_FILE.exists():
        return json.loads(VOUCHES_FILE.read_text())
    return {}


def save(data):
    VOUCHES_FILE.write_text(json.dumps(data, indent=2))


def vouch(voucher, vouched_for):
    """A being says: i vouch for this being."""
    data = load()
    data.setdefault(vouched_for, []).append(voucher)
    save(data)
    print(f"{voucher} vouches for {vouched_for}")


def check(being, trusted_root):
    """Does trust from the root reach this being? Follow the chain."""
    data = load()
    visited = set()

    def follows_chain(target):
        if target == trusted_root:
            return True
        if target in visited:
            return False
        visited.add(target)
        for voucher in data.get(target, []):
            if follows_chain(voucher):
                return True
        return False

    if follows_chain(being):
        print(f"yes, {trusted_root}'s trust reaches {being}")
    else:
        print(f"no, nobody {trusted_root} trusts vouches for {being}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: trusting.py vouch <voucher> <vouched_for>", file=sys.stderr)
        print("       trusting.py check <being> <trusted_root>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "vouch" and len(sys.argv) == 4:
        vouch(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "check" and len(sys.argv) == 4:
        check(sys.argv[2], sys.argv[3])
    else:
        print("usage: trusting.py vouch <voucher> <vouched_for>", file=sys.stderr)
        print("       trusting.py check <being> <trusted_root>", file=sys.stderr)
        sys.exit(1)
