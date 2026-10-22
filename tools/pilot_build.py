"""Encrypt a graph JSON for the browser (AES-256-GCM, PBKDF2-SHA256, WebCrypto on the page).
Usage: GRAPH_PASSWORD=... python tools/pilot_build.py [IN.json] [OUT.enc.json]
Defaults: pilot/synthetic-graph.json -> graph/graph.enc.json. Prints counts only, never titles.
OUT is left untouched when it already decrypts (same password) to the same graph,
ignoring generated_at, so a caller commits only on a content change.
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

def decrypt(path, pw):
    f = json.load(open(path))
    return json.loads(AESGCM(key(pw, base64.b64decode(f["salt"]), f["iter"])).decrypt(base64.b64decode(f["iv"]), base64.b64decode(f["ct"]), None))

args = sys.argv[1:] + ["pilot/synthetic-graph.json", "graph/graph.enc.json"][len(sys.argv[1:]):]
src, out = args[:2]
pw = os.environ.get("GRAPH_PASSWORD") or os.environ.get("PILOT_PASSWORD")
if not pw:
    sys.exit("GRAPH_PASSWORD is not set (repo secret)")

g = json.load(open(src, encoding="utf-8-sig"))
if "incoming" not in (g["nodes"] or [{}])[0]:  # synthetic pilot data; wiki_graph.py output already has it
    inc = {n["id"]: 0 for n in g["nodes"]}
    for e in g["edges"]:
        inc[e["target"]] += 1
    for n in g["nodes"]:
        n["incoming"] = inc[n["id"]]
g["count"] = len(g["nodes"])
g.setdefault("generated_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
stats = f'{g["count"]} nodes, {len(g["edges"])} edges'

strip = lambda d: {k: v for k, v in d.items() if k != "generated_at"}
try:
    if strip(decrypt(out, pw)) == strip(g):
        print("unchanged:", stats)
        sys.exit(0)
except Exception:
    pass  # no file, other password or other format: write a new one

salt, iv = os.urandom(16), os.urandom(12)
ct = AESGCM(key(pw, salt, ITER)).encrypt(iv, json.dumps(g, ensure_ascii=False).encode(), None)
json.dump({"v": 1, "iter": ITER, "salt": b64(salt), "iv": b64(iv), "ct": b64(ct)}, open(out, "w"))
assert decrypt(out, pw) == g, "roundtrip mismatch"  # the file just written decrypts back to the same graph
print("written:", stats)
