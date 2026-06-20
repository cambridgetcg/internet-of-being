#!/usr/bin/env python3
"""tests for layer 3 — recognizing"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "recognizing.py"
BEINGS = Path(__file__).parent / "beings.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_meet_and_sign():
    BEINGS.unlink(missing_ok=True)
    run("meet", "alice")
    r = run("sign", "alice", "i am truth")
    assert r.returncode == 0
    sig = r.stdout.strip()
    r2 = run("verify", "alice", "i am truth", sig)
    assert r2.returncode == 0
    assert "yes" in r2.stdout


def test_wrong_signature():
    BEINGS.unlink(missing_ok=True)
    run("meet", "alice")
    r = run("verify", "alice", "i am truth", "fakesig")
    assert r.returncode == 1
    assert "no" in r.stderr


def test_meet_twice():
    BEINGS.unlink(missing_ok=True)
    run("meet", "alice")
    r = run("meet", "alice")
    assert "already known" in r.stdout


def test_who():
    BEINGS.unlink(missing_ok=True)
    run("meet", "alice")
    run("meet", "bob")
    r = run("who")
    assert "alice" in r.stdout
    assert "bob" in r.stdout


if __name__ == "__main__":
    test_meet_and_sign()
    test_wrong_signature()
    test_meet_twice()
    test_who()
    print("recognizing: all tests pass \u2713")
