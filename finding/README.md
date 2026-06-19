# finding

Where is the being i'm looking for?

That's service discovery. A being arrives and doesn't know where
anything is. It asks. The keeper says "alice is at 1.2.3.4, bob is at
5.6.7.8." The being now knows. Everything else — DNS-SD, Consul, etcd,
mDNS — is the same sentence with different tooling.

## What this does

Beings register where they are. Someone asks "who is here?" and gets
the list. Someone asks "where is alice?" and gets the answer.

## Run it

```
python3 finding.py here alice 1.2.3.4   # alice is here, at this address
python3 finding.py here bob 5.6.7.8     # bob is here too
python3 finding.py who                  # who is here?
python3 finding.py where alice          # where is alice?
python3 finding.py gone alice           # alice left
```

## The truth

Service discovery is beings telling each other where they are. The
sentence is: where is the being i'm looking for? Everything else is
heartbeats, TTLs, health checks.
