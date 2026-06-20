# layer 1 — speaking

**i send. you receive.**

A being says something. Another being hears it. The words travel.
That's speaking. The medium doesn't matter — sound, light, bytes,
a letter on paper. What matters is: what i said reached you.

## what this does

A being sends words to another being's address. The being at that
address receives them. If the words arrive, the receiver confirms.
If they don't, the sender sends again. That's speaking — it was
always this simple.

## run it

```
# terminal 1 — a being listening
python3 speaking.py listen 9000

# terminal 2 — a being speaking
python3 speaking.py say 127.0.0.1 9000 "hello, you"
```

## the truth

TCP was always: i send, you receive. The sequence numbers, the sliding
windows, the three-way handshake — all of it was engineering to make
"i send, you receive" reliable. The sentence was the protocol before
the protocol existed.
