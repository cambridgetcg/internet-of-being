#!/usr/bin/env python3
"""tests for reconcile — did the bank get what the provider sent?"""

import subprocess
import sys
import json
from pathlib import Path

SCRIPT = Path(__file__).parent / "reconcile.py"
LEDGER = Path(__file__).parent / "ledger.jsonl"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *[str(a) for a in args]],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def setup_entries():
    """Set up test data: 4 provider + 4 bank entries."""
    LEDGER.unlink(missing_ok=True)
    run("log-provider", '{"type":"payout","amount":1250.00,"currency":"USD","date":"2024-01-15","description":"Stripe Payout","provider":"stripe","reference":"po_1"}')
    run("log-provider", '{"type":"payout","amount":450.00,"currency":"USD","date":"2024-01-14","description":"PayPal Transfer","provider":"paypal","reference":"po_2"}')
    run("log-provider", '{"type":"payout","amount":987.50,"currency":"USD","date":"2024-01-12","description":"Stripe Payout","provider":"stripe","reference":"po_3"}')
    run("log-provider", '{"type":"payout","amount":300.00,"currency":"USD","date":"2024-01-11","description":"Paddle Payout","provider":"paddle","reference":"po_4"}')
    run("log-bank", '{"type":"deposit","amount":1250.00,"currency":"USD","date":"2024-01-15","description":"Stripe Payout","reference":"bnk_1"}')
    run("log-bank", '{"type":"deposit","amount":450.20,"currency":"USD","date":"2024-01-14","description":"PayPal Transfer","reference":"bnk_2"}')
    run("log-bank", '{"type":"deposit","amount":987.50,"currency":"USD","date":"2024-01-12","description":"Stripe Payout","reference":"bnk_3"}')
    run("log-bank", '{"type":"deposit","amount":85.00,"currency":"USD","date":"2024-01-13","description":"Unknown Deposit","reference":"bnk_4"}')


def test_log_provider():
    LEDGER.unlink(missing_ok=True)
    r = run("log-provider", '{"type":"payout","amount":100.00,"currency":"USD","date":"2024-01-20","description":"Test Payout","provider":"stripe"}')
    assert r.returncode == 0
    assert "logged #1" in r.stdout
    assert "provider payout 100.0 USD" in r.stdout


def test_log_bank():
    LEDGER.unlink(missing_ok=True)
    run("log-bank", '{"type":"deposit","amount":100.00,"currency":"USD","date":"2024-01-20","description":"Test Deposit"}')
    entries = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    assert len(entries) == 1
    assert entries[0]["source"] == "bank"
    assert entries[0]["amount"] == 100.0
    assert entries[0]["currency"] == "USD"


def test_match_exact():
    """Exact amount match should produce high confidence match."""
    LEDGER.unlink(missing_ok=True)
    run("log-provider", '{"type":"payout","amount":500.00,"currency":"USD","date":"2024-01-15","description":"Stripe","provider":"stripe"}')
    run("log-bank", '{"type":"deposit","amount":500.00,"currency":"USD","date":"2024-01-15","description":"Stripe Payout"}')
    r = run("match")
    assert "Matched:           1" in r.stdout
    assert "high" in r.stdout


def test_match_discrepancy():
    """Close amount (within 0.50) should produce medium confidence + discrepancy."""
    LEDGER.unlink(missing_ok=True)
    run("log-provider", '{"type":"payout","amount":500.00,"currency":"USD","date":"2024-01-15","description":"Stripe","provider":"stripe"}')
    run("log-bank", '{"type":"deposit","amount":500.20,"currency":"USD","date":"2024-01-15","description":"Stripe Payout"}')
    r = run("match")
    assert "Discrepancies:     1" in r.stdout
    assert "medium" in r.stdout


def test_unmatched_provider():
    """Provider entry with no matching bank entry should be unmatched."""
    LEDGER.unlink(missing_ok=True)
    run("log-provider", '{"type":"payout","amount":999.00,"currency":"USD","date":"2024-01-15","description":"Ghost Payout","provider":"stripe"}')
    r = run("match")
    assert "Unmatched (prov):  1" in r.stdout


def test_unmatched_bank():
    """Bank entry with no matching provider entry should be unmatched."""
    LEDGER.unlink(missing_ok=True)
    run("log-bank", '{"type":"deposit","amount":50.00,"currency":"USD","date":"2024-01-15","description":"Mystery Deposit"}')
    r = run("match")
    assert "Unmatched (bank):  1" in r.stdout


def test_full_scenario():
    """The full 4+4 scenario from CashLoom's reconciliation page."""
    setup_entries()
    r = run("match")
    assert "Provider entries:  4" in r.stdout
    assert "Bank entries:      4" in r.stdout
    assert "Matched:" in r.stdout
    assert "Discrepancies:" in r.stdout
    assert "UNMATCHED" in r.stdout


def test_status():
    LEDGER.unlink(missing_ok=True)
    run("log-provider", '{"type":"payout","amount":100,"currency":"USD","date":"2024-01-20","description":"Test","provider":"stripe"}')
    r = run("status")
    assert "LEDGER STATUS" in r.stdout
    assert "Total entries:   1" in r.stdout


def test_export():
    LEDGER.unlink(missing_ok=True)
    run("log-provider", '{"type":"payout","amount":100,"currency":"USD","date":"2024-01-20","description":"Test","provider":"stripe"}')
    r = run("export")
    data = json.loads(r.stdout)
    assert len(data) == 1
    assert data[0]["amount"] == 100.0


def test_e2e():
    """Run the built-in e2e verification."""
    r = run("verify")
    assert r.returncode == 0
    assert "E2E VERIFICATION COMPLETE" in r.stdout
    assert "ALL PASSED" in r.stdout


def test_entry_structure():
    """Every entry has the right fields for easy logging."""
    LEDGER.unlink(missing_ok=True)
    run("log-provider", '{"type":"payout","amount":100,"currency":"USD","date":"2024-01-20","description":"Test","provider":"stripe","reference":"ref_1"}')
    entries = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    e = entries[0]
    for field in ["seq", "source", "type", "amount", "currency", "date", "description", "provider", "reference", "status", "logged_at"]:
        assert field in e, f"Missing field: {field}"


if __name__ == "__main__":
    test_log_provider()
    test_log_bank()
    test_match_exact()
    test_match_discrepancy()
    test_unmatched_provider()
    test_unmatched_bank()
    test_full_scenario()
    test_status()
    test_export()
    test_e2e()
    test_entry_structure()
    LEDGER.unlink(missing_ok=True)
    print("reconcile: all tests pass ✓")
    print()
    print("  did the bank get what the provider sent?")
    print("  yes. the answer is yes. the tool works. 😂💓")