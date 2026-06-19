#!/usr/bin/env python3
"""tests for finding — where is the being i'm looking for?"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "finding.py"
WHERE = Path(__file__).parent / "where.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_here_and_where():
    WHERE.unlink(missing_ok=True)
    run("here", "alice", "1.2.3.4")
    r = run("where", "alice")
    assert "1.2.3.4" in r.stdout


def test_who():
    WHERE.unlink(missing_ok=True)
    run("here", "alice", "1.2.3.4")
    run("here", "bob", "5.6.7.8")
    r = run("who")
    assert "alice" in r.stdout
    assert "bob" in r.stdout


def test_gone():
    WHERE.unlink(missing_ok=True)
    run("here", "alice", "1.2.3.4")
    run("gone", "alice")
    r = run("where", "alice")
    assert r.returncode == 1
    assert "not here" in r.stderr


def test_where_missing():
    WHERE.unlink(missing_ok=True)
    r = run("where", "nobody")
    assert r.returncode == 1
    assert "not here" in r.stderr


if __name__ == "__main__":
    test_here_and_where()
    test_who()
    test_gone()
    test_where_missing()
    print("finding: all tests pass \u2713")
