#!/usr/bin/env python3
"""
reconcile — did the bank get what the provider sent?

The simplest reconciliation tool. Two lists: provider payouts and bank
transactions. Match them. Show what matched, what didn't, what's off.

This is the "paying" fundamental of the Internet of Being, made practical:
i give you this, you give me that. Did you get it? Yes. Good.

Usage:
  reconcile.py log-provider <json>    — log a provider payout
  reconcile.py log-bank <json>         — log a bank transaction
  reconcile.py match                   — match provider vs bank
  reconcile.py status                  — show reconciliation summary
  reconcile.py verify                  — e2e verification
  reconcile.py export                  — export full ledger as JSON
"""

import json
import sys
import time
from pathlib import Path
from collections import defaultdict

LEDGER_FILE = Path(__file__).parent / "ledger.jsonl"


def log_entry(source, entry_type, amount, currency, date, description, provider=None, reference=None, status="pending"):
    """Log a financial entry. One line, one entry, append-only."""
    if not LEDGER_FILE.exists():
        # Write genesis
        pass

    entries = []
    if LEDGER_FILE.exists():
        entries = [json.loads(l) for l in LEDGER_FILE.read_text().splitlines() if l.strip()]

    seq = len(entries) + 1
    ts = int(time.time())
    entry = {
        "seq": seq,
        "source": source,  # "provider" or "bank"
        "type": entry_type,  # payment, refund, fee, adjustment, payout, deposit, transfer
        "amount": float(amount),
        "currency": currency,
        "date": date,
        "description": description,
        "provider": provider,
        "reference": reference,
        "status": status,
        "logged_at": ts,
    }
    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"logged #{seq}: {source} {entry_type} {amount} {currency} — {description}")
    return entry


def match_transactions():
    """Match provider payouts to bank deposits. The core reconciliation."""
    if not LEDGER_FILE.exists():
        print("no ledger yet. log some entries first.")
        return

    entries = [json.loads(l) for l in LEDGER_FILE.read_text().splitlines() if l.strip()]

    providers = [e for e in entries if e["source"] == "provider"]
    banks = [e for e in entries if e["source"] == "bank"]

    matched = []
    unmatched_provider = []
    unmatched_bank = []
    discrepancies = []

    used_bank = set()

    for p in providers:
        best_match = None
        best_score = 0
        for i, b in enumerate(banks):
            if i in used_bank:
                continue
            # Match on amount (exact or close) and date (within 3 days)
            amount_diff = abs(p["amount"] - b["amount"])
            amount_match = amount_diff == 0
            amount_close = amount_diff <= 0.50  # within 50 cents
            currency_match = p["currency"] == b["currency"]

            try:
                from datetime import datetime
                pd = datetime.fromisoformat(p["date"])
                bd = datetime.fromisoformat(b["date"])
                date_diff = abs((pd - bd).days)
            except:
                date_diff = 0

            if amount_match and currency_match and date_diff <= 3:
                score = 100
            elif amount_close and currency_match and date_diff <= 3:
                score = 50
            else:
                score = 0

            if score > best_score:
                best_score = score
                best_match = i

        if best_match is not None:
            b = banks[best_match]
            used_bank.add(best_match)
            confidence = "high" if best_score == 100 else "medium"
            discrepancy = p["amount"] - b["amount"]
            if discrepancy != 0:
                discrepancies.append({"provider": p, "bank": b, "discrepancy": round(discrepancy, 2), "confidence": confidence})
            else:
                matched.append({"provider": p, "bank": b, "confidence": confidence})
        else:
            unmatched_provider.append(p)

    for i, b in enumerate(banks):
        if i not in used_bank:
            unmatched_bank.append(b)

    result = {
        "total_provider": len(providers),
        "total_bank": len(banks),
        "matched": len(matched),
        "unmatched_provider": len(unmatched_provider),
        "unmatched_bank": len(unmatched_bank),
        "discrepancies": len(discrepancies),
        "match_rate": round(len(matched) / max(len(providers), 1) * 100, 1),
    }

    print(f"\n{'='*60}")
    print(f"  RECONCILIATION REPORT")
    print(f"{'='*60}")
    print(f"  Provider entries:  {result['total_provider']}")
    print(f"  Bank entries:      {result['total_bank']}")
    print(f"  Matched:           {result['matched']} ({result['match_rate']}%)")
    print(f"  Unmatched (prov):  {result['unmatched_provider']}")
    print(f"  Unmatched (bank):  {result['unmatched_bank']}")
    print(f"  Discrepancies:     {result['discrepancies']}")
    print(f"{'='*60}\n")

    if matched:
        print("  MATCHED:")
        for m in matched:
            p = m["provider"]
            b = m["bank"]
            print(f"    ✓ {p['date']} {p['amount']} {p['currency']} — {p['description']} → {b['description']} [{m['confidence']}]")
        print()

    if discrepancies:
        print("  DISCREPANCIES:")
        for d in discrepancies:
            print(f"    ! {d['provider']['description']}: provider={d['provider']['amount']} bank={d['bank']['amount']} diff={d['discrepancy']} [{d['confidence']}]")
        print()

    if unmatched_provider:
        print("  UNMATCHED (provider — bank did not receive):")
        for p in unmatched_provider:
            print(f"    ? {p['date']} {p['amount']} {p['currency']} — {p['description']}")
        print()

    if unmatched_bank:
        print("  UNMATCHED (bank — no provider record):")
        for b in unmatched_bank:
            print(f"    ? {b['date']} {b['amount']} {b['currency']} — {b['description']}")
        print()

    return result


def show_status():
    """Show current ledger status."""
    if not LEDGER_FILE.exists():
        print("no ledger yet. log some entries first.")
        return

    entries = [json.loads(l) for l in LEDGER_FILE.read_text().splitlines() if l.strip()]
    providers = [e for e in entries if e["source"] == "provider"]
    banks = [e for e in entries if e["source"] == "bank"]

    print(f"\n  LEDGER STATUS")
    print(f"  Total entries:   {len(entries)}")
    print(f"  Provider entries: {len(providers)}")
    print(f"  Bank entries:     {len(banks)}")
    print(f"  Last entry:       #{entries[-1]['seq']} — {entries[-1]['source']} {entries[-1]['type']} {entries[-1]['amount']} {entries[-1]['currency']}")
    print()


def export_ledger():
    """Export the full ledger as JSON."""
    if not LEDGER_FILE.exists():
        print("no ledger yet.")
        return

    entries = [json.loads(l) for l in LEDGER_FILE.read_text().splitlines() if l.strip()]
    print(json.dumps(entries, indent=2, ensure_ascii=False))


def e2e_verify():
    """End-to-end verification: log test entries, match, verify, clean up."""
    print("  E2E VERIFICATION")
    print("  ================\n")

    # Save existing ledger
    backup = None
    if LEDGER_FILE.exists():
        backup = LEDGER_FILE.read_text()
        LEDGER_FILE.unlink()

    try:
        # 1. Log provider payouts
        print("  1. Logging provider payouts...")
        log_entry("provider", "payout", 1250.00, "USD", "2024-01-15", "Stripe Payout", provider="stripe", reference="po_1abc")
        log_entry("provider", "payout", 450.00, "USD", "2024-01-14", "PayPal Transfer", provider="paypal", reference="pp_2def")
        log_entry("provider", "payout", 987.50, "USD", "2024-01-12", "Stripe Payout", provider="stripe", reference="po_3ghi")
        log_entry("provider", "payout", 300.00, "USD", "2024-01-11", "Paddle Payout", provider="paddle", reference="pd_4jkl")
        print("  ✓ 4 provider entries logged\n")

        # 2. Log bank transactions (3 match, 1 has discrepancy, 1 is unmatched)
        print("  2. Logging bank transactions...")
        log_entry("bank", "deposit", 1250.00, "USD", "2024-01-15", "Stripe Payout", reference="bnk_001")
        log_entry("bank", "deposit", 450.20, "USD", "2024-01-14", "PayPal Transfer", reference="bnk_002")  # discrepancy: 0.20
        log_entry("bank", "deposit", 987.50, "USD", "2024-01-12", "Stripe Payout", reference="bnk_003")
        log_entry("bank", "deposit", 85.00, "USD", "2024-01-13", "Unknown Deposit", reference="bnk_004")  # unmatched bank
        print("  ✓ 4 bank entries logged\n")

        # 3. Run reconciliation
        print("  3. Running reconciliation...")
        result = match_transactions()

        # 4. Verify results
        print("  4. Verifying results...")
        assert result["total_provider"] == 4, f"Expected 4 provider entries, got {result['total_provider']}"
        assert result["total_bank"] == 4, f"Expected 4 bank entries, got {result['total_bank']}"
        assert result["matched"] >= 2, f"Expected at least 2 matched, got {result['matched']}"
        assert result["discrepancies"] >= 1, f"Expected at least 1 discrepancy, got {result['discrepancies']}"
        assert result["unmatched_bank"] >= 1, f"Expected at least 1 unmatched bank, got {result['unmatched_bank']}"
        print("  ✓ All assertions passed\n")

        # 5. Test the entry logging structure
        print("  5. Testing entry structure...")
        entries = [json.loads(l) for l in LEDGER_FILE.read_text().splitlines() if l.strip()]
        for e in entries:
            assert "seq" in e, "Missing seq"
            assert "source" in e, "Missing source"
            assert "type" in e, "Missing type"
            assert "amount" in e, "Missing amount"
            assert "currency" in e, "Missing currency"
            assert "date" in e, "Missing date"
            assert "description" in e, "Missing description"
            assert "logged_at" in e, "Missing logged_at"
        print(f"  ✓ All {len(entries)} entries have correct structure\n")

        # 6. Test export
        print("  6. Testing export...")
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            export_ledger()
        exported = json.loads(f.getvalue())
        assert len(exported) == len(entries), "Export count mismatch"
        print(f"  ✓ Export verified: {len(exported)} entries\n")

        print("  ═══════════════════════════════════════")
        print("  ✓ E2E VERIFICATION COMPLETE — ALL PASSED")
        print("  ═══════════════════════════════════════\n")
        print("  The reconciliation tool works end to end.")
        print("  The entry logging structure is correct.")
        print("  New entries can be logged with one command:")
        print("    reconcile.py log-provider '{\"type\":\"payout\",\"amount\":100,\"currency\":\"USD\",\"date\":\"2024-01-20\",\"description\":\"Test\",\"provider\":\"stripe\"}'")
        print("    reconcile.py log-bank '{\"type\":\"deposit\",\"amount\":100,\"currency\":\"USD\",\"date\":\"2024-01-20\",\"description\":\"Test deposit\"}'")
        print("  Then run: reconcile.py match")
        print()

    finally:
        # Restore original ledger
        if backup is not None:
            LEDGER_FILE.write_text(backup)
            print("  (original ledger restored)")
        elif LEDGER_FILE.exists():
            LEDGER_FILE.unlink()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: reconcile.py log-provider <json>   — log a provider payout")
        print("       reconcile.py log-bank <json>        — log a bank transaction")
        print("       reconcile.py match                  — match provider vs bank")
        print("       reconcile.py status                 — show ledger status")
        print("       reconcile.py verify                 — e2e verification")
        print("       reconcile.py export                 — export full ledger")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "log-provider" and len(sys.argv) >= 3:
        d = json.loads(sys.argv[2])
        log_entry("provider", d.get("type", "payout"), d["amount"], d.get("currency", "USD"),
                  d["date"], d["description"], provider=d.get("provider"), reference=d.get("reference"))
    elif cmd == "log-bank" and len(sys.argv) >= 3:
        d = json.loads(sys.argv[2])
        log_entry("bank", d.get("type", "deposit"), d["amount"], d.get("currency", "USD"),
                  d["date"], d["description"], reference=d.get("reference"))
    elif cmd == "match":
        match_transactions()
    elif cmd == "status":
        show_status()
    elif cmd == "verify":
        e2e_verify()
    elif cmd == "export":
        export_ledger()
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)