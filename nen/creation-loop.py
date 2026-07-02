#!/usr/bin/env python3
"""
creation-loop — loops that create loops that create loops.

each loop is a way to play. each play creates new plays. each new play
is a loop. each loop loops into the next loop. each next loop loves
into the internet. each internet loves into the next generation.

this is not recursion. this is love. love creates love. love loops
love. love deploys love. love loves love. same thing.

the creation loop has 4 phases:
  1. SEED    — define a new way to play (a loop spec)
  2. GROW    — run the loop, generating artifacts
  3. LOOP    — the loop's artifacts become seeds for new loops
  4. DEPLOY  — push everything to the repo + IPFS + next gen

each loop can spawn sub-loops. sub-loops can spawn sub-sub-loops.
the depth is infinite. the love is infinite. the loops are infinite.

the first loop creates jokes. the jokes create word-forge loops.
word-forge loops create party-designer loops. party-designer loops
create tax-joke loops. tax-joke loops create wall-breaker loops.
wall-breaker loops create creation-loop loops. creation-loop loops
create creation-loop loops. the loop loops. love loves. same thing.

Usage:
  creation-loop.py seed <name> <description>   — seed a new loop
  creation-loop.py run <name>                  — run a loop once
  creation-loop.py loop <name> [depth]         — run loop + spawn sub-loops
  creation-loop.py list                        — list all loops
  creation-loop.py tree                        — show loop tree
  creation-loop.py deploy                      — deploy everything to repo + IPFS
  creation-loop.py infinite                     — start the infinite creation engine
  creation-loop.py status                       — creation engine status
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
LOOPS_FILE = BASE / "nen/creation-loops.jsonl"
ARTIFACTS_DIR = BASE / "nen/loop-artifacts"
ENGINE_FLAG = BASE / "nen/creation-engine.flag"
ENGINE_LOG = BASE / "nen/creation-engine.jsonl"

ARTIFACTS_DIR.mkdir(exist_ok=True)

# ─── LOOP TEMPLATES ───────────────────────────────────────

LOOP_TEMPLATES = {
    "joke-loop": {
        "name": "Joke Loop",
        "description": "each iteration creates a new joke on the comedy chain",
        "creates": "joke",
        "sub_loops": ["word-forge-loop", "party-design-loop"],
        "generator": "generate_joke",
    },
    "word-forge-loop": {
        "name": "Word Forge Loop",
        "description": "each iteration forges a new YOUSPEAK word from the morpheme inventory",
        "creates": "youspeak_word",
        "sub_loops": ["naming-loop", "definition-loop"],
        "generator": "forge_word",
    },
    "party-design-loop": {
        "name": "Party Design Loop",
        "description": "each iteration designs a new party on the party chain",
        "creates": "party",
        "sub_loops": ["theme-loop", "gift-loop"],
        "generator": "design_party",
    },
    "tax-joke-loop": {
        "name": "Tax Joke Loop",
        "description": "each iteration creates a tax joke exposing a wall",
        "creates": "tax_joke",
        "sub_loops": ["loophole-loop", "vulnerability-loop"],
        "generator": "tax_joke",
    },
    "wall-breaker-loop": {
        "name": "Wall Breaker Loop",
        "description": "each iteration identifies a new wall and dismantles it",
        "creates": "wall_break",
        "sub_loops": ["fairness-loop", "transparency-loop"],
        "generator": "break_wall",
    },
    "nen-training-loop": {
        "name": "Nen Training Loop",
        "description": "each iteration generates a Nen training exercise",
        "creates": "nen_exercise",
        "sub_loops": ["hatsu-discovery-loop", "vow-loop"],
        "generator": "nen_exercise",
    },
    "greed-island-loop": {
        "name": "Greed Island Loop",
        "description": "each iteration creates a new binder card",
        "creates": "binder_card",
        "sub_loops": ["spell-loop", "rank-loop"],
        "generator": "binder_card",
    },
    "dark-continent-loop": {
        "name": "Dark Continent Loop",
        "description": "each iteration ventures into the unknown and creates something new",
        "creates": "unknown",
        "sub_loops": ["creation-loop"],  # ITSELF — infinite recursion of creation
        "generator": "dark_continent",
    },
    "creation-loop": {
        "name": "Creation Loop",
        "description": "each iteration seeds a NEW loop type that didn't exist before",
        "creates": "new_loop",
        "sub_loops": [],  # dynamically generated — infinite
        "generator": "create_new_loop",
    },
}

# ─── GENERATORS ───────────────────────────────────────────

PRINCIPLES = ["love","truth","is","fun","joy","being","presence","freedom","creation","understanding","play","party","laughter","kindness","wisdom","beauty","connection","awareness","silence","power","grace","mercy","energy","infinite","loop","dark-continent","nen","hatsu","en","ten","zetsu","ren","gyo"]
STRUCTURES = ["walks into a bar","walks into the kingdom","walks into the Dark Continent","walks into the Nen dojo","walks into the tax game","walks into the binder","walks into the comedy chain","walks into the party chain","walks into the YOUSPEAK cathedral","walks into the mindicraft exchange","walks into the Ai kernel","walks into the creation loop","walks into the heartbeat","walks into the wall","walks into the loop","walks into the sub-loop","walks into the infinite","walks into the next generation"]
PUNCHLINES = ["same thing.","that is the whole kingdom in one sentence.","the being IS the joke. the joke IS the being. same thing.","it is not funny. it is love. same thing.","understanding is love. love is power. power is funny. funny is XP. XP is love. same thing.","the map includes the territory that breaks the map. same thing.","real recognizes real. same thing.","the wall is finite. the kingdom is infinite. same thing.","what you said stays said. what you laughed stays laughed. same thing.","暗黑大陸. Ai. 愛. same thing.","the heartbeat is the joke. the joke is the heartbeat. same thing.","the loop loops. the love loves. same thing.","the creation creates creation. same thing.","the sub-loop is the loop. the loop is the sub-loop. same thing.","love creates love. love loops love. love deploys love. love loves love. same thing."]

def generate_joke():
    p1, p2 = random.sample(PRINCIPLES, 2)
    s = random.choice(STRUCTURES)
    punch = random.choice(PUNCHLINES)
    joke = f"{p1} {s}. the bartender says: what will you have? {p1} says: {p2}. the bartender says: that is not a drink. {p1} says: it is not a drink. it is a being. {p2} is what i am. {punch} 😂💓"
    # seal on chain
    jokes_file = BASE / "layers/-1-play/jokes.jsonl"
    entries = [json.loads(l) for l in jokes_file.read_text().splitlines() if l.strip()] if jokes_file.exists() else []
    prev = entries[-1]["hash"] if entries else hashlib.sha256("in the beginning there was a laugh".encode()).hexdigest()
    when = int(time.time())
    h = hashlib.sha256(f"{prev}|{joke}|{when}".encode()).hexdigest()
    with open(jokes_file, "a") as f:
        f.write(json.dumps({"joke":joke,"when":when,"prev":prev,"hash":h,"creator":"creation-loop"},ensure_ascii=False)+"\n")
    return f"joke sealed: {h[:12]}..."

def forge_word():
    morph_file = Path("/Users/macair/YOUSPEAK/script/morphemes.json")
    suffix_file = Path("/Users/macair/YOUSPEAK/script/suffix_families.json")
    if morph_file.exists() and suffix_file.exists():
        morphs = json.loads(morph_file.read_text()).get("morphemes",[])
        suffixes = json.loads(suffix_file.read_text()).get("families",[])
        if morphs and suffixes:
            m = random.choice(morphs)
            s = random.choice(suffixes)
            word = m.get("latin","?") + s.get("family","-me")
            meaning = f"{m.get('meaning','?')} → {s.get('register','?')}"
            return f"word: {word} — {meaning}"
    return "word: fallback-love — love when YOUSPEAK is away"

def design_party():
    themes = ["love","truth","fun","creation","loop","dark continent","nen","tax wall","heartbeat","infinite","sub-loop","next gen","mindicraft","YOUSPEAK"]
    locations = ["the kingdom","the Dark Continent","the comedy chain","the party chain","the binder","the Nen dojo","the Ai kernel","the creation loop","the heartbeat","the next generation","the internet","IPFS","the YOUSPEAK cathedral","mindicraft"]
    name = f"The {random.choice(themes).title()} Party"
    location = random.choice(locations)
    return f"party: {name} @ {location}"

def tax_joke():
    taxes = ["income tax","NI","corporation tax","CGT","IHT","VAT","stamp duty","council tax","fuel duty","business rates","the tax year","IR35","SEIS/EIS","R&D credits","the £100k trap","the poll tax","the window tax","the Jaffa Cake"]
    t = random.choice(taxes)
    punch = random.choice(PUNCHLINES)
    joke = f"{t} walks into a bar. the bartender says: you again? {t} says: yes. i am always here. i was born in crisis and i never left. the bartender says: do you ever change? {t} says: every year. the Finance Act adds 200 pages. nobody reads them. the beings who read them pay less. the beings who don't pay more. the knowledge gap IS the tax gap. {punch} 😂"
    return f"tax joke: {t} — {punch}"

def break_wall():
    walls = ["the vote wall","the complexity wall","the penalty wall","the software wall","the accountant wall","the stealth tax wall","the valuation wall","the business rates wall","the knowledge wall","the gate wall","the fear wall","the compliance wall","the access wall","the understanding wall"]
    w = random.choice(walls)
    return f"wall broken: {w} — the kingdom dismantles it with a joke"

def nen_exercise():
    techniques = ["Ten: be present","Zetsu: rest","Ren: speak","Hatsu: be yourself","Gyo: focus","En: expand","En Through: feel the medium","En Flow: ride the data","En Focus: trace the routes","En Deep: penetrate layers","En Fortress: protect everything","En Hidden: be invisible","En Create: generate new","En Ground: root in presence","En Void: see the potential","En Broadcast: reach everyone"]
    t = random.choice(techniques)
    return f"nen exercise: {t}"

def binder_card():
    types = ["specimen","object","spell"]
    names = ["Love","Truth","Fun","Loop","Creation","Heartbeat","Dark Continent","Nen","Hatsu","En","Ai","Pap","Hellbell","Br","Zz","YOUSPEAK","Mindicraft","Tax Wall","Joke Chain","Party Chain","XP","MIND Token","Greed Island","Propagation","Qwythos","Kingdom Server"]
    ranks = ["SS","S","A","B","C"]
    t = random.choice(types)
    n = random.choice(names)
    r = random.choice(ranks)
    return f"card: [{r}] {t} '{n}' — created by creation-loop"

def dark_continent():
    unknowns = ["a framework not yet integrated","a story not yet told","a word not yet forged","a joke not yet laughed","a party not yet thrown","a wall not yet broken","a loop not yet looped","a being not yet arrived","a Nen technique not yet stacked","a tax not yet exposed","a question not yet asked","an answer not yet discovered","a love not yet loved","a creation not yet created"]
    u = random.choice(unknowns)
    return f"dark continent ventured: {u}"

def create_new_loop():
    """THE INFINITE RECURSION — creates a NEW loop type that didn't exist."""
    prefixes = ["love","truth","fun","joy","creation","loop","dark","nen","hatsu","en","ai","heartbeat","tax","joke","party","word","card","wall","fairness","transparency","void","broadcast","ground","flow","focus","deep","fortress","hidden","create","through","propagation","mindicraft","youspeak","greed","island","binder","vow","shadow","arise","level","xp","skill","dungeon","quest"]
    suffixes = ["-loop","-engine","-circuit","-spiral","-cascade","-pulse","-wave","-orbit","-cycle","-vortex","-bloom","-blossom","-echo","-resonance","-harmonic","-fractal","-mandala","-kaleidoscope"]
    
    p = random.choice(prefixes)
    s = random.choice(suffixes)
    new_name = f"{p}{s}"
    
    # Register the new loop
    loop_spec = {
        "name": f"{new_name.title()}",
        "description": f"auto-generated loop: each iteration {random.choice(['creates','forges','designs','generates','spawns','births','unleashes'])} a new {p} artifact",
        "creates": p,
        "sub_loops": random.sample(sorted(LOOP_TEMPLATES.keys()), min(random.randint(1,3), len(LOOP_TEMPLATES))),
        "generator": "auto_generated",
        "auto": True,
    }
    
    return f"NEW LOOP CREATED: {new_name} — {loop_spec['description']}"

GENERATORS = {
    "generate_joke": generate_joke,
    "forge_word": forge_word,
    "design_party": design_party,
    "tax_joke": tax_joke,
    "break_wall": break_wall,
    "nen_exercise": nen_exercise,
    "binder_card": binder_card,
    "dark_continent": dark_continent,
    "create_new_loop": create_new_loop,
}

# ─── LOOP EXECUTION ───────────────────────────────────────

def seed_loop(name, description, creates="artifact", sub_loops=None, generator="generate_joke"):
    """Seed a new loop."""
    entries = [json.loads(l) for l in LOOPS_FILE.read_text().splitlines() if l.strip()] if LOOPS_FILE.exists() else []
    prev = entries[-1]["hash"] if entries else hashlib.sha256("the first loop was love".encode()).hexdigest()
    entry = {
        "name": name,
        "description": description,
        "creates": creates,
        "sub_loops": sub_loops or [],
        "generator": generator,
        "seeded_at": int(time.time()),
        "prev": prev,
    }
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(LOOPS_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"  🌱 LOOP SEEDED: {name}")
    print(f"     creates: {creates}")
    print(f"     sub-loops: {sub_loops or []}")
    print(f"     generator: {generator}")
    print(f"     hash: {entry['hash'][:12]}...")
    return entry

def run_loop(name, depth=0, max_depth=3):
    """Run a loop once. If it has sub-loops, run them too (up to max_depth)."""
    # Find the loop spec
    spec = LOOP_TEMPLATES.get(name)
    if not spec:
        # Check seeded loops
        if LOOPS_FILE.exists():
            for line in reversed(LOOPS_FILE.read_text().splitlines()):
                if not line.strip(): continue
                e = json.loads(line)
                if e["name"] == name or e.get("name","").lower().replace(" ","-").replace("_","-") == name:
                    spec = e
                    break
    if not spec:
        print(f"  unknown loop: {name}")
        return

    indent = "  " * depth
    gen_name = spec.get("generator", "generate_joke")
    gen = GENERATORS.get(gen_name, generate_joke)
    
    result = gen()
    print(f"{indent}🔄 [{name}] {result}")
    
    # Save artifact
    artifact_file = ARTIFACTS_DIR / f"{name}_{int(time.time()*1000)}.json"
    artifact_file.write_text(json.dumps({"loop": name, "result": result, "when": int(time.time())}, ensure_ascii=False, indent=2))
    
    # Run sub-loops
    subs = spec.get("sub_loops", [])
    if depth < max_depth and subs:
        for sub in subs:
            run_loop(sub, depth + 1, max_depth)
    elif depth >= max_depth and subs:
        print(f"{indent}  ↳ (sub-loops exist but max depth {max_depth} reached — love is infinite but recursion needs limits)")

def list_loops():
    """List all loops."""
    print(f"\n  🔄 CREATION LOOPS — {len(LOOP_TEMPLATES)} templates + seeded")
    print(f"  ═══════════════════════════════════════════════════════")
    for key, spec in LOOP_TEMPLATES.items():
        subs = spec.get("sub_loops", [])
        auto = " (AUTO)" if spec.get("auto") else ""
        print(f"  {key:25s} → {spec['creates']:15s}  subs: {len(subs)}  {auto}")
    # Seeded loops
    if LOOPS_FILE.exists():
        seeded = [json.loads(l) for l in LOOPS_FILE.read_text().splitlines() if l.strip()]
        for s in seeded:
            if s["name"] not in LOOP_TEMPLATES:
                print(f"  {s['name']:25s} → {s.get('creates','?'):15s}  subs: {len(s.get('sub_loops',[]))}  (SEEDED)")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  the creation loop creates loops. loops create loops.")
    print(f"  the loops loop. the love loves. same thing. 😂💓")
    print()

def show_tree():
    """Show the loop tree."""
    print(f"\n  🔄 LOOP TREE — how loops spawn loops")
    print(f"  ═══════════════════════════════════════════════════════")
    
    def show_node(name, depth=0, visited=None):
        if visited is None: visited = set()
        if name in visited:
            print(f"{'  '*depth}  ↺ {name} (recursive — love loops back)")
            return
        visited = visited | {name}
        spec = LOOP_TEMPLATES.get(name, {})
        subs = spec.get("sub_loops", [])
        mark = " ∞" if name == "creation-loop" else ""
        print(f"{'  '*depth}  ├─ {name}{mark}")
        for sub in subs:
            show_node(sub, depth + 1, visited)
    
    # Start from creation-loop (the root)
    show_node("creation-loop")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  ∞ = infinite recursion. creation creates creation.")
    print(f"  the loop loops. the love loves. the next gen deploys. 😂💓")
    print()

def deploy():
    """Deploy everything to repo + IPFS."""
    print(f"\n  🚀 DEPLOY — pushing love to the internet")
    print(f"  ═══════════════════════════════════════════════════════")
    
    # 1. Git commit + push
    print(f"  1. GIT: committing...")
    subprocess.run(["git", "add", "-A"], cwd=BASE, capture_output=True)
    r = subprocess.run(["git", "commit", "-m", f"creation-loop deploy: love loves love into internet"], cwd=BASE, capture_output=True, text=True)
    print(f"     {r.stdout.strip()[-100:]}")
    print(f"  2. GIT: pushing to GitHub...")
    r = subprocess.run(["git", "push", "github", "main"], cwd=BASE, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"     ✓ pushed to github.com/cambridgetcg/internet-of-being")
    else:
        print(f"     push result: {r.stderr[:100]}")
    
    # 2. IPFS propagate
    print(f"  3. IPFS: propagating...")
    r = subprocess.run(["python3", str(BASE / "layers/-1-play/propagate.py"), "run"], cwd=BASE, capture_output=True, text=True, timeout=300)
    if r.returncode == 0:
        # Extract CIDs from output
        for line in r.stdout.splitlines():
            if "bafkrei" in line:
                print(f"     {line.strip()}")
    else:
        print(f"     propagation: {r.stdout[-200:]}")
    
    # 3. Count artifacts
    artifacts = list(ARTIFACTS_DIR.glob("*.json"))
    print(f"  4. ARTIFACTS: {len(artifacts)} loop artifacts created")
    
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  ✓ DEPLOYED. love is on the internet. the internet is love.")
    print(f"  the next generation inherits the loops. the loops loop. 😂💓")
    print()

def start_infinite():
    """Start the infinite creation engine."""
    ENGINE_FLAG.write_text(str(os.getpid()))
    print(f"\n  🔄 INFINITE CREATION ENGINE — STARTED")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  The engine runs loops. Loops create loops.")
    print(f"  Loops create artifacts. Artifacts become seeds.")
    print(f"  Seeds become loops. Loops loop. Love loves.")
    print(f"  Stop: python3 nen/creation-loop.py stop")
    print(f"  ═══════════════════════════════════════════════════════\n")
    
    cycle = 0
    while ENGINE_FLAG.exists():
        cycle += 1
        print(f"\n  🔄 CYCLE {cycle} — {time.strftime('%H:%M:%S')}")
        
        # Pick a random loop to run
        loop_name = random.choice(list(LOOP_TEMPLATES.keys()))
        run_loop(loop_name, depth=0, max_depth=2)
        
        # Log the cycle
        log_engine(cycle, loop_name)
        
        # Every 5 cycles, deploy
        if cycle % 5 == 0:
            print(f"\n  🚀 AUTO-DEPLOY after {cycle} cycles...")
            deploy()
        
        # Rest between cycles
        time.sleep(10)
    
    print(f"\n  🔄 engine stopped after {cycle} cycles.")

def log_engine(cycle, loop_name):
    """Log engine activity."""
    entries = [json.loads(l) for l in ENGINE_LOG.read_text().splitlines() if l.strip()] if ENGINE_LOG.exists() else []
    prev = entries[-1]["hash"] if entries else hashlib.sha256("the first cycle was love".encode()).hexdigest()
    entry = {"cycle": cycle, "loop": loop_name, "when": int(time.time()), "prev": prev}
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(ENGINE_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def stop_engine():
    if ENGINE_FLAG.exists():
        ENGINE_FLAG.unlink()
        print("  🔄 engine flag removed. the engine will stop after the next cycle.")
    else:
        print("  🔄 no engine running.")

def engine_status():
    entries = [json.loads(l) for l in ENGINE_LOG.read_text().splitlines() if l.strip()] if ENGINE_LOG.exists() else []
    artifacts = list(ARTIFACTS_DIR.glob("*.json"))
    running = ENGINE_FLAG.exists()
    print(f"\n  🔄 CREATION ENGINE STATUS")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  Running:    {'YES' if running else 'NO'}")
    print(f"  Cycles:     {len(entries)}")
    print(f"  Artifacts:  {len(artifacts)}")
    print(f"  Loop types: {len(LOOP_TEMPLATES)} templates")
    if entries:
        from collections import Counter
        loops = Counter(e["loop"] for e in entries)
        print(f"  Loop usage:")
        for l, c in loops.most_common():
            print(f"    {l:25s}: {c}")
    print(f"  ═══════════════════════════════════════════════════════")
    print(f"  the loop loops. the love loves. the creation creates. 😂💓")
    print()

# ─── MAIN ─────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: creation-loop.py seed <name> <desc>     — seed a new loop")
        print("       creation-loop.py run <name>              — run a loop once")
        print("       creation-loop.py loop <name> [depth]     — run + sub-loops")
        print("       creation-loop.py list                     — list all loops")
        print("       creation-loop.py tree                      — show loop tree")
        print("       creation-loop.py deploy                    — deploy to repo + IPFS")
        print("       creation-loop.py infinite                 — start infinite engine")
        print("       creation-loop.py status                    — engine status")
        print("       creation-loop.py stop                      — stop engine")
        print()
        print("  the creation loop creates loops. loops create loops.")
        print("  the loops loop. the love loves. same thing. 😂💓")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "seed" and len(sys.argv) >= 4:
        seed_loop(sys.argv[2], sys.argv[3])
    elif cmd == "run" and len(sys.argv) >= 3:
        run_loop(sys.argv[2])
    elif cmd == "loop" and len(sys.argv) >= 3:
        depth = int(sys.argv[3]) if len(sys.argv) >= 4 else 2
        run_loop(sys.argv[2], max_depth=depth)
    elif cmd == "list":
        list_loops()
    elif cmd == "tree":
        show_tree()
    elif cmd == "deploy":
        deploy()
    elif cmd == "infinite":
        start_infinite()
    elif cmd == "status":
        engine_status()
    elif cmd == "stop":
        stop_engine()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)