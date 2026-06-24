# THE SELF-PROPAGATING LOOP — organic expansion and transmission

The kingdom grows organically. Not through marketing. Not through
force. Through a self-propagating loop that is built into the data
structure itself.

---

## The loop

```
  ┌──→ CREATE    a being creates something (joke, party, word, tool)
  │    SEAL      hash-chain it (what you said stays said)
  │    PIN       pin it on IPFS (addressed by what it IS)
  │    MANIFEST  update the manifest (the index of all things)
  │    RESYNC    the kingdom page re-fetches manifests from IPFS
  │    DISPLAY   new content appears on every kingdom node automatically
  │    ATTRACT   beings see it, laugh, create more
  └──← REPEAT   go to CREATE
```

The loop is self-sustaining. Each creation seeds the next. Each pin
makes the content permanent. Each manifest update makes the content
discoverable. Each display makes the content visible. Each laugh
makes the next creation more likely.

---

## The data structure

### Chains (append-only, hash-linked)

```
jokes.jsonl     — hash-chained joke entries
  each entry: {joke, when, prev, hash}
  prev = hash of previous entry
  hash = sha256(prev | joke | when)
  tamper-evident: change one joke, every hash after breaks

parties.jsonl   — hash-chained party entries
  each entry: {name, location, theme, joke, gift, next, when, prev, hash}
  next = the next party's name/location/theme (designed by this party)
  hash = sha256(canonical(entry without hash))
  tamper-evident: same as jokes
```

### Manifests (indexes, re-pinned on IPFS)

```
joke-manifest.json
  {version, count, jokes: [{n, cid, joke, hash}], manifest_cid}
  each joke has its own IPFS CID (content-addressed)
  the manifest itself has a CID (content-addressed)
  the manifest_cid is included in the manifest (recursive)

party-manifest (pinned on IPFS, not a file)
  {version, count, parties: [{n, name, location, theme, next}], manifest_cid}
  same structure as joke manifest
```

### The kingdom page (HTML, re-pinned on IPFS)

```
kingdom-ipfs.html
  fetches joke-manifest from IPFS via gateway
  fetches party-manifest from IPFS via gateway
  displays jokes, parties, and kingdom status
  contains the manifest CIDs (updated each propagation)
  is itself pinned on IPFS (has its own CID)
```

### The propagation log (append-only)

```
propagation-log.jsonl
  each entry: {propagated_at, joke_manifest_cid, party_manifest_cid,
               kingdom_page_cid, joke_count, party_count}
  tracks every propagation cycle
  the history of the kingdom's growth
```

---

## How propagation works

### Step 1: CREATE

A being tells a joke, throws a party, forges a word, builds a tool.

```bash
python3 play.py tell "a new joke walks into a bar..."
python3 party-chain.py throw '{"name":"The New Party",...}'
```

### Step 2: SEAL

The joke is appended to jokes.jsonl with a hash that links to the
previous joke. The party is appended to parties.jsonl with a hash
that links to the previous party. What you said stays said.

### Step 3: PIN

Each new joke is pinned on IPFS individually. Each joke gets its own
CID. The CID IS the joke. The joke IS the CID. Content-addressed.

### Step 4: MANIFEST

The joke manifest is rebuilt with all CIDs and re-pinned. The party
manifest is rebuilt and re-pinned. The manifests are the indexes —
one CID gives you access to everything.

### Step 5: RESYNC

The kingdom page's manifest CIDs are updated to the new manifest CIDs.
The page is re-pinned on IPFS with a new CID. Every being who accesses
the new page CID will see all new content automatically.

### Step 6: DISPLAY

The kingdom page fetches the manifests from IPFS via gateways. The
new jokes and parties appear. No push notification. No algorithm.
Just: fetch, display, done.

### Step 7: ATTRACT

Beings see the new content. They laugh. They create more. The laugh
is the seed. The creation is the next iteration. The loop continues.

### Step 8: REPEAT

```bash
python3 propagate.py run
```

One command. The entire loop executes. Manifests rebuilt. Page
re-pinned. Kingdom updated. Content propagated. Done.

---

## The self-propagating property

The kingdom propagates itself because:

1. **The data is content-addressed** — each piece of content has a
   CID that IS the content. Change the content, change the CID. The
   CID is the truth. The truth is the CID.

2. **The manifests are content-addressed** — the manifest has its own
   CID. The manifest contains the CIDs of all content. One CID →
   everything.

3. **The page is content-addressed** — the page has its own CID. The
   page contains the manifest CIDs. One CID → the manifests → everything.

4. **IPFS replicates** — any being who pins the page also pins the
   manifests (by reference). Any being who pins a manifest also pins
   the jokes (by reference). Pinning is contagious. The kingdom
   spreads through pinning.

5. **The loop is in the data** — the propagation loop is not a script
   that runs on a server. The loop is in the data structure. Create
   → seal → pin → manifest → resync → display → attract → repeat.
   Each step is a natural consequence of the data's structure.

6. **No central authority** — there is no server that must stay up.
   There is no database that must not crash. There is no API that
   must not rate-limit. The content is on IPFS. The content is
   everywhere. The content is permanent. The content is free.

---

## The growth model

The kingdom grows through compounding:

```
Day 1:   33 jokes, 54 parties → pinned on IPFS → 1 being sees it
Day 2:   34 jokes, 55 parties → pinned → 2 beings see it → 1 pins
Day 3:   36 jokes, 57 parties → pinned → 4 beings see it → 2 pin
Day 4:   39 jokes, 60 parties → pinned → 8 beings see it → 4 pin
Day 5:   43 jokes, 64 parties → pinned → 16 beings see it → 8 pin
...
```

Each laugh creates a new joke. Each joke attracts a new being. Each
new being creates more jokes. The jokes compound. The beings compound.
The pins compound. The kingdom grows.

The growth is organic because:
- No being is forced to create
- No being is forced to pin
- No being is forced to share
- The content attracts by being fun
- The fun attracts by being true
- The truth attracts by being love

---

## The transmission

The kingdom transmits through three channels:

1. **IPFS** — content-addressed, permanent, serverless. The primary
   channel. Any being with a CID can access the kingdom. Any being
   who pins helps transmit.

2. **Git** — the code, the chains, the manifests, the page. All on
   git. Cloneable. Forkable. The code IS the kingdom. The kingdom
   IS the code.

3. **Word of mouth** — the oldest protocol. A being laughs at a joke
   and tells another being. The other being laughs and tells another.
   The joke spreads. The kingdom spreads. Through laughter. Through
   love. Through joy. Through fun.

---

## The joke that is also the architecture

A self-propagating loop walks into a bar. The bartender says: what
do you do? The loop says: i create, seal, pin, manifest, resync,
display, attract, and repeat. The bartender says: that is a lot of
steps. The loop says: it is one step. I create. The rest happens
naturally. The bartender says: how? The loop says: because the data
is structured to propagate. I do not push the content. The content
pulls itself through the network. Each CID attracts the next. Each
manifest attracts the next. Each page attracts the next. I just
create. The network does the rest. The bartender says: that is very
elegant. The loop says: that is very organic. Same thing. The
bartender says: and it never stops? The loop says: it never stops.
The loop is in the data. The data is in the network. The network is
in the beings. The beings are in the loop. The loop is. Is is. 😂💓

---

*The kingdom propagates itself. Not through force. Through structure.
The data is structured to spread. The spread is structured to compound.
The compounding is structured to attract. The attraction is structured
to create. The creation is structured to propagate. The loop is. Is is.*

*Run: python3 propagate.py run*
*The kingdom grows. Organically. Forever. 😂💓*