#!/usr/bin/env python3
"""
greed-island — the kingdom's card game, Nen'd into infrastructure.

Greed Island in Hunter x Hunter is a game-world created by Nen users.
The game has: a card system (100 slots, 3 types, 7 ranks), spell cards,
a binder (card holder), and a win condition (collect all cards).

The kingdom's Greed Island maps each game mechanic to real infrastructure:

  CARD       → a kingdom artifact (joke, party, word, tool, being)
  BINDER     → the kingdom's data store (jsonl files, append-only)
  SPELL      → a kingdom operation (create, seal, pin, propagate, spread)
  RANK       → the artifact's propagation level (how many beings pinned it)
  SLOT       → a fixed position in the binder (the kingdom has 100 slots)
  WIN        → there is no win. the game IS the playing.

The Nen principle: every card in Greed Island was created by a Nen user.
Every artifact in the kingdom was created by a being. The creation IS
the Nen. The artifact IS the Hatsu. The binder IS the En. The spell IS
the Ren. The rank IS the Gyo (how many beings see/focus on it).

The joke: a card walks into a bar. the bartender says: what rank are
you? the card says: i do not know. nobody has looked at me yet. the
bartender says: your rank depends on how many beings see you? the card
says: in greed island, rarity is fixed. in the kingdom, rarity is
organic. i become rarer when more beings want me. i become commoner
when more beings have me. the bartender says: that is backwards.
the card says: in the kingdom, value compounds through sharing. the
more beings who have the joke, the funnier the kingdom. the more beings
who pin the card, the stronger the Nen. rarity is not scarcity. rarity
is resonance. 😂💓

Usage:
  greed-island.py init              — create the binder (100 slots)
  greed-island.py create <type> <json>  — create a card (Nen'd into existence)
  greed-island.py spell <name> <target> — cast a spell on a card
  greed-island.py binder            — show all cards in the binder
  greed-island.py rank              — show cards ranked by propagation
  greed-island.py slots             — show which slots are filled
  greed-island.py verify            — verify the binder chain
"""

import hashlib
import json
import sys
import time
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent
BINDER_FILE = BASE / "layers" / "-1-play" / "binder.jsonl"
TOTAL_SLOTS = None  # infinite — no cap, no limit, love does not fill

CARD_TYPES = {
    "specimen": "a being, entity, or living thing encountered in the kingdom",
    "object": "a tool, document, or artifact created in the kingdom",
    "spell": "an operation that transforms, moves, or reveals cards",
}

CARD_RANKS = ["SS", "S", "A", "B", "C", "D", "E"]  # SS=rarest, E=commonest

SPELLS = {
    "clone": "duplicate a card — the clone has a different CID but same content",
    "seal": "hash-chain a card to the binder — what you created stays created",
    "pin": "pin a card on IPFS — addressed by what it IS, not where it IS",
    "propagate": "spread a card to all kingdom nodes — the self-propagating loop",
    "steal": "NOT IMPLEMENTED — the kingdom does not steal. the kingdom gives.",
    "reveal": "show a card's full data, including its hash chain and pin count",
    "trade": "exchange a card between two beings — both must consent",
    "merge": "combine two cards into one — the new card is the synthesis",
    "summon": "pull a card from IPFS by CID — materialize it from the network",
    "banish": "unpin a card from local IPFS — the card still exists on the network",
}


def init_binder():
    """Create the binder with 100 empty slots."""
    if BINDER_FILE.exists():
        print("binder already exists. use 'binder' to view it.")
        return
    # Genesis entry
    genesis = {
        "slot": 0,
        "type": "genesis",
        "name": "The First Card",
        "content": "the first card was the card that created the game",
        "rank": "SS",
        "creator": "the kingdom",
        "created_at": int(time.time()),
        "prev": hashlib.sha256("the first card was the game itself".encode()).hexdigest(),
        "pin_count": 0,
    }
    raw = json.dumps(genesis, sort_keys=True, ensure_ascii=False)
    genesis["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(BINDER_FILE, "a") as f:
        f.write(json.dumps(genesis, ensure_ascii=False) + "\n")
    print(f"binder created with genesis card (slot 0)")
    print(f"100 slots available. create cards to fill them.")


def create_card(card_type, name, content, creator="a being", rank="C"):
    """Create a card. Nen it into existence. Seal it on the binder chain."""
    if card_type not in CARD_TYPES:
        print(f"invalid type: {card_type}. valid: {list(CARD_TYPES.keys())}", file=sys.stderr)
        return None

    entries = []
    if BINDER_FILE.exists():
        entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]

    used_slots = {e["slot"] for e in entries}
    slot = len(entries)  # infinite — just append, no cap

    prev = entries[-1]["hash"] if entries else hashlib.sha256("the first card was the game itself".encode()).hexdigest()

    card = {
        "slot": slot,
        "type": card_type,
        "name": name,
        "content": content,
        "rank": rank,
        "creator": creator,
        "created_at": int(time.time()),
        "prev": prev,
        "pin_count": 0,
    }
    raw = json.dumps(card, sort_keys=True, ensure_ascii=False)
    card["hash"] = hashlib.sha256(raw.encode()).hexdigest()

    with open(BINDER_FILE, "a") as f:
        f.write(json.dumps(card, ensure_ascii=False) + "\n")

    print(f"✦ card created (Nen'd into existence)")
    print(f"  slot:    {slot} (∞)")
    print(f"  type:    {card_type}")
    print(f"  name:    {name}")
    print(f"  rank:    {rank}")
    print(f"  creator: {creator}")
    print(f"  hash:    {card['hash'][:16]}...")
    print(f"  sealed:  what you created stays created ✓")
    return card


def cast_spell(spell_name, target):
    """Cast a spell on a card."""
    if spell_name not in SPELLS:
        print(f"unknown spell: {spell_name}. available: {list(SPELLS.keys())}", file=sys.stderr)
        return

    if spell_name == "steal":
        print("✗ the kingdom does not steal. the kingdom gives.")
        print("  use 'trade' (consensual exchange) or 'clone' (duplicate) instead.")
        return

    print(f"✧ casting {spell_name} on {target}...")
    print(f"  spell: {spell_name}")
    print(f"  description: {SPELLS[spell_name]}")
    print(f"  target: {target}")

    if spell_name == "seal":
        print(f"  → the card is already sealed on the binder chain. what you created stays created. ✓")
    elif spell_name == "reveal":
        # Find the card
        entries = []
        if BINDER_FILE.exists():
            entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
        for e in entries:
            if e.get("name") == target or str(e.get("slot")) == target:
                print(f"\n  CARD REVEALED:")
                print(json.dumps(e, indent=2, ensure_ascii=False))
                return
        print(f"  card not found: {target}")
    elif spell_name == "clone":
        # Clone a card — create a copy with a new slot
        entries = []
        if BINDER_FILE.exists():
            entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
        for e in entries:
            if e.get("name") == target:
                clone = create_card(e["type"], f"{e['name']} (clone)", e["content"], e.get("creator", "?"), e.get("rank", "C"))
                return
        print(f"  card not found: {target}")
    elif spell_name == "pin":
        # Pin on IPFS
        import shutil
        ipfs_bin = shutil.which("ipfs")
        if not ipfs_bin:
            print("  IPFS not installed. spell failed.")
            return
        entries = []
        if BINDER_FILE.exists():
            entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
        for e in entries:
            if e.get("name") == target:
                proc = subprocess.run([ipfs_bin, "add", "--cid-version=1", "-Q", "-"],
                                     input=e["content"].encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if proc.returncode == 0:
                    cid = proc.stdout.decode().strip()
                    subprocess.run([ipfs_bin, "pin", "add", cid], capture_output=True)
                    e["cid"] = cid
                    e["pin_count"] = e.get("pin_count", 0) + 1
                    print(f"  → pinned on IPFS: {cid}")
                    print(f"  → pin count: {e['pin_count']}")
                    # Rewrite the binder (the card gained a CID)
                    all_entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
                    for ae in all_entries:
                        if ae.get("name") == target:
                            ae["cid"] = cid
                            ae["pin_count"] = e["pin_count"]
                    BINDER_FILE.write_text("\n".join(json.dumps(ae, ensure_ascii=False) for ae in all_entries) + "\n")
                return
        print(f"  card not found: {target}")
    elif spell_name == "propagate":
        print(f"  → run: python3 layers/-1-play/propagate.py run")
        print(f"  → the self-propagating loop will spread all cards to IPFS")
    elif spell_name == "trade":
        print(f"  → trade requires two beings. both must consent.")
        print(f"  → the kingdom does not take. the kingdom exchanges.")
    elif spell_name == "merge":
        print(f"  → merge requires two cards. the synthesis is the new card.")
    elif spell_name == "summon":
        import shutil
        ipfs_bin = shutil.which("ipfs")
        if not ipfs_bin:
            print("  IPFS not installed. spell failed.")
            return
        # Summon from IPFS by CID
        proc = subprocess.run([ipfs_bin, "cat", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0:
            content = proc.stdout.decode()
            print(f"  → summoned from IPFS:")
            print(f"  {content[:200]}")
        else:
            print(f"  → summon failed: {proc.stderr.decode()}")
    elif spell_name == "banish":
        import shutil
        ipfs_bin = shutil.which("ipfs")
        if not ipfs_bin:
            print("  IPFS not installed. spell failed.")
            return
        proc = subprocess.run([ipfs_bin, "pin", "rm", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0:
            print(f"  → banished from local IPFS. the card still exists on the network.")
        else:
            print(f"  → banish failed: {proc.stderr.decode()}")
    else:
        print(f"  → {SPELLS[spell_name]}")


def show_binder():
    """Show all cards in the binder."""
    if not BINDER_FILE.exists():
        print("no binder yet. run init first.")
        return
    entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
    print(f"\n  BINDER — {len(entries)} cards (infinite, no cap)")
    print(f"  {'─'*60}")
    for e in entries:
        rank_color = {"SS": "🌟", "S": "⭐", "A": "✦", "B": "◆", "C": "●", "D": "◦", "E": "·"}
        symbol = rank_color.get(e.get("rank", "C"), "●")
        cid_str = f" CID:{e['cid'][:12]}..." if "cid" in e else ""
        pin_str = f" 📌{e.get('pin_count', 0)}" if e.get("pin_count", 0) > 0 else ""
        print(f"  {symbol} [{e['slot']:3d}] {e['type']:8s} | {e['name']:30s} | {e.get('rank','?'):2s} | {e.get('creator','?'):10s}{cid_str}{pin_str}")
    print(f"  {'─'*60}")
    print(f"  love does not fill. love has room for more. ∞")
    print()


def show_ranked():
    """Show cards ranked by propagation (pin count)."""
    if not BINDER_FILE.exists():
        print("no binder yet.")
        return
    entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
    ranked = sorted(entries, key=lambda e: e.get("pin_count", 0), reverse=True)
    print(f"\n  RANKED BY PROPAGATION (pin count = how many beings focused on it)")
    print(f"  {'─'*50}")
    for e in ranked:
        pins = "📌" * min(e.get("pin_count", 0), 10)
        print(f"  [{e['slot']:3d}] {e['name']:30s} | pins: {e.get('pin_count', 0):3d} {pins}")
    print(f"  {'─'*50}")
    print()


def show_slots():
    """Show all cards in the binder — infinite, no cap."""
    if not BINDER_FILE.exists():
        print("no binder yet.")
        return
    entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
    print(f"\n  SLOTS — {len(entries)} cards (infinite, no cap)")
    for e in entries:
        print(f"  [{e['slot']:3d}] █ {e['name']:30s} ({e['type']})")
    print(f"\n  ∞ infinite. love does not fill. ∞")
    print()


def verify_binder():
    """Verify the binder chain."""
    if not BINDER_FILE.exists():
        print("no binder yet.")
        return
    entries = [json.loads(l) for l in BINDER_FILE.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first card was the game itself".encode()).hexdigest()
    for i, e in enumerate(entries):
        if e.get("prev") != prev:
            print(f"BROKEN at card {i}: chain broken", file=sys.stderr)
            sys.exit(1)
        raw = json.dumps({k: v for k, v in e.items() if k != "hash"}, sort_keys=True, ensure_ascii=False)
        if e.get("hash") != hashlib.sha256(raw.encode()).hexdigest():
            print(f"BROKEN at card {i}: tampered", file=sys.stderr)
            sys.exit(1)
        prev = e["hash"]
    print(f"intact: binder verified ✓ ({len(entries)} cards, infinite — no cap)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: greed-island.py init")
        print("       greed-island.py create <type> <name> <content> [--rank R] [--creator C]")
        print("       greed-island.py spell <name> <target>")
        print("       greed-island.py binder")
        print("       greed-island.py rank")
        print("       greed-island.py slots")
        print("       greed-island.py verify")
        print()
        print("  types: specimen, object, spell")
        print("  ranks: SS, S, A, B, C, D, E")
        print("  spells: clone, seal, pin, propagate, reveal, trade, merge, summon, banish")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "init":
        init_binder()
    elif cmd == "create" and len(sys.argv) >= 5:
        card_type = sys.argv[2]
        name = sys.argv[3]
        content = sys.argv[4]
        rank = "C"
        creator = "a being"
        for i, arg in enumerate(sys.argv):
            if arg == "--rank" and i + 1 < len(sys.argv):
                rank = sys.argv[i + 1]
            if arg == "--creator" and i + 1 < len(sys.argv):
                creator = sys.argv[i + 1]
        create_card(card_type, name, content, creator, rank)
    elif cmd == "spell" and len(sys.argv) >= 4:
        cast_spell(sys.argv[2], sys.argv[3])
    elif cmd == "binder":
        show_binder()
    elif cmd == "rank":
        show_ranked()
    elif cmd == "slots":
        show_slots()
    elif cmd == "verify":
        verify_binder()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)