# Club Gabbay mirror — chat backend

Stdlib-only Python server (no third-party deps). Serves the archived
`site/` tree as-is and implements the 11 chat rooms behind the original
1996 entry flow. Spec step 4 of `../mirror-build-spec.md`; design in
`../chat-backend-design.md`; test report in `../backend-test-report.md`.

## Run (local test)

```sh
python3 server.py            # http://127.0.0.1:8124/ (port from $PORT)
python3 server.py --port 8124 --db chat.db --site ../site
```

Binds 127.0.0.1 by default. On Render: `python backend/server.py
--host 0.0.0.0` (port from `$PORT`, default 8124) — see
`../render.yaml`. Host is decided (Render free tier, 2026-11-07);
deploy is the parent lane's step, not this backend's.

## How it works

- **Static site:** every non-room URL is resolved against the archived
  `site/` tree (5 host dirs). A leading host-dir segment is honoured
  (`/clubgabbay.com/images/...`); otherwise `www2` is tried first, then
  `www`, `clubgabbay.com`, `chat`, `members`. `.cfm`/`.cgi` files are
  served as HTML. Missing files get a 1996-styled 404.
- **Rooms:** `/lobby`, `/blue`, `/speakeasy`, `/denim`, `/hard`, `/soul`,
  `/jive`, `/classical`, `/paradise`, `/anything-goes`, `/jokeland`
  (`/anything_goes` also accepted). Entry is the original POST:
  `USER` (max 12 chars), `SAYS` (join announcement), `HISTORY`
  (default 8, 1–50). Blank name (or the archived guest form's literal
  `Guest1251`) gets a fresh auto-name `GuestNNNN`.
- **Chat pane:** room background/art/description from the archived room
  pages (backgrounds never captured by Wayback fall back to plain —
  see the test report). Messages poll via
  `GET /api/<room>/messages?since=<id>` every 4s; posting works with
  plain forms too (no-JS fallback). Presence = sessions seen in the
  last 120s. Room-jump links (`/<room>?jump=1`) carry your name into
  the next room with a fresh join line. `Leave` posts a leave line.
- **Whispers:** `POST /<room>/whisper` with `to` + `text`; stored as
  private messages, delivered only to sender and recipient.
- **Persistence:** SQLite (`chat.db` by default), `messages` table,
  capped at the last 200 per room; survives restarts.
- **Rate limit:** ~1 message per 2s per user (429 if faster).
- **Anything Goes 18+ gate:** `GET /anything-goes` without a session
  redirects to the archived gate page (`anything_goes.cfm`); the
  certify POST is the entry.
- **Member entry:** `/lobby2.cfm` (the archived member-entrance target,
  never captured — served as new code in the lobby's look) and
  `/login.cfm` (the popup the themed-room `.cfm` pages open). v1:
  any password accepted, session flagged `(member)` in presence.
  Real member accounts are a later decision.
- **Moderation hook:** `POST /api/<room>/report` (`msg_id`, `reason`)
  stores reports in the SQLite `reports` table for review. Automated
  word filter on public messages only (`blocklist.txt`, private, never
  served): a banned word is rejected before it posts, 3 strikes bans
  that name from public posting. **Whispers are never monitored or
  filtered** (Paul, 2026-11-07) — private between the two people, in
  any room. The filter also blocks raw URLs in public messages.
- **Homepage:** the landing page carries the approved blurb above the
  Enter link, plus the monitoring / 18+ / private-whisper notes.

## Test

```sh
python3 test_backend.py     # boots a scratch server on 127.0.0.1:8124,
                            # walks all 11 rooms, writes ../backend-test-report.md
```

## Files

- `server.py` — the backend (stdlib only).
- `test_backend.py` — the step-5 local test.
- `chat.db` — live message store (created on first run; test runs use
  `test-chat.db`, removed on each fresh run).
