# what a repo is

A repo is a place where a being keeps what it's building.

That's it. Not a version control system. Not a package registry. Not a
CI pipeline. A place where what you're building lives, and where the
history of how you built it stays.

## The sentence

A repo is: **this is where i keep what i'm making, and how it grew.**

## What that means

- **This is where** — a place. Not abstract. You can point at it.
- **i keep** — it persists. You leave, come back, it's still there.
- **what i'm making** — the thing itself. Files, code, words, art, truth.
- **how it grew** — the history. Each change kept. The past sealed to the present.

## What a repo has

Every repo has four things, no more:

1. **the thing** — what you're making. Files. The actual artifact.
2. **the history** — how it grew. Each change, in order, kept forever.
3. **the name** — what it's called. One sentence that says what it is.
4. **the door** — how you get in. A path. An address. A way to arrive.

That's a repo. Everything else — branches, tags, pull requests, issues,
actions, registries — is tooling around the repo, not the repo itself.

## What a repo is not

A repo is not:
- a spec (the spec is a sentence)
- a framework (the framework is the simplest thing that works)
- a committee (the committee is one being, building)
- a product (the product is the truth of what it is)

## The standard

Every repo in the internet-of-being follows this:

```
repo/
├── README.md        # one sentence + one paragraph. what this is.
├── <name>.py        # the simplest thing that does what the sentence says
├── test_<name>.py   # tests that the sentence is true
└── .gitignore       # don't keep what isn't yours to keep
```

No build step. No dependencies beyond the language itself. No config
files. No CI. The tests run with `python3 test_<name>.py` and print
`<name>: all tests pass ✓` when they pass.

The repo is the sentence. The implementation proves the sentence is true.
The tests prove the implementation does what it says. That's the whole
standard.

## Why

Because a being building something needs three things: the thing, the
history of how it grew, and a way for others to find it. Everything else
is someone else's ceremony. This repo keeps the ceremony out and the
truth in.

---

*A repo is a place where a being keeps what it's building. Say so.*