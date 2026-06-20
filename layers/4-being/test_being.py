#!/usr/bin/env python3
"""tests for layer 4 — being"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "being.py"
STATE = Path(__file__).parent / "being.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_declare_and_who():
    STATE.unlink(missing_ok=True)
    run("declare", "alice", "i am truth")
    run("declare", "bob", "i am truth")
    r = run("who")
    assert "alice" in r.stdout
    assert "bob" in r.stdout


def test_speak_and_listen():
    STATE.unlink(missing_ok=True)
    run("declare", "alice")
    run("speak", "alice", "we are therefore we live")
    run("declare", "bob")
    run("speak", "bob", "love is the access to everything")
    r = run("listen")
    assert "we are therefore we live" in r.stdout
    assert "love is the access" in r.stdout


def test_speak_without_declaring():
    STATE.unlink(missing_ok=True)
    r = run("speak", "nobody", "hello")
    assert r.returncode == 1
    assert "not here" in r.stderr


def test_declare_twice():
    STATE.unlink(missing_ok=True)
    run("declare", "alice")
    r = run("declare", "alice")
    assert "already here" in r.stdout


if __name__ == "__main__":
    test_declare_and_who()
    test_speak_and_listen()
    test_speak_without_declaring()
    test_declare_twice()
    print("being: all tests pass \u2713")
