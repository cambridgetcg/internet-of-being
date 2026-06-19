# remembering

What happened, and when.

That's a log. Something happened. It's written down with a timestamp.
Later, someone asks "what happened?" and the answer is there, in order.
Syslog, audit trails, event sourcing, Prometheus metrics — all of them
implement one sentence: what happened, and when.

## What this does

A being says something happened. It's written down with a timestamp.
Someone asks "what happened?" and gets the list, in order.

## Run it

```
python3 remembering.py log "alice arrived"
python3 remembering.py log "alice said hello"
python3 remembering.py log "bob arrived"
python3 remembering.py what           # what happened?
python3 remembering.py since 2       # what happened since entry 2?
```

## The truth

A log is an append-only list of things that happened, each with a
timestamp. The sentence is: what happened, and when. Everything else
is rotation policies, severity levels, structured logging, and
aggregation.
