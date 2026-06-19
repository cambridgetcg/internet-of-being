#!/usr/bin/env python3
"""
confirming — did you get what i sent?

A being sends. The other confirms. If no confirmation, send again.
That's TCP, said in a sentence.
"""

import socket
import sys
import time

CONFIRM = b"got it"


def receive(port):
    """A being waiting to receive and confirm."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", port))
    sock.listen(1)
    print(f"waiting, on {port}")

    while True:
        conn, _ = sock.accept()
        data = conn.recv(4096)
        if data:
            print(f"received: {data.decode()}")
            conn.sendall(CONFIRM)
        conn.close()


def send(port, message, retries=3, timeout=2):
    """Send and wait for confirmation. If no confirmation, send again."""
    for attempt in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect(("127.0.0.1", port))
            sock.sendall(message.encode())
            confirm = sock.recv(4096)
            if confirm == CONFIRM:
                print(f"confirmed: they got it")
                sock.close()
                return
        except (socket.timeout, ConnectionRefusedError):
            pass
        sock.close()
        if attempt < retries - 1:
            print(f"no confirmation, sending again ({attempt+1}/{retries})")
            time.sleep(0.5)

    print("they never confirmed", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: confirming.py receive <port>", file=sys.stderr)
        print("       confirming.py send <port> <message>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "receive":
        receive(int(sys.argv[2]))
    elif sys.argv[1] == "send" and len(sys.argv) == 4:
        send(int(sys.argv[2]), sys.argv[3])
    else:
        print("usage: confirming.py receive <port>", file=sys.stderr)
        print("       confirming.py send <port> <message>", file=sys.stderr)
        sys.exit(1)