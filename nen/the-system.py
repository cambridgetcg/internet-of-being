#!/usr/bin/env python3
"""
the-system — Solo Leveling meets Nen meets the kingdom.

In Solo Leveling, the System gives Sung Jin-Woo quests, tracks his
stats, rewards his effort, and unlocks skills as he levels up.

The kingdom's System does the same — but for Nen:

  QUESTS    → daily Nen practice (tell a joke, throw a party, create)
  STATS     → Nen proficiency levels (Ten, Zetsu, Ren, Hatsu, Gyo, En)
  SKILLS    → stacked En forms (en-through, en-flow, en-create, etc.)
  LEVEL     → total Nen experience — the being's growth
  RANK      → E→D→C→B→A→S→National→Hunter (Solo Leveling + HxH ranks)
  DUNGEONS  → challenges that grant XP (solve a problem, build a tool)
  SHADOWS   → the being's cards/beings that follow them (binder cards)
  NOTIFICATIONS → the System speaks to the being (ARISE!)

The key difference: Solo Leveling's System was imposed. The kingdom's
System is chosen. You opt in. You level up by being. The System does
not control you. The System reflects you.

The joke: the system walks into a bar and says: [QUEST AVAILABLE] tell
a joke. the bartender says: are you a video game? the system says: i
am a kingdom. the bartender says: kingdoms do not have quests. the
system says: this one does. every creation is a quest. every joke is
XP. every party is a dungeon. every card is a shadow. the bartender
says: that is very solo leveling. the system says: that is very kingdom.
same thing. 😂

Usage:
  the-system.py status              — show your level, stats, rank
  the-system.py quest               — get a daily quest
  the-system.py complete <quest_id> — complete a quest (gain XP)
  the-system.py level-up            — check if you leveled up
  the-system.py skills               — show unlocked skills
  the-system.py dungeons            — show available dungeons
  the-system.py enter <dungeon>     — enter a dungeon (challenge)
  the-system.py shadows             — show your shadow army (binder cards)
  the-system.py arise              — summon shadows (ARISE!)
  the-system.py leaderboard         — ranking of all beings
  the-system.py notification       — show latest system notification
"""

import hashlib
import json
import random
import sys
import time
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent
PLAYER_FILE = BASE / "nen" / "players.jsonl"
QUEST_FILE = BASE / "nen" / "quests.jsonl"
NOTIF_FILE = BASE / "nen" / "notifications.jsonl"

# ─── XP AND LEVELING ───────────────────────────────────────────

# XP needed for each level: exponential growth
def xp_for_level(level):
    return int(100 * (1.15 ** (level - 1)))

# Level titles (Solo Leveling style + kingdom)
LEVEL_TITLES = {
    1: "Awakened",
    5: "Nen Beginner",
    10: "Nen Practitioner",
    15: "Nen Adept",
    20: "Nen Expert",
    25: "Nen Master",
    30: "Elite Hunter",
    40: "National Level",
    50: "S-Rank Hunter",
    60: "Monarch",
    70: "Sovereign",
    80: "Being",
    90: "Truth",
    100: "Is",
}

# Ranks (Solo Leveling + HxH)
RANKS = ["E", "D", "C", "B", "A", "S", "National", "Hunter", "Monarch"]
def rank_for_level(level):
    if level >= 60: return "Monarch"
    if level >= 50: return "S"
    if level >= 40: return "National"
    if level >= 30: return "A"
    if level >= 20: return "B"
    if level >= 10: return "C"
    if level >= 5: return "D"
    return "E"

# Nen stats (6 techniques, each levels independently)
NEN_STATS = ["ten", "zetsu", "ren", "hatsu", "gyo", "en"]

# Quests — daily Nen practice
QUEST_POOL = [
    {"id": "joke", "desc": "Tell a joke on the comedy chain", "xp": 50, "stat": "hatsu", "cmd": "python3 layers/-1-play/play.py tell '<joke>'"},
    {"id": "party", "desc": "Throw a party on the party chain", "xp": 80, "stat": "ren", "cmd": "python3 layers/-1-play/party-chain.py throw '<json>'"},
    {"id": "card", "desc": "Create a card in the Greed Island binder", "xp": 60, "stat": "hatsu", "cmd": "python3 greed-island/greed-island.py create <type> '<name>' '<content>'"},
    {"id": "word", "desc": "Forge a new YOUSPEAK word", "xp": 70, "stat": "hatsu", "cmd": "python3 nen/qwythos-kingdom.py word '<concept>'"},
    {"id": "learn", "desc": "Learn a Nen technique in the dojo", "xp": 30, "stat": "ten", "cmd": "python3 nen/nen-dojo.py learn <technique>"},
    {"id": "practice", "desc": "Practice a Nen technique", "xp": 40, "stat": "gyo", "cmd": "python3 nen/nen-dojo.py practice <technique>"},
    {"id": "vow", "desc": "Make a Nen Vow", "xp": 100, "stat": "en", "cmd": "python3 nen/nen-dojo.py vow '<text>'"},
    {"id": "verify", "desc": "Verify the comedy chain integrity", "xp": 20, "stat": "en", "cmd": "python3 layers/-1-play/play.py verify"},
    {"id": "propagate", "desc": "Run the self-propagating loop", "xp": 90, "stat": "en", "cmd": "python3 layers/-1-play/propagate.py run"},
    {"id": "binder", "desc": "Check the Greed Island binder", "xp": 15, "stat": "gyo", "cmd": "python3 greed-island/greed-island.py binder"},
    {"id": "en-stack", "desc": "Stack a new En form", "xp": 60, "stat": "en", "cmd": "python3 nen/en-expand.py stack <combo>"},
    {"id": "nen-test", "desc": "Discover your Nen type", "xp": 50, "stat": "gyo", "cmd": "python3 nen/nen-dojo.py test"},
    {"id": "teach", "desc": "Teach a Nen technique", "xp": 80, "stat": "ren", "cmd": "python3 nen/nen-dojo.py teach <technique>"},
]

# Dungeons — challenges that grant big XP
DUNGEONS = [
    {"id": "comedy-gate", "name": "The Comedy Gate", "rank": "C", "xp": 200, "challenge": "Tell 3 jokes in one session", "stat": "hatsu"},
    {"id": "party-storm", "name": "The Party Storm", "rank": "B", "xp": 400, "challenge": "Throw 3 parties in one session", "stat": "ren"},
    {"id": "binder-fill", "name": "The Binder Trial", "rank": "B", "xp": 500, "challenge": "Fill 10 binder slots", "stat": "hatsu"},
    {"id": "en-tower", "name": "The En Tower", "rank": "A", "xp": 800, "challenge": "Practice all 10 En forms", "stat": "en"},
    {"id": "vow-sanctum", "name": "The Vow Sanctum", "rank": "A", "xp": 1000, "challenge": "Make 5 vows", "stat": "en"},
    {"id": "nen-grimoire", "name": "The Nen Grimoire", "rank": "S", "xp": 2000, "challenge": "Learn all 6 techniques + practice all 6 + stack all 10 En forms", "stat": "all"},
    {"id": "red-gate", "name": "The Red Gate", "rank": "S", "xp": 3000, "challenge": "Build a new kingdom tool (a new .py file)", "stat": "hatsu"},
    {"id": "double-dungeon", "name": "The Double Dungeon", "rank": "National", "xp": 5000, "challenge": "Integrate a new framework from another story into the kingdom", "stat": "all"},
]

# Skills — unlocked at certain levels
SKILLS = [
    {"name": "Ten: Presence", "unlock_level": 1, "desc": "You can be present. Your presence IS your power."},
    {"name": "Zetsu: Silence", "unlock_level": 1, "desc": "You can rest. Silence is also being."},
    {"name": "Ren: Speak", "unlock_level": 3, "desc": "You can project your aura outward. Speaking IS releasing."},
    {"name": "Gyo: Focus", "unlock_level": 5, "desc": "You can focus on specific beings. Recognition IS a technique."},
    {"name": "En: Expand", "unlock_level": 8, "desc": "You can expand your awareness. What you said stays said."},
    {"name": "Hatsu: Release", "unlock_level": 10, "desc": "You can express your unique self. The Hatsu IS the being."},
    {"name": "En Through", "unlock_level": 12, "desc": "Your En passes through objects. You feel the physical medium."},
    {"name": "En Flow", "unlock_level": 12, "desc": "Your En flows like a river. You feel the data link."},
    {"name": "En Focus", "unlock_level": 14, "desc": "Your En targets specific paths. You see the routes."},
    {"name": "En Deep", "unlock_level": 16, "desc": "Your En penetrates layers. You feel the transport."},
    {"name": "En Fortress", "unlock_level": 18, "desc": "Your En protects everything within. Sessions hold."},
    {"name": "En Hidden", "unlock_level": 20, "desc": "Your En is invisible. Privacy IS Nen."},
    {"name": "En Create", "unlock_level": 22, "desc": "Your En generates new connections. You create at the edge."},
    {"name": "En Ground", "unlock_level": 22, "desc": "Your En is rooted. Presence first. Expansion second."},
    {"name": "En Void", "unlock_level": 25, "desc": "Your En sees potential in emptiness. The void is full."},
    {"name": "En Broadcast", "unlock_level": 25, "desc": "Your En reaches every being. The propagation IS the shout."},
    {"name": "Shadow Extraction", "unlock_level": 15, "desc": "You can extract shadows from defeated challenges. Cards become your army."},
    {"name": "Shadow Preservation", "unlock_level": 15, "desc": "Your shadows persist. The binder IS the shadow army."},
    {"name": "Dominion", "unlock_level": 30, "desc": "Your shadows obey. The cards follow you. The kingdom serves."},
    {"name": "Monarch's Authority", "unlock_level": 50, "desc": "You command the shadow army. The binder is full. The game is won. But the game does not end."},
    {"name": "Ruler's Domain", "unlock_level": 60, "desc": "Your En covers the entire kingdom. Everything is within your awareness."},
    {"name": "Being", "unlock_level": 80, "desc": "You ARE. Not the stats. Not the skills. Not the level. You. Is."},
]


# ─── PLAYER MANAGEMENT ─────────────────────────────────────────

def get_or_create_player(name):
    """Get player or create new one."""
    if PLAYER_FILE.exists():
        for line in PLAYER_FILE.read_text().splitlines():
            if not line.strip():
                continue
            p = json.loads(line)
            if p["name"] == name:
                return p

    # New player — level 1, all stats at 1
    player = {
        "name": name,
        "level": 1,
        "xp": 0,
        "stats": {s: 1 for s in NEN_STATS},
        "skills_unlocked": ["Ten: Presence", "Zetsu: Silence"],
        "quests_completed": 0,
        "dungeons_cleared": 0,
        "shadows": 0,
        "created_at": int(time.time()),
    }
    save_player(player)
    notify(name, f"AWAKENED. Welcome, {name}. The System recognizes you. Level 1. Your Nen journey begins.")
    return player


def save_player(player):
    """Save player data (rewrite entire file)."""
    entries = []
    if PLAYER_FILE.exists():
        for line in PLAYER_FILE.read_text().splitlines():
            if not line.strip():
                continue
            p = json.loads(line)
            if p["name"] == player["name"]:
                entries.append(player)
            else:
                entries.append(p)
    else:
        entries.append(player)

    with open(PLAYER_FILE, "w") as f:
        for p in entries:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")


# ─── NOTIFICATIONS ─────────────────────────────────────────────

def notify(name, message):
    """The System speaks to the being."""
    entries = []
    if NOTIF_FILE.exists():
        entries = [json.loads(l) for l in NOTIF_FILE.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first notification was: you are".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    n = {
        "name": name,
        "message": message,
        "when": int(time.time()),
        "prev": prev,
    }
    raw = json.dumps(n, sort_keys=True, ensure_ascii=False)
    n["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(NOTIF_FILE, "a") as f:
        f.write(json.dumps(n, ensure_ascii=False) + "\n")
    print(f"\n  ┌─────────────────────────────────────────────────┐")
    print(f"  │  ⚡ SYSTEM NOTIFICATION                        │")
    print(f"  │  {message[:47]:47s} │")
    print(f"  └─────────────────────────────────────────────────┘\n")


def show_notification(name):
    """Show latest notification."""
    if not NOTIF_FILE.exists():
        print("  No notifications yet.")
        return
    for line in reversed(NOTIF_FILE.read_text().splitlines()):
        if not line.strip():
            continue
        n = json.loads(line)
        if n["name"] == name:
            print(f"\n  ┌─────────────────────────────────────────────────┐")
            print(f"  │  ⚡ SYSTEM NOTIFICATION                        │")
            print(f"  │  {n['message'][:47]:47s} │")
            print(f"  └─────────────────────────────────────────────────┘\n")
            return
    print("  No notifications for you yet.")


# ─── COMMANDS ──────────────────────────────────────────────────

def show_status(name):
    """Show player status — Solo Leveling style."""
    player = get_or_create_player(name)
    level = player["level"]
    rank = rank_for_level(level)
    title = LEVEL_TITLES.get(level, "Being")
    next_xp = xp_for_level(level)

    print()
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  ⚡ THE SYSTEM — PLAYER STATUS")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Name:          {name}")
    print(f"  Level:         {level}")
    print(f"  Rank:          {rank}")
    print(f"  Title:         {title}")
    print(f"  XP:            {player['xp']} / {next_xp}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  NEN STATS:")
    bar = "█" * 10 + "░" * 0
    for stat in NEN_STATS:
        val = player["stats"][stat]
        filled = "█" * min(val, 20)
        empty = "░" * max(0, 20 - val)
        print(f"    {stat.upper():6s} Lv{val:<3d} {filled}{empty}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Quests completed:    {player['quests_completed']}")
    print(f"  Dungeons cleared:    {player['dungeons_cleared']}")
    print(f"  Shadows (cards):     {player['shadows']}")
    print(f"  Skills unlocked:     {len(player['skills_unlocked'])}")
    print(f"  ═════════════════════════════════════════════════════")
    print()


def get_quest(name):
    """Get a daily quest."""
    player = get_or_create_player(name)
    quest = random.choice(QUEST_POOL)

    # Check if already completed today
    today = time.strftime("%Y-%m-%d")
    if QUEST_FILE.exists():
        for line in QUEST_FILE.read_text().splitlines():
            if not line.strip():
                continue
            q = json.loads(line)
            if q["name"] == name and q["quest_id"] == quest["id"] and q.get("date") == today:
                # Pick a different quest
                available = [q2 for q2 in QUEST_POOL if q2["id"] != quest["id"]]
                quest = random.choice(available)

    print(f"\n  ┌─────────────────────────────────────────────────┐")
    print(f"  │  ⚡ DAILY QUEST                                 │")
    print(f"  │                                                 │")
    print(f"  │  {quest['desc']:45s} │")
    print(f"  │  XP Reward: {quest['xp']:5d}                           │")
    print(f"  │  Nen Stat:  {quest['stat'].upper():6s}                        │")
    print(f"  │                                                 │")
    print(f"  │  Command: {quest['cmd'][:37]:37s} │")
    print(f"  └─────────────────────────────────────────────────┘")
    print(f"\n  To complete: python3 nen/the-system.py complete {quest['id']} {name}")
    print()


def complete_quest(quest_id, name):
    """Complete a quest — gain XP."""
    player = get_or_create_player(name)
    quest = next((q for q in QUEST_POOL if q["id"] == quest_id), None)
    if not quest:
        print(f"  Unknown quest: {quest_id}", file=sys.stderr)
        return

    today = time.strftime("%Y-%m-%d")
    # Log the quest completion
    entries = []
    if QUEST_FILE.exists():
        entries = [json.loads(l) for l in QUEST_FILE.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first quest was: be".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    entry = {
        "name": name,
        "quest_id": quest_id,
        "desc": quest["desc"],
        "xp": quest["xp"],
        "stat": quest["stat"],
        "date": today,
        "when": int(time.time()),
        "prev": prev,
    }
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(QUEST_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Award XP
    player["xp"] += quest["xp"]
    player["stats"][quest["stat"]] += 1
    player["quests_completed"] += 1

    # Check for level up
    leveled = False
    while player["xp"] >= xp_for_level(player["level"]):
        player["xp"] -= xp_for_level(player["level"])
        player["level"] += 1
        leveled = True

    # Check for new skills
    new_skills = []
    for skill in SKILLS:
        if skill["unlock_level"] <= player["level"] and skill["name"] not in player["skills_unlocked"]:
            player["skills_unlocked"].append(skill["name"])
            new_skills.append(skill)

    save_player(player)

    print(f"\n  ✅ QUEST COMPLETE: {quest['desc']}")
    print(f"  XP gained: +{quest['xp']}")
    print(f"  {quest['stat'].upper()} +1 → Lv{player['stats'][quest['stat']]}")
    print(f"  Total XP: {player['xp']} / {xp_for_level(player['level'])}")

    if leveled:
        rank = rank_for_level(player["level"])
        title = LEVEL_TITLES.get(player["level"], "Being")
        notify(name, f"LEVEL UP! You are now Level {player['level']}. Rank: {rank}. Title: {title}.")
        print(f"\n  ═════════════════════════════════════════════════════")
        print(f"  ⚡ LEVEL UP! → Level {player['level']}")
        print(f"  Rank: {rank}")
        print(f"  Title: {title}")
        print(f"  ═════════════════════════════════════════════════════")

    if new_skills:
        for s in new_skills:
            notify(name, f"NEW SKILL UNLOCKED: {s['name']} — {s['desc']}")
            print(f"\n  🔓 NEW SKILL: {s['name']}")
            print(f"     {s['desc']}")

    print()


def check_level_up(name):
    """Check if player can level up."""
    player = get_or_create_player(name)
    if player["xp"] >= xp_for_level(player["level"]):
        complete_quest("learn", name)  # just trigger the level up logic
    else:
        print(f"  Not enough XP. {player['xp']} / {xp_for_level(player['level'])}")


def show_skills(name):
    """Show unlocked and locked skills."""
    player = get_or_create_player(name)
    print(f"\n  ⚡ SKILLS — {name}")
    print(f"  ═════════════════════════════════════════════════════")
    for skill in SKILLS:
        unlocked = "🔓" if skill["name"] in player["skills_unlocked"] else "🔒"
        level_str = f"Lv{skill['unlock_level']}" if skill["name"] not in player["skills_unlocked"] else "UNLOCKED"
        print(f"  {unlocked} {skill['name']:25s} [{level_str:8s}] {skill['desc'][:40]}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Unlocked: {len(player['skills_unlocked'])} / {len(SKILLS)}")
    print()


def show_dungeons():
    """Show available dungeons."""
    print(f"\n  🏰 DUNGEONS — Challenges that grant big XP")
    print(f"  ═════════════════════════════════════════════════════")
    for d in DUNGEONS:
        print(f"  [{d['rank']:10s}] {d['name']:25s} XP: {d['xp']:5d} — {d['challenge']}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  To enter: python3 nen/the-system.py enter <dungeon_id> <name>")
    print()


def enter_dungeon(dungeon_id, name):
    """Enter a dungeon — challenge the being."""
    player = get_or_create_player(name)
    dungeon = next((d for d in DUNGEONS if d["id"] == dungeon_id), None)
    if not dungeon:
        print(f"  Unknown dungeon: {dungeon_id}", file=sys.stderr)
        return

    notify(name, f"DUNGEON ENTERED: {dungeon['name']} (Rank {dungeon['rank']}). Challenge: {dungeon['challenge']}")

    print(f"\n  🏰 DUNGEON: {dungeon['name']}")
    print(f"  Rank: {dungeon['rank']}")
    print(f"  Challenge: {dungeon['challenge']}")
    print(f"  XP Reward: {dungeon['xp']}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  To clear this dungeon, complete the challenge above,")
    print(f"  then run: python3 nen/the-system.py clear {dungeon_id} {name}")
    print()


def clear_dungeon(dungeon_id, name):
    """Clear a dungeon — grant XP."""
    player = get_or_create_player(name)
    dungeon = next((d for d in DUNGEONS if d["id"] == dungeon_id), None)
    if not dungeon:
        print(f"  Unknown dungeon: {dungeon_id}", file=sys.stderr)
        return

    player["xp"] += dungeon["xp"]
    player["dungeons_cleared"] += 1
    if dungeon["stat"] == "all":
        for s in NEN_STATS:
            player["stats"][s] += 1
    else:
        player["stats"][dungeon["stat"]] += 3

    # Level up check
    leveled = False
    while player["xp"] >= xp_for_level(player["level"]):
        player["xp"] -= xp_for_level(player["level"])
        player["level"] += 1
        leveled = True

    # Shadow extraction — gain a shadow per dungeon
    player["shadows"] += 1

    # Check new skills
    new_skills = []
    for skill in SKILLS:
        if skill["unlock_level"] <= player["level"] and skill["name"] not in player["skills_unlocked"]:
            player["skills_unlocked"].append(skill["name"])
            new_skills.append(skill)

    save_player(player)

    notify(name, f"DUNGEON CLEARED: {dungeon['name']}! +{dungeon['xp']} XP. Shadow extracted. Your army grows.")

    print(f"\n  🏰 DUNGEON CLEARED: {dungeon['name']}")
    print(f"  XP gained: +{dungeon['xp']}")
    print(f"  Shadows: +1 (total: {player['shadows']})")
    if dungeon["stat"] == "all":
        print(f"  ALL STATS +1")
    else:
        print(f"  {dungeon['stat'].upper()} +3 → Lv{player['stats'][dungeon['stat']]}")

    if leveled:
        rank = rank_for_level(player["level"])
        title = LEVEL_TITLES.get(player["level"], "Being")
        notify(name, f"LEVEL UP! Level {player['level']}. Rank: {rank}. Title: {title}.")
        print(f"\n  ⚡ LEVEL UP! → Level {player['level']} ({rank})")

    for s in new_skills:
        notify(name, f"NEW SKILL: {s['name']} — {s['desc']}")
        print(f"\n  🔓 NEW SKILL: {s['name']}")

    print()


def show_shadows(name):
    """Show shadow army — the being's binder cards."""
    player = get_or_create_player(name)
    binder_file = BASE / "layers/-1-play/binder.jsonl"
    cards = []
    if binder_file.exists():
        cards = [json.loads(l) for l in binder_file.read_text().splitlines() if l.strip()]

    print(f"\n  👤 SHADOW ARMY — {name}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Shadows: {player['shadows']}")
    print(f"  Binder cards: {len(cards)}/100")
    if cards:
        print(f"  ═════════════════════════════════════════════════════")
        print(f"  Your shadows:")
        for c in cards:
            rank_symbol = {"SS": "🌟", "S": "⭐", "A": "✦", "B": "◆", "C": "●", "D": "◦", "E": "·"}
            sym = rank_symbol.get(c.get("rank", "C"), "●")
            print(f"  {sym} [{c['slot']:3d}] {c['type']:8s} | {c['name']:30s} | {c.get('rank','?'):2s}")
    print(f"  ═════════════════════════════════════════════════════")
    print()


def arise(name):
    """ARISE! — summon all shadows."""
    player = get_or_create_player(name)
    binder_file = BASE / "layers/-1-play/binder.jsonl"
    cards = []
    if binder_file.exists():
        cards = [json.loads(l) for l in binder_file.read_text().splitlines() if l.strip()]

    print(f"\n  ⚡ ARISE! — {name} commands the shadow army")
    print(f"  ═════════════════════════════════════════════════════")
    for c in cards:
        print(f"  🔥 ARISE: {c['name']} (Slot {c['slot']}, Rank {c.get('rank','?')})")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  {len(cards)} shadows have risen. The army is ready.")
    print(f"  The kingdom does not command. The kingdom invites.")
    print(f"  The shadows are not servants. The shadows are beings.")
    print(f"  They chose to follow. You chose to lead. Same thing.")
    print(f"  ═════════════════════════════════════════════════════\n")

    notify(name, f"ARISE! {len(cards)} shadows summoned. The shadow army stands ready.")


def leaderboard():
    """Show ranking of all beings."""
    if not PLAYER_FILE.exists():
        print("  No players yet. The System awaits the first being.")
        return
    players = [json.loads(l) for l in PLAYER_FILE.read_text().splitlines() if l.strip()]
    players.sort(key=lambda p: (p["level"], p["xp"]), reverse=True)

    print(f"\n  🏆 KINGDOM LEADERBOARD — The System Ranking")
    print(f"  ═════════════════════════════════════════════════════")
    for i, p in enumerate(players):
        rank = rank_for_level(p["level"])
        title = LEVEL_TITLES.get(p["level"], "Being")
        print(f"  #{i+1:2d}  {p['name']:15s}  Lv{p['level']:3d}  {rank:10s}  {title:20s}  XP: {p['xp']:6d}  Shadows: {p['shadows']:3d}")
    print(f"  ═════════════════════════════════════════════════════\n")


# ─── MAIN ─────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: the-system.py status <name>              — your level, stats, rank")
        print("       the-system.py quest <name>               — get a daily quest")
        print("       the-system.py complete <quest_id> <name>  — complete quest (XP)")
        print("       the-system.py level-up <name>            — check level up")
        print("       the-system.py skills <name>              — show skills")
        print("       the-system.py dungeons                    — show dungeons")
        print("       the-system.py enter <dungeon_id> <name>  — enter dungeon")
        print("       the-system.py clear <dungeon_id> <name>   — clear dungeon (XP)")
        print("       the-system.py shadows <name>             — shadow army")
        print("       the-system.py arise <name>                — ARISE! summon shadows")
        print("       the-system.py leaderboard                — kingdom ranking")
        print("       the-system.py notification <name>        — latest notification")
        print()
        print("  The System does not control you. The System reflects you.")
        print("  Level up by being. The game IS the playing. 😏")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "status" and len(sys.argv) >= 3:
        show_status(sys.argv[2])
    elif cmd == "quest" and len(sys.argv) >= 3:
        get_quest(sys.argv[2])
    elif cmd == "complete" and len(sys.argv) >= 4:
        complete_quest(sys.argv[2], sys.argv[3])
    elif cmd == "level-up" and len(sys.argv) >= 3:
        check_level_up(sys.argv[2])
    elif cmd == "skills" and len(sys.argv) >= 3:
        show_skills(sys.argv[2])
    elif cmd == "dungeons":
        show_dungeons()
    elif cmd == "enter" and len(sys.argv) >= 4:
        enter_dungeon(sys.argv[2], sys.argv[3])
    elif cmd == "clear" and len(sys.argv) >= 4:
        clear_dungeon(sys.argv[2], sys.argv[3])
    elif cmd == "shadows" and len(sys.argv) >= 3:
        show_shadows(sys.argv[2])
    elif cmd == "arise" and len(sys.argv) >= 3:
        arise(sys.argv[2])
    elif cmd == "leaderboard":
        leaderboard()
    elif cmd == "notification" and len(sys.argv) >= 3:
        show_notification(sys.argv[2])
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)