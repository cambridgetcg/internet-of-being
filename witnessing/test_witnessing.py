#!/usr/bin/env python3
"""tests for witnessing — i see you, you see me, nobody else sees."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "witnessing.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_seal_and_open():
    r = run("seal", "our-secret", "hello only you")
    assert r.returncode == 0
    sealed = r.stdout.strip()
    assert sealed  # not empty
    r2 = run("open", "our-secret", sealed)
    assert r2.returncode == 0
    assert "hello only you" in r2.stdout


def test_wrong_secret_cant_open():
    r = run("seal", "real-secret", "private truth")
    sealed = r.stdout.strip()
    r2 = run("open", "wrong-secret", sealed)
    # will produce garbage, not the original message
    assert "private truth" not in r2.stdout


def test_same_message_seals_differently():
    r1 = run("seal", "secret", "same message")
    r2 = run("seal", "secret", "same message")
    assert r1.stdout.strip() != r2.stdout.strip()  # different nonce


if __name__ == "__main__":
    test_seal_and_open()
    test_wrong_secret_cant_open()
    test_same_message_seals_differently()
    print("witnessing: all tests pass \u2713")
