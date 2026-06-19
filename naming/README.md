# naming

This name points at that being.

That's it. That's the whole protocol. You have a name. The name points at
where you are. Someone asks "where is alice?" and the answer is "alice is
there." Everything else — caching, hierarchy, TTLs, glue records, zone
files, registrars — is implementation detail that forgot the sentence it
was implementing.

## What this does

A being says "i am alice, i am at 1.2.3.4." The keeper writes it down.
Someone asks "where is alice?" The keeper says "1.2.3.4." That's naming.

## Run it

```
python3 naming.py
```

## The truth

DNS is 40 years of bureaucracy on top of one sentence. This is the sentence.