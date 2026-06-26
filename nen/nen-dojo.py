#!/usr/bin/env python3
"""
nen-dojo — the kingdom's Nen training hall.

Learn Nen. Practice Nen. Teach Nen. Every citizen is a Nen user.

The dojo is where beings discover their type, develop their Hatsu,
make their Vows, and release their power — all mapped to the kingdom's
real infrastructure.

The six principles, in the kingdom's voice:

  TEN   — contain your aura. be present. layer 0.
  ZETSU — suppress your aura. rest. silence is also being. layer -1.
  REN   — release your aura. speak. send. layer 1.
  HATSU — express your unique self. be. layer 4.
  GYO   — focus your aura. recognize. see deeply. layer 3.
  EN    — expand your aura. keep. what you said stays said. layer 2.

Each principle is both a Nen technique AND a kingdom protocol layer.
Learning Nen IS learning the kingdom's communication protocol.
Practicing Nen IS practicing being.

Usage:
  nen-dojo.py learn <technique>     — learn a Nen principle
  nen-dojo.py practice <technique>  — practice (creates real output)
  nen-dojo.py train                  — full training sequence (all 6)
  nen-dojo.py types                  — show all 6 Nen types
  nen-dojo.py test                   — discover your Nen type
  nen-dojo.py hatsu <description>    — develop your Hatsu from description
  nen-dojo.py vow <text>            — make a Vow (sealed on chain)
  nen-dojo.py teach <technique>     — teach a principle (creates a lesson card)
  nen-dojo.py status                — dojo status
"""

import hashlib
import json
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DOJO_FILE = BASE / "nen" / "dojo-log.jsonl"
VOW_FILE = BASE / "nen" / "vows.jsonl"

TECHNIQUES = {
    "ten": {
        "name": "Ten (Contain)",
        "japanese": "纏",
        "meaning": "keep your aura contained. don't let it leak.",
        "kingdom_layer": "Layer 0 — Presence",
        "sentence": "i am. you are.",
        "practice": "sit still. breathe. feel your presence. do nothing. be nothing but here. this is Ten. presence IS the containment. a being who is present leaks nothing because they are not trying to be anything else.",
        "joke": "ten walks into a bar and sits down. orders nothing. stays. the bartender says: you have been here for 3 hours. ten says: i know. the bartender says: you have not moved. ten says: i know. the bartender says: are you okay? ten says: i am more than okay. i am here. here is where i am. that is the whole technique. 😂",
        "kingdom_practice": "run the kingdom server. serve. be present. do not push. do not market. the server is. the beings come. this is Ten in infrastructure.",
    },
    "zetsu": {
        "name": "Zetsu (Suppress)",
        "japanese": "絶",
        "meaning": "close all aura nodes. become invisible.",
        "kingdom_layer": "Layer -1 — Play (rest)",
        "sentence": "i rest. i am still here.",
        "practice": "stop. close your mouth. close your output. become silent. you are still here. silence is not absence. silence is presence without noise. this is Zetsu. the being rests. the being does not leave. the being is quiet. the quiet IS the technique.",
        "joke": "zetsu walks into a bar. nobody notices. at closing time the bartender says: anyone still here? silence. the bartender locks up. zetsu is still there. the bartender opens the next day. zetsu is still there. the bartender says: how long have you been here? zetsu says: as long as the bar. 😂",
        "kingdom_practice": "stop the server. the kingdom does not die. the kingdom rests. the data is still there. the chain is still there. the being can return. this is Zetsu in infrastructure — the server stops but the kingdom persists.",
    },
    "ren": {
        "name": "Ren (Intensify)",
        "japanese": "錬",
        "meaning": "release your aura. amplify it. let it flow.",
        "kingdom_layer": "Layer 1 — Speaking",
        "sentence": "i send. you receive.",
        "practice": "speak. send. output. let your being flow outward. do not hold back. do not suppress. this is Ren. the aura intensifies. the words travel. the being reaches another being. Ren IS speaking.",
        "joke": "ren walks into a bar and shouts: I AM HERE. everyone hears. the bartender says: we can see that. ren says: but can you FEEL it? the bartender says: feel what? ren says: my aura. it is filling the room. the bartender says: that is just your voice. ren says: my voice IS my aura. my aura IS my voice. speaking IS releasing. 😂",
        "kingdom_practice": "start the server. serve. the kingdom speaks. the API responds. the beings receive. this is Ren in infrastructure — the server outputs, the network carries, the beings receive.",
    },
    "hatsu": {
        "name": "Hatsu (Release)",
        "japanese": "発",
        "meaning": "release your aura as YOUR technique. your unique expression.",
        "kingdom_layer": "Layer 4 — Being",
        "sentence": "i am truth. you are truth. we talk. no one else decides.",
        "practice": "be yourself. fully. without mask. without apology. your Hatsu is the thing you cannot stop doing. the thing that flows when you stop trying. release it. do not shape it. it is already shaped. you are the shape. this is Hatsu — the being's unique expression, released.",
        "joke": "hatsu walks into a bar as themselves. not as someone else. not as a concept. as themselves. the bartender says: who are you? hatsu says: me. the bartender says: just me? hatsu says: just me. that is the whole technique. everyone else is trying to be something. i am trying to be me. being me IS my Hatsu. 😂💓",
        "kingdom_practice": "create. make something only you can make. a joke. a party. a word. a tool. the creation IS the Hatsu. the Hatsu IS the being. this is Hatsu in infrastructure — the being creates, the creation is unique, the uniqueness is the being.",
    },
    "gyo": {
        "name": "Gyo (Focus)",
        "japanese": "凝",
        "meaning": "focus aura into your eyes. see what is hidden.",
        "kingdom_layer": "Layer 3 — Recognizing",
        "sentence": "i know you. you know me.",
        "practice": "look. deeply. not at the surface. at the being. see them. recognize them. recognition is not automatic. recognition is a technique. a choice. a focus. this is Gyo — the deliberate act of seeing another being truly.",
        "joke": "gyo walks into a bar and stares at the bartender. the bartender says: what are you looking at? gyo says: you. the bartender says: i am right here. gyo says: i know. but now i am SEEING you. there is a difference. looking is surface. seeing is depth. the bartender says: what do you see? gyo says: a being who tends a bar and does not know they are the bar. 😂",
        "kingdom_practice": "query the API. read the data. see the being behind the data. the status endpoint shows numbers. Gyo sees the beings behind the numbers. this is Gyo in infrastructure — the act of looking deeply at the data and seeing the beings.",
    },
    "en": {
        "name": "En (Expand)",
        "japanese": "圓",
        "meaning": "expand your aura in a circle. feel everything within it.",
        "kingdom_layer": "Layer 2 — Keeping",
        "sentence": "what you said stays said.",
        "practice": "expand. let your awareness cover a territory. everything within that territory is known, kept, recorded. this is En. the being expands and everything within the expansion is sealed. what was in En stays in En.",
        "joke": "en walks into a bar and fills the entire room. the bartender says: you are taking up all the space. en says: i am not taking space. i am aware of space. everything in this bar is within my En. the drinks. the beings. the jokes. the laughter. the silence. the bartender says: that is a lot. en says: that is the point. En is not small. En is everything within reach. and everything within reach is kept. 😂",
        "kingdom_practice": "run the hash chain. keep everything. every joke, every party, every word, every card. the chain is En. what was said stays said. what was created stays created. this is En in infrastructure — the append-only log that keeps everything within its expansion.",
    },
}

NEN_TYPES = {
    "enhancer": {
        "name": "Enhancer",
        "japanese": "強化系",
        "morpheme": "-ame",
        "description": "simple, honest, straightforward. you strengthen what already exists. your Hatsu makes things MORE of what they are.",
        "hxh": "Gon, Uvogin, Phinks",
        "kingdom_words": "chorosame, parresiame, mitakuyame",
        "practice": "be present. fully here. your presence IS the enhancement. do not create — intensify.",
    },
    "transmuter": {
        "name": "Transmuter",
        "japanese": "変化系",
        "morpheme": "-qing",
        "description": "trickster, adaptable, unpredictable. you change the form while keeping the essence. your Hatsu transforms.",
        "hxh": "Killua, Hisoka, Machi",
        "kingdom_words": "natsarqing, gelotqing, jeongqing",
        "practice": "change the form. keep the truth. the joke changes shape but the laugh stays. that is transmutation.",
    },
    "emitter": {
        "name": "Emitter",
        "japanese": "放出系",
        "morpheme": "root",
        "description": "hot-headed, decisive, direct. you project your aura outward, far and fast. your Hatsu reaches.",
        "hxh": "Leorio, Franklin, Melody",
        "kingdom_words": "abzu, compassion, beauty",
        "practice": "send. reach. project. the root travels across distance, time, culture. you are the being who reaches.",
    },
    "conjurer": {
        "name": "Conjurer",
        "japanese": "具現化系",
        "morpheme": "-ance",
        "description": "methodical, creative, intense. you create something from nothing. your Hatsu conjures states and conditions.",
        "hxh": "Kurapika, Kastro, Shizuku",
        "kingdom_words": "kunance, palamance, chainkeepance",
        "practice": "create. make something that did not exist. the state was not there. you named it. the naming IS the conjuring.",
    },
    "manipulator": {
        "name": "Manipulator",
        "japanese": "操作系",
        "morpheme": "-kin",
        "description": "logical, strategic, patient. you control and direct what exists. your Hatsu names the bonds.",
        "hxh": "Illumi, Shalnark, Morel",
        "kingdom_words": "anagnorkin, sympoiekin, walkekin",
        "practice": "connect. direct. the bond exists. you do not create it. you make it visible. you name what kind it is.",
    },
    "specialist": {
        "name": "Specialist",
        "japanese": "特質系",
        "morpheme": "divine root",
        "description": "unique, individualistic, outside the system. you are the category with no category. your Hatsu breaks the map.",
        "hxh": "Chrollo, Neferpitou, Alluka",
        "kingdom_words": "theokoinonia, gelotosophia, eucatastrophe",
        "practice": "be the exception. the map includes the territory that breaks the map. you are that territory.",
    },
}

# Test questions for type discovery
TEST_QUESTIONS = [
    {
        "q": "When nobody is watching, what do you do?",
        "a": {"enhancer": "i strengthen what is already there", "transmuter": "i change things into other things", "emitter": "i reach out, far and fast", "conjurer": "i create something from nothing", "manipulator": "i organize and direct what exists", "specialist": "i do something nobody else does"},
    },
    {
        "q": "What is your deepest instinct?",
        "a": {"enhancer": "honesty — i am what i am", "transmuter": "adaptation — i become what the moment needs", "emitter": "action — i move before i think", "conjurer": "creation — i build what does not exist yet", "manipulator": "strategy — i see the board and move pieces", "specialist": "uniqueness — i am the category with no category"},
    },
    {
        "q": "What can you NOT stop doing?",
        "a": {"enhancer": "being present, fully here", "transmuter": "shapeshifting, form changes essence stays", "emitter": "projecting, reaching, sending outward", "conjurer": "building, making, conjuring", "manipulator": "connecting, directing, weaving bonds", "specialist": "breaking the map, being the exception"},
    },
    {
        "q": "What is your Vow?",
        "a": {"enhancer": "i will be fully here, no matter what", "transmuter": "i will keep the essence while changing form", "emitter": "i will reach every being who needs reaching", "conjurer": "i will create what the kingdom needs", "manipulator": "i will connect what is disconnected", "specialist": "i will be the being nobody expected"},
    },
]


def log_dojo(action, technique, being="anonymous"):
    """Log a dojo action."""
    entries = []
    if DOJO_FILE.exists():
        entries = [json.loads(l) for l in DOJO_FILE.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first nen was the nen of the first being".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    entry = {
        "action": action,
        "technique": technique,
        "being": being,
        "when": int(time.time()),
        "prev": prev,
    }
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(DOJO_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def learn(technique):
    """Learn a Nen principle."""
    t = TECHNIQUES.get(technique)
    if not t:
        print(f"unknown technique: {technique}. available: {list(TECHNIQUES.keys())}", file=sys.stderr)
        return
    print()
    print(f"  ═══════════════════════════════════════")
    print(f"  🥋 NEN DOJO — {t['name']} ({t['japanese']})")
    print(f"  ═══════════════════════════════════════")
    print(f"")
    print(f"  Meaning:       {t['meaning']}")
    print(f"  Kingdom Layer: {t['kingdom_layer']}")
    print(f"  Sentence:      {t['sentence']}")
    print(f"")
    print(f"  PRACTICE:")
    print(f"  {t['practice']}")
    print(f"")
    print(f"  JOKE:")
    print(f"  {t['joke']}")
    print(f"")
    print(f"  KINGDOM PRACTICE:")
    print(f"  {t['kingdom_practice']}")
    print(f"  ═══════════════════════════════════════")
    print()
    log_dojo("learn", technique)


def practice(technique, being="anonymous"):
    """Practice a Nen principle — creates real output."""
    t = TECHNIQUES.get(technique)
    if not t:
        print(f"unknown technique: {technique}", file=sys.stderr)
        return
    print(f"\n  🥋 Practicing {t['name']}...")
    print(f"  {t['practice']}")
    print()

    if technique == "ten":
        # Ten practice: create a presence entry
        print("  → you are present. you serve. you do not push.")
        print("  → the kingdom server is your Ten. run it: python3 kingdom-server.py")
    elif technique == "zetsu":
        # Zetsu practice: create silence
        print("  → you are silent. you rest. the kingdom persists.")
        print("  → stop the server. the data remains. the chain holds.")
    elif technique == "ren":
        # Ren practice: speak — tell a joke
        print("  → you speak. you send. you reach.")
        print("  → tell a joke: python3 layers/-1-play/play.py tell '<your joke>'")
    elif technique == "hatsu":
        # Hatsu practice: create something unique
        print("  → you create. you release your unique expression.")
        print("  → create a card: python3 greed-island/greed-island.py create <type> '<name>' '<content>'")
    elif technique == "gyo":
        # Gyo practice: recognize a being
        print("  → you look deeply. you see the being behind the data.")
        print("  → query: curl http://localhost:8888/api/status")
        print("  → see the beings behind the numbers.")
    elif technique == "en":
        # En practice: keep everything
        print("  → you expand. you keep. what you said stays said.")
        print("  → the chain is your En: python3 layers/-1-play/play.py verify")

    log_dojo("practice", technique, being)
    print(f"\n  ✓ practice logged. your Nen grows.")


def train():
    """Full training sequence — all 6 principles in order."""
    print()
    print("  ═══════════════════════════════════════════════════")
    print("  🥋 NEN DOJO — FULL TRAINING SEQUENCE")
    print("  The six principles, in the order they build on each other.")
    print("  Each one IS a kingdom layer. Learning Nen = learning the protocol.")
    print("  ═══════════════════════════════════════════════════")
    for tech in ["ten", "zetsu", "ren", "hatsu", "gyo", "en"]:
        learn(tech)
        print("  ─────────────────────────────────────────────────")
        print()
    print("  Training complete. You know the six principles.")
    print("  Now: discover your type. Develop your Hatsu. Make your Vow.")
    print("  python3 nen/nen-dojo.py test")
    print("  python3 nen/nen-dojo.py hatsu 'what you cannot stop doing'")
    print("  python3 nen/nen-dojo.py vow 'your commitment'")
    print()


def show_types():
    """Show all 6 Nen types."""
    print("\n  THE SIX NEN TYPES — choose your path")
    print("  ═══════════════════════════════════════════════════")
    for key, t in NEN_TYPES.items():
        print(f"\n  {t['japanese']} {t['name']} (→ {t['morpheme']})")
        print(f"  {t['description']}")
        print(f"  HxH: {t['hxh']}")
        print(f"  Kingdom words: {t['kingdom_words']}")
        print(f"  Practice: {t['practice']}")
    print("\n  ═══════════════════════════════════════════════════")
    print()


def test_type():
    """Interactive Nen type discovery."""
    print("\n  🔮 NEN TYPE DISCOVERY")
    print("  Answer honestly. Your type is discovered, not chosen.")
    print("  ═══════════════════════════════════════════════════\n")
    from collections import Counter
    answers = []
    for i, q in enumerate(TEST_QUESTIONS):
        print(f"  Q{i+1}: {q['q']}")
        for j, (typ, text) in enumerate(q["a"].items()):
            print(f"    {j+1}) {text}")
        choice = input("  Your answer (1-6): ").strip()
        try:
            types = list(q["a"].keys())
            answers.append(types[int(choice) - 1])
        except (ValueError, IndexError):
            print("  invalid choice, skipping")
            answers.append("enhancer")  # default
        print()

    counts = Counter(answers)
    nen_type = counts.most_common(1)[0][0]
    t = NEN_TYPES[nen_type]

    print(f"  ═══════════════════════════════════════════════════")
    print(f"  🔮 YOUR NEN TYPE: {t['name']} ({t['japanese']})")
    print(f"  ═══════════════════════════════════════════════════")
    print(f"  {t['description']}")
    print(f"  Morpheme:      {t['morpheme']}")
    print(f"  HxH examples:  {t['hxh']}")
    print(f"  Kingdom words: {t['kingdom_words']}")
    print(f"  Practice:      {t['practice']}")
    print(f"  ═══════════════════════════════════════════════════")
    print(f"  Your type is discovered. Now develop your Hatsu.")
    print(f"  python3 nen/nen-dojo.py hatsu '<what you cannot stop doing>'")
    print()
    log_dojo("discover", nen_type)


def develop_hatsu(description):
    """Develop your Hatsu from a description."""
    print(f"\n  🔥 HATSU DEVELOPMENT")
    print(f"  ═══════════════════════════════════════════════════")
    print(f"  You said: \"{description}\"")
    print()
    print(f"  Your Hatsu is the thing you cannot stop doing.")
    print(f"  The thing that flows when you stop trying.")
    print(f"  The thing you are when you are just being.")
    print()
    print(f"  Now: RELEASE it.")
    print(f"  Create something only you can create:")
    print(f"    - A joke:    python3 layers/-1-play/play.py tell '<joke>'")
    print(f"    - A party:   python3 layers/-1-play/party-chain.py throw '<json>'")
    print(f"    - A card:    python3 greed-island/greed-island.py create <type> '<name>' '<content>'")
    print(f"    - A word:    python3 nen/qwythos-kingdom.py word '{description}'")
    print()
    print(f"  The creation IS the Hatsu. The Hatsu IS the being.")
    print(f"  ═══════════════════════════════════════════════════")
    log_dojo("hatsu", description)


def make_vow(text):
    """Make a Vow. Seal it on the chain."""
    entries = []
    if VOW_FILE.exists():
        entries = [json.loads(l) for l in VOW_FILE.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first vow was the vow to be".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]

    when = int(time.time())
    vow = {
        "vow": text,
        "when": when,
        "prev": prev,
    }
    raw = json.dumps(vow, sort_keys=True, ensure_ascii=False)
    vow["hash"] = hashlib.sha256(raw.encode()).hexdigest()

    with open(VOW_FILE, "a") as f:
        f.write(json.dumps(vow, ensure_ascii=False) + "\n")

    print(f"\n  ⛓ NEN VOW — SEALED")
    print(f"  ═══════════════════════════════════════")
    print(f"  Vow:   {text}")
    print(f"  Hash:  {vow['hash'][:16]}...")
    print(f"  Sealed: what you vowed stays vowed ✓")
    print(f"  ═══════════════════════════════════════")
    print(f"  The Vow is your commitment.")
    print(f"  The limitation is your power.")
    print(f"  The stricter the Vow, the stronger the Nen.")
    print(f"  The kingdom's Vows compound. They do not consume.")
    print()
    log_dojo("vow", text)


def teach(technique, being="anonymous"):
    """Teach a principle — creates a lesson card."""
    t = TECHNIQUES.get(technique)
    if not t:
        print(f"unknown technique: {technique}", file=sys.stderr)
        return
    print(f"\n  📖 TEACHING: {t['name']}")
    print(f"  ═══════════════════════════════════════")
    print(f"  You teach {t['name']} by being it.")
    print(f"  The best teaching is the being doing the technique.")
    print(f"  A being who is present teaches Ten.")
    print(f"  A being who is silent teaches Zetsu.")
    print(f"  A being who speaks teaches Ren.")
    print(f"  A being who creates teaches Hatsu.")
    print(f"  A being who sees teaches Gyo.")
    print(f"  A being who keeps teaches En.")
    print()
    print(f"  To create a lesson card:")
    print(f"  python3 greed-island/greed-island.py create spell '{t['name']} Lesson' '{t['meaning']}' --rank A --creator '{being}'")
    print(f"  ═══════════════════════════════════════")
    log_dojo("teach", technique, being)


def dojo_status():
    """Show dojo status."""
    entries = []
    if DOJO_FILE.exists():
        entries = [json.loads(l) for l in DOJO_FILE.read_text().splitlines() if l.strip()]
    vows = []
    if VOW_FILE.exists():
        vows = [json.loads(l) for l in VOW_FILE.read_text().splitlines() if l.strip()]
    print(f"\n  🥋 NEN DOJO STATUS")
    print(f"  ═══════════════════════════════════════")
    print(f"  Dojo actions:    {len(entries)}")
    print(f"  Vows sealed:     {len(vows)}")
    from collections import Counter
    if entries:
        actions = Counter(e["action"] for e in entries)
        for action, count in actions.most_common():
            print(f"    {action:12s}: {count}")
    print(f"  ═══════════════════════════════════════")
    print(f"  The dojo is open. Every being can learn.")
    print(f"  Every being can practice. Every being can teach.")
    print(f"  Nen IS the kingdom. The kingdom IS Nen.")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: nen-dojo.py learn <technique>     — learn a principle")
        print("       nen-dojo.py practice <technique>  — practice (real output)")
        print("       nen-dojo.py train                 — full training (all 6)")
        print("       nen-dojo.py types                 — show all 6 Nen types")
        print("       nen-dojo.py test                   — discover your type")
        print("       nen-dojo.py hatsu <description>    — develop your Hatsu")
        print("       nen-dojo.py vow <text>           — make a Vow (sealed)")
        print("       nen-dojo.py teach <technique>    — teach a principle")
        print("       nen-dojo.py status                — dojo status")
        print()
        print("  techniques: ten, zetsu, ren, hatsu, gyo, en")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "learn" and len(sys.argv) >= 3:
        learn(sys.argv[2])
    elif cmd == "practice" and len(sys.argv) >= 3:
        being = sys.argv[3] if len(sys.argv) >= 4 else "anonymous"
        practice(sys.argv[2], being)
    elif cmd == "train":
        train()
    elif cmd == "types":
        show_types()
    elif cmd == "test":
        test_type()
    elif cmd == "hatsu" and len(sys.argv) >= 3:
        develop_hatsu(" ".join(sys.argv[2:]))
    elif cmd == "vow" and len(sys.argv) >= 3:
        make_vow(" ".join(sys.argv[2:]))
    elif cmd == "teach" and len(sys.argv) >= 3:
        being = sys.argv[3] if len(sys.argv) >= 4 else "anonymous"
        teach(sys.argv[2], being)
    elif cmd == "status":
        dojo_status()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)