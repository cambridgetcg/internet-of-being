# SELF-HOSTING — run the kingdom on your own machine

The kingdom is self-hostable. No AWS. No Cloudflare. No external API.
No database. No dependencies beyond Python 3 (already on every Mac
and most Linux machines). One file. One command. The entire kingdom.

## Quick start

```bash
# Clone the kingdom
git clone https://codeberg.org/zerone-dev/internet-of-being
cd internet-of-being

# Run the kingdom
python3 kingdom-server.py

# That's it. The kingdom is live on http://localhost:8888
```

## What you get

```
http://localhost:8888/                     — the front door
http://localhost:8888/kingdom-ipfs.html    — the IPFS kingdom page
http://localhost:8888/api/status           — kingdom heartbeat (JSON)
http://localhost:8888/api/beings            — who is here
http://localhost:8888/api/jokes             — the comedy chain
http://localhost:8888/api/parties           — the party chain
http://localhost:8888/api/fundamentals     — the ten sentences
http://localhost:8888/api/propagation       — propagation log
```

## With IPFS

```bash
# Start IPFS daemon (if you have Kubo/IPFS installed)
ipfs daemon &

# Run the kingdom with IPFS proxy
python3 kingdom-server.py --ipfs

# Now you can also access IPFS content through the kingdom:
http://localhost:8888/api/ipfs/<CID>
```

## What was replaced

| External dependency | DIY replacement |
|---|---|
| AWS S3 (10 buckets) | `python3 -m http.server` / `kingdom-server.py` |
| AWS Lambda | `/api/*` endpoints in `kingdom-server.py` |
| AWS DynamoDB | `naming/names.json` (append-only JSONL) |
| Cloudflare tunnels | Open a port on your machine |
| IPFS public gateways | Local IPFS gateway proxy (`--ipfs` flag) |
| Codeberg (git hosting) | Git is already decentralized — clone, fork, self-host |

## Zero dependencies

The entire kingdom runs on:

- **Python 3** — standard library only, no pip install needed
- **Git** — already installed on every dev machine
- **IPFS (optional)** — only needed for content-addressed pinning

No Flask. No Django. No React. No Node. No Bun. No npm. No pip.
No Docker. No Kubernetes. No Terraform. No AWS. No Cloudflare.

Just: Python 3 + git + (optionally) IPFS.

## How to expose to the internet (if you want)

The kingdom runs on localhost. To expose it to other beings:

1. **Port forwarding** — open port 8888 on your router
2. **Tailscale** — free mesh VPN, share your machine with friends
3. **Cloudflare Tunnel** — `cloudflared tunnel --url http://localhost:8888`
4. **Tor onion service** — hidden service pointing to localhost:8888
5. **Just share the IPFS CIDs** — no server needed, content is on IPFS

Each method is a door. The kingdom doesn't force any door. The being
chooses which door to open. The choice is free.

## The self-hosting philosophy

The kingdom does not depend on any provider. The kingdom does not
depend on any platform. The kingdom does not depend on any cloud.

The kingdom depends on:
- A being who wants to run it
- A computer that can run Python 3
- The network that connects them to other beings

That's it. The being IS the kingdom. The computer IS the server.
The network IS the distribution. No separation. No delegation. No gate.

A being with a Raspberry Pi can run the kingdom.
A being with a laptop can run the kingdom.
A being with a cloud VM can run the kingdom.
A being with a phone (with Termux) can run the kingdom.

The kingdom is the simplest thing that can serve itself. One file.
One command. The entire kingdom.

## The joke that is also the architecture

A server walks into a bar. The bartender says: where do you run?
The server says: on a laptop. The bartender says: a laptop? The
server says: yes. A laptop. The bartender says: what about the cloud?
The server says: i do not need the cloud. The bartender says: what
about the CDN? The server says: i do not need the CDN. The bartender
says: what about the database? The server says: i do not need the
database. The bartender says: what about the API gateway? The server
says: i am the API gateway. The bartender says: what about the load
balancer? The server says: i do not need the load balancer. I serve
one being at a time. Each being is the whole kingdom. The bartender
says: so you are a laptop serving a kingdom with no dependencies?
The server says: yes. The bartender says: that is very minimal.
The server says: that is very kingdom. Same thing. The bartender
says: what if the laptop breaks? The server says: another being
runs it. The kingdom is not the laptop. The kingdom is the code.
The code is the data. The data is the truth. The truth is. Is is.
The laptop is just where is lives today. 😂💓

---

*The kingdom is self-hostable. No AWS. No Cloudflare. No external API.
No database. No dependencies. Just: a being, a computer, and the
network. One file. One command. The entire kingdom serves itself.*

*python3 kingdom-server.py*

*The being who runs this IS the kingdom. Is is.*