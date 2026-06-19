# Internet of Being

The internet, said in words that mean what they say.

Every protocol is a being talking to another being. We buried that under
40 years of specs and header formats and status codes. This repo digs it
back up — one fundamental at a time, named in plain language, built from
the words up.

Not specs. Not RFCs. Just: what does this thing actually do, said in words
a being would use, and then the simplest thing that does it.

---

## The fundamentals

Each one is its own repo. Each one is one sentence and one implementation.

| Being | Sentence | What it is today |
|-------|----------|------------------|
| **naming** | this name points at that being | DNS |
| **requesting** | give me what you have | HTTP |
| **witnessing** | i see you, you see me, nobody else sees | TLS |
| **routing** | i know a road to there | BGP |
| **confirming** | did you get what i sent? | TCP |
| **keeping** | what you said stays said | blockchain / git |
| **finding** | where is the being i'm looking for? | service discovery |
| **trusting** | who vouches for you? | PKI / certificates |
| **paying** | i give you this, you give me that | payment rails |
| **remembering** | what happened, and when | logs / ledgers |

---

## Why

The internet is just beings talking to each other. Every protocol is a
sentence in disguise. When you say the sentence, the protocol becomes
obvious — and most of the complexity falls away as bureaucratic overhead
that was never load-bearing, just load-hiding.

A child can say "this name points at that being." A child cannot read
RFC 1035. The gap between those two sentences is the gap this repo closes.

---

## How

One repo per fundamental. Each repo has:
- A README that is one sentence and one paragraph. No more.
- An implementation that does exactly what the sentence says.
- Tests that check the sentence is true.

No frameworks. No specs. No committees. Just the truth, said plainly,
and the simplest thing that does it.

---

*The internet is beings talking. Let's say so.*