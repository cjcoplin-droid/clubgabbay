# Club Gabbay Chat — Backend Design (mirror)

Written 2026-11-06 night. The archive download is DONE (310 files, 290 on disk). This doc is the technical design for the NEW chat backend that sits behind the archived front-end look. The original chat was ColdFusion server-side (ports 2000/2010) — that code is gone; the mirror keeps the look and rebuilds the behaviour.

## What the original did (from the archived pages)

Entry flow, confirmed from the 1996–1999 snapshots:
- Pick a room (Lobby, or one of the 10 themed rooms).
- Type your name (input, max 12 chars) OR enter as Guest (auto-name like `Guest1251`).
- Click Enter → POST to the room's chat server with hidden fields:
  - `USER` = your name
  - `SAYS` = `<b>Joins The Lobby...</b>` (join announcement, HTML bold)
  - `HISTORY` = 8 (how many previous messages to show — the "choose how many messages to see" control Paul remembered)
- Each room ran on its OWN chat-server port: Lobby = `chat.clubgabbay.com:2000`, Anything Goes = `204.7.247.51:2010`. Members had a separate entrance (form → `lobby2.cfm`); guests POST directly to the port.
- The live in-chat interface (dropdowns, typing, whispers) lived on the chat server's POST response — never captured as static pages. AndyChat v3.00 Build 1302 implemented the Club Gabbay web room, but its source is not retrievable right now (SourceForge blocks automated download). The in-chat protocol detail is therefore reconstructed from the entry flow + standard 90s chat behaviour, not from a spec.

The 10 themed rooms + Lobby (from the archive):
| Room | File | Theme |
|---|---|---|
| The Lobby | lobby (port 2000) | foyer, oak walls, fountain |
| Blue Notes | blue.cfm | blues |
| Speak Easy | speakeasy.cfm | jazz |
| Denim & Dialog | denim.cfm | country |
| Hard Rock Gabbay | hard.cfm | rock |
| Soul Searching | soul.cfm | soul |
| Jive Talkin' | jive.cfm | dance |
| Classical Comment | classical.cfm | classical |
| Paradise Patio | paradise.cfm | reggae |
| Anything Goes | anything_goes.cfm (port 2010) | 18+, unpatrolled |
| Jackies JokeLand | jokeland.cfm | comedy |

Plus: message board (`cgi-bin/clubgabbay/board/index.cgi`), guestbook, Dear Gabby (`deargabby.htm`), Calendar of Events, member directory (`directory_search.cfm`), `destiny/` story section.

## What the mirror backend must do

Functional requirements (the behaviour, not the look — the look comes from the archived pages):
1. **Rooms.** 11 rooms (Lobby + 10 themed). Each room is a separate chat space. Users jump between rooms (multi-room jumping — Paul's requirement).
2. **Entry.** Name (max 12 chars) or Guest (auto-name `GuestNNNN`). Join announcement posted to the room (`<b>Joins The Lobby...</b>` style, rendered as bold).
3. **Messages.** Post a message, see the last N messages (HISTORY count, default 8, user-choosable). Messages show in order, newest last (90s chat style).
4. **Presence.** Show who's in the room (the user list / dropdown Paul remembered). Join/leave announcements.
5. **Whispers (private).** A user can message one other user privately (the dropdown "whisper" action). Private messages go only to that user.
6. **Actions.** The original had action controls (the dropdowns). Minimum: whisper, and a way to see a user's info. Keep the set small and faithful.
7. **Persistence.** Messages persist per room (at least the last N). A room's history survives a reload.
8. **Multi-room.** One user can be in one room at a time but jump freely; the room list is always visible.

## Architecture (fits free-tier hosting)

Keep it simple — a small server, no heavy framework. The mirror is a proof of concept on a free tier.

- **Transport:** WebSocket for live chat (messages + presence push), with a plain HTTP fallback for the entry form (so the archived-style POST entry still works and degrades gracefully). If the host's free tier doesn't support WebSocket, fall back to short polling (the 90s original effectively polled via refresh — polling is authentic).
- **Server:** a single small process (Node or Python — pick when the host is chosen; the host's free tier decides the runtime). One process serves all 11 rooms; rooms are in-memory channels with a small persistent store.
- **Storage:** messages per room, capped (e.g. last 200 per room). A tiny SQLite file is enough for the proof of concept. No user accounts for guests; members (if revived) get a simple name+password later — not in v1.
- **Front-end:** the archived HTML/CSS/images, with the chat form wired to the new backend. Keep the 1996 look pixel-for-pixel where the archive has it. The chat pane is the one part that is new code (it has to be — the original was server-rendered).
- **Room routing:** the mirror does NOT need separate ports per room (that was a 90s ColdFusion constraint). One server, rooms as paths (`/lobby`, `/blue`, `/anything-goes`, ...). The archived room URLs map to these paths.

## Message format (mirror's own — new, not the ColdFusion protocol)

- A chat message: `{ room, user, text, ts }`. Rendered as `user: text`, with join/leave as bold system lines (`<b>Joins The Lobby...</b>`).
- A whisper: `{ room, from, to, text, ts, private: true }` — delivered only to `to` (and shown to `from` as sent).
- Presence: server broadcasts the room's user list on join/leave.
- HISTORY: on entry, the server sends the last N messages (N from the entry form, default 8).

## Moderation (Paul: "same rules as back then, kept clean, not a place for weirdos")

- Anything Goes is 18+ and was unpatrolled originally — the mirror keeps the 18+ gate (the certify button) but the room is still moderated (no unpatrolled room on our watch).
- Mod tools (v1, minimal): a mod can mute/kick a user from a room; a user can report a message. Reports go to a mod queue Mira reviews.
- Rate limit: one message per ~2s per user (spam control, invisible to normal chatters).
- Name rules: 12-char max (as original); no impersonation of staff/mods.
- Full moderation policy + who handles reports is a Paul decision (see plan.md). This doc only provides the hooks.

## Open decisions (Paul's — do not decide for him)

1. Host (free tier to start?) — decides the runtime (Node vs Python) and whether WebSocket is available.
2. Domain name for the hub.
3. Scope after Club Gabbay.
4. Moderation strictness + who handles reports.

## Status

- 2026-11-06 night: archive download DONE (310 files). This design written. Nothing built yet — build starts once Paul picks host + domain.
- AndyChat source still unretrieved (SourceForge blocks curl). If it becomes available, cross-check the whisper/dropdown behaviour against it and update this doc.
