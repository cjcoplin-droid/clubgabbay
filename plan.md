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
