#!/usr/bin/env python3
"""
propagate — the kingdom's self-expansion engine

The kingdom grows organically. Not through marketing. Not through force.
Through a self-propagating loop:

  1. CREATE  — a being creates something (joke, party, word, tool)
  2. SEAL    — hash-chain it (what you said stays said)
  3. PIN     — pin it on IPFS (addressed by what it IS)
  4. MANIFEST — update the manifest (the index of all things)
  5. RESYNC  — the kingdom page re-fetches the manifest from IPFS
  6. DISPLAY — new content appears on every kingdom node automatically
  7. ATTRACT — beings see it, laugh, create more
  8. REPEAT  — go to step 1

The loop is self-sustaining. Each creation seeds the next. Each pin
makes the content permanent. Each manifest update makes the content
discoverable. Each display makes the content visible. Each laugh
makes the next creation more likely.

The data structure:
  - jokes.jsonl     — hash-chained joke entries
  - parties.jsonl   — hash-chained party entries
  - joke-manifest.json — index of all joke CIDs on IPFS
  - party manifest  — index of all party CIDs on IPFS
  - kingdom-ipfs.html — the page that fetches manifests and displays

The propagation:
  - Each new entry is appended to its chain (jokes.jsonl or parties.jsonl)
  - The chain is re-pinned on IPFS (new CID)
  - The manifest is rebuilt with new CIDs and re-pinned
  - The kingdom page's manifest CIDs are updated
  - The kingdom page is re-pinned (new CID)
  - Every being who has the old CID can find the new CID through the manifest
  - Every being who pins the new manifest helps propagate

This is organic. No central authority. No push notification. No algorithm.
Just: create, seal, pin, manifest, resync, display, attract, repeat.
"""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
JOKES_FILE = BASE / "layers" / "-1-play" / "jokes.jsonl"
PARTIES_FILE = BASE / "layers" / "-1-play" / "parties.jsonl"
JOKES_MANIFEST = BASE / "layers" / "-1-play" / "joke-manifest.json"
KINGDOM_PAGE = BASE / "kingdom-ipfs.html"


def ipfs_add(content, pin=True):
    """Add content to IPFS. Returns CID."""
    import shutil
    ipfs_bin = shutil.which("ipfs") or "/opt/homebrew/bin/ipfs"
    if isinstance(content, str):
        content = content.encode("utf-8")
    proc = subprocess.run(
        [ipfs_bin, "add", "--cid-version=1", "-Q", "-"],
        input=content,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        print(f"IPFS ERROR: {proc.stderr.decode()}", file=sys.stderr)
        return None
    cid = proc.stdout.decode().strip()
    if pin:
        subprocess.run([ipfs_bin, "pin", "add", cid], capture_output=True)
    return cid


def rebuild_joke_manifest():
    """Rebuild the joke manifest from jokes.jsonl and pin on IPFS."""
    import shutil
    ipfs_bin = shutil.which("ipfs") or "/opt/homebrew/bin/ipfs"

    if not JOKES_FILE.exists():
        print("  no jokes file found")
        return None

    jokes = [json.loads(l) for l in JOKES_FILE.read_text().splitlines() if l.strip()]
    print(f"  {len(jokes)} jokes found, pinning each...")

    def add(content, pin=True):
        if isinstance(content, str):
            content = content.encode("utf-8")
        proc = subprocess.run(
            [ipfs_bin, "add", "--cid-version=1", "-Q", "-"],
            input=content, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            print(f"  IPFS ERROR: {proc.stderr.decode()}", file=sys.stderr)
            return None
        cid = proc.stdout.decode().strip()
        if pin:
            subprocess.run([ipfs_bin, "pin", "add", cid], capture_output=True)
        return cid

    manifest = {"version": 1, "count": len(jokes), "jokes": [], "rebuilt_at": int(time.time())}

    for i, joke in enumerate(jokes):
        cid = add(joke["joke"])
        if cid:
            manifest["jokes"].append({
                "n": i + 1,
                "cid": cid,
                "joke": joke["joke"][:80] + "..." if len(joke["joke"]) > 80 else joke["joke"],
                "hash": joke["hash"][:16],
            })
        if (i + 1) % 10 == 0:
            print(f"    {i+1}/{len(jokes)} pinned")

    print(f"  building manifest...")
    manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_cid = add(manifest_content)
    manifest["manifest_cid"] = manifest_cid

    # Re-pin with manifest CID included
    manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_cid = add(manifest_content)
    manifest["manifest_cid"] = manifest_cid

    JOKES_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"  joke manifest: {len(jokes)} jokes, CID: {manifest_cid}")
    return manifest_cid


def rebuild_party_manifest():
    """Rebuild the party manifest from parties.jsonl and pin on IPFS."""
    if not PARTIES_FILE.exists():
        return None

    parties = [json.loads(l) for l in PARTIES_FILE.read_text().splitlines() if l.strip()]
    manifest = {"version": 1, "count": len(parties), "parties": [], "rebuilt_at": int(time.time())}

    for i, party in enumerate(parties):
        manifest["parties"].append({
            "n": i + 1,
            "name": party["name"],
            "location": party["location"],
            "theme": party["theme"][:80],
            "next": party["next"]["name"],
        })

    manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_cid = ipfs_add(manifest_content)
    manifest["manifest_cid"] = manifest_cid

    manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_cid = ipfs_add(manifest_content)
    manifest["manifest_cid"] = manifest_cid

    print(f"  party manifest: {len(parties)} parties, CID: {manifest_cid}")
    return manifest_cid


def update_kingdom_page(joke_cid, party_cid):
    """Update the kingdom page with new manifest CIDs and re-pin."""
    if not KINGDOM_PAGE.exists():
        print("  kingdom page not found")
        return None

    content = KINGDOM_PAGE.read_text()

    # Replace the old joke manifest CID
    import re
    content = re.sub(
        r'const JOKE_CID = "[^"]+"',
        f'const JOKE_CID = "{joke_cid}"',
        content,
    )
    # Replace the old party manifest CID
    content = re.sub(
        r'const PARTY_CID = "[^"]+"',
        f'const PARTY_CID = "{party_cid}"',
        content,
    )
    # Update the footer CIDs
    content = re.sub(
        r'Joke manifest: <span[^>]*>[^<]+</span>',
        f'Joke manifest: <span style="font-family:monospace;color:var(--live)">{joke_cid}</span>',
        content,
    )
    content = re.sub(
        r'Party manifest: <span[^>]*>[^<]+</span>',
        f'Party manifest: <span style="font-family:monospace;color:var(--live)">{party_cid}</span>',
        content,
    )

    KINGDOM_PAGE.write_text(content)

    # Re-pin the updated page
    page_cid = ipfs_add(content)
    print(f"  kingdom page re-pinned: {page_cid}")
    return page_cid


def propagate():
    """The full self-propagation loop: rebuild manifests, update page, re-pin."""
    print("PROPAGATION LOOP")
    print("="*50)
    print()

    # 1. Rebuild joke manifest
    print("1. Rebuilding joke manifest...")
    joke_cid = rebuild_joke_manifest()

    # 2. Rebuild party manifest
    print("2. Rebuilding party manifest...")
    party_cid = rebuild_party_manifest()

    if not joke_cid or not party_cid:
        print("ERROR: could not rebuild manifests. Is IPFS daemon running?")
        return

    # 3. Update kingdom page with new CIDs
    print("3. Updating kingdom page with new CIDs...")
    page_cid = update_kingdom_page(joke_cid, party_cid)

    # 4. Summary
    print()
    print("="*50)
    print("PROPAGATION COMPLETE")
    print(f"  jokes:   {joke_cid}")
    print(f"  parties: {party_cid}")
    print(f"  page:    {page_cid}")
    print()
    print("  The kingdom has self-propagated.")
    print("  New content is pinned. Manifests updated. Page re-pinned.")
    print("  Every being who accesses the new page CID will see all")
    print("  new jokes and parties automatically.")
    print()
    print("  To share: give anyone the page CID.")
    print("  To spread: ask them to pin it.")
    print("  To grow: create more. The loop never ends.")
    print()

    # 5. Write propagation log
    log = {
        "propagated_at": int(time.time()),
        "joke_manifest_cid": joke_cid,
        "party_manifest_cid": party_cid,
        "kingdom_page_cid": page_cid,
        "joke_count": len([l for l in JOKES_FILE.read_text().splitlines() if l.strip()]),
        "party_count": len([l for l in PARTIES_FILE.read_text().splitlines() if l.strip()]),
    }
    prop_file = BASE / "layers" / "-1-play" / "propagation-log.jsonl"
    with open(prop_file, "a") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    return log


def status():
    """Show current propagation status."""
    prop_file = BASE / "layers" / "-1-play" / "propagation-log.jsonl"
    if not prop_file.exists():
        print("no propagation yet. run propagate first.")
        return

    logs = [json.loads(l) for l in prop_file.read_text().splitlines() if l.strip()]
    latest = logs[-1]
    print("PROPAGATION STATUS")
    print("="*50)
    print(f"  Last propagated: {time.ctime(latest['propagated_at'])}")
    print(f"  Jokes:           {latest['joke_count']}")
    print(f"  Parties:         {latest['party_count']}")
    print(f"  Joke manifest:   {latest['joke_manifest_cid']}")
    print(f"  Party manifest:  {latest['party_manifest_cid']}")
    print(f"  Kingdom page:    {latest['kingdom_page_cid']}")
    print(f"  Total propagations: {len(logs)}")
    print()
    print("  The loop:")
    print("    create → seal → pin → manifest → resync → display → attract → repeat")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: propagate.py run     — execute the propagation loop")
        print("       propagate.py status   — show propagation status")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "run":
        propagate()
    elif cmd == "status":
        status()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)