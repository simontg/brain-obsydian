# CLAUDE.md — brain-obsydian

## START HERE
The migration (stages 0-5) is FINISHED (2026-10-22). Read `docs/ORCHESTRATOR-HANDOFF.md` first: current setup, secrets, open items, how to work. `PLAN.md` keeps the stage history and evidence. `PLAN-WORKSPACE.md` (shared GitHub workspace for projects, sources and skills in the notes repo) is FINISHED (2026-10-28); its non-blocking open items are listed at the top of that file.
Parked ideas for the future VPS: `docs/VPS-IDEAS.md`.
Read `docs/GITHUB-ACCESS.md` for how repository access works from a Claude session (tools, steps, pitfalls; verified 2026-10-22 from the owner's mobile chat).

## Working model
- One stage = one new session (window) in this project. Each session does only its stage, then reports in Polish (done / verified / unknown) and STOPS.
- The orchestrator session only reviews each stage report, checks the result and waits for the owner's approval before the next stage. It does not do stage work itself.
- Roles (owner rule 2026-10-23, applies to every staged project): the orchestrator is the single control point. Only the orchestrator proposes the next stage, starts stage windows, verifies reports and merges PRs. A stage window NEVER merges a PR, never asks the owner to merge, never proposes, plans or starts a later stage, and never edits other stages' sections. It may open a (draft) PR for its own stage and must end with the report block below, which the owner pastes to the orchestrator (or the window sends it with `send_message` when it knows the orchestrator session ID).
- Window hand-off to the owner (owner rule 2026-10-23): for every new window the orchestrator gives, in one block: who starts it, window name, model, effort, the skills it must load, and either the exact copy-paste prompt (owner starts the window) or the explicit line "nic nie wklejać, okno już działa" with its link (orchestrator started it via `create_session`, which cannot set effort). It also lists every consent sentence the owner may have to type in that window, and in which window.
- Every stage session MUST load a skill before writing code: `lazy-senior` (minimal, optimized code, no over-engineering) for any script/page change; `to-spec` first when the task is a new script. If a skill is missing in the session, say so in the report instead of skipping silently.
- Use skills where they fit (grill-me for owner decisions, to-spec for script specs, wiki-brain/handoff for the wiki) and save tokens: scripts over manual copying, never load whole large files, cheaper model for mechanical conversion. The orchestrator names in every window prompt the skills that window must load (e.g. `grill-me` before open owner decisions, `to-spec` before a new script, `lazy-senior` before any code) and the model and effort; it uses `grill-me` itself when a decision is still open before a stage starts.
- Stage report format (Polish, mandatory). First line: `STATUS: ZAMKNIĘTY` | `ZAMKNIĘTY Z UWAGAMI` | `OTWARTY`. Then: Zrobione / Zweryfikowane (with how: commit hash, counts, command) / Nie wiem / Pozycje otwarte (ID, opis, kto decyduje, czy blokuje następny etap) / Do orkiestratora (PR number and head SHA, what to re-verify, decisions needed from the owner; no next-stage proposal). The whole report is one copy-paste block and is the last thing the window writes.
- A stage is `ZAMKNIĘTY` only when every "Zaliczone gdy" criterion in PLAN.md is verified. Any unmet or unverified criterion makes it `OTWARTY` or `ZAMKNIĘTY Z UWAGAMI` with each item listed under "Pozycje otwarte" in the PLAN.md results section. Do not claim a check you did not run; the orchestrator re-verifies key claims independently.
- Every stage session writes its results into PLAN.md (section "Etap N: WYNIKI", with STATUS) via a PR, so later windows do not depend on chat history.
- Private notes live in the PRIVATE repo `simontg/Brain-Obsydian-NOTES` (67 notes in `wiki/` since stage 2, 2026-10-22). Nothing personal ever goes into this public repo.

## What this is
Personal knowledge-base tooling. Owner: Stanley (writes Polish; code, comments and technical labels in English).
UI strings in the graph page are Polish.

## Hard rules
- This repo is PUBLIC. Never commit notes, wiki exports, `GRAPH-AUTO.json`, real note titles, tokens or any personal data.
  Test data must be synthetic. `.gitignore` already blocks `wiki/`, `data/`, `GRAPH-AUTO.json`.
- Never invent facts. If something is unknown or unverified, say so.
- Answers to the owner: Polish, concise, no boilerplate disclaimers.

## Architecture (as of 2026-10-22, after migration stage 5)
- Source of truth for notes: the PRIVATE repo `simontg/Brain-Obsydian-NOTES` (`wiki/*.txt`, UTF-8 with BOM, CRLF). Changed only through the account skill `wiki-brain-git` ("wiki save / ask / lint", "zapisz do wiki"); the old Drive skill `wiki-brain` is disabled.
- Google Drive (folder Wiki) is a read-only backup copy. Do not write notes there and never delete anything there.
- Graph and index: the Action `generate-graph-index` in the notes repo (template: `tools/notes-repo/generate-graph-index.yml`) runs `tools/wiki_graph.py` and `tools/wiki_index.py` on every push to `wiki/`, commits `graph/GRAPH-AUTO.json` and `graph/INDEX-AUTO.txt` there, and pushes the encrypted `graph/graph.enc.json` to this repo; `pilot-graph.yml` deploys it to GitHub Pages (https://simontg.github.io/brain-obsydian/, password decrypted in the browser). Update time about one minute.
- The notes repo is the only source of truth also for `projekty/`, `zrodla/` and `skille/` (skills `write-to-github`, `read-whole`, `handoff` write there); Google Drive is a read-only copy (exception: the active study stays on Drive until about 2027-02).
- The phone cron jobs (Termux: `run_wiki_index.sh` :07, `run_wiki_graph.sh` :12) are disabled since stage 5; the Drive copies of `GRAPH-AUTO.json` and `INDEX-AUTO.txt` are frozen.
- `graph/graf-wiki.html` serves both the Pages site and the old Claude artifact. The artifact (reads from Drive) is RETIRED: kept, not deleted, but its data no longer updates.

## Graph page notes
- Single file; d3 loaded from cdnjs. State lives in plain JS variables; theme in localStorage (wrapped in try/catch).
- Data load: on Pages, `graph.enc.json` decrypted with WebCrypto (password kept in sessionStorage); inside a Claude artifact (retired), the Google Drive connector `search_files` + `download_file_content` (base64 JSON) with a fixed file ID fallback.
- Encoding: colour = area (owning hub), shape = note type, size = incoming links, orange dot = has [unverified] claims.
  Edge style: hub solid, related dashed, link dotted; cross-area edges use a gradient.
- Views are position functions over the same nodes: rings (`rx,ry`), net (force sim, meta nodes pinned, HOT at centre),
  time (`tx,ty`, day-based axis), sphere (3D projection of sphere coords, per-frame in `draw()`; the orbit view was removed 2026-10-22).
- Testing approach used so far: Playwright with a stubbed `window.claude.use("mcp")` returning synthetic graph JSON;
  check no page errors at 1280x780 and 392x820, dark and light.

## Open questions
- None from the migration. Remaining items (lint clean-up, SHA pinning of the tools) are listed in `PLAN.md`.
