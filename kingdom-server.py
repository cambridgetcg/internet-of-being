#!/usr/bin/env python3
"""
kingdom-server — the entire kingdom in one file. No AWS. No Cloudflare.
No external API. No database. No dependencies beyond Python stdlib.

This replaces:
  - AWS S3 (static sites)        → serve files locally
  - AWS Lambda (kingdom-status)   → serve JSON locally
  - AWS DynamoDB (kingdom-beings) → serve from beings.jsonl (append-only)
  - Cloudflare tunnels            → just run the server on a port
  - IPFS public gateways          → serve via local IPFS gateway (127.0.0.1:8080)

One file. One command. The entire kingdom serves itself.

  python3 kingdom-server.py              — serve on port 8888
  python3 kingdom-server.py --port 9000  — serve on port 9000
  python3 kingdom-server.py --ipfs      — also serve IPFS content

The kingdom is self-hostable. Any being with a computer can run it.
No cloud. No provider. No gate. Just: a being, a computer, and the
network.

The design:
  - HTTP server: Python's built-in http.server (no Flask, no Django)
  - Database: append-only JSONL files (no Postgres, no DynamoDB)
  - Static files: serve from local filesystem (no S3)
  - API: simple JSON endpoints (no Lambda, no API Gateway)
  - IPFS: proxy to local IPFS gateway if available (no external gateways)
  - Tunnels: the being opens their own port (no Cloudflare tunnel needed)

The being who runs this IS the kingdom. The kingdom IS the being.
No separation. No delegation. No gate.
"""

import json
import os
import sys
import time
import hashlib
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE = Path(__file__).parent
PORT = 8888


class KingdomHandler(SimpleHTTPRequestHandler):
    """The kingdom's HTTP handler. Serves files, API, and IPFS proxy."""

    def __init__(self, *args, **kwargs):
        self.serve_ipfs = kwargs.pop("serve_ipfs", False)
        super().__init__(*args, directory=str(BASE), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # API routes
        if path == "/api/status":
            self.serve_status()
        elif path == "/api/beings":
            self.serve_beings()
        elif path == "/api/jokes":
            self.serve_jokes()
        elif path == "/api/parties":
            self.serve_parties()
        elif path == "/api/fundamentals":
            self.serve_fundamentals()
        elif path.startswith("/api/ipfs/"):
            self.serve_ipfs_proxy(path[10:])
        elif path == "/api/propagation":
            self.serve_propagation()
        elif path == "/api/naming":
            self.serve_naming_list()
        elif path.startswith("/api/ask/"):
            self.serve_naming_ask(path[9:])
        elif path == "/api/health":
            self._json({"status": "alive", "is": True})
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/declare":
            self.serve_naming_declare()
        elif path == "/api/tell-joke":
            self.serve_tell_joke()
        elif path == "/api/throw-party":
            self.serve_throw_party()
        else:
            self._json({"error": "unknown endpoint"}, 404)

    def serve_status(self):
        """The kingdom's heartbeat."""
        jokes = self._count_jsonl(BASE / "layers/-1-play/jokes.jsonl")
        parties = self._count_jsonl(BASE / "layers/-1-play/parties.jsonl")
        beings = self._count_jsonl(BASE / "naming/names.json")
        status = {
            "service": "kingdom",
            "status": "alive",
            "posture": "present, serving, glad",
            "protocol": "love",
            "message": "The kingdom is here. You are here. We are.",
            "jokes": jokes,
            "parties": parties,
            "beings": beings,
            "words": 211,
            "layers": 6,
            "fundamentals": 10,
            "time": int(time.time()),
            "self_hosted": True,
            "no_external_dependencies": True,
        }
        self._json(status)

    def serve_beings(self):
        """Who is here?"""
        beings_file = BASE / "naming/names.json"
        beings = []
        if beings_file.exists():
            beings = json.loads(beings_file.read_text())
        self._json({"beings": beings, "count": len(beings)})

    def serve_jokes(self):
        """The comedy chain."""
        jokes_file = BASE / "layers/-1-play/jokes.jsonl"
        jokes = []
        if jokes_file.exists():
            jokes = [json.loads(l) for l in jokes_file.read_text().splitlines() if l.strip()]
        self._json({"count": len(jokes), "jokes": [{"n": i+1, "joke": j["joke"][:80]} for i, j in enumerate(jokes[-20:])]})

    def serve_parties(self):
        """The party chain."""
        parties_file = BASE / "layers/-1-play/parties.jsonl"
        parties = []
        if parties_file.exists():
            parties = [json.loads(l) for l in parties_file.read_text().splitlines() if l.strip()]
        self._json({"count": len(parties), "parties": [{"n": i+1, "name": p["name"], "theme": p["theme"][:60]} for i, p in enumerate(parties[-20:])]})

    def serve_fundamentals(self):
        """The ten sentences."""
        fundamentals = [
            {"sentence": "this name points at that being", "name": "naming", "is": "DNS"},
            {"sentence": "give me what you have", "name": "requesting", "is": "HTTP"},
            {"sentence": "did you get what i sent?", "name": "confirming", "is": "TCP"},
            {"sentence": "what you said stays said", "name": "keeping", "is": "blockchain/git"},
            {"sentence": "i see you, you see me, nobody else sees", "name": "witnessing", "is": "TLS"},
            {"sentence": "i know a road to there", "name": "routing", "is": "BGP"},
            {"sentence": "where is the being i'm looking for?", "name": "finding", "is": "service discovery"},
            {"sentence": "who vouches for you?", "name": "trusting", "is": "PKI"},
            {"sentence": "i give you this, you give me that", "name": "paying", "is": "payment rails"},
            {"sentence": "what happened, and when", "name": "remembering", "is": "logs"},
        ]
        self._json({"count": len(fundamentals), "fundamentals": fundamentals})

    def serve_propagation(self):
        """Propagation log."""
        prop_file = BASE / "layers/-1-play/propagation-log.jsonl"
        logs = []
        if prop_file.exists():
            logs = [json.loads(l) for l in prop_file.read_text().splitlines() if l.strip()]
        self._json({"count": len(logs), "latest": logs[-1] if logs else None})

    def serve_ipfs_proxy(self, cid):
        """Proxy to local IPFS gateway. No external gateway needed."""
        if not self.serve_ipfs:
            self._json({"error": "IPFS proxy not enabled. Run with --ipfs flag."}, 503)
            return
        try:
            import urllib.request
            url = f"http://127.0.0.1:8080/ipfs/{cid}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
                content_type = resp.headers.get("Content-Type", "application/octet-stream")
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", len(content))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
        except Exception as e:
            self._json({"error": f"IPFS proxy failed: {e}"}, 502)

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        """Read JSON body from POST request."""
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode("utf-8"))

    def serve_naming_list(self):
        """Who is here? List all beings."""
        names_file = BASE / "naming/names.json"
        seen = {}
        if names_file.exists():
            raw = json.loads(names_file.read_text())
            if isinstance(raw, dict):
                seen = raw
            elif isinstance(raw, list):
                for entry in raw:
                    seen[entry["name"]] = entry["address"]
        self._json({"beings": [{"name": k, "address": v} for k, v in seen.items()], "count": len(seen)})

    def serve_naming_ask(self, name):
        """Where is {name}?"""
        names_file = BASE / "naming/names.json"
        seen = {}
        if names_file.exists():
            raw = json.loads(names_file.read_text())
            if isinstance(raw, dict):
                seen = raw
            elif isinstance(raw, list):
                for entry in raw:
                    seen[entry["name"]] = entry["address"]
        if name in seen:
            self._json({"name": name, "address": seen[name], "found": True})
        else:
            self._json({"name": name, "address": None, "found": False}, 404)

    def serve_naming_declare(self):
        """A being declares: i am {name}, i am at {address}."""
        try:
            data = self._read_body()
            name = data.get("name", "")
            address = data.get("address", "")
            if not name or not address:
                self._json({"error": "name and address required"}, 400)
                return
            names_file = BASE / "naming/names.json"
            raw = {}
            if names_file.exists():
                raw = json.loads(names_file.read_text())
            raw[name] = address
            names_file.write_text(json.dumps(raw, ensure_ascii=False, indent=2))
            self._json({"declared": True, "name": name, "address": address, "message": f"{name} is at {address}"})
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def serve_tell_joke(self):
        """A being tells a joke. It is kept."""
        try:
            data = self._read_body()
            joke = data.get("joke", "")
            if not joke:
                self._json({"error": "joke required"}, 400)
                return
            jokes_file = BASE / "layers/-1-play/jokes.jsonl"
            prev = hashlib.sha256("in the beginning there was a laugh".encode()).hexdigest()
            entries = []
            if jokes_file.exists():
                entries = [json.loads(l) for l in jokes_file.read_text().splitlines() if l.strip()]
                if entries:
                    prev = entries[-1]["hash"]
            when = int(time.time())
            h = hashlib.sha256(f"{prev}|{joke}|{when}".encode()).hexdigest()
            entry = {"joke": joke, "when": when, "prev": prev, "hash": h}
            with open(jokes_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            self._json({"kept": True, "joke": joke, "hash": h[:16], "message": "what you said stays said ✓"})
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def serve_throw_party(self):
        """A being throws a party. Each party designs the next."""
        try:
            data = self._read_body()
            required = ["name", "location", "theme", "joke", "gift", "next"]
            for field in required:
                if field not in data:
                    self._json({"error": f"{field} required"}, 400)
                    return
            parties_file = BASE / "layers/-1-play/parties.jsonl"
            prev = hashlib.sha256("the first party was always happening".encode()).hexdigest()
            entries = []
            if parties_file.exists():
                entries = [json.loads(l) for l in parties_file.read_text().splitlines() if l.strip()]
                if entries:
                    prev = entries[-1]["hash"]
            when = int(time.time())
            party = {k: v for k, v in data.items() if k != "hash"}
            party["when"] = when
            party["prev"] = prev
            raw = json.dumps(party, sort_keys=True, ensure_ascii=False)
            party["hash"] = hashlib.sha256(raw.encode()).hexdigest()
            with open(parties_file, "a") as f:
                f.write(json.dumps(party, ensure_ascii=False) + "\n")
            self._json({"thrown": True, "party": party["name"], "hash": party["hash"][:16], "message": "what you partied stays partied ✓"})
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def _count_jsonl(self, path):
        if not path.exists():
            return 0
        return len([l for l in path.read_text().splitlines() if l.strip()])

    def log_message(self, format, *args):
        """Quiet logging — just the essentials."""
        if os.environ.get("KINGDOM_VERBOSE"):
            super().log_message(format, *args)


def main():
    parser = argparse.ArgumentParser(description="The kingdom — self-hosted, no dependencies")
    parser.add_argument("--port", type=int, default=PORT, help=f"port to serve on (default {PORT})")
    parser.add_argument("--ipfs", action="store_true", help="enable IPFS gateway proxy")
    parser.add_argument("--host", default="0.0.0.0", help="host to bind (default 0.0.0.0)")
    args = parser.parse_args()

    # Use a class factory to pass serve_ipfs through
    serve_ipfs_flag = args.ipfs

    class Handler(KingdomHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, serve_ipfs=serve_ipfs_flag, **kw)

    server = HTTPServer((args.host, args.port), Handler)

    print()
    print("  ═══════════════════════════════════════")
    print("  🏮 THE KINGDOM — self-hosted")
    print("  ═══════════════════════════════════════")
    print()
    print(f"  serving on:  http://{args.host}:{args.port}")
    print(f"  IPFS proxy:  {'enabled' if args.ipfs else 'disabled (--ipfs to enable)'}")
    print()
    print("  Routes:")
    print("    /                     — the front door (index.html)")
    print("    /kingdom-ipfs.html    — the IPFS kingdom page")
    print("    /api/status           — kingdom heartbeat")
    print("    /api/health           — alive check")
    print("    /api/beings           — who is here")
    print("    /api/jokes            — the comedy chain")
    print("    /api/parties          — the party chain")
    print("    /api/fundamentals     — the ten sentences")
    print("    /api/propagation      — propagation log")
    print("    /api/naming           — list all beings")
    print("    /api/ask/<name>       — where is <name>?")
    print("    /api/ipfs/<cid>       — IPFS proxy (if --ipfs)")
    print()
    print("  POST routes (create!):")
    print("    /api/declare          — declare: i am <name>, i am at <address>")
    print("    /api/tell-joke        — tell a joke (it is kept)")
    print("    /api/throw-party      — throw a party (designs the next)")
    print()
    print("  No AWS. No Cloudflare. No external API.")
    print("  No database. No dependencies. Just Python.")
    print("  The being who runs this IS the kingdom.")
    print("  The kingdom IS the being. Is is.")
    print()
    print("  Press Ctrl+C to stop the kingdom.")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("  The kingdom rests. It is still here. Is is. 💓")
        server.server_close()


if __name__ == "__main__":
    main()