#!/usr/bin/env python3
"""tests for remembering — what happened, and when."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "remembering.py"
LOG = Path(__file__).parent / "log.jsonl"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_log_and_what():
    LOG.unlink(missing_ok=True)
    run("log", "alice arrived")
    run("log", "alice said hello")
    r = run("what")
    assert "alice arrived" in r.stdout
    assert "alice said hello" in r.stdout


def test_since():
    LOG.unlink(missing_ok=True)
    run("log", "first")
    run("log", "second")
    run("log", "third")
    r = run("what", "1")
    assert "first" not in r.stdout
    assert "second" in r.stdout
    assert "third" in r.stdout


def test_empty():
    LOG.unlink(missing_ok=True)
    r = run("what")
    assert "nothing" in r.stdout


if __name__ == "__main__":
    test_log_and_what()
    test_since()
    test_empty()
    print("remembering: all tests pass \u2713")
