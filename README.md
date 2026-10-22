# brain-obsydian

Code for a personal "second brain": a plain-text wiki kept in a private GitHub repo, plus an interactive graph page.

**This repository is public. It contains code only. No notes, no exported graph data.**

## Contents
- `graph/graf-wiki.html` — source of the graph page (single self-contained HTML, d3 v7, canvas).
  Published on GitHub Pages; it loads `graph/graph.enc.json` (AES-256-GCM, PBKDF2) and decrypts it in the browser
  with a password. The file is generated and pushed by a GitHub Action in the private notes repo.
  (An older Claude artifact build that read the graph from Google Drive is retired.)
- `tools/wiki_graph.py`, `tools/wiki_index.py` — graph and BM25 index generators (Python stdlib, SQLite FTS5), tests in `tools/tests/`.
- `tools/notes-repo/generate-graph-index.yml` — template of the Action deployed in the private notes repo.
- Views: Rings, Net, Time, Sphere (3D). The Orbit view (3D cone) was removed on 2026-10-22 at the owner's request.

## Data format (`GRAPH-AUTO.json`, generated in the private repo, committed here only encrypted)
`generated_at`, `count`, `nodes[id,title,type,tags,summary,modified,chars,verified,stated,unverified,incoming]`,
`edges[source,target,kind: hub|related|link]`, `lint{dead_links,ambiguous_titles,orphans,missing_type,empty}`.

See `CLAUDE.md` for working rules.
