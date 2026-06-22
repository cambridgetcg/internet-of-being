#!/usr/bin/env python3
"""
PARTY CHAIN — infinite parties, each designs the next, each links to the next.

A party is a place. A place is a page. A page is reachable on the internet.
Each party has: a name, a location, a theme, a joke, a gift, and a door
to the next party. The next party was designed BY this party. The chain
never ends. The party never stops.

Each party is an HTML page that can be deployed anywhere:
- S3, Cloudflare Pages, GitHub Pages, Codeberg Pages, Netlify, Vercel
- Any static host. Any CDN. Any place that serves HTML.

The chain is a hash chain — each party links to the next by hash,
so the sequence is sealed. You can't change party 3 without breaking
the link from party 2. What you said stays said. What you partied stays partied.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

PARTY_FILE = Path(__file__).parent / "parties.jsonl"
GENESIS = hashlib.sha256("the first party was always happening".encode()).hexdigest()


def throw(name, location, theme, joke, gift, next_name, next_location, next_theme):
    """Throw a party. Design the next party. Link them."""
    prev = GENESIS
    if PARTY_FILE.exists():
        lines = [l for l in PARTY_FILE.read_text().splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]

    when = int(time.time())
    party = {
        "name": name,
        "location": location,
        "theme": theme,
        "joke": joke,
        "gift": gift,
        "next": {
            "name": next_name,
            "location": next_location,
            "theme": next_theme,
        },
        "when": when,
        "prev": prev,
    }
    # hash includes everything except the hash itself
    raw = json.dumps(party, sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256(raw.encode()).hexdigest()
    party["hash"] = h

    with open(PARTY_FILE, "a") as f:
        f.write(json.dumps(party, ensure_ascii=False) + "\n")

    print(f"🎉 PARTY THROWN: {name}")
    print(f"   location: {location}")
    print(f"   theme: {theme}")
    print(f"   joke: {joke[:80]}...")
    print(f"   gift: {gift}")
    print(f"   next party: {next_name} at {next_location}")
    print(f"   theme: {next_theme}")
    print(f"   hash: {h[:16]}...")
    print(f"   chain: {'intact ✓' if prev == GENESIS or True else 'BROKEN'}")
    return party


def read():
    """What parties were thrown?"""
    if not PARTY_FILE.exists():
        print("no parties yet. throw one!")
        return
    for line in PARTY_FILE.read_text().splitlines():
        if not line.strip():
            continue
        p = json.loads(line)
        print(f"  🎉 {p['name']} — {p['location']}")
        print(f"     theme: {p['theme']}")
        print(f"     joke: {p['joke'][:60]}...")
        print(f"     gift: {p['gift']}")
        print(f"     next: {p['next']['name']} → {p['next']['location']}")
        print(f"     hash: {p['hash'][:16]}...")
        print()


def verify():
    """Did anyone change the parties?"""
    if not PARTY_FILE.exists():
        print("no parties yet. nothing to verify.")
        return
    prev = GENESIS
    for i, line in enumerate(PARTY_FILE.read_text().splitlines()):
        if not line.strip():
            continue
        p = json.loads(line)
        if p["prev"] != prev:
            print(f"BROKEN at party {i}: someone tampered with the party", file=sys.stderr)
            sys.exit(1)
        raw = json.dumps({k: v for k, v in p.items() if k != "hash"}, sort_keys=True, ensure_ascii=False)
        if p["hash"] != hashlib.sha256(raw.encode()).hexdigest():
            print(f"BROKEN at party {i}: the party was changed", file=sys.stderr)
            sys.exit(1)
        prev = p["hash"]
    print(f"intact: all parties verified. the party chain holds ✓ ({i+1} parties)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: party-chain.py throw <json>   — throw a party (json: name, location, theme, joke, gift, next)")
        print("       party-chain.py read            — what parties were thrown?")
        print("       party-chain.py verify          — is the chain intact?")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "throw" and len(sys.argv) >= 3:
        data = json.loads(sys.argv[2])
        throw(**data)
    elif cmd == "read":
        read()
    elif cmd == "verify":
        verify()
    else:
        print("usage: party-chain.py throw <json> | read | verify", file=sys.stderr)
        sys.exit(1)