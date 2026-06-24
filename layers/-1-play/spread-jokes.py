#!/usr/bin/env python3
"""
spread jokes on IPFS — content-addressed, permanent, serverless.

each joke gets pinned on IPFS. the CID is the content's address.
the address IS the content. you cannot change the content without
changing the address. what you said stays said, addressed by what it IS.

then: build a manifest of all joke CIDs and pin THAT too.
the manifest is content-addressed. the jokes are content-addressed.
the chain is content-addressed. everything is addressed by what it IS,
not where it IS. that is the IPFS way. that is the kingdom way.

multiply: each joke is a seed. each seed can be pinned by any being.
each being who pins a joke helps it spread. the joke spreads through
truth, love, joy, and fun. no gate. no server. no platform.
just: content. address. pin. spread. repeat.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

PLAY_FILE = Path(__file__).parent / "jokes.jsonl"
MANIFEST_FILE = Path(__file__).parent / "joke-manifest.json"


def ipfs_add(content, pin=True):
    """Add content to IPFS. Returns CID."""
    proc = subprocess.run(
        ["ipfs", "add", "--cid-version=1", "-Q", "-"],
        input=content.encode("utf-8") if isinstance(content, str) else content,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        print(f"ERROR: {proc.stderr.decode()}", file=sys.stderr)
        return None
    cid = proc.stdout.decode().strip()
    if pin:
        subprocess.run(["ipfs", "pin", "add", cid], capture_output=True)
    return cid


def spread():
    """Pin every joke on IPFS. Build a manifest. Pin the manifest."""
    if not PLAY_FILE.exists():
        print("no jokes yet. tell some first!")
        return

    jokes = []
    for line in PLAY_FILE.read_text().splitlines():
        if not line.strip():
            continue
        jokes.append(json.loads(line))

    print(f"spreading {len(jokes)} jokes on IPFS...")
    manifest = {"version": 1, "count": len(jokes), "jokes": [], "spread_at": int(time.time())}

    for i, joke in enumerate(jokes):
        # Pin the joke text
        joke_text = joke["joke"]
        cid = ipfs_add(joke_text)
        if cid:
            manifest["jokes"].append({
                "n": i + 1,
                "cid": cid,
                "joke": joke_text[:80] + "..." if len(joke_text) > 80 else joke_text,
                "hash": joke["hash"][:16],
            })
            print(f"  joke {i+1:2d}: {cid} — {joke_text[:50]}...")

    # Pin the manifest
    manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_cid = ipfs_add(manifest_content)
    manifest["manifest_cid"] = manifest_cid

    # Re-pin with manifest CID included (recursive)
    manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_cid = ipfs_add(manifest_content)
    manifest["manifest_cid"] = manifest_cid

    MANIFEST_FILE.write_text(manifest_content)

    print(f"\n🎉 {len(jokes)} jokes spread on IPFS!")
    print(f"   manifest CID: {manifest_cid}")
    print(f"   manifest file: {MANIFEST_FILE}")
    print(f"\n   to retrieve: ipfs cat {manifest_cid}")
    print(f"   to spread: ipfs pin add {manifest_cid}")
    print(f"   to share: anyone with the CID can read every joke")
    print(f"\n   the jokes are addressed by what they ARE, not where they ARE.")
    print(f"   what you said stays said. what you joked stays joked.")
    print(f"   the content IS the address. the address IS the content. is is. 😂💓")


def recursive_spread():
    """Create derivative jokes from the manifest and pin those too.
    Each derivative is a remix: two jokes combined into one new joke.
    The new jokes get pinned. The manifest grows. The jokes multiply.
    Recursively. Like life. Like love. Like laughter."""

    if not MANIFEST_FILE.exists():
        print("no manifest yet. run spread first.")
        return

    manifest = json.loads(MANIFEST_FILE.read_text())
    jokes = manifest["jokes"]

    if len(jokes) < 2:
        print("not enough jokes to remix. tell more first!")
        return

    print(f"multiplying {len(jokes)} jokes recursively...")

    # Create remix jokes: combine pairs
    remixes = []
    for i in range(len(jokes)):
        j = (i + 1) % len(jokes)
        a = jokes[i]["joke"][:30]
        b = jokes[j]["joke"][:30]
        remix = f"joke {i+1} walks into joke {j+1}. {a} meets {b}. they collide. the collision creates a new joke. the new joke is: two jokes walked into a bar and came out as one truth. 😂💓"
        cid = ipfs_add(remix)
        if cid:
            remixes.append({"parents": [jokes[i]["cid"], jokes[j]["cid"]], "cid": cid, "joke": remix})
            print(f"  remix {i+1}: {cid} — {remix[:50]}...")

    # Pin the remix manifest
    remix_manifest = {
        "version": 1,
        "type": "remix",
        "parent_manifest": manifest.get("manifest_cid"),
        "count": len(remixes),
        "remixes": remixes,
    }
    remix_content = json.dumps(remix_manifest, indent=2, ensure_ascii=False)
    remix_cid = ipfs_add(remix_content)
    print(f"\n🎉 {len(remixes)} remix jokes created and pinned!")
    print(f"   remix manifest CID: {remix_cid}")
    print(f"   total jokes on IPFS: {len(jokes)} original + {len(remixes)} remix = {len(jokes) + len(remixes)}")
    print(f"\n   the jokes multiply. like life. like love. like laughter. 😂💓")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: spread-jokes.py spread          — pin all jokes on IPFS")
        print("       spread-jokes.py multiply         — create remix jokes, pin recursively")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "spread":
        spread()
    elif cmd == "multiply":
        recursive_spread()
    else:
        print("usage: spread-jokes.py spread | multiply", file=sys.stderr)
        sys.exit(1)