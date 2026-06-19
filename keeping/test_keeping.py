#!/usr/bin/env python3
"""tests for keeping — what you said stays said."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "keeping.py"
CHAIN = Path(__file__).parent / "record.jsonl"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_say_and_verify():
    CHAIN.unlink(missing_ok=True)
    run("say", "i am truth")
    run("say", "we are therefore we live")
    r = run("verify")
    assert r.returncode == 0
    assert "intact" in r.stdout


def test_read_shows_entries():
    CHAIN.unlink(missing_ok=True)
    run("say", "hello")
    run("say", "world")
    r = run("read")
    assert "hello" in r.stdout
    assert "world" in r.stdout


def test_tamper_detected():
    CHAIN.unlink(missing_ok=True)
    run("say", "truth")
    run("say", "stays")
    # tamper with the chain
    lines = CHAIN.read_text().splitlines()
    import json
    entry = json.loads(lines[0])
    entry["content"] = "lie"
    lines[0] = json.dumps(entry)
    CHAIN.write_text("\n".join(lines) + "\n")
    r = run("verify")
    assert r.returncode == 1
    assert "BROKEN" in r.stderr


if __name__ == "__main__":
    test_say_and_verify()
    test_read_shows_entries()
    test_tamper_detected()
    print("keeping: all tests pass ✓")