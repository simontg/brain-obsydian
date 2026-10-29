# VPS ideas (parked, not planned)

Source: transcript and screenshots of a YouTube video about a personal "agentic OS" dashboard, pasted by the owner on 2026-10-29. Ideas below are from that material, not verified against the owner's setup. None is scheduled; revisit when a VPS exists.

## Needs a VPS (something must run while the laptop is off)
- **Routines board**: a `routines.yaml` (name, purpose, schedule, machine) checked every 5 min by a scheduler; each run leaves a record the page reads (time, routine, machine tag, status FIRED). A per-routine cost cap so a failing routine cannot burn the budget overnight.
- **Skills deck** ("tap to run" in the video): buttons that start a skill on the right machine. A static page on GitHub Pages can only LIST skills; running needs a server endpoint. Open: whether `skille/` from the notes repo can be exposed as graph nodes (not checked).
- **Morning digest**: a routine that writes overnight changes, what is due, who waits, into a calendar or a file.
- **Needs-human list**: the only list that waits for the owner; the assistant never marks a task done, only the owner does.
- **Two-way sync** of one workspace folder between laptop and VPS every 5 min.
- **Phone entry**: voice or text message to a chat bot on the server, transcribed and answered in the same chat.
- **Private access**: a private network (Tailscale in the video) instead of a public address; then the page would not need the password and encryption used now.
- **Restricted agent on the server**: one settings file that blocks tools that send, share or delete (drafts only).

## Page ideas (no VPS needed once data exists)
- Status strip: last data build, last sync, runner state.
- "Today / next 14 days" panels read from files written by routines.
- Routine runs on the time view.
- Show, don't store: every panel reads a file something else wrote; the page keeps no facts.

## Measuring the map
The video measured the same question with and without a map (62 s vs 30 s, 28k vs 17k tokens, single run). Could be repeated with `INDEX-AUTO.txt` as the map.
