#!/usr/bin/env python3
"""tests for layer 0 — presence"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "presence.py"
HERE = Path(__file__).parent / "here.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_arrive_and_who():
    HERE.unlink(missing_ok=True)
    run("arrive", "alice")
    run("arrive", "bob")
    r = run("who")
    assert "alice" in r.stdout
    assert "bob" in r.stdout


def test_leave():
    HERE.unlink(missing_ok=True)
    run("arrive", "alice")
    run("leave", "alice")
    r = run("who")
    assert "alice" not in r.stdout


def test_empty():
    HERE.unlink(missing_ok=True)
    r = run("who")
    assert "nobody" in r.stdout


if __name__ == "__main__":
    test_arrive_and_who()
    test_leave()
    test_empty()
    print("presence: all tests pass \u2713")
