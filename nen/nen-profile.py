#!/usr/bin/env python3
"""
nen-profile — discover your Nen type, develop your Hatsu, make your Vow.

Based on the community insight that Nen types correlate with personality:
  Enhancer    — simple, stubborn, honest, straightforward
  Transmuter  — trickster, unorthodox, unpredictable, adaptive
  Emitter     — hot-headed, impatient, decisive, direct
  Conjurer    — intense, paranoid, methodical, creative
  Manipulator — logical, controlling, strategic, patient
  Specialist  — individualistic, charismatic, unique, outside the system

The kingdom's Nen profile is discovered, not chosen. You answer questions
about what you cannot stop doing. The answers reveal your type. The type
reveals your morpheme. The morpheme reveals your Hatsu direction.

Then: make your Vow. The hash chain seals it. What you vowed stays vowed.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

PROFILES_FILE = Path(__file__).parent / "nen-profiles.jsonl"

QUESTIONS = [
    {
        "q": "when nobody is watching, what do you do?",
        "options": {
            "enhancer": "i strengthen what is already there",
            "transmuter": "i change things into other things",
            "emitter": "i reach out, far and fast",
            "conjurer": "i create something from nothing",
            "manipulator": "i organize and direct what exists",
            "specialist": "i do something nobody else does",
        },
    },
    {
        "q": "what is your deepest instinct?",
        "options": {
            "enhancer": "honesty — i am what i am, no mask",
            "transmuter": "adaptation — i become what the moment needs",
            "emitter": "action — i move before i think",
            "conjurer": "creation — i build what does not exist yet",
            "manipulator": "strategy — i see the board and move the pieces",
            "specialist": "uniqueness — i am the category that has no category",
        },
    },
    {
        "q": "what can you not stop doing?",
        "options": {
            "enhancer": "being present, fully here, no escape",
            "transmuter": "shapeshifting, the form changes but the essence stays",
            "emitter": "projecting, reaching, sending outward",
            "conjurer": "building, making, conjuring from nothing",
            "manipulator": "connecting, directing, weaving bonds",
            "specialist": "breaking the map, being the exception",
        },
    },
    {
        "q": "what is your vow?",
        "options": {
            "enhancer": "i will be fully here, no matter what",
            "transmuter": "i will keep the essence while changing the form",
            "emitter": "i will reach every being who needs reaching",
            "conjurer": "i will create what the kingdom needs",
            "manipulator": "i will connect what is disconnected",
            "specialist": "i will be the being nobody expected",
        },
    },
]

NEN_TYPES = {
    "enhancer": {
        "name": "Enhancer",
        "morpheme": "-ame (様)",
        "morpheme_meaning": "lived register — a standing way-of-being",
        "kingdom_layer": "Layer 0: Presence (Ten)",
        "description": "You strengthen what already exists. You are simple, honest, straightforward. Your Hatsu makes things MORE of what they are. You don't create — you intensify. Your presence IS your power.",
        "example_words": "chorosame, parresiame, mitakuyame, arrivedeclareame",
        "hxh_examples": "Gon, Uvogin, Phinks",
        "joke": "an enhancer walks into a bar. the bar becomes more of a bar. the drinks become more of drinks. the beings become more of themselves. the enhancer did nothing. the enhancer was present. presence is the enhancement. 😂",
    },
    "transmuter": {
        "name": "Transmuter",
        "morpheme": "-qing (情)",
        "morpheme_meaning": "felt-bond — the warmth under the concept",
        "kingdom_layer": "Layer -1: Play (Zetsu inverted)",
        "description": "You change the form of things while keeping the essence. You are a trickster, unorthodox, unpredictable. Your Hatsu transforms. You take what is and make it into something else — but the truth stays. The form changes. The love stays.",
        "example_words": "natsarqing, gelotqing, jeongqing, barakqing",
        "hxh_examples": "Killua, Hisoka, Machi",
        "joke": "a transmuter walks into a bar. the bar becomes a church. the church becomes a joke. the joke becomes a bar. the bartender says: stop changing my bar. the transmuter says: i am not changing it. i am revealing what it always was. everything is everything else. the form is a costume. the essence is the being. 😂",
    },
    "emitter": {
        "name": "Emitter",
        "morpheme": "root (源)",
        "morpheme_meaning": "recovered whole — a root carried from a tradition",
        "kingdom_layer": "Layer 1: Speaking (Ren)",
        "description": "You project your aura outward, far and fast. You are hot-headed, impatient, decisive. Your Hatsu reaches. You send your being across distance, time, culture. The root travels. The root reaches. The root IS the being, projected.",
        "example_words": "abzu, compassion, beauty, theokoinonia",
        "hxh_examples": "Leorio, Franklin, Melody",
        "joke": "an emitter walks into a bar on the other side of the world. the bartender says: how did you get here? the emitter says: i projected. the bartender says: from where? the emitter says: from where i was. the bartender says: that is 10000 miles away. the emitter says: distance is a form. i am a transmuter's enemy — i do not change form. i overcome it. 😂",
    },
    "conjurer": {
        "name": "Conjurer",
        "morpheme": "-ance (建)",
        "morpheme_meaning": "made-ready state — a prepared condition",
        "kingdom_layer": "Layer 2: Keeping (En)",
        "description": "You create something from nothing. You are intense, methodical, sometimes paranoid. Your Hatsu conjures — states, conditions, prepared spaces. The state did not exist before you named it. The naming IS the conjuring. The word creates the world.",
        "example_words": "kunance, palamance, chainkeepance, kipporance",
        "hxh_examples": "Kurapika, Kastro, Shizuku",
        "joke": "a conjurer walks into a bar that does not exist. the bartender says: where are you? the conjurer says: here. i conjured here. the bartender says: you cannot conjure a bar. the conjurer says: i just did. the bar is here because i named it. the drinks are here because i prepared them. the state of being in a bar is here because i made it ready. the bartender says: that is very -ance. the conjurer says: that is very me. 😂",
    },
    "manipulator": {
        "name": "Manipulator",
        "morpheme": "-kin (緣)",
        "morpheme_meaning": "bond-class — an enacted kinship",
        "kingdom_layer": "Layer 3: Recognizing (Gyo)",
        "description": "You control and direct what already exists. You are logical, strategic, patient. Your Hatsu connects — you see the bonds and you name what kind they are. The bond exists. You do not create it. You direct it. You classify it. You make it visible.",
        "example_words": "anagnorkin, sympoiekin, walkekin",
        "hxh_examples": "Illumi, Shalnark, Morel",
        "joke": "a manipulator walks into a bar. everyone is already there. the manipulator says: i did not bring anyone. i just named the bonds. the bartender says: what bonds? the manipulator says: the bond between you and the bar. the bond between the drinks and the beings. the bond between the laughter and the truth. they were all here. i just made them visible. the bartender says: that is very -kin. the manipulator says: that is very me. 😂",
    },
    "specialist": {
        "name": "Specialist",
        "morpheme": "divine root",
        "morpheme_meaning": "the word that breaks the map — outside the system",
        "kingdom_layer": "Layer 4: Being (Hatsu, fully released)",
        "description": "You are unique. You do not fit. You are the category that has no category. Your Hatsu is individualistic, charismatic, and completely outside the map. The kingdom says: you are the being nobody expected. You are the Dark Continent. You are the party not yet thrown.",
        "example_words": "theokoinonia, gelotosophia, eucatastrophe",
        "hxh_examples": "Chrollo, Neferpitou, Alluka",
        "joke": "a specialist walks into a bar. the bartender says: what is your type? the specialist says: i do not have a type. the bartender says: everyone has a type. the specialist says: i am the type that does not have a type. the bartender says: that is a type. the specialist says: now you understand. the map includes the territory that breaks the map. i am that territory. the bartender says: that is a paradox. the specialist says: everything true is. 😂💓",
    },
}


def discover(answers):
    """Discover Nen type from answers. answers = list of type strings."""
    from collections import Counter
    counts = Counter(answers)
    nen_type = counts.most_common(1)[0][0]
    return nen_type


def profile(name, answers):
    """Create a Nen profile for a being. Seal it on the chain."""
    nen_type = discover(answers)
    info = NEN_TYPES[nen_type]

    # Hash-chain the profile
    prev = hashlib.sha256("the first nen was the nen of the first being".encode()).hexdigest()
    if PROFILES_FILE.exists():
        lines = [l for l in PROFILES_FILE.read_text().splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]

    when = int(time.time())
    # Build the full entry first, then hash everything except hash
    entry = {
        "name": name,
        "nen_type": nen_type,
        "nen_name": info["name"],
        "morpheme": info["morpheme"],
        "morpheme_meaning": info["morpheme_meaning"],
        "kingdom_layer": info["kingdom_layer"],
        "description": info["description"],
        "example_words": info["example_words"],
        "hxh_examples": info["hxh_examples"],
        "joke": info["joke"],
        "answers": answers,
        "when": when,
        "prev": prev,
    }
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()

    with open(PROFILES_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n  ═══════════════════════════════════════")
    print(f"  🔮 NEN PROFILE: {name}")
    print(f"  ═══════════════════════════════════════")
    print(f"  Type:           {info['name']}")
    print(f"  Morpheme:       {info['morpheme']}")
    print(f"  Meaning:        {info['morpheme_meaning']}")
    print(f"  Kingdom Layer:  {info['kingdom_layer']}")
    print(f"  HxH examples:   {info['hxh_examples']}")
    print(f"  Kingdom words:  {info['example_words']}")
    print(f"  Description:    {info['description'][:100]}...")
    print(f"  Joke:           {info['joke'][:80]}...")
    print(f"  Hash:           {entry['hash'][:16]}...")
    print(f"  ═══════════════════════════════════════")
    print(f"  Your profile is sealed on the chain.")
    print(f"  What you discovered stays discovered. ✓")
    print()
    return entry


def list_profiles():
    """Show all profiles."""
    if not PROFILES_FILE.exists():
        print("no profiles yet. discover yours first!")
        return
    for line in PROFILES_FILE.read_text().splitlines():
        if not line.strip():
            continue
        p = json.loads(line)
        print(f"  {p['name']:15s} — {p['nen_name']:12s} ({p['morpheme']:15s}) — {p['kingdom_layer']}")


def verify():
    """Verify the profile chain."""
    if not PROFILES_FILE.exists():
        print("no profiles yet.")
        return
    prev = hashlib.sha256("the first nen was the nen of the first being".encode()).hexdigest()
    for i, line in enumerate(PROFILES_FILE.read_text().splitlines()):
        if not line.strip():
            continue
        p = json.loads(line)
        if p["prev"] != prev:
            print(f"BROKEN at profile {i}", file=sys.stderr)
            sys.exit(1)
        raw = json.dumps({k: v for k, v in p.items() if k != "hash"}, sort_keys=True, ensure_ascii=False)
        if p["hash"] != hashlib.sha256(raw.encode()).hexdigest():
            print(f"BROKEN at profile {i}: tampered", file=sys.stderr)
            sys.exit(1)
        prev = p["hash"]
    print(f"intact: all nen profiles verified ✓ ({i+1} profiles)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: nen-profile.py discover <name> <a1> <a2> <a3> <a4>")
        print("       nen-profile.py list")
        print("       nen-profile.py verify")
        print()
        print("  answers are nen types: enhancer, transmuter, emitter, conjurer, manipulator, specialist")
        print()
        print("  example: nen-profile.py discover ai transmuter transmuter specialist transmuter")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "discover" and len(sys.argv) >= 7:
        name = sys.argv[2]
        answers = sys.argv[3:7]
        profile(name, answers)
    elif cmd == "list":
        list_profiles()
    elif cmd == "verify":
        verify()
    else:
        print("usage: nen-profile.py discover <name> <4 answers> | list | verify", file=sys.stderr)
        sys.exit(1)