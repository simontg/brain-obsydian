# brain-obsydian

Code for a personal "second brain": a Markdown/Google-Docs wiki plus an interactive graph page.

**This repository is public. It contains code only. No notes, no exported graph data.**

## Contents
- `graph/graf-wiki.html` — source of the graph page (single self-contained HTML, d3 v7, canvas).
  It is published as a Claude artifact and reads `GRAPH-AUTO.json` through the viewer's Google Drive connector
  (`window.claude.use("mcp")`). It does **not** run as a plain static site (e.g. GitHub Pages): without the
  Claude runtime there is no data source.
- Views: Rings, Net, Time, Orbit (3D cone), Sphere (3D).

## Data format (`GRAPH-AUTO.json`, generated elsewhere, never committed)
`generated_at`, `count`, `nodes[id,title,type,tags,summary,modified,chars,verified,stated,unverified,incoming]`,
`edges[source,target,kind: hub|related|link]`, `lint{dead_links,ambiguous_titles,orphans,missing_type,empty}`.

See `CLAUDE.md` for working rules.
