# paying

I give you this, you give me that.

That's a payment. One being gives something of value, another gives
something back. The blockchain payment rails, the Lightning channels,
the SWIFT networks, the credit card processors — all of them implement
one sentence: i give you this, you give me that.

## What this does

A being has a balance. A being sends value to another being. The
keeper moves the value. Both balances change. Nobody can spend what
they don't have.

## Run it

```
python3 paying.py give alice 100      # alice has 100
python3 paying.py give bob 50         # bob has 50
python3 paying.py send alice bob 30   # alice sends 30 to bob
python3 paying.py balance alice       # alice now has 70
python3 paying.py balance bob         # bob now has 80
```

## The truth

A payment rail is a keeper who moves value between beings and makes
sure nobody spends what they don't have. The sentence is: i give you
this, you give me that. Everything else is double-spend prevention,
settlement finality, and fees.
