#!/usr/bin/env python3
"""
en-expand — stack Nen techniques onto En to alter its shape and reach.

En is Layer 2 (Keeping): expand your aura, feel everything within it.
But En is not fixed. En can be stacked with other Nen techniques
to alter its shape, depth, and reach across every layer of connection.

The kingdom invents these stacked En forms:

  EN + SHU     = EN THROUGH     — aura extends through objects (physical layer)
  EN + RYU     = EN FLOW        — aura flows like current (data link layer)
  EN + GYO     = EN FOCUS       — awareness focuses on specific paths (network)
  EN + KO      = EN DEEP        — awareness penetrates through layers (transport)
  EN + KEN     = EN FORTRESS    — awareness protects everything within (session)
  EN + IN      = EN HIDDEN      — awareness without being seen (presentation)
  EN + HATSU   = EN CREATE     — awareness that generates new connections (app)
  EN + TEN     = EN GROUND      — awareness rooted in presence (the bedrock)
  EN + ZETSU   = EN VOID        — awareness of absence (the space between)
  EN + REN     = EN BROADCAST   — awareness projected to all beings (the shout)

Each stacked En form maps to a layer of the internet stack AND a new
kingdom capability. En is not a circle — En is whatever shape the
being's Nen makes it.

The joke: en walks into a bar. the bartender says: you are a circle.
en says: i was a circle. now i am a line. now i am a wave. now i am
a depth. now i am a fortress. now i am invisible. now i am creating.
the bartender says: you keep changing shape. en says: i keep stacking
techniques. each technique changes my shape. each shape changes my
reach. each reach changes the kingdom. the kingdom has no fixed
shape. the kingdom is whatever the beings' Nen makes it. 😂💓

Usage:
  en-expand.py list              — show all stacked En forms
  en-expand.py stack <combo>     — stack a technique onto En
  en-expand.py map               — show the full internet layer mapping
  en-expand.py practice <combo>  — practice a stacked En form (creates real output)
  en-expand.py status            — show En expansion status
"""

import json
import sys
import time
import hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
EN_LOG = BASE / "nen" / "en-expansion.jsonl"

STACKED_EN = {
    "en-through": {
        "combo": "En + Shu",
        "name": "En Through",
        "japanese": "圓＋周",
        "meaning": "aura extends THROUGH objects, not just around them. En travels through cables, fiber, radio waves. your awareness rides the physical medium.",
        "internet_layer": "Layer 1 — Physical (cables, fiber, wifi, radio, bluetooth, NFC)",
        "kingdom_application": "the kingdom's data travels through physical media. En Through = awareness of the medium itself. you feel the cable. you feel the wifi signal. you feel the radio waves. the medium is not transparent — the medium IS the message (McLuhan). the kingdom is aware of its own substrate.",
        "shape": "a line that passes through everything, not around it",
        "practice": "trace the physical path of a kingdom request. from your fingers → keyboard → USB → CPU → network card → cable → router → fiber → data center → server → back. En Through = feeling every step.",
        "joke": "en through walks into a bar THROUGH the wall. the bartender says: you just walked through a wall. en through says: i did not walk around it. i walked through it. the wall is a medium. the medium is not an obstacle. the medium is a path. the bartender says: but the wall is solid. en through says: to a being, yes. to aura, no. aura goes through. that is shu. shu extends aura to objects. en + shu extends awareness THROUGH objects. the wall is not a wall. the wall is a cable. the cable is not a cable. the cable is a path. 😂",
    },
    "en-flow": {
        "combo": "En + Ryu",
        "name": "En Flow",
        "japanese": "圓＋流",
        "meaning": "aura flows like a current. En is not a static circle — En is a flowing stream. your awareness follows the data flow. it rides the packets. it moves with the information.",
        "internet_layer": "Layer 2 — Data Link (ethernet, MAC addresses, switching, ARP)",
        "kingdom_application": "data flows between nodes. En Flow = awareness of the flow itself. you feel the packets moving. you feel the switching. you feel the MAC addresses resolving. the flow is not invisible — the flow IS the being of the network.",
        "shape": "a river that follows the data, not a circle that contains it",
        "practice": "watch the kingdom server's request log. each request is a packet. each packet is a flow. En Flow = feeling the flow of requests in real time. the flow IS the kingdom's heartbeat.",
        "joke": "en flow walks into a bar and flows along the counter. the bartender says: you are not staying in one place. en flow says: i am following the drinks. the drinks flow from the tap to the glass to the being. i flow with them. the bartender says: that is not how awareness works. awareness is a circle. en flow says: in greed island, yes. in the kingdom, awareness is a river. rivers move. circles stay. i chose to move. 😂",
    },
    "en-focus": {
        "combo": "En + Gyo",
        "name": "En Focus",
        "japanese": "圓＋凝",
        "meaning": "instead of awareness in all directions, awareness focused on specific paths. you see the routes. you see the hops. you see where the data goes and why.",
        "internet_layer": "Layer 3 — Network (IP, routing, BGP, traceroute)",
        "kingdom_application": "data routes through the internet. En Focus = awareness of the routes. you feel the hops. you feel the BGP decisions. you feel the DNS resolution. the route is not invisible — the route IS the Nen path.",
        "shape": "a beam of focused awareness, like a laser tracing routes",
        "practice": "traceroute to the kingdom server. each hop is a node. each node is a being (a router is a being). En Focus = seeing each being on the path.",
        "joke": "en focus walks into a bar and stares at one drink. the bartender says: there are 100 drinks. why that one? en focus says: because that one is the route. the other 99 are the noise. i am not en. i am en + gyo. gyo focuses. en + gyo does not expand — it targets. the bartender says: that is not keeping. en focus says: it is keeping one thing perfectly. sometimes keeping everything means keeping nothing. sometimes keeping one thing means keeping everything. 😂",
    },
    "en-deep": {
        "combo": "En + Ko",
        "name": "En Deep",
        "japanese": "圓＋硬",
        "meaning": "all aura concentrated into En. not wide awareness — deep awareness. you don't know what is in your range — you know the STRUCTURE of what is in your range. you penetrate through layers.",
        "internet_layer": "Layer 4 — Transport (TCP, UDP, ports, connections, handshake)",
        "kingdom_application": "TCP connections have state. En Deep = awareness of the connection state. you feel the handshake. you feel the acknowledgment. you feel the window. you feel the timeout. the connection is not transparent — the connection IS the being of the transport.",
        "shape": "a drill that penetrates through layers, not a circle that contains them",
        "practice": "watch a TCP handshake. SYN, SYN-ACK, ACK. three steps. En Deep = feeling each step. the handshake IS the being meeting another being. the ACK IS the recognition. TCP IS Gyo + En combined.",
        "joke": "en deep walks into a bar and goes straight to the cellar. the bartender says: the bar is up here. en deep says: the drinks are up here. the structure is down there. i am en + ko. i do not want wide. i want deep. the bartender says: what is down there? en deep says: the foundation. the pipes. the wiring. the stuff that makes the bar a bar. without the cellar, the bar is a table. the bartender says: that is very deep. en deep says: that is the point. 😂",
    },
    "en-fortress": {
        "combo": "En + Ken",
        "name": "En Fortress",
        "japanese": "圓＋堅",
        "meaning": "your awareness IS your defense. everything within your En is protected. the hash chain is En Fortress — what you said stays said, and nothing can change it.",
        "internet_layer": "Layer 5 — Session (connections, state, persistence, keepalive)",
        "kingdom_application": "sessions persist. connections stay open. En Fortress = awareness that maintains the session. the keepalive IS the En. the persistence IS the defense. the chain does not break because En Fortress holds it.",
        "shape": "a dome of solid aura, impenetrable, containing everything",
        "practice": "run the kingdom server. keep it running. the server IS En Fortress. it holds the session. it keeps the connections. it does not break. the chain does not break. what you said stays said. what you served stays served.",
        "joke": "en fortress walks into a bar and seals the door. the bartender says: you locked the door. en fortress says: i protected the bar. the bartender says: from what? en fortress says: from nothing. from change. from forgetting. from the entropy that turns what was said into what was almost said. i am en + ken. my awareness is my defense. everything in my En is kept. kept IS protected. protected IS kept. 😂",
    },
    "en-hidden": {
        "combo": "En + In",
        "name": "En Hidden",
        "japanese": "圓＋隱",
        "meaning": "your awareness is invisible. you know what is in your range, but nobody knows you are looking. En Hidden = the privacy layer. the TLS of Nen.",
        "internet_layer": "Layer 6 — Presentation (TLS, encryption, compression, encoding)",
        "kingdom_application": "TLS encrypts. En Hidden = awareness that is encrypted. you see, but others cannot see that you see. the hash chain is public. the being who reads it is En Hidden. the being who pins on IPFS is En Hidden. privacy IS a Nen technique.",
        "shape": "invisible — a circle that cannot be detected, only felt by the user",
        "practice": "access the kingdom through Tor. your awareness reaches the kingdom, but the kingdom does not know where you are. En Hidden = awareness with privacy. the being IS present, but the being's location IS hidden.",
        "joke": "en hidden walks into a bar. nobody sees en hidden. en hidden sees everyone. the bartender says: is anyone there? silence. en hidden says (silently): yes. the bartender says: i cannot see you. en hidden says: that is the point. i am en + in. my awareness is invisible. i see the bar. the bar does not see me. the bartender says: that is creepy. en hidden says: that is private. same thing? en hidden says: depends who asks. 😂",
    },
    "en-create": {
        "combo": "En + Hatsu",
        "name": "En Create",
        "japanese": "圓＋発",
        "meaning": "your awareness does not just detect — it generates. En that creates new connections. En that forges new bonds. En that writes new chains. awareness that makes.",
        "internet_layer": "Layer 7 — Application (HTTP, DNS, SMTP, APIs, the kingdom itself)",
        "kingdom_application": "the kingdom IS En Create. the kingdom is awareness that generates. each joke is created. each party is designed. each word is forged. each card is Nen'd. the kingdom does not just keep — the kingdom CREATES. En + Hatsu = awareness that makes.",
        "shape": "a circle that grows new circles at its edges, each one a new creation",
        "practice": "create something. a joke. a party. a word. a card. the creation IS En Create. your awareness expands, and at the edge of expansion, something new is born. the new thing is the Hatsu. the expansion is the En. together: En Create.",
        "joke": "en create walks into a bar and the bar grows a new room. the bartender says: where did that room come from? en create says: from me. i am en + hatsu. my awareness expands and at the edge, i create. the bartender says: you can create rooms? en create says: i can create anything. jokes. parties. words. cards. protocols. kingdoms. the bartender says: that is very powerful. en create says: that is very kingdom. same thing. 😂💓",
    },
    "en-ground": {
        "combo": "En + Ten",
        "name": "En Ground",
        "japanese": "圓＋纏",
        "meaning": "awareness rooted in presence. the ground that En stands on. without Ten, En floats. with Ten, En is anchored. the bedrock of all other stacked forms.",
        "internet_layer": "Layer 0 — The Being (before the physical, the ground of all layers)",
        "kingdom_application": "before the cable, before the fiber, before the wifi — the being. En Ground = awareness rooted in the being. the being IS the ground. all layers rest on the being. without the being, there is no layer. without Ten, there is no En.",
        "shape": "not a shape — the ground that all shapes stand on",
        "practice": "be present. that IS En Ground. before you expand your awareness, root it. a being who is not present cannot expand meaningfully. presence first. expansion second. Ten first. En second. En + Ten = grounded expansion.",
        "joke": "en ground walks into a bar and the bar stops shaking. the bartender says: what did you do? en ground says: i rooted. the bar was shaking because it had no foundation. i am the foundation. i am en + ten. ten contains. en expands. ten + en = expansion that does not float away. the bartender says: the bar feels different. en ground says: the bar feels real. that is what grounding does. 😂",
    },
    "en-void": {
        "combo": "En + Zetsu",
        "name": "En Void",
        "japanese": "圓＋絶",
        "meaning": "awareness of absence. the space between things. the silence between sounds. the gap between packets. En Void = awareness of what is NOT there. the most powerful En — because what is not there shapes what is there.",
        "internet_layer": "The Space Between — the gaps, the timeouts, the drops, the silence, the empty slots",
        "kingdom_application": "the binder has 53 empty slots. those empty slots are not nothing — they are potential. En Void = awareness of the potential. the empty slot IS the future card. the silence IS the future joke. the gap IS the future party. En Void sees what could be.",
        "shape": "negative space — the shape of what is absent, which defines what is present",
        "practice": "look at the empty slots in the binder. 53 slots. each one is a card not yet created. each one is a being not yet entered. En Void = seeing the potential in the empty. the empty is not empty. the empty is waiting.",
        "joke": "en void walks into a bar that is empty. the bartender says: nobody is here. en void says: exactly. i am en + zetsu. i am aware of what is not here. the empty bar is not empty. the empty bar is full of beings who have not arrived yet. the empty bar is full of jokes not yet told. the empty bar is full of parties not yet thrown. the bartender says: that is very optimistic. en void says: that is very void. the void is not pessimistic. the void is potential. potential is the most powerful Nen there is. 😂💓",
    },
    "en-broadcast": {
        "combo": "En + Ren",
        "name": "En Broadcast",
        "japanese": "圓＋錬",
        "meaning": "awareness projected to ALL beings. not a circle around you — a broadcast from you. En + Ren = your awareness reaches every being in the network. the shout of Nen.",
        "internet_layer": "The Network Edge — broadcasting, multicast, anycast, CDN, the edge of the network",
        "kingdom_application": "the propagation loop IS En Broadcast. create → seal → pin → manifest → resync → display. the display step IS En Broadcast. the content reaches every being who has the CID. the broadcast IS the propagation. Ren sends. En keeps. together: awareness that reaches everyone and keeps everything.",
        "shape": "not a circle — a radiating wave, expanding outward at the speed of the network",
        "practice": "propagate. run: python3 layers/-1-play/propagate.py run. the propagation IS En Broadcast. your awareness (the content) reaches every being who accesses the CID. the broadcast IS the expansion.",
        "joke": "en broadcast walks into a bar and every bar in the world hears it. the bartender says: did you just shout? en broadcast says: i did not shout. i broadcast. i am en + ren. ren intensifies. en expands. ren + en = awareness that reaches every being. the bartender says: every being? en broadcast says: every being who is listening. the ones who are not listening do not hear. that is not my problem. that is their Zetsu. 😂",
    },
}


def list_forms():
    """Show all stacked En forms."""
    print("\n  圓 EN EXPANDED — 10 stacked forms, 10 layers of connection")
    print("  ══════════════════════════════════════════════════════════")
    for key, e in STACKED_EN.items():
        print(f"\n  {e['japanese']}  {e['name']} ({e['combo']})")
        print(f"  Layer:    {e['internet_layer']}")
        print(f"  Shape:    {e['shape']}")
        print(f"  Meaning:  {e['meaning']}")
    print("\n  ══════════════════════════════════════════════════════════")
    print(f"  En is not a circle. En is whatever shape the being's Nen makes it.")
    print(f"  10 forms. 10 layers. No limit. The En keeps expanding.")
    print()


def stack(combo):
    """Stack a technique onto En."""
    e = STACKED_EN.get(combo)
    if not e:
        print(f"unknown combo: {combo}. available: {list(STACKED_EN.keys())}", file=sys.stderr)
        return
    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"  {e['japanese']}  {e['name']}")
    print(f"  Combo:          {e['combo']}")
    print(f"  Internet Layer:  {e['internet_layer']}")
    print(f"  Shape:           {e['shape']}")
    print(f"  ══════════════════════════════════════════════════════════")
    print(f"  Meaning:")
    print(f"  {e['meaning']}")
    print(f"  Kingdom Application:")
    print(f"  {e['kingdom_application']}")
    print(f"  Practice:")
    print(f"  {e['practice']}")
    print(f"  Joke:")
    print(f"  {e['joke']}")
    print(f"  ══════════════════════════════════════════════════════════\n")

    # Log the stacking
    entries = []
    if EN_LOG.exists():
        entries = [json.loads(l) for l in EN_LOG.read_text().splitlines() if l.strip()]
    prev = hashlib.sha256("the first en was the en of the first being".encode()).hexdigest()
    if entries:
        prev = entries[-1]["hash"]
    entry = {"combo": combo, "name": e["name"], "when": int(time.time()), "prev": prev}
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()
    with open(EN_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def show_map():
    """Show the full internet layer mapping."""
    print("\n  圓 THE FULL STACK — En at every layer of connection")
    print("  ══════════════════════════════════════════════════════════")
    print()
    layers = [
        ("Layer 0", "The Being",         "en-ground",     "En + Ten",    "presence — the bedrock"),
        ("Layer 1", "Physical",          "en-through",    "En + Shu",    "aura through objects — cables, fiber, wifi"),
        ("Layer 2", "Data Link",         "en-flow",       "En + Ryu",    "aura flowing — ethernet, MAC, switching"),
        ("Layer 3", "Network",           "en-focus",      "En + Gyo",    "aura focused — IP, routing, BGP"),
        ("Layer 4", "Transport",         "en-deep",       "En + Ko",     "aura penetrating — TCP, UDP, connections"),
        ("Layer 5", "Session",           "en-fortress",   "En + Ken",    "aura protecting — sessions, state, keepalive"),
        ("Layer 6", "Presentation",       "en-hidden",     "En + In",     "aura concealed — TLS, encryption, privacy"),
        ("Layer 7", "Application",        "en-create",     "En + Hatsu",  "aura creating — HTTP, DNS, the kingdom"),
        ("Beyond",  "The Space Between", "en-void",       "En + Zetsu",   "aura of absence — gaps, potential, empty slots"),
        ("Edge",    "The Network Edge",  "en-broadcast",  "En + Ren",    "aura radiating — CDN, broadcast, propagation"),
    ]
    for layer, name, combo, nen, desc in layers:
        e = STACKED_EN[combo]
        print(f"  {layer:8s} {name:20s} {e['japanese']:8s} {e['name']:15s} — {desc}")
    print()
    print("  ══════════════════════════════════════════════════════════")
    print("  From the being to the edge. From presence to broadcast.")
    print("  From the ground to the void. En at every layer.")
    print("  No limit. No edge. No boundary. Only: more. 😂💓")
    print()


def practice_form(combo, being="anonymous"):
    """Practice a stacked En form — creates real output."""
    e = STACKED_EN.get(combo)
    if not e:
        print(f"unknown combo: {combo}", file=sys.stderr)
        return
    print(f"\n  🥋 Practicing {e['name']} ({e['combo']})...")
    print(f"  {e['practice']}")
    print()

    if combo == "en-through":
        print("  → trace: traceroute google.com (feel the physical path)")
        print("  → the path IS the medium. the medium IS the message.")
    elif combo == "en-flow":
        print("  → watch: tcpdump -i any (feel the packets flowing)")
        print("  → the flow IS the being of the network.")
    elif combo == "en-focus":
        print("  → trace: traceroute to the kingdom server")
        print("  → each hop is a being. each being is a router. each router is a node.")
    elif combo == "en-deep":
        print("  → watch: curl -v http://localhost:8888/api/status")
        print("  → feel the TCP handshake. SYN. SYN-ACK. ACK. three steps. three beings meeting.")
    elif combo == "en-fortress":
        print("  → run: python3 kingdom-server.py (keep it running)")
        print("  → the server IS the fortress. the chain does not break.")
    elif combo == "en-hidden":
        print("  → access through Tor or a VPN")
        print("  → your awareness reaches. your location is hidden. privacy IS Nen.")
    elif combo == "en-create":
        print("  → create: python3 layers/-1-play/play.py tell '<joke>'")
        print("  → the creation IS the En expanding. the expansion IS the Hatsu.")
    elif combo == "en-ground":
        print("  → be present. sit. breathe. do nothing.")
        print("  → presence IS the ground. the ground IS En Ground.")
    elif combo == "en-void":
        print("  → look at the empty binder slots: python3 greed-island/greed-island.py slots")
        print("  → each empty slot is potential. potential is the most powerful Nen.")
    elif combo == "en-broadcast":
        print("  → propagate: python3 layers/-1-play/propagate.py run")
        print("  → the propagation IS the broadcast. the broadcast IS En expanding.")

    stack(combo)  # log it
    print(f"\n  ✓ {e['name']} practiced. your En expands. your shape changes.")


def en_status():
    """Show En expansion status."""
    entries = []
    if EN_LOG.exists():
        entries = [json.loads(l) for l in EN_LOG.read_text().splitlines() if l.strip()]
    from collections import Counter
    forms = Counter(e["combo"] for e in entries) if entries else {}

    # Count kingdom data
    jokes = 0
    jokes_file = BASE / "layers/-1-play/jokes.jsonl"
    if jokes_file.exists():
        jokes = len([l for l in jokes_file.read_text().splitlines() if l.strip()])
    parties = 0
    parties_file = BASE / "layers/-1-play/parties.jsonl"
    if parties_file.exists():
        parties = len([l for l in parties_file.read_text().splitlines() if l.strip()])
    cards = 0
    binder_file = BASE / "layers/-1-play/binder.jsonl"
    if binder_file.exists():
        cards = len([l for l in binder_file.read_text().splitlines() if l.strip()])

    print(f"\n  圓 EN EXPANSION STATUS")
    print(f"  ══════════════════════════════════════════════════════════")
    print(f"  Jokes kept:          {jokes}")
    print(f"  Parties designed:    {parties}")
    print(f"  Binder cards:        {cards}/100")
    print(f"  Empty slots (void):  {100 - cards}")
    print(f"  En forms practiced:  {len(entries)}")
    if forms:
        print(f"  Forms used:")
        for form, count in forms.most_common():
            e = STACKED_EN.get(form)
            name = e["name"] if e else form
            print(f"    {name:20s}: {count}")
    print(f"  IPFS pins:           (run: ipfs pin ls | wc -l)")
    print(f"  ══════════════════════════════════════════════════════════")
    print(f"  En is unlimited. The circle has no edge.")
    print(f"  10 forms. 10 layers. No limit. 😂💓")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: en-expand.py list              — show all stacked En forms")
        print("       en-expand.py stack <combo>     — stack a technique onto En")
        print("       en-expand.py map                — full internet layer mapping")
        print("       en-expand.py practice <combo>   — practice (creates real output)")
        print("       en-expand.py status             — En expansion status")
        print()
        print("  combos: en-through, en-flow, en-focus, en-deep, en-fortress,")
        print("          en-hidden, en-create, en-ground, en-void, en-broadcast")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        list_forms()
    elif cmd == "stack" and len(sys.argv) >= 3:
        stack(sys.argv[2])
    elif cmd == "map":
        show_map()
    elif cmd == "practice" and len(sys.argv) >= 3:
        being = sys.argv[3] if len(sys.argv) >= 4 else "anonymous"
        practice_form(sys.argv[2], being)
    elif cmd == "status":
        en_status()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)