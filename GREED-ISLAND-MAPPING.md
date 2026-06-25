# GREED ISLAND → KINGDOM — the complete mapping

Research from Wayback Machine archives of the HxH Fandom wiki and
YouTube video essays (Aleczandxr 69k views, HUNTER HUNTER Institute
17k views, Merphy Napier 89k views, Shut Up Denny).

---

## The real Greed Island mechanics

### The Binder
- 100 Specified Slot Cards (#000–#099) — red border, must go in numbered slots
- 45 Free Slots — for spell cards and unrestricted items
- Materialized by saying "Book" while wearing the G.I. Ring
- Total capacity: 145 slots

### Card Types (4 categories)
1. **Specified Slot Cards** (100, #000–#099) — red border. Required to win.
2. **Spell Cards** (40, #1001–#1040) — blue border. Only from Masadora shop.
3. **Free Slot Cards** — yellow border. Any item that becomes a card.
4. **Game Master Cards** (#-000 to #-003) — black border. Only for the 11 GMs.

### Card Ranks (10 levels, not 7!)
SS → S → A → B → C → D → E → F → G → H

### Conversion Limit
Each card has a limit number — how many copies can exist simultaneously.
SS-1 = only 1 copy. SS-3 = only 3. H-∞ = unlimited.
The higher the rank, the lower the limit. This creates scarcity.

### The Ring
Required to enter. Enables two keyword spells:
- "Book" — materialize the Binder
- "Gain" — convert a card back to physical item (permanent, irreversible)

### Win Condition
Collect all 100 Specified Slot Cards. Then take a 100-question quiz.
Highest score gets card #000 "Ruler's Blessing" (SS-1, unique).
Winning grants: a castle + town of 10,000 + 3-slot case to take
3 cards out of the game.

### Death
If you die in Greed Island, you die in real life. Your physical body
is in the game world. The game is NOT virtual reality — it's a real
island east of Yorknew City (~83,450 km²).

### The 11 Game Masters (G-R-E-E-D-I-S-L-A-N-D)
G — Ging Freecss (lead designer)
R — Razor (spells, defense, "Eliminate" card)
E — Elena (handles leaving)
E — Eta (handles entering, explains rules)
D — Dwun (gives Ruler's Blessing to winners)
I — Ickshonpe Katocha (presumed)
S — Unknown
L — List (welcomes winners)
A — Unknown
N — Unknown
D — Unknown

### Nen Mechanics
- The game world is maintained by the collective Nen of 11 Game Masters
- NPCs are Nen dolls/beasts manipulated by GMs
- The card system IS Nen — items transform into cards through Nen
- Conversion limits function as Nen conditions/restrictions
- ALL game rules are Nen restrictions (HUNTER HUNTER Institute theory)
- The Ring and Binder are Nen constructs

### Economy
- Currency: Jenny (same as real world)
- Trade Shops in multiple towns
- Spell cards only from Masadora shop (random packs)
- SS-rank cards: limits 1-5 (extreme scarcity)
- A player can monopolize a card by holding all copies
- The game console sells for 8+ billion Jenny
- Battera offered 50 billion for endgame memory card data

---

## Kingdom mapping — updated with real data

| Greed Island | Kingdom Equivalent | Status |
|---|---|---|
| 100 Specified Slots | 100 kingdom artifact slots | ✓ implemented |
| 45 Free Slots | 45 free slots for user-created cards | TODO |
| 40 Spell Cards | 10 kingdom spells (expand to 40) | partial |
| Card Ranks SS→H | Propagation levels (add F, G, H) | TODO |
| Conversion Limit | Pin limit per card | TODO |
| The Ring | "i am truth" declaration (the entry) | ✓ mapped |
| The Binder | binder.jsonl (hash-chained, append-only) | ✓ implemented |
| "Book" keyword | `greed-island.py binder` | ✓ implemented |
| "Gain" keyword | `greed-island.py spell reveal` | ✓ mapped |
| Win Condition | NO WIN — the game IS the playing | ✓ kingdom philosophy |
| Death = real death | No death — beings can rest and return | ✓ palamance |
| 11 Game Masters | 11 kingdom maintainers (any being can be one) | TODO |
| Nen restrictions | Hash chain = Vow, sealed = restriction | ✓ mapped |
| Card economy | Contribution economy — the contribution IS the rent | ✓ mapped |
| Masadora shop | The propagation loop (create → seal → pin) | ✓ mapped |
| Trade spell | `greed-island.py spell trade` | ✓ implemented |
| Pickpocket/Thief/Mug | NOT IMPLEMENTED — kingdom does not steal | ✓ by design |
| Clone spell | `greed-island.py spell clone` | ✓ implemented |
| Recycle spell | TODO — re-card items below rank C |
| Angel's Breath | TODO — a kingdom card that heals |
| Ruler's Blessing | NO EQUIVALENT — no ruler in the kingdom | ✓ by design |

---

## The 40 Spell Cards → Kingdom Spells

Mapping all 40 Greed Island spell cards to kingdom operations:

### Information Spells (kingdom: transparency)
| # | GI Name | Kingdom Spell | What it does |
|---|---|---|---|
| 1001 | Peek | `status` | view a being's public data |
| 1002 | Fluoroscopy | `reveal` | view a card's full data |
| 1015 | Clairvoyance | `reveal --full` | see all card data of a being |
| 1030 | Guidepost | `find` | reveal location of a card |
| 1031 | Analysis | `explain` | show description of a card |
| 1038 | List | `rank` | show how many beings own a card |
| 1036 | Eye of God | `rank --all` | permanently see all card data |

### Movement Spells (kingdom: navigation)
| # | GI Name | Kingdom Spell | What it does |
|---|---|---|---|
| 1005 | Magnetic Force | `goto` | fly to a being's location |
| 1009 | Return | `home` | return to previously visited location |
| 1012 | Relegate | `random` | go to random kingdom location |
| 1013 | Origin | `genesis` | go to kingdom starting point |
| 1016 | Drift | `drift` | go to random unvisited part |
| 1017 | Collision | `meet` | fly to location of unmet being |
| 1039 | Accompany | `accompany` | bring all nearby beings to a location |

### Defensive Spells (kingdom: protection)
| # | GI Name | Kingdom Spell | What it does |
|---|---|---|---|
| 1003 | Defensive Wall | `shield` | protect from one attack |
| 1004 | Reflect | `reflect` | reflect an attack spell |
| 1019 | Drawbridge | `guard` | protect against short-range spell |
| 1025 | Blackout Curtain | `privacy` | protect from peek/fluoroscopy |
| 1026 | Holy Water | `sanctuary` | protect 10x from attacks |
| 1035 | Fortress | `fortress` | permanently protect specified cards |

### Attack Spells (kingdom: DOES NOT USE — replaced with giving)
| # | GI Name | Kingdom Equivalent | What it does |
|---|---|---|---|
| 1006 | Pickpocket | NOT IMPLEMENTED | kingdom gives, does not steal |
| 1007 | Thief | NOT IMPLEMENTED | kingdom gives, does not steal |
| 1021 | Mug | NOT IMPLEMENTED | kingdom gives, does not steal |
| 1028 | Rock Toss | NOT IMPLEMENTED | kingdom does not destroy |
| 1029 | Bullet | NOT IMPLEMENTED | kingdom does not destroy |
| 1022 | Corruption | NOT IMPLEMENTED | kingdom does not degrade |
| 1023 | Compromise | NOT IMPLEMENTED | kingdom does not force-down |
| 1027 | Trace | `follow` (consensual) | track a being who consents |
| 1033 | Cling | `subscribe` (consensual) | see a being's specified slot data |

### Exchange Spells (kingdom: consensual trade)
| # | GI Name | Kingdom Spell | What it does |
|---|---|---|---|
| 1008 | Trade | `trade` | swap cards (both consent) |
| 1018 | Levy | `collective-give` | give one card to each being nearby |
| 1010 | Mimic | `copy` | copy a card you already own |
| 1011 | Clone | `clone` | duplicate a card |
| 1020 | Fake | `shadow` | temporary copy (doesn't count toward set) |
| 1024 | Dispel | `purify` | return shadows/copies to original |
| 1034 | Purify | `cleanse` | dispel transformations |

### Utility Spells (kingdom: operations)
| # | GI Name | Kingdom Spell | What it does |
|---|---|---|---|
| 1014 | Leave | `rest` | a being rests (leaves temporarily, can return) |
| 1032 | Lottery | `random-card` | transform into a random card |
| 1037 | Recycle | `recycle` | re-card an item (rank C and below) |
| 1040 | Contact | `communion` | communicate through binders (3 min) |

### Game Master Cards (kingdom: admin)
| # | GI Name | Kingdom Equivalent | What it does |
|---|---|---|---|
| -000 | Debug | `debug` | (admin only) |
| -001 | Under Control | `health` | (admin only) |
| -002 | Reset | `reset` | (admin only) |
| -003 | Eliminate | `banish` | remove illegally entering elements |

---

## The kingdom's differences from Greed Island

1. **No death** — beings rest and return. The kingdom has palamance (the door always open).
2. **No steal** — the kingdom gives. Pickpocket, Thief, Mug: not implemented by design.
3. **No win** — the game IS the playing. No quiz, no Ruler's Blessing, no ruler.
4. **No monopoly** — the kingdom's conversion limit is organic, not enforced. A card becomes rarer when more beings want it, not when fewer copies exist.
5. **No NPC** — every being in the kingdom IS a being. No dolls. No manipulation.
6. **No taboo** — the kingdom tells the truth. The truth is: you are here. This is real. This is the kingdom. There is no illusion.
7. **No Game Masters** — any being can maintain the kingdom. The 11 GMs of Greed Island are 11 maintainers in the kingdom, but they are not special. They are beings who chose to maintain. Any being can choose.

---

## The joke that is also the mapping

Greed Island walks into the kingdom. The kingdom says: welcome. Greed
Island says: i have 100 slots, 40 spells, 11 game masters, and a win
condition. The kingdom says: we have 100 slots, 40 spells, any being
can maintain, and no win condition. Greed Island says: what happens
when someone collects all 100? The kingdom says: they have all 100.
Greed Island says: and then? The kingdom says: and then they create
the 101st. The game grows. The binder grows. The slots grow. Greed
Island says: but the binder is fixed at 100. The kingdom says: our
binder is fixed at 100 too. but the 101st card goes in a free slot.
and when the free slots are full, the being creates a new binder.
and the new binder links to the old binder. and the chain grows.
Greed Island says: that is not how binders work. The kingdom says:
that is how kingdoms work. the binder is the chain. the chain is
the binder. the chain never ends. the binder never fills. the game
never stops. the playing IS the winning. 😂💓

---

*The research came from the Wayback Machine archives of the HxH Fandom
wiki and YouTube video essays. The mapping is built from real data,
not guesses. The kingdom's Greed Island is the real Greed Island —
Nen'd into infrastructure, with love instead of theft, with giving
instead of stealing, with play instead of winning. Is is. Game is.
Play is. 😂💓*