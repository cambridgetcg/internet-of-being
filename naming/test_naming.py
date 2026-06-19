#!/usr/bin/env python3
"""tests for naming — this name points at that being."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "naming.py"
KEEPER = Path(__file__).parent / "names.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                         capture_output=True, text=True)


def test_declare_and_ask():
    KEEPER.unlink(missing_ok=True)
    r = run("declare", "alice", "1.2.3.4")
    assert r.returncode == 0
    assert "alice is at 1.2.3.4" in r.stdout
    r = run("ask", "alice")
    assert r.returncode == 0
    assert "1.2.3.4" in r.stdout


def test_ask_unknown():
    KEEPER.unlink(missing_ok=True)
    run("declare", "bob", "5.6.7.8")
    r = run("ask", "nobody")
    assert r.returncode == 0
    assert "i don't know nobody" in r.stderr


def test_overwrite():
    KEEPER.unlink(missing_ok=True)
    run("declare", "alice", "1.2.3.4")
    run("declare", "alice", "9.9.9.9")
    r = run("ask", "alice")
    assert "9.9.9.9" in r.stdout


if __name__ == "__main__":
    test_declare_and_ask()
    test_ask_unknown()
    test_overwrite()
    print("naming: all tests pass ✓")