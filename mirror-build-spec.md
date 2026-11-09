# Club Gabbay mirror — build spec (overnight queue, section F)

Written 2026-11-06 ~22:45 PST by the overnight watchdog, from the confirmed
archive research in `club-gabby-hunt-2026-11-06.md`. The archive hunt and
download are DONE; this spec is the build order for the mirror itself.
Host choice is Paul's decision — do not pick one without his word.
Mirror lives on an external host, NEVER on Paul's PC.

## Archive state (verified)
- Source: Wayback Machine, domain `clubgabbay.com` (NOT geocities.com — it
  had its own domain; that is why every `geocities.com/*gabbay*` CDX search
  was empty). CDX matchType=domain, 1996–1999: **296 unique URLs**.
- Inventory on PC: `C:\ghost\clubgabbay_urls_1996-1999.txt` +
  `C:\ghost\clubgabbay_captures_1996-1999.json`.
- Mirror download DONE 2026-11-06 ~22:06 PST (PC, `C:\ghost\gabbay-mirror\`):
  310 items, **309 OK + 1 FAIL** (`destiny/part10.html`, Wayback 404 at the
  time). 290 files on disk — flat save, so duplicate basenames from different
  paths overwrote each other (e.g. `cake_birthday_sm.jpg`).
- **GAP CLOSED by this run (2026-11-06 ~22:40 PST, VM-side):** CDX shows
  three status-200 captures of `destiny/part10.html` (1999-11-27, 2000-02-26,
  2000-06-16). Fetched from the VM:
  `~/workspace/geocities-revival/part10-20001006.html` (21,027 B, real
  content — "Journey to Destiny" studio diary by Michael Gabbay, ends
  `</body></html>`, signed "gab"). Wayback redirected the 1999 timestamp to
  the 2000-10-06 capture. Mirror is now **310/310 recoverable**.

## Site map (from the archived pages — confirmed, not guessed)
- **Homepage** (`clubgabbay.com/`, earliest capture 1996-10-31): splash page,
  single centered narrow column of black serif text on a tiled pastel
  tropical-beach background (HOLLYWOOD sign, palms, purple mountains,
  thatched huts, white limousine, blue sea). Top banner: sharper full-colour
  version, orange-yellow sky, red circular "Club Gabbay" sign, "Welcome to
  Club Gabbay" in white script over blue water. Opening line: "As you gently
  wind your way down and around the final bend..." Three choices separated
  by "OR": "New Download Utility", "MFEN129's Club Gabbay FAQ and Tour
  Guide", "Enter ClubGabbay" (largest, boldest). Footer: comments@clubgabbay.com.
  246 homepage captures, 31 Oct 1996 – 3 Dec 2022.
- **Chat directory** (`chat.htm`, 1997): Lobby + "ANYTHING GOES! Uncensored
  chat for 18 and over" + members-only preview (`chat2.htm`) + Calendar of
  Events + Message Board links.
- **Members rooms** (`chat2.htm`, 1997) — 10 themed rooms + Lobby = 11 entry
  points: Blue Notes (blues), Speak Easy (jazz), Denim & Dialog (country),
  Hard Rock Gabbay (rock), Soul Searching (soul/R&B), Jive Talkin' (dance),
  Classical Comment (classical), Paradise Patio (reggae), Anything Goes
  (18+), Jackies JokeLand (comedy), plus the Lobby.
- **Room pages** (ColdFusion .cfm + HTML versions): anything_goes, blue,
  classical, denim, hard, jive, jokeland, lobby, paradise, soul, speakeasy.
- **Other sections:** `deargabby.htm`, `events.html`, `directory.html`,
  message board (`cgi-bin/clubgabbay/board/index.cgi`), guestbook, "destiny"
  story section (part1–part10+), `help.htm` (= CLUB RECRUITMENT page, not
  chat help), Gabbay Guide (MFEN129, hosted at nethaus.net — NO Wayback
  captures, not recoverable under that URL).
- **Images:** room backgrounds (`images/bg/*_bg.jpg`), room art (`blue.jpg`,
  `classical.jpg`, `denim.jpg`, `lobby.jpg`, `paradise.jpg`,
  `soul_searching.jpg`, `speakeasy.jpg`, `jive_talkin.jpg`, `rock.jpg`,
  `webdates.jpg`), day-of-week images, buttons/gifs. The full look is
  recoverable from the archive.

## Chat entry flow (confirmed from the real 1997 pages)
- **Lobby** (`chat.clubgabbay.com/htmls/lobby.html`, 1999): room description
  (classy foyer, oak walls, vaulted ceiling, fountain, complimentary
  cocktails + appetizers). Entry form: Name input (12 chars max), hidden
  `SAYS="<b>Joins The Lobby...</b>"`, hidden `HISTORY=8`, POST to
  `http://www.clubgabbay.com:2000/`. Typing a name + Enter posts your bold
  "Joins The Lobby..." line and shows the last 8 messages. HISTORY=8 is the
  "how many previous messages to see" control Paul remembered.
- **Lobby.cfm** (1997, built by Mohave Mirage Company, Long Beach CA):
  TWO entrances — Members ("Members Enter Lobby Here" → lobby2.cfm) and
  Guest (auto-name like "Guest1251", POST to `http://chat.clubgabbay.com:2000/`).
- **Anything Goes** (1997): black bg, white text, 18+ warning (unpatrolled).
  Entry POSTs to `http://204.7.247.51:2010/` — a DIFFERENT server/port than
  the Lobby (2000). Button: "I CERTIFY THAT I AM 18 AND I'LL TAKE MY
  CHANCES" + "ON SECOND THOUGHT BETTER NOT..." back to chat.htm.
- **Per-room ports:** each room ran on its own chat-server port (Lobby 2000,
  Anything Goes 2010, others presumably 2001–2009). The mirror backend must
  keep rooms separate the same way (separate room state, same entry shape).
- **NOT archived / still unknown:** the live in-chat interface (dropdowns,
  typing box, private whispers). Those lived on the chat server's POST
  response (ports 2000/2010), which Wayback never captured as static pages.
  Lead: AndyChat source (implemented Club Gabbay web-room support, v3.00
  Alpha Build 1302, Perl) — NOT retrievable by curl right now (SourceForge
  returns a 2-byte "no"; Build 1302 tar.gz path 404s). Retry via browser or
  a SourceForge mirror later; not a blocker — the entry flow + HISTORY=8
  are already documented. The mirror backend is new code anyway.

## Build steps (in order)
1. **Pull the archive to the VM** (first run with a live PC link): scp
   `C:\ghost\gabbay-mirror\` (290 files) + `download.log` +
   `C:\ghost\clubgabbay_captures_1996-1999.json` + the recovered
   `part10-20001006.html` (already on the VM). Verify counts on arrival.
2. **Inventory + repair the flat-save collisions.** The 290 files lost
   their paths (309 OK → 290 files). Rebuild the URL→file mapping from
   `download.log` + the captures JSON; where two URLs share a basename,
   restore them under their real paths (e.g. `images/bg/...` vs root).
   Anything still colliding gets re-fetched from Wayback by full URL.
3. **Reconstruct the link structure.** Rewrite absolute
   `http://www.clubgabbay.com...` / `chat.clubgabbay.com...` links to
   relative paths inside the mirror. Keep the exact look (layout, colours,
   fonts, images) — a mirror, not a remake (Paul's rule).
   **DONE 2026-11-07 ~00:50 PST (overnight watchdog):** 90 files changed,
   196 links rewritten (225 absolute clubgabbay.com occurrences → 29).
   24 chat form actions → backend room routes (`/lobby`, `/blue`, …,
   `/anything-goes`, `/jokeland`, per chat-backend-design.md); 54
   cross-host resolutions (bare-host archived copy where the link names
   www — the 1996 host move). 29 remaining absolute occurrences are all
   genuinely unarchived targets (webdates_bg.jpg 5×, queue CGI 5×,
   otherhalf.gif 3×, main.cfm 2×, anything_goes_sm.jpg 2×, destiny/ 2×,
   club_store 2×, vip_form.htm 2×, member_pages.cfm,
   jakies_jokeland_sm.gif, gabby.jpg, calendar/events, webdates.htm,
   members/). Verified against `site-backup-pre-step3.tar.gz`: 0
   regressions (112 pre-existing broken relative links unchanged; the 23
   "new broken" links are the intentional room routes, served by the
   backend in step 4). Script + report: `rewrite_step3.py`,
   `rewrite_step3_report.json`. External hosts (linkexchange, bookshop,
   nethaus, …) deliberately untouched.
4. **Build the chat backend (new code, ours).** One room = one state:
   message history (HISTORY=N on entry, default 8), join announcements
   (`<b>Joins The Lobby...</b>`), guest auto-names (GuestNNNN), member
   entry path. Entry form posts Name + SAYS + HISTORY exactly as the
   originals did. Rooms: the 10 themed + Lobby. Anything Goes keeps its
   18+ gate. Keep it simple and portable (stdlib-only server preferred —
   the host is undecided and the backend must move easily).
5. **Local test.** Walk every room: homepage → Enter → Lobby entry (guest
   + member paths) → post a message → HISTORY=8 shows last 8 → jump to
   another room (multi-room jumping is a named feature — rooms link to
   each other like the original). Check images load, no broken links.
6. **Host decision (PAUL).** Free tier to start? Domain name? Do not pick
   without his word. Deploy only after he picks.
7. **Moderation (open decision, Paul's call).** Public rooms need spam/abuse
   handling — approach undecided (see plan.md). Host does NOT moderate;
   operating = our responsibility.

## Standing rules that bind this build
- Paul's username in any old log is **cjcoplin** — if it shows up as a chat
  user in anyone's old logs, that's Paul. (Deep dive 2026-11-06 found no
  trace of it in the board/guestbook/directory; in-chat lines were never
  captured. Keep watching in future archive dives.)
- Do NOT use geocities.ws as a source (flagged scam, 1/100 trust).
- The pages are the original creators' work — archive/preserve, never claim
  authorship; take down on a creator's request. The new chat code is ours;
  the room look/name honors the original.
- Paul was there as a kid (Lobby + Anything Goes, age 16–17). This one is
  personal — get the look right.
