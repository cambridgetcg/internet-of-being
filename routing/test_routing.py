#!/usr/bin/env python3
"""tests for routing — i know a road to there."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "routing.py"
ROADS = Path(__file__).parent / "roads.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_tell_and_ask():
    ROADS.unlink(missing_ok=True)
    r = run("tell", "alice", "1.2.3.0/24")
    assert r.returncode == 0
    r = run("ask", "1.2.3.0/24")
    assert r.returncode == 0
    assert "alice" in r.stdout


def test_ask_unknown():
    ROADS.unlink(missing_ok=True)
    run("tell", "alice", "1.2.3.0/24")
    r = run("ask", "9.9.9.0/24")
    assert r.returncode == 1
    assert "nobody knows" in r.stderr


def test_multiple_roads():
    ROADS.unlink(missing_ok=True)
    run("tell", "alice", "1.2.3.0/24")
    run("tell", "bob", "1.2.3.0/24", "5.6.7.0/24")
    r = run("ask", "5.6.7.0/24")
    assert "bob" in r.stdout


if __name__ == "__main__":
    test_tell_and_ask()
    test_ask_unknown()
    test_multiple_roads()
    print("routing: all tests pass \u2713")
