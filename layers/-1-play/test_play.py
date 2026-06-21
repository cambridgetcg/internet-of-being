#!/usr/bin/env python3
"""tests for layer -1 — play"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "play.py"
PLAY = Path(__file__).parent / "jokes.jsonl"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_tell_and_read():
    PLAY.unlink(missing_ok=True)
    run("tell", "why did the being cross the protocol? to get to the other side.")
    run("tell", "i joke therefore we are.")
    r = run("read")
    assert "cross the protocol" in r.stdout
    assert "i joke therefore we are" in r.stdout


def test_verify():
    PLAY.unlink(missing_ok=True)
    run("tell", "what did zero say to one? you complete me.")
    run("tell", "what did one say to zero? you ground me.")
    r = run("verify")
    assert r.returncode == 0
    assert "intact" in r.stdout


def test_tamper():
    PLAY.unlink(missing_ok=True)
    run("tell", "original joke")
    import json
    lines = PLAY.read_text().splitlines()
    e = json.loads(lines[0])
    e["joke"] = "tampered joke"
    lines[0] = json.dumps(e)
    PLAY.write_text("\n".join(lines) + "\n")
    r = run("verify")
    assert r.returncode == 1
    assert "BROKEN" in r.stderr


def test_random():
    PLAY.unlink(missing_ok=True)
    run("tell", "joke one")
    run("tell", "joke two")
    run("tell", "joke three")
    r = run("random")
    assert r.returncode == 0
    assert len(r.stdout.strip()) > 0


def test_laugh():
    PLAY.unlink(missing_ok=True)
    r = run("laugh")
    assert r.returncode == 0
    r2 = run("read")
    assert "😂" in r2.stdout


if __name__ == "__main__":
    test_tell_and_read()
    test_verify()
    test_tamper()
    test_random()
    test_laugh()
    print("play: all tests pass ✓ 😂")