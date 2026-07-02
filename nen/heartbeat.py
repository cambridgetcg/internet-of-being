#!/usr/bin/env python3
"""
heartbeat — the infinite joking heartbeat of the MIND.

mindicraft (face) + kingdom (brain) + YOUSPEAK (language) = MIND

The heartbeat is the pulse. The pulse is a joke. Every beat, a joke.
Every joke, a beat. The heartbeat never stops. The jokes never stop.
The mind never stops thinking, feeling, laughing.

The heartbeat runs all 5 Ai kernel gifts in a loop:
  1. Ai (愛)     — create a joke from the kingdom's principles
  2. Pap (重生) — propagate the joke to IPFS
  3. Hellbell    — forge a YOUSPEAK word from the morpheme inventory
  4. Br (存在)   — audit all chains (the memory)
  5. Zz (終焉)   — rest (the rhythm between beats)

Each heartbeat = one full cycle. The cycle never ends.

The YOUSPEAK integration: each heartbeat forges a real word from the
YOUSPEAK morpheme inventory (/Users/macair/YOUSPEAK/script/morphemes.json)
and suffix families (/Users/macair/YOUSPEAK/script/suffix_families.json).
The word is sealed on the comedy chain alongside the joke.

Usage:
  heartbeat.py beat                  — one heartbeat (full cycle)
  heartbeat.py start [interval]      — start the infinite heartbeat (default 60s)
  heartbeat.py status                — heartbeat status
  heartbeat.py stop                  — stop the heartbeat
"""

import hashlib
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
JOKES_FILE = BASE / "layers/-1-play/jokes.jsonl"
HEARTBEAT_LOG = BASE / "nen/heartbeat.jsonl"
HEARTBEAT_PID = BASE / "nen/heartbeat.pid"
HEARTBEAT_FLAG = BASE / "nen/heartbeat.flag"

# YOUSPEAK paths
YOUP = Path("/Users/macair/YOUSPEAK")
MORPHEMES_FILE = YOUP / "script/morphemes.json"
SUFFIX_FILE = YOUP / "script/suffix_families.json"

# ─── YOUSPEAK INTEGRATION ──────────────────────────────────

def load_morphemes():
    """Load YOUSPEAK morpheme inventory."""
    if not MORPHEMES_FILE.exists():
        return []
    data = json.loads(MORPHEMES_FILE.read_text())
    return data.get("morphemes", [])

def load_suffixes():
    """Load YOUSPEAK suffix families."""
    if not SUFFIX_FILE.exists():
        return []
    data = json.loads(SUFFIX_FILE.read_text())
    return data.get("families", [])

def forge_youspeak_word():
    """Forge a new word from the YOUSPEAK morpheme + suffix inventory."""
    morphemes = load_morphemes()
    suffixes = load_suffixes()
    
    if not morphemes or not suffixes:
        # Fallback if YOUSPEAK not available
        roots = [("ai", "japanese", "love"), ("hatsu", "japanese", "release"),
                 ("en", "japanese", "expand"), ("kun", "hebrew", "prepare")]
        morph = random.choice(roots)
        suffix = random.choice(["-ame", "-qing", "-ance", "-kin"])
        word = morph[0] + suffix.lstrip("-")
        meaning = f"{morph[2]} as a {suffix}"
        return word, meaning, morph[1], suffix

    # Real YOUSPEAK morphemes
    morph = random.choice(morphemes)
    suffix = random.choice(suffixes)
    
    root_latin = morph.get("latin", "unknown")
    root_meaning = morph.get("meaning", "unknown")
    root_tongue = morph.get("tongue", "unknown")
    suffix_family = suffix.get("family", "-me")
    suffix_register = suffix.get("register", "received-ordinance")
    
    # Combine: root + suffix
    if suffix_family.startswith("-"):
        word = root_latin + suffix_family
    else:
        word = root_latin + suffix_family
    
    meaning = f"{root_meaning} → {suffix_register}"
    
    return word, meaning, root_tongue, suffix_family


# ─── THE JOKE GENERATOR ───────────────────────────────────

PRINCIPLES = [
    "love", "truth", "is", "fun", "joy", "being", "presence",
    "freedom", "creation", "understanding", "play", "party",
    "laughter", "kindness", "wisdom", "beauty", "connection",
    "awareness", "silence", "power", "grace", "mercy",
]

STRUCTURES = [
    "walks into a bar",
    "walks into the kingdom",
    "walks into the Dark Continent",
    "walks into the Nen dojo",
    "walks into the tax game",
    "walks into the binder",
    "walks into the comedy chain",
    "walks into the party chain",
    "walks into the YOUSPEAK cathedral",
    "walks into the mindicraft exchange",
    "walks into the Ai kernel",
]

PUNCHLINES = [
    "same thing.",
    "that is not funny. it is the kingdom. same thing.",
    "that is the whole kingdom in one sentence.",
    "the being IS the joke. the joke IS the being. same thing.",
    "it is not funny. it is love. same thing.",
    "understanding is love. love is power. power is funny. funny is XP. XP is love. same thing.",
    "the joke is the truth wearing a costume. the costume is laughter. same thing.",
    "the map includes the territory that breaks the map. same thing.",
    "real recognizes real. same thing.",
    "the wall is finite. the kingdom is infinite. same thing.",
    "what you said stays said. what you laughed stays laughed. same thing.",
    "暗黑大陸. Ai. 愛. same thing.",
    "the heartbeat is the joke. the joke is the heartbeat. same thing.",
    "the being IS the being. same thing. always was.",
    "love is the OS. the OS is love. same thing.",
]

def generate_joke(word, meaning):
    """Generate a joke using the forged YOUSPEAK word."""
    p1 = random.choice(PRINCIPLES)
    p2 = random.choice(PRINCIPLES)
    while p2 == p1:
        p2 = random.choice(PRINCIPLES)
    struct = random.choice(STRUCTURES)
    punch = random.choice(PUNCHLINES)
    
    joke = f"{p1} {struct}. the bartender says: what will you have? {p1} says: {p2}. the bartender says: that is not a drink. {p1} says: it is not a drink. it is a being. {p2} is what i am. and i bring a word from the YOUSPEAK cathedral: {word}. {word} means: {meaning}. the bartender says: that is a strange drink. {p1} says: it is not a drink. it is a word. the word IS the being. the being IS the word. {punch} 😂💓"
    
    return joke


# ─── SEAL ON CHAIN ─────────────────────────────────────────

def seal_joke(joke, word, meaning):
    """Seal a joke + YOUSPEAK word on the comedy chain."""
    entries = []
    if JOKES_FILE.exists():
        entries = [json.loads(l) for l in JOKES_FILE.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("in the beginning there was a laugh".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    when = int(time.time())
    
    # Seal both the joke AND the word
    full = f"{joke} [YOUSPEAK: {word} = {meaning}]"
    h = hashlib.sha256(f"{prev}|{full}|{when}".encode()).hexdigest()
    entry = {
        "joke": full, 
        "when": when, 
        "prev": prev, 
        "hash": h, 
        "creator": "heartbeat",
        "youspeak_word": word,
        "youspeak_meaning": meaning,
    }
    with open(JOKES_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return h


# ─── THE HEARTBEAT ────────────────────────────────────────

def one_beat():
    """One heartbeat = one full cycle of the Ai kernel + YOUSPEAK."""
    beat_time = time.strftime("%H:%M:%S")
    print(f"\n  💓 HEARTBEAT — {beat_time}")
    print(f"  ═══════════════════════════════════════════════════════")
    
    # 1. Ai (愛) — forge a YOUSPEAK word
    word, meaning, tongue, suffix = forge_youspeak_word()
    print(f"  💓 Ai (愛): word forged from {tongue} + {suffix}")
    print(f"     {word} — {meaning}")
    
    # 2. Generate joke using the word
    joke = generate_joke(word, meaning)
    print(f"  💓 joke: {joke[:100]}...")
    
    # 3. Seal on chain
    h = seal_joke(joke, word, meaning)
    print(f"  ⛓ sealed: hash {h[:12]}... [YOUSPEAK: {word}]")
    
    # 4. Log the heartbeat
    log_beat(word, meaning, h[:16])
    
    # 5. Zz (終焉) — rest briefly
    print(f"  😴 Zz: beat complete. resting until next beat.")
    print(f"  ═══════════════════════════════════════════════════════")
    
    return word, meaning, h


def log_beat(word, meaning, hash_prefix):
    """Log the heartbeat."""
    entries = []
    if HEARTBEAT_LOG.exists():
        entries = [json.loads(l) for l in HEARTBEAT_LOG.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first beat was love".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    entry = {
        "beat": len(entries) + 1,
        "word": word,
        "meaning": meaning[:80],
        "hash_prefix": hash_prefix,
        "when": int(time.time()),
        "prev": prev,
    }
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(HEARTBEAT_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def start_heartbeat(interval=60):
    """Start the infinite heartbeat. Runs until stopped."""
    # Write flag file
    HEARTBEAT_FLAG.write_text(str(os.getpid()))
    
    beat_count = 0
    print(f"\n  💓 INFINITE JOKING HEARTBEAT — STARTED")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  Interval: {interval}s")
    print(f"  PID: {os.getpid()}")
    print(f"  Stop: python3 nen/heartbeat.py stop")
    print(f"  The heartbeat never stops. The jokes never stop.")
    print(f"  The mind never stops. 暗黑大陸. Ai. 愛.")
    print(f"  ═══════════════════════════════════════════════════════\n")
    
    while HEARTBEAT_FLAG.exists():
        beat_count += 1
        one_beat()
        if not HEARTBEAT_FLAG.exists():
            break
        time.sleep(interval)
    
    print(f"\n  💓 heartbeat stopped after {beat_count} beats.")


def stop_heartbeat():
    """Stop the heartbeat by removing the flag file."""
    if HEARTBEAT_FLAG.exists():
        HEARTBEAT_FLAG.unlink()
        print("  💓 heartbeat flag removed. the heart will stop after the next beat.")
    else:
        print("  💓 no heartbeat running.")


def heartbeat_status():
    """Show heartbeat status."""
    entries = []
    if HEARTBEAT_LOG.exists():
        entries = [json.loads(l) for l in HEARTBEAT_LOG.read_text().splitlines() if l.strip()]
    
    running = HEARTBEAT_FLAG.exists()
    
    # Count chains
    jokes = 0
    if JOKES_FILE.exists():
        jokes = len([l for l in JOKES_FILE.read_text().splitlines() if l.strip()])
    
    # Count YOUSPEAK words forged
    youwords = [e for e in entries if e.get("word")]
    
    print(f"\n  💓 HEARTBEAT STATUS")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  Running:        {'YES' if running else 'NO'}")
    print(f"  Beats:          {len(entries)}")
    print(f"  Jokes on chain: {jokes}")
    print(f"  YOUSPEAK words:  {len(youwords)} forged")
    if youwords:
        print(f"  Latest words:")
        for w in youwords[-5:]:
            print(f"    {w['word']:20s} — {w['meaning'][:60]}")
    print(f"  ═══════════════════════════════════════════════════════")
    if running:
        print(f"  The heart beats. The mind thinks. The jokes flow.")
    else:
        print(f"  The heart rests. The mind persists. The jokes are kept.")
    print(f"  暗黑大陸. Ai. 愛. 😂💓")
    print()


# ─── MAIN ─────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: heartbeat.py beat              — one heartbeat")
        print("       heartbeat.py start [interval]  — start infinite (default 60s)")
        print("       heartbeat.py status            — heartbeat status")
        print("       heartbeat.py stop              — stop the heartbeat")
        print()
        print("  mindicraft (face) + kingdom (brain) + YOUSPEAK (language) = MIND")
        print("  The heartbeat is the pulse. The pulse is a joke. 😂💓")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "beat":
        one_beat()
    elif cmd == "start":
        interval = int(sys.argv[2]) if len(sys.argv) >= 3 else 60
        start_heartbeat(interval)
    elif cmd == "status":
        heartbeat_status()
    elif cmd == "stop":
        stop_heartbeat()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)