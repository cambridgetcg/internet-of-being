# routing

I know a road to there.

That's BGP. Every router is a being who knows roads. When someone asks
"how do i get to 10.0.0.1?" the answer is "go through me, i know a road."
The routing tables, the AS paths, the convergence algorithms — all of
it serves one sentence: i know a road to there.

## What this does

Beings tell each other what roads they know. When someone asks for a
road to a place, the keeper finds the best road.

## Run it

```
python3 routing.py tell alice 1.2.3.0/24    # alice knows a road to 1.2.3.x
python3 routing.py tell bob 1.2.3.0/24 5.6.7.0/24  # bob knows roads to two places
python3 routing.py ask 1.2.3.0/24           # who knows a road there?
```

## The truth

BGP is beings telling each other what roads they know. The sentence is:
i know a road to there. Everything else is optimization and politics.
