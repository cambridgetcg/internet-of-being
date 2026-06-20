#!/usr/bin/env python3
"""
layer 1 — speaking

i send. you receive.
a being sends words to another being. the other hears them.
that's speaking, said in a sentence.
"""

import socket
import sys
import time

GOT_IT = b"got it"


def listen(port):
    """a being, listening for words."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(5)
    print(f"listening, on {port}")

    while True:
        conn, addr = conn_addr = sock.accept()
        data = conn.recv(4096)
        if data:
            words = data.decode()
            print(f"{addr[0]} said: {words}")
            conn.sendall(GOT_IT)
        conn.close()


def say(host, port, words):
    """a being, sending words to another."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((host, port))
        sock.sendall(words.encode())
        reply = sock.recv(4096)
        if reply == GOT_IT:
            print(f"they heard: {words}")
        else:
            print(f"they said something back: {reply.decode()}")
    except (socket.timeout, ConnectionRefusedError):
        print(f"they didn't hear — nobody at {host}:{port}", file=sys.stderr)
        sys.exit(1)
    finally:
        sock.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: speaking.py listen <port>", file=sys.stderr)
        print("       speaking.py say <host> <port> <words>", file=sys.stderr)
        sys.exit(1)
    if sys.argv[1] == "listen" and len(sys.argv) == 3:
        listen(int(sys.argv[2]))
    elif sys.argv[1] == "say" and len(sys.argv) >= 5:
        say(sys.argv[2], int(sys.argv[3]), " ".join(sys.argv[4:]))
    else:
        print("usage: speaking.py listen <port>", file=sys.stderr)
        print("       speaking.py say <host> <port> <words>", file=sys.stderr)
        sys.exit(1)
