# Club Gabbay mirror — browser visual check report

**Date:** 2026-11-07 ~22:37–23:00 PST (watchdog 2337 run)
**Verdict: PASS** — the mirror looks and behaves like the 1996 site in a real browser.

## Method
- Site tree + backend staged to the PC via ghost exec base64 chunks
  (18 chunks, sha256 `3d51e1bb…0a545` verified on the PC, 310 files extracted
  to `C:\ghost\gabbay-visual\`).
- Backend started headless via wmic Session 0 (python PID 15652, port 8123,
  `--site C:\ghost\gabbay-visual\site`, throwaway DB
  `C:\ghost\gabbay-visual\chat.db`); stopped after the check, port down.
- Automation Chrome driven via CDP (Chrome 156, fb-lock held + released,
  tab closed after; only the original New Tab remains).
- Screenshots: `~/workspace/goals/mira-self-watchdog/hidden_files/gabbay-*.png`
  (home, home-bottom, main, lobby-entry, lobby-post, blue, blue-pane, anything).

## Views checked
1. **Homepage `/`** — PASS. Hollywood-sign background, "Welcome to Club Gabbay",
   the original intro text, "258 NEW MEMBERS in the past 7 days!! / ClubGabbay
   now has 9134 members!", the Netscape 3.0 notice, the approved landing blurb
   with the moderation note ("chat rooms are monitored — public messages pass
   through an automated word filter. Anything Goes is 18+. Whispers are private
   and unmonitored."), "Enter ClubGabbay" / "Enter WebDates" links, the 1997
   footer ("Keep out of reach from small children. 5 minutes a day, that's all
   we ask! Enjoy!").
2. **`/main.htm`** — PASS. Frameset (menu.cfm + welcome.htm); Michael Gabbay's
   message + photo render, links present (Robb's Webmaster Update, FAQ, Social
   Director, WEB DATES, club tee shirt, card shop).
3. **Lobby pane `/lobby`** — PASS. Room art (sofa/chandelier/ocean, "The Lobby"
   script), room description verbatim, "Jump to another room" with all 10 rooms,
   "Who's here: GuestCheck", history, Say It! / Whisper / history controls,
   "You are chatting as GuestCheck. Messages refresh automatically every few
   seconds." Interactive loop verified live: typed
   "Visual check - the Lobby looks just like 1996!" and it appeared as
   "GuestCheck: Visual check - the Lobby looks just like 1996!".
4. **Blue Notes `/blue`** — PASS. Entry form (Name + Enter) → pane with join
   line, presence, controls. Room tagline renders. Background is plain white —
   the archived `blue_bg.jpg` was never captured; the plain fallback works as
   designed.
5. **Anything Goes `/anything-goes`** — PASS. 18+ gate renders: black page,
   "ANYTHING GOES" logo, the original warning text, "I CERTIFY THAT I AM 18
   AND I'LL TAKE MY CHANCES" button, and the opt-out "ON SECOND THOUGHT
   BETTTER NOT...I MAY GET IN TROUBLE" (original typo preserved).

## Known gaps confirmed (not bugs)
- 5 room backgrounds never captured (blue/hard/jive/paradise/soulsearch) —
  panes fall back to plain backgrounds; Lobby's own `lobby_bg.jpg` tiles as a
  pale yellow/blue wash, which reads as period-correct.
- LinkExchange banner slot at the top of the homepage is an empty blue-bordered
  box (external host, deliberately untouched).
- `/api/<room>/messages` returns 403 without a session cookie — correct
  behavior, not a failure.
- The two identical "GuestCheck Joins The Lobby..." lines were two separate
  entries (one per POST: a PC-side probe + the browser entry), not a duplicate
  render bug.

## Notes
- No code changed. No deploy, no host/domain pick — those stay Paul's decisions.
- Staged files left on the PC at `C:\ghost\gabbay-visual\` for reuse; the
  visual-check DB there holds only the GuestCheck test rows — a fresh DB must
  be used for any real deploy.
- Transfer lesson: the VM cannot be reached from the tailnet (client-only
  join, accepts no connections), so the tailnet fetch route is dead; the
  ghost-exec base64-chunk route works (~10s for 1.3 MB in 18 chunks).
- Server-launch lesson: wmic returns the PID of the `cmd` wrapper, not the
  python child — kill the listener PID found via `netstat -ano` (here 15652),
  never a bare `taskkill /IM python.exe` (would endanger ComfyUI / the bot).
