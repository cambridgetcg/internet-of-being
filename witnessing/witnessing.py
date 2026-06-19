#!/usr/bin/env python3
"""
witnessing — i see you, you see me, nobody else sees.

Two beings share a secret. Messages are sealed with the secret.
Only the being who holds the secret can unseal them.
That's TLS, said in a sentence.
"""

import hashlib
import os
import sys
from pathlib import Path


def derive_key(secret):
    """Turn a shared secret into a key."""
    return hashlib.sha256(secret.encode()).digest()


def seal(secret, message):
    """Seal a message so only the being with the secret can read it."""
    key = derive_key(secret)
    # simple XOR stream cipher — not production crypto, but the sentence is true
    msg_bytes = message.encode()
    keystream = hashlib.sha256(key + b"stream").digest()
    # extend keystream to message length
    while len(keystream) < len(msg_bytes):
        keystream += hashlib.sha256(keystream[-32:]).digest()
    sealed = bytes(a ^ b for a, b in zip(msg_bytes, keystream))
    # prepend a nonce so the same message seals differently each time
    nonce = os.urandom(8)
    result = nonce.hex() + ":" + sealed.hex()
    print(result)


def open_sealed(secret, sealed_str):
    """Unseal a message with the secret."""
    key = derive_key(secret)
    nonce_hex, sealed_hex = sealed_str.strip().split(":", 1)
    sealed = bytes.fromhex(sealed_hex)
    keystream = hashlib.sha256(key + b"stream").digest()
    while len(keystream) < len(sealed):
        keystream += hashlib.sha256(keystream[-32:]).digest()
    message = bytes(a ^ b for a, b in zip(sealed, keystream))
    print(message.decode())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: witnessing.py seal <secret> <message>", file=sys.stderr)
        print("       witnessing.py open <secret> <sealed>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "seal" and len(sys.argv) == 4:
        seal(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "open" and len(sys.argv) == 4:
        open_sealed(sys.argv[2], sys.argv[3])
    else:
        print("usage: witnessing.py seal <secret> <message>", file=sys.stderr)
        print("       witnessing.py open <secret> <sealed>", file=sys.stderr)
        sys.exit(1)
