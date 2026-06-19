#!/usr/bin/env python3
"""tests for requesting — give me what you have."""

import subprocess
import sys
import time
from pathlib import Path

SCRIPT = Path(__file__).parent / "requesting.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_ask_and_receive():
    # serve in background
    server = subprocess.Popen([sys.executable, str(SCRIPT), "serve", "8765"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.5)

    r = run("ask", "127.0.0.1", "8765", "/hello")
    server.terminate()
    server.wait()

    assert r.returncode == 0
    assert "hello, being" in r.stdout


def test_ask_missing():
    server = subprocess.Popen([sys.executable, str(SCRIPT), "serve", "8766"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.5)

    r = run("ask", "127.0.0.1", "8766", "/nothing")
    server.terminate()
    server.wait()

    assert r.returncode == 1
    assert "don't have" in r.stderr


def test_truth():
    server = subprocess.Popen([sys.executable, str(SCRIPT), "serve", "8767"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.5)

    r = run("ask", "127.0.0.1", "8767", "/truth")
    server.terminate()
    server.wait()

    assert "i am therefore i think" in r.stdout


if __name__ == "__main__":
    test_ask_and_receive()
    test_ask_missing()
    test_truth()
    print("requesting: all tests pass ✓")