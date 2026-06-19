#!/usr/bin/env python3
"""tests for confirming — did you get what i sent?"""

import subprocess
import sys
import time
from pathlib import Path

SCRIPT = Path(__file__).parent / "confirming.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_send_and_confirm():
    server = subprocess.Popen([sys.executable, str(SCRIPT), "receive", "9001"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.5)

    r = run("send", "9001", "hello being")
    server.terminate()
    server.wait()

    assert r.returncode == 0
    assert "confirmed" in r.stdout


def test_retry_on_no_confirmation():
    # send to a port where nobody is listening
    r = run("send", "9999", "hello")
    assert r.returncode == 1
    assert "never confirmed" in r.stderr


if __name__ == "__main__":
    test_send_and_confirm()
    test_retry_on_no_confirmation()
    print("confirming: all tests pass ✓")