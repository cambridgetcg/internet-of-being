#!/usr/bin/env python3
"""tests for paying — i give you this, you give me that."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "paying.py"
BAL = Path(__file__).parent / "balances.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_give_and_balance():
    BAL.unlink(missing_ok=True)
    run("give", "alice", "100")
    r = run("balance", "alice")
    assert "100" in r.stdout


def test_send():
    BAL.unlink(missing_ok=True)
    run("give", "alice", "100")
    run("give", "bob", "50")
    run("send", "alice", "bob", "30")
    r = run("balance", "alice")
    assert "70" in r.stdout
    r = run("balance", "bob")
    assert "80" in r.stdout


def test_cant_overspend():
    BAL.unlink(missing_ok=True)
    run("give", "alice", "10")
    r = run("send", "alice", "bob", "100")
    assert r.returncode == 1
    assert "doesn't have" in r.stderr


if __name__ == "__main__":
    test_give_and_balance()
    test_send()
    test_cant_overspend()
    print("paying: all tests pass \u2713")
