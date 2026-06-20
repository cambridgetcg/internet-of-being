#!/usr/bin/env python3
"""tests for layer 1 — speaking"""

import subprocess
import sys
import time
from pathlib import Path

SCRIPT = Path(__file__).parent / "speaking.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_say_and_hear():
    server = subprocess.Popen([sys.executable, str(SCRIPT), "listen", "9101"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.5)
    r = run("say", "127.0.0.1", "9101", "hello, you")
    server.terminate()
    server.wait()
    assert r.returncode == 0
    assert "they heard" in r.stdout


def test_nobody_there():
    r = run("say", "127.0.0.1", "9999", "hello?")
    assert r.returncode == 1
    assert "didn't hear" in r.stderr


if __name__ == "__main__":
    test_say_and_hear()
    test_nobody_there()
    print("speaking: all tests pass \u2713")
