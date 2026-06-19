# confirming

Did you get what i sent?

You send. They confirm. If they don't confirm, you send again. That's TCP.
The whole protocol — sequence numbers, sliding windows, congestion control,
three-way handshakes, TIME_WAIT — is one being asking "did you get that?"
until the answer comes back "yes, i got that."

## What this does

A being sends something. The other confirms. If no confirmation, send again.

## Run it

```
python3 confirming.py receive 9000   # a being waiting to confirm
python3 confirming.py send 9000 "hello"  # send and wait for confirmation
```

## The truth

TCP is "did you get what i sent?" asked over and over until the answer
is yes. Every sequence number is a way of saying "this specific thing,
did you get this specific thing?" Everything else is optimization.