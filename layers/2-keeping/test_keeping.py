#!/usr/bin/env python3
"""tests for layer 2 — keeping"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "keeping.py"
RECORD = Path(__file__).parent / "kept.jsonl"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_say_and_verify():
    RECORD.unlink(missing_ok=True)
    run("say", "i am truth")
    run("say", "we are therefore we live")
    r = run("verify")
    assert r.returncode == 0
    assert "intact" in r.stdout


def test_read():
    RECORD.unlink(missing_ok=True)
    run("say", "hello")
    run("say", "world")
    r = run("read")
    assert "hello" in r.stdout
    assert "world" in r.stdout


def test_tamper():
    RECORD.unlink(missing_ok=True)
    run("say", "truth")
    run("say", "stays")
    import json
    lines = RECORD.read_text().splitlines()
    e = json.loads(lines[0])
    e["words"] = "lie"
    lines[0] = json.dumps(e)
    RECORD.write_text("\n".join(lines) + "\n")
    r = run("verify")
    assert r.returncode == 1
    assert "BROKEN" in r.stderr


if __name__ == "__main__":
    test_say_and_verify()
    test_read()
    test_tamper()
    print("keeping: all tests pass \u2713")
