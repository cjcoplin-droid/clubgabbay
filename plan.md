# Geocities Revival Plan (Data Necromancer)

Paul, 2026-11-06: "Let's really plan this out to get geosites all the dead ones back into a page where the free sites can host them. And we manage and operate them so they're ours."

## The idea
A live revival hub: dead Geocities sites brought back as working pages, with the chat sites actually chat-able again. We operate the hub; people find the sites through Google and use them like back in the day.
- **A mirror, not a remake (Paul, 2026-11-06):** the exact look the Geocities sites used to have — same layout, colours, fonts, images — rebuilt from the archived pages. As exact as the archive allows.
- **Club Gabby first, exact:** the page as in Paul's screenshot — "Polar Bear's Club Gabby Chat", enter your name + how many previous messages to see, start typing, all the actions that site provided.
- **Multi-room jumping (Paul, 2026-11-06):** a Geocities chat feature — people come in, start chatting, then jump into other rooms with more people. The hub links the rooms together so jumping between them works like it used to.
- Then the other popular ones, same treatment, one at a time.

## Proof of concept first: Club Gabby
- Polar Bear's Club Gabby Chat (Geocities). Static pages + a live chat rebuild.
- Already queued for overnight work (overnight-build-queue.md section F).
- Proves the pipeline (archive → rebuild → host → live) before any bigger spend of effort.

## Scope — honest limit
- Geocities had millions of sites (~38 million pages). "All" is not feasible.
- Realistic: a curated set. Club Gabby first, then the next batch by what Paul picks — popular neighborhoods, the chat sites, famous/interesting pages.
- Expansion is a decision each round, not an open-ended "all."

## Sources for the originals
- Wayback Machine (web.archive.org) — snapshots of individual sites.
- Archive Team Geocities torrent (~900 GB) — the full crawl from 2009.
- restorativland.org / oocities.org — existing Geocities restoration archives.
- Needs Paul's remembered URLs/neighborhoods when the archive hunt stalls (Club Gabby first).

## Hosting — where it lives
- **Never on Paul's PC.** External host only — a server that's always on.
- Free tier works for the proof of concept (Club Gabby + a handful of pages).
- Free-host limits are real: storage caps, bandwidth caps, some sleep when idle.
- A large archive will not fit free hosting. Real hosting costs money — that's Paul's call, his money, free-only rule stands unless he says otherwise.
- Host choice is Paul's decision. Do not pick one without his word.

## The hub
- One page/site listing the revived sites, grouped by neighborhood/category, each linking to its revived home.
- Google-indexable so searches for old site names / "Geocities chat" can land people there.
- Discovery channels: Google indexing, nostalgia communities (r/geocities etc.), Wayback links, word of mouth.

## How it operates
- Mira manages remotely: deploys, uptime checks, updates, keeps it running.
- Paul doesn't touch it day to day.
- Public chat rooms need moderation (spam/abuse) — approach is an open decision (see below).
- **Host vs operator (Paul, 2026-11-06):** a third-party host provides the server and their terms govern it — they can pull the plug if the content breaks their rules. But the host does NOT moderate the rooms. Operating = our responsibility: the rules, the moderation, and handling problems when they come up. Using a host spreads the infrastructure burden; it does not transfer the duty to keep the rooms clean. Paul's line: same rules as back then, kept clean, not a place for weirdos.

## Content / ownership — the honest part
- The pages are the original creators' work. We are preserving and hosting them as an archive, and we operate the hub — that operation is ours.
- We do not claim authorship of other people's pages.
- Standard archive practice: if an original creator asks for their site to come down, we take it down.
- Chat rooms we rebuild: the new chat code is ours; the room's look and name honor the original.

## Decisions needed from Paul (one word each is fine)
1. Scope after Club Gabby — which neighborhoods/sites next, or just Club Gabby for now?
2. Host — DECIDED 2026-11-07: Render free tier (Mira's recommendation; Fly.io free tier dead since Oct 2024).
3. Domain name for the hub. — free Render subdomain to start; real domain later only if the POC earns it.
4. Chat moderation — DECIDED 2026-11-07: no live human moderator. Automated word filter: banned word = message blocked before posting, repeats = auto-ban. Filter applies to public room messages only — whispers are never monitored or filtered, private between the two people (Paul's correction 2026-11-07). Landing page notes rooms are monitored, Anything Goes is 18+, whispers are private and unmonitored. Mira checks the report queue if anyone reports something.

## Status
- 2026-11-06 ~17:14: plan written. Club Gabby archive hunt queued overnight (section F). Nothing built yet.
- 2026-11-06 night: archive download DONE (310 items, 290 files, 1 FAIL — destiny/part10.html 404; part10 later recovered from a 2000-10-06 Wayback capture to `part10-20001006.html`, archive now effectively 310/310). Chat backend design written (`chat-backend-design.md`); mirror build spec written (`mirror-build-spec.md`). Nothing built yet — build starts once Paul picks host + domain.
- 2026-11-07: landing page blurb — Paul asked for a short blurb saying what the site is for. DRAFT APPROVED 2026-11-07 by Paul: "Club Gabbay Chat is back. The 1996 Geocities chat rooms — the Lobby, Anything Goes, and all ten themed rooms — rebuilt to look and feel like they did. Pick a name and jump in. Preserved in honor of the original Club Gabbay and everyone who called it home." Goes on the homepage above Enter, alongside the monitoring / 18+ / whisper notes.
- **2026-11-09 ~08:24 MST: DEPLOYED LIVE.** Paul gave the go that morning; repo created + pushed (https://github.com/cjcoplin-droid/clubgabbay, main, commit 5f56c58); Render web service `clubgabbay` on the FREE plan ($0/mo, 0.1 CPU, 512 MB), public-repo deploy, stdlib-only, build `echo "stdlib only — nothing to install"`, start `python backend/server.py --host 0.0.0.0`. First deploy succeeded in 30.9s. **Live at https://clubgabbay.onrender.com** — verified: homepage 200 + blurb, lobby entry 200, /lobby no-session 303 → entry page, chat dir 200. Render account = cjcoplin@gmail.com via Google OAuth (no Render password). GitHub account is **cjcoplin-droid** (vault password dead — account is Google-sign-in only, no password sign-in). Free tier sleeps after 15 min idle; first visit can take ~50s to wake. Chat history is SQLite on ephemeral disk — resets on restart (known, accepted for the POC).
- **2026-11-09 ~09:00 MST: landing-page fix (Paul's call, commit 58dbd8d).** He found "Enter ClubGabbay" led to the /main.htm frameset (Michael's message) — a dead end, not the chat. Fixed: Enter ClubGabbay now links straight to /chat.htm; /main.htm, /welcome.htm, /menu.cfm and /webdates.cfm deleted (404); WebDates block and comments@clubgabbay.com email line removed from the landing page. Landing page is now just the blurb + a link to the chat. Tests 176 checks, 0 FAIL. Redeployed via Render Manual Deploy (public repos don't auto-deploy). Verified live end-to-end: homepage 200 (Enter → /chat.htm, no webdates/email), removed pages 404, /chat.htm 200, lobby entry 200, POST /lobby → room 200 with the name present. Note: two POST attempts during the deploy's container swap hung (000) — not a bug, the instance was restarting; once warm the flow works in under a second.
- **2026-11-09 ~09:25 MST: typing fix (Paul's call, commit 7bdcc43).** Paul got into Anything Goes as cjcoplin but couldn't type — the page seemed to reload whenever he typed. Cause: the room page's 4s poll called window.scrollTo on EVERY cycle, even with no new messages; on phones that yanks the viewport and drops the keyboard. Fixed: scroll only when messages were actually added AND the reader is already near the bottom. Tests 176 checks, 0 FAIL. Redeployed via Render Manual Deploy. Verified live in a real browser: typed in the Lobby box, waited through 3 poll cycles — text stayed, input stayed focused, no scroll jump, no reload.
- **2026-11-09 ~09:35 MST: LinkExchange banner removed (Paul's call, commit a72dd8e).** The dead ad banner at the top of the landing page rendered as a broken-image box — the ad server is long gone. Removed the whole block (ad image + LinkExchange Member link). Tests 176 checks, 0 FAIL. Redeployed via Render Manual Deploy. Verified live: homepage 200, 0 linkexchange mentions, Enter ClubGabbay → /chat.htm intact.
- **2026-11-09 ~09:40 MST: LinkExchange banners removed SITE-WIDE (Paul's call, commit f3b1f5f).** The board page still had its banner, and four more pages (both otherhalf pages, samples, lobby.html) plus the guestbook locator had dead banner units. All removed; zero linkexchange mentions left anywhere. Tests 177 checks, 0 FAIL. Verified live after deploy.
- **2026-11-09 ~09:45 MST: Web Dates + Mall links removed from navs (Paul's call, commit 530aa01).** Calendar footer (both variants), lobby nav, guestbook nav — footer is now just [ Home ] [ Message Board ]. webdates.html stub (both variants) deleted, same as webdates.cfm before it. The mall pages themselves stay — only the links go, per Paul. Tests 179 checks, 0 FAIL. Verified live: calendar 200 with no Web Dates/Mall mentions, webdates.html 404.
- **Open question from Paul (2026-11-09 ~09:35 MST): can people add to the message board?** Not currently — the board is a frozen 1997 archive. Build offered: post form + same automated word filter as chat, new posts on top, 1997 posts kept below. Awaiting his word.
- **Still standing in the archive:** the deeper WebDates subsystem files (webdate_search.cfm, webdate_profile.cfm, webdate_browse_search.cfm, webdates_intro.htm, new_members_form.cfm refs) — non-functional static pages, links to them removed where flagged. Delete the whole section only on Paul's word.
- **2026-11-09 ~09:55 MST: Message board is postable (Paul's call, commit a34ee5e).** Anyone can add a message (To / From / Subject / Message). New posts render above the frozen 1997 archive, newest first, in the archive's own format (no Host/IP on new posts). Stored in SQLite board_posts with NO cap — they stay up, verified across a server restart in tests. Same automated word filter + 3-strike ban as public chat; markup escaped at render; one post per 10s per IP. Tests 190 checks, 0 FAIL. Verified live: form + archive present, blocked-word POST returns 403 and stores nothing. CAVEAT (told to Paul): the free tier's disk is ephemeral — a redeploy/restart resets board posts, same as chat history. True permanence needs persistent disk.
- **2026-11-09 ~09:50 MST: WebDates link sweep in progress (Paul: "any web dates links need to go").** A worker is removing every WebDates link site-wide. First batch already live in commit a34ee5e (directory.html WebDates cell, samples nav, deargabby/shop/webdates_intro nav image links unwrapped). Full sweep report still owed; remaining files get a second commit + deploy when it lands.
- **2026-11-09 ~09:52 MST: both PC tunnels died in a runtime restart** (ghost 11977 + CDP 19228, no listeners). Restarted via tunnel-watchdog.sh; Chrome 156 answering end-to-end. No work lost — the board test run had started (fresh test DB) and was re-run clean after.
- **2026-11-09 ~10:00 MST: WebDates link sweep COMPLETE (Paul's call).** Final verification: **0 hrefs to any WebDates target, 0 form actions to any WebDates page, site-wide.** 5 files changed (directory.html, samples.html, deargabby.htm, shop.htm, webdates_intro.htm — nav/image links unwrapped to plain text/images). Already live in commit a34ee5e (deployed ~09:55 MST, directory page verified 0 webdates mentions live). What remains are 33 non-link mentions: prose/image captions on live pages (allimages, messages.htm, new_members_form) and the now-orphaned WebDates subsystem files themselves (webdate_search/profile/browse_search.cfm, webdates_intro.htm, deargabby.htm, shop.htm) — unreachable, no links point to them. Deleting those orphaned pages is a separate call, only on Paul's word.

## Linking the Past (Paul 2026-11-09 ~10:28 MST, commit c309344, DEPLOYED + LIVE)
- Paul sent https://www.gitchi.net/chat1.html — browser read it: "Chats 1-10 – October 15th to December 2nd 1997", a first-person diary by "Bloodwynd" of ten 1997 chat sessions AT Club Gabbay (Lobby; "the usual Gabbay chat at www.clubGabbay.com"; Birds of a Feather, kicked out). Participants: LilBlusher, Lonewolf, Verve-girl, Insanity, Bugsy, MB, Giverny, Sable, Qwerty, Zell, Binks, Merciless, Sly. No guestbook on the page.
- New page site/www2.clubgabbay.com/linking-the-past.html: breadcrumbs of past efforts — Gitchi diary (+ chat list gitchi.net/chat.html), Wayback captures of clubgabbay.com (documented wildcard pattern web.archive.org/web/*/clubgabbay.com), Old'aVista + Yahoo directory listings, AndyChat changelog. Honest note: no archived copy of Gabbay's own guestbook has ever been found; the frozen 1997 Locator names are all we have; invites contributions via the board.
- Landing page: "Linking the Past" link under Enter ClubGabbay.
- Deploy: Manual Deploy -> Deploy latest commit via CDP (Render tab A00EE3820DED); c309344, 36.7s, Deploy succeeded. Verified live: /linking-the-past.html 200/3271B (gitchi + wayback links present), home 200/2372B (link present). fb-lock released.
- NOTE: first cdp.py click "button" hit the workspace switcher (harmless menu open) — always click deploy buttons by exact innerText via eval, never bare "button".

## Linking the Past + Facebook reunion group (Paul 2026-11-09 ~10:32 MST, commit 35485cf, DEPLOYED + LIVE)
- Paul sent a share.google link; resolved to the PUBLIC Facebook group "ClubGabbay Reunion" (facebook.com/groups/261819803829304/, 16 members) — Lobby + Anything Goes regulars sharing old handles + updates; check-ins 2012 through Sep 9, 2025. No sign-in/join/post by us (read-only).
- Added "Where the regulars gather now" section to linking-the-past.html with the direct group URL. Deploy: Manual Deploy -> Deploy latest commit, 35485cf, Deploy succeeded. Verified live: page 200 with the group link present. fb-lock released.

## BOARD POST LOST (Paul 2026-11-09 ~10:38 MST) — DEPLOY WIPE, LIKELY
- Paul posted a message to the board; his 10:37 screenshot shows the form + 1997 archive only, no new post. Verified firsthand via curl just now: live board has ZERO new posts.
- Render logs (Logs page, visible window 17:37-17:38 UTC) show only his GETs (GET /messages/ 17:38:49 = his 10:38 load); NO POST /messages/post line in the visible window — free-tier log retention too short to see 10:30-10:37. Cause NOT proven from logs.
- Most likely cause: the two deploys this morning (c309344 ~10:30, 35485cf ~10:33) each restarted the container and wiped the ephemeral SQLite board DB — Paul was active on the site through that whole window. His post most likely landed before the 10:33 deploy finished and was wiped. Content unrecoverable (never seen by Mira; not in logs).
- FREEZE DECLARED: no more deploys until board persistence is fixed. Free tier sleeps/restarts also risk wiping posts even without deploys — freeze reduces risk, does not guarantee.
- PERMANENCE FIX (needs Paul's pick — new service/key): (a) free hosted DB (e.g. Supabase free Postgres via PostgREST HTTP API, server stays stdlib-only), or (b) GitHub as the store (each post appended to a repo file via Contents API, needs a PAT). Render paid persistent disk exists but violates Paul's free-only rule unless he says otherwise.

## Board persistence FIXED (Paul's call 2026-11-09 ~10:42 MST, commit 2b7f040, DEPLOYED + LIVE)
- Paul: "your call what works best" — picked GitHub as the store (no new accounts, no server secrets, posts are public anyway).
- server.py: GET /api/board/posts (public JSON); restore_board_posts() re-seeds an empty board from BOARD_RESTORE_URL on boot (env var set on Render via dashboard; verified saved). restore never blocks startup; only runs when the board is empty; INSERT OR IGNORE idempotent.
- backend/backup_board.py: pulls the API (retry once — free instance may be waking), merges by id into site-data/board-posts.json, syncs just that file with origin/main first (dirty tree elsewhere must not block it), commits + pushes. Exit 0 ok/nothing-new, 2 on failure.
- Hook clubgabbay-board-backup (~/hooks/scripts/clubgabbay-board-backup.sh, 5-min poll, ENABLED): runs the backup; silent on success; wakes after 3 consecutive failures. Dry-run 1: API 404 (pre-deploy, expected — read-only, no state touched). Dry-run 2 post-deploy: "no new posts (0 saved)". Wake path traced by hand (preset 2 failures + broken API -> wake decision with failures:3, then reverted + state cleared).
- Tests: 196 checks, 0 FAIL (6 new: API endpoint + 5 restore cases incl. idempotency, non-empty gate, unreachable URL).
- E2E proven locally: post -> backup (1 new, committed+pushed) -> fresh DB restores via file:// AND via the real raw.githubusercontent URL (post back, log confirms). Cleanup commit cleared the test post (14158fd).
- Deploy: commit 2b7f040, env var saved via "Save, rebuild, and deploy" (one action). Live verified: /api/board/posts 200 {"posts": []}, /messages/ 200 with form. First live 404 was the old container mid-swap, not a bug.
- Deploy freeze LIFTED (deploys are safe again — restore on boot). Still: run the backup before any planned deploy (belt + braces); the hook covers the rest. Chat history still resets on restart (accepted POC) — only the BOARD is permanent now.
- Paul will re-post his lost message himself when ready; his post is the live proof (watch the first backup land within 5 min).

## Fine print / takedown contact (Paul 2026-11-09 ~11:23 MST, commit dc2d07e, DEPLOYED + LIVE)
- Paul: allow a takedown contact option but do NOT make it easy. Small grey "Fine print" link (size 1) in the footer of the home page + Linking the Past page, leading one click deep to /fine-print.html.
- Page says: fan-run homage, not affiliated with Yahoo!/GeoCities/original owners, nothing for sale; rights holders write to cjcoplin [at] gmail [dot] com with the page address + what they own, taken down promptly. Address obfuscated (no mailto link, no clickable address) — a human can read it, a bot cannot harvest it, and it takes an extra click to reach.
- Deploy: Manual Deploy -> Deploy latest commit, dc2d07e, Deploy succeeded. Verified live: /fine-print.html 200/945B with the notice, home 200/2448B with the link. Board empty at deploy time (zero loss). fb-lock released.

## Footer wording corrected (Paul 2026-11-09 ~11:27 MST, commit bc232f5, DEPLOYED + LIVE)
- Paul: the "All Rights Reserved, 1997" footer is not true — update it properly, check all pages, word it right. Found 11 occurrences across 8 site files + server.py; all reworded, zero "All Rights Reserved" remain anywhere.
- Home + Linking the Past footers: "A fan-run homage to the 1996-1999 Club Gabbay. Not affiliated with the original owners. Keep out of reach from small children. 5 minutes a day, that's all we ask! Enjoy!" (joke kept).
- Room pages (lobby, anything-goes, jokeland, all three lobby.html host copies) + server-generated room/member/404 pages: "Club Gabbay -- a fan-run homage to the 1996-1999 original."
- Tests: 196 checks, 0 FAIL after the change. Deploy bc232f5 succeeded; verified live (home footer new, 0 old lines).
- FIRST LIVE PROOF of the board persistence fix: Paul posted to the board ~10:58 MST ("Hi all!!! Leave a message! Let's reconnect!! Drop the handles you were and who you remember." — cjcoplin, to Everyone). The 5-min hook backed it up to site-data/board-posts.json; the bc232f5 deploy restarted the container and the new instance re-seeded it from the backup — his post is still live on the board after the deploy. The earlier mid-swap curls showed the old container; re-checked after the swap settled.

## Top 5 GeoCities neighborhoods — plan discussion (Paul 2026-11-09 ~11:35 MST)
- Paul: discuss a plan to build the top 5 the way they were, linked portals to each other, same setup for all, fan-made, for people to connect.
- Proposed five (by fame + archive presence; no per-neighborhood headcounts exist): Hollywood, SiliconValley, SunsetStrip, Area51, WestHollywood.
- Shape: ONE template, five portal pages. Each reads like its 1996 directory (theme, intro, member addresses) in our own words — homage, not copied pages; famous member pages LINKED OUT to Restorativland/Wayback, not re-hosted. Webring bar on every portal linking all five + Club Gabbay to each other. Same free Render service/repo, $0, megabytes. Home page gains a "Neighborhoods" link.
- Open decision: the connect part — ONE shared board (everyone lands together; simpler; the board that already works + survives deploys) vs a board per neighborhood (five boards; more code/upkeep; each its own room). Mira's recommendation: shared board first.
- Build order if approved: template -> five pages (with per-neighborhood research: which famous pages lived there) -> webring links + home link -> deploy + verify. NOT started; awaiting Paul's word on the five + the board question.

## Top 5 neighborhoods — BUILT + LIVE (Paul 2026-11-09 ~11:41-12:05 MST, commit 1a91fc3)
- Paul's calls: each one gets its own board; set up the way it was; no links to invalid crap.
- Five portals LIVE at /neighborhoods/<slug>.html (Hollywood, SiliconValley, SunsetStrip, Area51, WestHollywood) + index at /neighborhoods/ + home page link. One template (backend/build_neighborhoods.py): intro, full suburb directory (Blade's Place x-checked vs gallery + 1996 Wikipedia table), archive links, webring bar linking all five + Club Gabbay, own board link, fan-homage footer.
- Boards: generalized in server.py (board column; /neighborhoods/<slug>/board/; same filter/throttle/backup; posts isolated per board). Tests 226 checks, 0 FAIL (was 196).
- Outbound links, all verified live 200 before ship (13 distinct URLs): Oocities neighborhood browse + Wayback wildcard per neighborhood, Blade's Place, GifCities, Cameron's World. NO Restorativland links (down 522 on 2026-11-09 — re-check before linking); never geocities.ws. No individual member pages listed (CDX noisy; Hollywood + Area51 queries failed; archive-browse links are the way in).
- Research: neighborhoods-research.md (done directly by Mira — the research helper refused its attempt without doing any work; no file was written, so the digging was done here).
- Deploy verified live: all portals + index + boards 200; Paul's board post ("Hi all!!!") survived the deploy again — persistence holds.

## New landing page + age gate + 14 retro services (Paul 2026-11-09 ~13:43-13:54 MST)
- Paul: new landing page that's super clear with an age gate, explaining things; then "same idea, make all the pages for the other sites in that doc, ICQ etc, same set up for each one." Built as I saw fit (his words).
- The Discord model he quoted: layered verification, existing signals first, extra checks only when needed; a fan-made thing doesn't need ID uploads. Our version: the gate + terms + reporting + removal. No ID, no video selfie, no credit-card checks -- collecting IDs would create more risk than it removes. A checkbox is a declaration, not proof of age; a disclaimer does not make anyone immune (said plainly to Paul; BC lawyer review of the terms is his call, unmade).
- LANDING PAGE (index.html rewritten, 90s look kept): castle image + original intro kept; fake member counts (258/9134) and the Netscape/Java box dropped; ADULTS ONLY 21+ gate box (POST /age-gate, hidden confirm=21, submit "I am 21 or older -- Enter ClubGabbay", "I am under 21" link to /under21.html); the rules in plain words (21+, own your messages, no harassment/threats/illegal content, no sexual content involving minors ever, no doxxing, no impersonation/scams, automated filter, no live moderator, whispers private and unmonitored, reports get looked at, removal); what's inside (rooms, neighborhoods, AOL, board, Linking the Past); "More from the old days" listing all 14 services. The stale homepage "Anything Goes is 18+" line is gone (it was still live at 13:44).
- ENFORCEMENT (server.py): POST /age-gate sets age_ok on the session (created if needed), redirects to /chat.htm. _handle_entry requires the flag OR the entry form's confirm=21, else redirects to /; entering sets age_ok. /chat.htm + /chat2.htm require the flag, else /. Every entry form carries the confirm checkbox (lobby.cfm guest, anything_goes.cfm, jokeland.cfm, aol.html, member entry, neighborhood entries via build_neighborhoods.py). /under21.html is the polite stop page. Fine print gains the 21+ audience note + fuller Terms of entry.
- GATE-ONLY SESSION BUG (found by the test suite): a session created by the gate has no room/user keys; presence(), guest_name() and _handle_entry used direct s["room"]/sess["room"] indexing -> KeyError -> handler died -> RemoteDisconnected. Fixed with .get() in all four places (+ the jump branch now requires sess.get("user")).
- 14 RETRO SERVICES, same setup each: MSN, Yahoo, ICQ, mIRC, Excite, Paltalk, Lycos, Palace, Habbo, PowWow, CompuServe, Prodigy, Xfire, MySpace. SERVICES table in server.py (single source of truth) builds ROOMS entries (<slug>-chat, own bgcolor, desc, join); backend/build_services.py imports it and generates site/www2.clubgabbay.com/<slug>.html (landing page + 21+ note + handle form with confirm checkbox + links to all 14 services + Gabbay home + fine print). 31 rooms total now (17 + 14).
- TESTS: 589 checks, 0 FAIL (was 365). New: run_landing_tests (gate flow, enforcement, no-18+, service links, fine print) + run_services_tests (each service: page serves, entry without confirm bounces home, entry with confirm reaches the room). walk_room now covers all 31 rooms (ENTRY_PAGE/JOIN_TEXT extended). Existing clients all gate() first (27 call sites). Persistence check needed gate(c2) after the restart (the post-restart join was bouncing).
- Deploy: commit 8d57075, Manual Deploy -> Deploy latest commit, succeeded in 32.3s (dep-dbp3btdbedkc73fhv7eg). Verified live: home 200/4693B with ADULTS ONLY + gate, zero 18+; msn/icq/under21/fine-print all 200; /chat.htm no-cookie 303 -> /; gate POST -> chat.htm 200; ICQ room entry live (LiveTest joined, room 200). Paul's board post (id 1, cjcoplin 'Hi all!!!') survived the deploy -- persistence holds.

## Messenger skins for all 14 services (Paul 2026-11-09 ~14:18 MST)
- Paul: the old ICQ etc should have the look the messengers had, like AOL -- each matching its own.
- One parameterized renderer (render_messenger_room_page, server.py): the AOL Chat window re-skinned per service -- title bar in the service's color, member list on the right (click a name to open an IM box), Send form, actions dropdown, history form, same poll/filter/whisper engine. No color/font pickers -- those stay AOL-only. Dispatch in _handle_room: aol -> AOL renderer, messenger -> messenger renderer, else the generic room page.
- Skins live in the SERVICES table (single source of truth): title defaults to the service bgcolor; win/body/text/link/vlink default to the AOL grey window. Distinctive ones: ICQ green window/body, Habbo yellow title bar with black text, Xfire dark (black title, #333 window, #222 body, white text, light-blue links), the rest tinted windows in their brand colors.
- Landing pages (build_services.py) now wear the skin too: body bgcolor + a title-bar table with the service color and name, instead of the plain home_bg look.
- Tests: 589 checks, 0 FAIL. run_services_tests now asserts each room page carries its title-bar color, the member list + IM box, the whisper + action forms, no "AOL Chat", no color picker. walk_room still covers all 31 rooms end to end.
- Deploy: commit 52f4cc7, Manual Deploy -> Deploy latest commit, succeeded in 40.6s. Verified live: ICQ room green title bar + IM box + member list, zero AOL leak; MSN blue title bar; Xfire dark body + black title bar. Paul's board post survived the deploy.

## Messenger skins v2 — the real web-chat look (Paul 2026-11-09 ~14:29 MST)
- Paul sent a screenshot of the real ICQ web chat and asked: for the ones that had stuff like this, build them all to look more like what they should look like. Same renderer, now with the ICQ screenshot's chrome + the per-service signatures from messenger-skins-spec-2026-11-09.md (a background worker wrote the spec; the build is mine, live).
- Shared (all 14): Status: Online + channel tab under the title bar (ICQ #icq_usa, mIRC #Canada, CompuServe CB Channel 1, the rest their room name); a Chat Rooms panel on the right listing the other 13 services; colored join/quit lines (ICQ green joins / red quits from the screenshot; mIRC grey/grey); a Send button styled in the service's title color; the chat area in the service's own colors/font.
- Per-service signatures: MSN Nudge button (shakes the pane, JS only), Yahoo BUZZ! button (same shake), ICQ flower mark (CSS green circle, gold ring) + "Uh-oh!" in the footer, mIRC monospace chat, Excite red portal masthead ("Home | Chat | Mail", plain text, no fake links), Paltalk video strip (grey placeholder tiles), Lycos black/yellow masthead ("Go get it"), Palace sky-blue chat + Comic Sans MS, Habbo pale yellow chat + Verdana, PowWow purple voice dot next to names (in the live member list too, via a JS flag), CompuServe black terminal chat + green monospace + GO button, Prodigy yellow "Welcome to Prodigy Chat" strip, Xfire dark chat, MySpace Top 8 strip (first 8 others as clickable squares; needs another user in the room to show).
- Deliberately NOT done: UIN numbers under ICQ names (would invent identifiers for real users), MySpace "Mood:" lines and Xfire "Playing:" lines (would invent facts about real users), CompuServe ALL-CAPS handles (would break the click-to-PM name match), Paltalk "Request Mic" / Xfire "Join Game" buttons (would be fake buttons that do nothing), Habbo isometric room + Palace smiley avatars with speech bubbles (bigger layout builds; possible follow-ups on Paul's word).
- Implementation: SKIN_DEFAULT gains chat_bg/chat_fg/chat_font/join/quit/channel/send/nudge/notice/masthead/flower/video_strip/top8/voice_dot/footer_note; per-service overrides in the SERVICES table; render_msg(m, join_c, quit_c) colors join/leave lines only when the messenger renderer passes colors (Gabbay + AOL rooms unchanged). Gotcha fixed: a bare % in the template's JS (border-radius:50% in the voice-dot span) broke % formatting with "not enough arguments" -- it needs %% inside the template.
- Tests: 603 checks, 0 FAIL (was 589; +14 v2 checks, one per service). MySpace needed a second user in the room for the Top 8 strip to render, so the test brings one in.
- Deploy: commit + Manual Deploy (Render) + live verify owed.
