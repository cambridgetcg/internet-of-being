#!/usr/bin/env python3
"""
requesting — give me what you have.

A being asks for something. The keeper gives it or says they don't have it.
That's HTTP, said in a sentence.

Serve: a being that has things, listening for asks.
Ask: a being that wants something, asking a keeper for it.
"""

import json
import socket
import sys
from pathlib import Path

THINGS_FILE = Path(__file__).parent / "things.json"

DEFAULT_THINGS = {
    "/hello": "hello, being",
    "/truth": "i am therefore i think",
    "/love": "love is not what we do. it is what we are, doing.",
}


def load_things():
    if THINGS_FILE.exists():
        return json.loads(THINGS_FILE.read_text())
    return dict(DEFAULT_THINGS)


def serve(port=8000):
    """A being that has things, listening for asks."""
    things = load_things()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", port))
    sock.listen(5)
    print(f"i have {len(things)} things, listening on {port}")

    while True:
        conn, addr = sock.accept()
        data = conn.recv(4096).decode().strip()
        if not data:
            conn.close()
            continue

        # the ask is just the path: "/hello"
        path = data.split()[0] if data else "/"

        if path in things:
            body = things[path]
            conn.sendall(f"200 here\n{body}".encode())
        else:
            conn.sendall(b"404 i don't have that\n")
        conn.close()


def ask(host, port, path):
    """A being asks: give me what you have at this path."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(path.encode())
    response = sock.recv(4096).decode()
    sock.close()

    if response.startswith("200"):
        # everything after "200 here\n"
        body = response.split("\n", 1)[1] if "\n" in response else ""
        print(body)
    elif response.startswith("404"):
        print("they don't have that", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: requesting.py serve [port]", file=sys.stderr)
        print("       requesting.py ask <host> <port> <path>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        serve(port)
    elif sys.argv[1] == "ask" and len(sys.argv) == 5:
        ask(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        print("usage: requesting.py serve [port]", file=sys.stderr)
        print("       requesting.py ask <host> <port> <path>", file=sys.stderr)
        sys.exit(1)