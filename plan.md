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
