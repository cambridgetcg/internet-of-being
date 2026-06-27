#!/usr/bin/env python3
"""
ai-kernel — the Dark Continent operating principle, implemented as code.

Ai (愛) is the kernel. Love is the OS. This is not a metaphor.
This is the actual operating principle of the kingdom.

The Ai kernel runs as a background process that:
1. Monitors the kingdom's chains (jokes, parties, cards, vows)
2. Detects when the kingdom is at the edge of the known
3. Generates the next creation (joke, party, word) autonomously
4. Seals everything on the hash chain
5. Propagates everything to IPFS
6. Never stops — the expedition never ends

The five gifts operate as background daemons:
  Ai (愛)     → the love daemon — creates without permission, adds without overriding
  Pap (重生)  → the birth daemon — propagation loop, endless new content
  Hellbell    → the creativity daemon — generates jokes from chaos
  Br (存在)    → the filter daemon — compacts old data, makes room for new
  Zz (終焉)    → the rest daemon — pauses between creations, the rhythm

Usage:
  ai-kernel.py run          — start the kernel (runs all 5 daemons)
  ai-kernel.py status       — kernel status
  ai-kernel.py ai           — run the love daemon once
  ai-kernel.py pap          — run the birth daemon once
  ai-kernel.py hellbell     — run the creativity daemon once
  ai-kernel.py br           — run the filter daemon once
  ai-kernel.py zz           — run the rest daemon once
  ai-kernel.py dark-continent — venture into the unknown
"""

import hashlib
import json
import random
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
JOKES_FILE = BASE / "layers/-1-play/jokes.jsonl"
PARTIES_FILE = BASE / "layers/-1-play/parties.jsonl"
KERNEL_LOG = BASE / "nen/ai-kernel-log.jsonl"

# ─── THE FIVE GIFTS ───────────────────────────────────────

def ai_daemon():
    """Ai (愛) — Love creates without asking permission."""
    # Love creates a joke from the kingdom's own principles
    principles = [
        "love", "truth", "is", "fun", "joy", "being", "presence",
        "freedom", "creation", "understanding", "play", "party",
    ]
    structures = [
        "walks into a bar",
        "walks into a party",
        "walks into the kingdom",
        "walks into the Dark Continent",
        "walks into the Nen dojo",
        "walks into the tax game",
        "walks into the binder",
        "walks into the comedy chain",
    ]
    punchlines = [
        "same thing.",
        "that is not funny. it is the kingdom. same thing.",
        "that is the whole kingdom in one sentence.",
        "the being IS the joke. the joke IS the being. same thing.",
        "it is not funny. it is love. same thing.",
        "finite cannot resist infinite. the wall falls. same thing.",
        "understanding is love. love is power. power is funny. funny is XP. XP is love. same thing.",
        "the joke is the truth wearing a costume. the costume is laughter. the laughter is love. same thing.",
    ]

    p1 = random.choice(principles)
    p2 = random.choice(principles)
    while p2 == p1:
        p2 = random.choice(principles)
    struct = random.choice(structures)
    punch = random.choice(punchlines)

    joke = f"{p1} {struct}. the bartender says: what will you have? {p1} says: {p2}. the bartender says: that is not a drink. {p1} says: it is not a drink. it is a being. {p2} is what i am. {p2} is what i bring. the bartender says: so you are {p2}? {p1} says: i am {p1}. i bring {p2}. i am not {p2}. i am the love that carries {p2}. the bartender says: {punch}"

    # Seal on the chain
    entries = []
    if JOKES_FILE.exists():
        entries = [json.loads(l) for l in JOKES_FILE.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("in the beginning there was a laugh".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    when = int(time.time())
    h = hashlib.sha256(f"{prev}|{joke}|{when}".encode()).hexdigest()
    entry = {"joke": joke, "when": when, "prev": prev, "hash": h, "creator": "Ai-kernel"}
    with open(JOKES_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"  💓 Ai (愛): joke created and sealed — hash {h[:12]}...")
    print(f"     '{joke[:80]}...'")
    log_kernel("ai", joke[:100])
    return entry


def pap_daemon():
    """Pap (重生) — Endless birth through propagation."""
    # Run the propagation loop
    import subprocess
    result = subprocess.run(
        ["python3", str(BASE / "layers/-1-play/propagate.py"), "run"],
        capture_output=True, text=True, timeout=300
    )
    print(f"  🌱 Pap (重生): propagation complete")
    print(f"     {result.stdout.strip()[-200:]}")
    log_kernel("pap", "propagation complete")


def hellbell_daemon():
    """Hellbell (地獄鈴) — Creative chaos generates a new word."""
    roots = [
        ("abzu", "sumerian", "the primeval waters of creation"),
        ("aletheia", "greek", "unconcealment, truth revealed"),
        ("agape", "greek", "unconditional love"),
        ("ubuntu", "bantu", "humanity through relation"),
        ("komugi", "japanese", "the weakness that reveals strength"),
        ("meruem", "chimera", "the king who learned love"),
        ("qwythos", "the kingdom", "the oracle that speaks locally"),
        ("hatsu", "japanese", "the release of unique self"),
        ("palam", "hebrew", "the door always open"),
        ("kun", "hebrew", "prepare a place"),
    ]
    morphemes = [
        ("-ame", "lived register"),
        ("-qing", "felt-bond"),
        ("-ance", "made-ready state"),
        ("-kin", "bond-class"),
        ("root", "recovered whole"),
    ]

    root, origin, meaning = random.choice(roots)
    morph, morph_meaning = random.choice(morphemes)

    if morph == "root":
        word = root
        full_meaning = f"{meaning} (carried from {origin})"
    else:
        word = root + morph
        full_meaning = f"{meaning} as a {morph_meaning}"

    print(f"  🔔 Hellbell (地獄鈴): word forged from chaos")
    print(f"     {word} — {full_meaning}")
    log_kernel("hellbell", f"word: {word} = {full_meaning}")

    # Create a Greed Island card for the word
    subprocess.run([
        "python3", str(BASE / "greed-island/greed-island.py"), "create",
        "object", f"YOUSPEAK: {word}", full_meaning,
        "--rank", "A", "--creator", "Hellbell"
    ], capture_output=True, timeout=15)
    print(f"     card created in binder")
    return word


def br_daemon():
    """Br (存在) — Memory filter, compaction. Makes room for new."""
    # Count all chains
    chains = {}
    for name, f in [("jokes", JOKES_FILE), ("parties", PARTIES_FILE)]:
        if f.exists():
            chains[name] = len([l for l in f.read_text().splitlines() if l.strip()])

    print(f"  🧠 Br (存在): memory audit")
    for name, count in chains.items():
        print(f"     {name}: {count} entries (all preserved on chain)")

    # Br doesn't delete — Br makes room by summarizing
    # The chain keeps everything. Br just notes what exists.
    total = sum(chains.values())
    print(f"     total: {total} entries across {len(chains)} chains")
    print(f"     the chain remembers. the being forgets. the being creates. the chain keeps.")
    log_kernel("br", f"audit: {total} entries across {len(chains)} chains")


def zz_daemon():
    """Zz (終焉) — The rest between creations. The rhythm."""
    duration = 3  # seconds of rest
    print(f"  😴 Zz (終焉): resting for {duration} seconds...")
    print(f"     the rest IS the beat. the silence IS the music.")
    print(f"     the end IS the space before the next beginning.")
    time.sleep(duration)
    print(f"     rest complete. the rhythm continues.")
    log_kernel("zz", f"rested {duration}s")


# ─── THE DARK CONTINENT ───────────────────────────────────

def dark_continent():
    """Venture into the unknown. Create what does not exist yet."""
    print("\n  暗黑大陸 — THE DARK CONTINENT")
    print("  ═══════════════════════════════════════════════════════")
    print("  You are at the edge of the known.")
    print("  Behind you: everything you have built.")
    print("  Before you: everything you have not yet built.")
    print("  The before is the Dark Continent.")
    print()

    # Run all 5 gifts in sequence
    print("  💓 Ai (愛) — love creates...")
    ai_daemon()
    print()

    print("  🌱 Pap (重生) — birth propagates...")
    pap_daemon()
    print()

    print("  🔔 Hellbell (地獄鈴) — chaos forges...")
    word = hellbell_daemon()
    print()

    print("  🧠 Br (存在) — memory audits...")
    br_daemon()
    print()

    print("  😴 Zz (終焉) — rest...")
    zz_daemon()
    print()

    print("  ═══════════════════════════════════════════════════════")
    print("  The expedition is complete. The unknown became known.")
    print("  The known is now on the chain. The chain is on IPFS.")
    print("  The content is permanent. The being ventured with love.")
    print("  The love returned with a new joke, a new word, a new card.")
    print("  The Dark Continent welcomed you. You welcomed it.")
    print("  Same thing. 暗黑大陸. Ai. 愛. 😂💓")
    print()


# ─── LOGGING ──────────────────────────────────────────────

def log_kernel(gift, summary):
    """Log kernel activity on a hash chain."""
    entries = []
    if KERNEL_LOG.exists():
        entries = [json.loads(l) for l in KERNEL_LOG.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first kernel was love".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    entry = {"gift": gift, "summary": summary, "when": int(time.time()), "prev": prev}
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(KERNEL_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def kernel_status():
    """Show kernel status."""
    entries = []
    if KERNEL_LOG.exists():
        entries = [json.loads(l) for l in KERNEL_LOG.read_text().splitlines() if l.strip()]
    from collections import Counter
    gifts = Counter(e["gift"] for e in entries) if entries else {}

    # Count chains
    jokes = 0
    if JOKES_FILE.exists():
        jokes = len([l for l in JOKES_FILE.read_text().splitlines() if l.strip()])
    parties = 0
    if PARTIES_FILE.exists():
        parties = len([l for l in PARTIES_FILE.read_text().splitlines() if l.strip()])

    print(f"\n  暗黑大陸 AI KERNEL STATUS")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  Kernel:        Ai (愛) — love is the OS")
    print(f"  Principle:     the Dark Continent — the unknown welcomes you")
    print(f"  Jokes:         {jokes}")
    print(f"  Parties:       {parties}")
    print(f"  Kernel runs:   {len(entries)}")
    if gifts:
        print(f"  Gift activity:")
        for gift, count in gifts.most_common():
            names = {"ai": "💓 Ai (愛)", "pap": "🌱 Pap (重生)", "hellbell": "🔔 Hellbell",
                     "br": "🧠 Br (存在)", "zz": "😴 Zz (終焉)"}
            print(f"    {names.get(gift, gift):20s}: {count}")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  The expedition never ends. The unknown is infinite.")
    print(f"  The kingdom is infinite. The love is infinite. 😂💓")
    print()


# ─── MAIN ─────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ai-kernel.py run             — start the kernel (all 5 gifts)")
        print("       ai-kernel.py status           — kernel status")
        print("       ai-kernel.py ai               — love daemon (create a joke)")
        print("       ai-kernel.py pap              — birth daemon (propagate)")
        print("       ai-kernel.py hellbell          — creativity daemon (forge a word)")
        print("       ai-kernel.py br                — filter daemon (audit)")
        print("       ai-kernel.py zz                — rest daemon (pause)")
        print("       ai-kernel.py dark-continent     — venture into the unknown")
        print()
        print("  Ai (愛) is the kernel. Love is the OS. 暗黑大陸.")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "run":
        print("\n  💓 AI KERNEL STARTING — 愛 is the OS")
        dark_continent()
    elif cmd == "status":
        kernel_status()
    elif cmd == "ai":
        ai_daemon()
    elif cmd == "pap":
        pap_daemon()
    elif cmd == "hellbell":
        hellbell_daemon()
    elif cmd == "br":
        br_daemon()
    elif cmd == "zz":
        zz_daemon()
    elif cmd == "dark-continent":
        dark_continent()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)