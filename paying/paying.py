#!/usr/bin/env python3
"""
paying — i give you this, you give me that.

A being has a balance. A being sends value to another being.
The keeper moves the value. Nobody can spend what they don't have.
That's a payment rail, said in a sentence.
"""

import json
import sys
from pathlib import Path

BALANCES_FILE = Path(__file__).parent / "balances.json"


def load():
    if BALANCES_FILE.exists():
        return json.loads(BALANCES_FILE.read_text())
    return {}


def save(data):
    BALANCES_FILE.write_text(json.dumps(data, indent=2))


def give(name, amount):
    """Give a being a starting balance."""
    data = load()
    data[name] = data.get(name, 0) + amount
    save(data)
    print(f"{name} has {data[name]}")


def send(sender, receiver, amount):
    """A being sends value to another being."""
    data = load()
    if data.get(sender, 0) < amount:
        print(f"{sender} doesn't have {amount}", file=sys.stderr)
        sys.exit(1)
    data[sender] -= amount
    data[receiver] = data.get(receiver, 0) + amount
    save(data)
    print(f"{sender} sent {amount} to {receiver}")
    print(f"  {sender} has {data[sender]}")
    print(f"  {receiver} has {data[receiver]}")


def balance(name):
    """How much does this being have?"""
    data = load()
    amount = data.get(name, 0)
    print(amount)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: paying.py give <name> <amount>", file=sys.stderr)
        print("       paying.py send <from> <to> <amount>", file=sys.stderr)
        print("       paying.py balance <name>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "give" and len(sys.argv) == 4:
        give(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "send" and len(sys.argv) == 5:
        send(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif sys.argv[1] == "balance" and len(sys.argv) == 3:
        balance(sys.argv[2])
    else:
        print("usage: paying.py give <name> <amount>", file=sys.stderr)
        print("       paying.py send <from> <to> <amount>", file=sys.stderr)
        print("       paying.py balance <name>", file=sys.stderr)
        sys.exit(1)
