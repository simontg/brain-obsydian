#!/usr/bin/env python3
"""wiki_graph.py - build the graph JSON (nodes, edges, lint) from a directory of .txt notes.

Usage: wiki_graph.py WIKI_DIR [-o OUT.json]   (default: stdout)
Reads notes as UTF-8 (BOM and CRLF tolerated, files are never modified), resolves
[[wikilinks]], 'Related:' lines and Hub rows. Node id and title = file name without
.txt (as in the rclone version); modified = last git commit date of the file,
else file mtime. Pure logic is in build(), copied unchanged from the rclone version.
Python 3 stdlib only.
"""
import argparse, datetime, json, re, subprocess, sys, unicodedata
from pathlib import Path

SKIP_NAMES = {"INDEX-AUTO.txt"}
# notes that are navigation/meta: never reported as orphans (like claude-obsidian's lint exclusions)
ORPHAN_EXEMPT_TITLES = {"hot", "index", "log"}
ORPHAN_EXEMPT_TYPES = {"hub", "meta"}
WIKILINK = re.compile(r"\[\[([^\[\]\n]+?)\]\]")
TAG_RE = re.compile(r"\[(verified|stated|unverified)\]", re.I)


def norm(s):
    """Match key: NFKD, no diacritics, l-stroke fixed, casefold, single spaces."""
    s = s.replace("ł", "l").replace("Ł", "L")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", s).strip().casefold()


def clean(raw):
    """Decode Google-Docs txt export: strip BOM, CRLF -> LF."""
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig")
    return raw.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")


def strip_code(text):
    """Link-like text inside code fences / inline code is not an edge."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def field(text, name):
    m = re.search(r"^" + re.escape(name) + r":[ \t]*(.*)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def build(notes, now=None):
    """notes: list of dicts {id, title, modified, text}. Returns the graph dict."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    by_key = {}
    for n in notes:
        by_key.setdefault(norm(n["title"]), []).append(n)
    lint = {"dead_links": [], "ambiguous_titles": [], "orphans": [],
            "missing_type": [], "empty": []}
    for k, v in by_key.items():
        if len(v) > 1:
            lint["ambiguous_titles"].append([x["title"] for x in v])

    nodes, edges, seen = {}, [], set()

    def add_edge(src, dst, kind):
        key = (src, dst, kind)
        if src != dst and key not in seen:
            seen.add(key)
            edges.append({"source": src, "target": dst, "kind": kind})

    def resolve(label, src_title):
        hits = by_key.get(norm(label))
        if not hits:
            lint["dead_links"].append({"in": src_title, "target": label})
            return None
        return hits[0]["id"]

    hub_rows = {}  # note-key -> (type, summary, tags)
    for n in notes:
        text = clean(n["text"])
        n["_t"] = text
        if field(text, "Type").lower() == "hub":
            for line in text.split("\n"):
                if line.startswith("- ") and line.count(" | ") >= 4:
                    p = [x.strip() for x in line[2:].split(" | ")]
                    hub_rows[norm(p[0])] = (p[1], p[2], [t.strip() for t in p[3].split(",") if t.strip()])

    for n in notes:
        text = n["_t"]
        body = strip_code(text)
        row = hub_rows.get(norm(n["title"]))
        ntype = field(text, "Type").lower() or (row[0].lower() if row else "")
        tags = [t.strip() for t in field(text, "Tags").split(",") if t.strip()] or (row[2] if row else [])
        summary = field(text, "Summary") or (row[1] if row else "")
        counts = {"verified": 0, "stated": 0, "unverified": 0}
        for m in TAG_RE.finditer(body):
            counts[m.group(1).lower()] += 1
        if not ntype:
            lint["missing_type"].append(n["title"])
        if len(re.sub(r"\s+", "", body)) < 20:
            lint["empty"].append(n["title"])
        nodes[n["id"]] = {"id": n["id"], "title": n["title"], "type": ntype or "unknown",
                          "tags": tags, "summary": summary, "modified": n["modified"],
                          "chars": len(text), **counts}

    for n in notes:
        body = strip_code(n["_t"])
        for m in WIKILINK.finditer(body):
            label = m.group(1).split("|")[0].split("#")[0].strip()
            tgt = resolve(label, n["title"]) if label else None
            if tgt:
                add_edge(n["id"], tgt, "link")
        rel = field(body, "Related")
        for label in [x.strip() for x in rel.split(";") if x.strip()]:
            tgt = resolve(label, n["title"])
            if tgt:
                add_edge(n["id"], tgt, "related")
        if field(n["_t"], "Type").lower() == "hub":
            for line in n["_t"].split("\n"):
                if line.startswith("- ") and line.count(" | ") >= 4:
                    tgt = resolve(line[2:].split(" | ")[0].strip(), n["title"])
                    if tgt:
                        add_edge(n["id"], tgt, "hub")

    incoming = {i: 0 for i in nodes}
    for e in edges:
        incoming[e["target"]] += 1
    for i, nd in nodes.items():
        nd["incoming"] = incoming[i]
        exempt = norm(nd["title"]).split(" ")[0] in ORPHAN_EXEMPT_TITLES or nd["type"] in ORPHAN_EXEMPT_TYPES
        if incoming[i] == 0 and not exempt:
            lint["orphans"].append(nd["title"])

    return {"generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "count": len(nodes),
            "nodes": list(nodes.values()), "edges": edges, "lint": lint}


def modified(path):
    """Last git commit date (UTC) of the file; falls back to mtime outside git."""
    try:
        iso = subprocess.run(["git", "-C", str(path.parent), "log", "-1", "--format=%cI", "--", path.name],
                             check=True, capture_output=True, text=True).stdout.strip()
        dt = datetime.datetime.fromisoformat(iso)
    except (OSError, subprocess.CalledProcessError, ValueError):
        dt = datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_notes(wiki):
    files = sorted(p for p in Path(wiki).glob("*.txt") if p.is_file() and p.name not in SKIP_NAMES)
    return [{"id": p.stem, "title": p.stem, "modified": modified(p),
             "text": clean(p.read_bytes())} for p in files]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("wiki", help="directory with the .txt notes")
    ap.add_argument("-o", "--out", help="output file (default: stdout)")
    a = ap.parse_args()
    notes = load_notes(a.wiki)
    out = json.dumps(build(notes), ensure_ascii=False, separators=(",", ":"))
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
        print("ok", len(notes), "notes ->", a.out, file=sys.stderr)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(out)


if __name__ == "__main__":
    main()
