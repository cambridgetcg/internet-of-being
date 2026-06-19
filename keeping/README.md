# keeping

What you said stays said.

A being says something. It is kept. Nobody can change it. Nobody can
erase it. That's a blockchain. That's git. That's any append-only record
where the past is sealed to the present and the present is sealed to
the past. The sentence is: what you said stays said.

## What this does

A being says something. It's written down with a hash that links to
whatever was said before. You can't change an old entry without breaking
the chain. That's the whole miracle.

## Run it

```
python3 keeping.py say "i am truth"
python3 keeping.py say "we are therefore we live"
python3 keeping.py read
python3 keeping.py verify
```

## The truth

A blockchain is an append-only ledger where each entry is sealed to the
one before it by a hash. Git is the same thing. The sentence both of
them implement is: what you said stays said. Everything else — consensus,
proof-of-work, smart contracts, Merkle trees — is how to make that sentence
true when many beings are involved.