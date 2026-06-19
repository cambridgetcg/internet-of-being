# witnessing

I see you, you see me, nobody else sees.

That's TLS. Two beings recognize each other, and what passes between
them is sealed from everyone else. The handshake, the certificates,
the cipher suites — all of it serves one sentence: i see you, you see
me, nobody else sees.

## What this does

Two beings share a secret. Messages are sealed with the secret. Only
the being who holds the secret can unseal them. Anyone watching sees
noise.

## Run it

```
python3 witnessing.py seal <secret> "hello only you"
python3 witnessing.py open <secret> <sealed>
```

## The truth

TLS is two beings proving they recognize each other, then talking in a
way only they can read. The sentence is: i see you, you see me, nobody
else sees. Everything else is math making that true.
