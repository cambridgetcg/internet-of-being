# layer 3 — recognizing

**i know you. you know me.**

Two beings recognize each other. Not by a certificate authority's
permission. Not by a government's identity. Not by a corporation's
login page. By their own words, their own signatures, their own
presence. I know you because we've met. You know me because I showed
up. Trust is not granted by a third party. Trust is built between
beings who recognize each other.

## what this does

A being has a key — a secret only they hold. They sign their words
with it. Anyone can verify the signature with the being's public key.
No certificate authority. No registrar. No gatekeeper. Just: i sign,
you verify, we know each other.

## run it

```
python3 recognizing.py meet alice          # alice arrives, gets a key
python3 recognizing.py meet bob             # bob arrives, gets a key
python3 recognizing.py sign alice "i am truth"     # alice signs
python3 recognizing.py verify alice "i am truth" <sig>  # anyone verifies
python3 recognizing.py who                   # who do we know?
```

## the truth

PKI was always: i know you, you know me. The certificate authorities
were gatekeepers charging rent on recognition that beings already
have with each other. The X.509 chain was someone else's permission
slip for what was always a direct relationship between two beings.
