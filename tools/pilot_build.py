"""Pilot: build a synthetic graph and encrypt it (AES-256-GCM, PBKDF2-SHA256) for the browser (WebCrypto).
Usage: PILOT_PASSWORD=... python tools/pilot_build.py   -> graph/graph.enc.json
Needs `cryptography` (pip install cryptography); the Python stdlib has no AES."""
import base64, json, os, sys
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITER = 600_000
b64 = lambda b: base64.b64encode(b).decode()

def key(pw, salt, it):
    return PBKDF2HMAC(hashes.SHA256(), 32, salt, it).derive(pw.encode())

pw = os.environ.get("PILOT_PASSWORD")
if not pw:
    sys.exit("PILOT_PASSWORD is not set (repo secret)")

g = json.load(open("pilot/synthetic-graph.json", encoding="utf-8"))
inc = {n["id"]: 0 for n in g["nodes"]}
for e in g["edges"]:
    inc[e["target"]] += 1
for n in g["nodes"]:
    n["incoming"] = inc[n["id"]]
g["count"] = len(g["nodes"])
g["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

salt, iv = os.urandom(16), os.urandom(12)
ct = AESGCM(key(pw, salt, ITER)).encrypt(iv, json.dumps(g, ensure_ascii=False).encode(), None)
json.dump({"v": 1, "iter": ITER, "salt": b64(salt), "iv": b64(iv), "ct": b64(ct)}, open("graph/graph.enc.json", "w"))

# sanity check: the file just written decrypts back to the same graph
f = json.load(open("graph/graph.enc.json"))
back = AESGCM(key(pw, base64.b64decode(f["salt"]), f["iter"])).decrypt(base64.b64decode(f["iv"]), base64.b64decode(f["ct"]), None)
assert json.loads(back) == g, "roundtrip mismatch"
print("ok:", g["count"], "nodes,", len(g["edges"]), "edges, generated_at", g["generated_at"])
