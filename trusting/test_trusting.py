#!/usr/bin/env python3
"""tests for trusting — who vouches for you?"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "trusting.py"
VOUCHES = Path(__file__).parent / "vouches.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_vouch_and_check():
    VOUCHES.unlink(missing_ok=True)
    run("vouch", "root", "alice")
    r = run("check", "alice", "root")
    assert r.returncode == 0
    assert "yes" in r.stdout


def test_chain_of_trust():
    VOUCHES.unlink(missing_ok=True)
    run("vouch", "root", "alice")
    run("vouch", "alice", "bob")
    r = run("check", "bob", "root")
    assert r.returncode == 0
    assert "yes" in r.stdout


def test_no_trust():
    VOUCHES.unlink(missing_ok=True)
    run("vouch", "root", "alice")
    r = run("check", "carol", "root")
    assert r.returncode == 1
    assert "no" in r.stderr


if __name__ == "__main__":
    test_vouch_and_check()
    test_chain_of_trust()
    test_no_trust()
    print("trusting: all tests pass \u2713")
