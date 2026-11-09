#!/usr/bin/env python3
"""Local test for the Club Gabbay mirror backend (spec step 5).

Starts server.py on a scratch port with a scratch SQLite DB, walks every
room (homepage -> Enter -> Lobby guest + member entry -> post -> HISTORY
check -> jump -> images -> broken-link spot check), verifies persistence
across a restart, and writes a Markdown report to
../backend-test-report.md. Also prints a one-line summary.

Usage: python3 test_backend.py [--keep-server]
"""
import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(HERE)
REPORT = os.path.join(BASE_DIR, "backend-test-report.md")
PORT = 8124
DB = os.path.join(HERE, "test-chat.db")

results = []  # (room, check, status, detail)


def check(room, name, ok, detail=""):
    results.append((room, name, "PASS" if ok else "FAIL", detail))
    print(("PASS " if ok else "FAIL ") + room + " :: " + name +
          (" — " + detail if detail else ""))


class Client:
    """urllib client with its own cookie jar (one browser user)."""

    def __init__(self, base):
        self.base = base
        self.jar = CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar))

    def req(self, method, path, data=None, headers=None):
        url = self.base + path
        body = None
        hdrs = dict(headers or {})
        if data is not None:
            body = urllib.parse.urlencode(data).encode()
            hdrs["Content-Type"] = "application/x-www-form-urlencoded"
        r = urllib.request.Request(url, data=body, method=method, headers=hdrs)
        try:
            resp = self.opener.open(r)
            return resp.status, resp.read(), dict(resp.headers)
        except urllib.error.HTTPError as e:
            return e.code, e.read(), dict(e.headers)

    def get(self, path, **kw):
        return self.req("GET", path, **kw)

    def post(self, path, data, **kw):
        return self.req("POST", path, data=data, **kw)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def raw_get(base, path):
    """GET without following redirects, no cookies."""
    opener = urllib.request.build_opener(NoRedirect)
    try:
        resp = opener.open(base + path)
        return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def start_server(fresh=True):
    if fresh and os.path.exists(DB):
        os.remove(DB)
    proc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "server.py"),
         "--port", str(PORT), "--db", DB],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    base = "http://127.0.0.1:%d" % PORT
    for _ in range(50):
        try:
            s, _, _ = raw_get(base, "/")
            if s == 200:
                return proc, base
        except Exception:
            pass
        time.sleep(0.2)
    raise RuntimeError("server did not come up;\n" +
                       (proc.stdout.read() if proc.stdout else ""))


def stop_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


ROOMS = ["lobby", "blue", "speakeasy", "denim", "hard", "soul", "jive",
         "classical", "paradise", "anything-goes", "jokeland"]
ENTRY_PAGE = {
    "lobby": "/www2.clubgabbay.com/lobby.cfm",
    "blue": "/www.clubgabbay.com/htmls/blue.html",
    "speakeasy": "/www.clubgabbay.com/htmls/speakeasy.html",
    "denim": "/www.clubgabbay.com/htmls/denim.html",
    "hard": "/www.clubgabbay.com/htmls/hard.html",
    "soul": "/www.clubgabbay.com/htmls/soul.html",
    "jive": "/www.clubgabbay.com/htmls/jive.html",
    "classical": "/www.clubgabbay.com/htmls/classical.html",
    "paradise": "/www.clubgabbay.com/htmls/paradise.html",
    "anything-goes": "/www2.clubgabbay.com/anything_goes.cfm",
    "jokeland": "/www2.clubgabbay.com/jokeland.cfm",
}
JOIN_TEXT = {
    "lobby": "Joins The Lobby", "blue": "Joins Blue Notes",
    "speakeasy": "Joins The Speak Easy", "denim": "Joins Denim",
    "hard": "Joins Hard Rock", "soul": "Joins Soul Searching",
    "jive": "Joins Jive Talkin", "classical": "Joins Classical Comment",
    "paradise": "Joins Paradise Patio",
    "anything-goes": "Joins Anything Goes",
    "jokeland": "Joins Jackie",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep-server", action="store_true")
    args = ap.parse_args()

    proc, base = start_server()
    print("server up on", base)
    current = proc
    try:
        run_tests(base)
        # persistence across restart
        proc2, base2 = persistence_check(proc, base)
        current = proc2
        base = base2
    finally:
        if not args.keep_server:
            stop_server(current)
    write_report()
    fails = [r for r in results if r[2] == "FAIL"]
    print("\n%d checks, %d FAIL" % (len(results), len(fails)))
    return 1 if fails else 0


def run_tests(base):
    # ---- site shell: homepage -> Enter -> chat directory
    anon = Client(base)
    s, body, _ = anon.get("/")
    check("site", "homepage / returns 200 + Enter ClubGabbay -> /chat.htm, "
          "no webdates/email/linkexchange (Paul 2026-11-09)",
          s == 200 and b"Enter ClubGabbay" in body
          and b'href="/chat.htm"' in body
          and b"webdates" not in body.lower()
          and b"comments@clubgabbay.com" not in body
          and b"linkexchange" not in body.lower(),
          "status=%d" % s)
    # Removed pages (Paul 2026-11-09): the /main.htm frameset (menu +
    # Michael message) is not live, and WebDates is gone.
    for gone in ["/main.htm", "/welcome.htm", "/menu.cfm", "/webdates.cfm"]:
        s, body, _ = anon.get(gone)
        check("site", "%s removed 404 (Paul 2026-11-09)" % gone,
              s == 404, "status=%d" % s)
    # Bulletin board keeps the 1997 posts; the dead LinkExchange banner
    # is gone from it and from every other page (Paul 2026-11-09).
    # Since 2026-11-09 the board is server-rendered and postable: the
    # 1997 archive frozen below, new posts above it.
    s, body, _ = anon.get("/www.clubgabbay.com/messages/index.html")
    check("site", "bulletin board 200, no linkexchange (Paul 2026-11-09)",
          s == 200 and b"Bulletin Board" in body
          and b"linkexchange" not in body.lower()
          and b'action="/messages/post"' in body,
          "status=%d" % s)
    # Calendar footer: Web Dates + Mall links removed (Paul 2026-11-09);
    # the webdates.html stub page is gone too.
    s, body, _ = anon.get("/www.clubgabbay.com/htmls/calendar.html")
    check("site", "calendar footer has no webdates/mall links",
          s == 200 and b"Calendar of Events" in body
          and b"Web Dates" not in body
          and b"Have It All Mall" not in body,
          "status=%d" % s)
    s, body, _ = anon.get("/htmls/webdates.html")
    check("site", "/htmls/webdates.html removed 404 (Paul 2026-11-09)",
          s == 404, "status=%d" % s)
    s, body, _ = anon.get("/chat.htm")
    check("site", "/chat.htm directory 200", s == 200 and b"Lobby" in body,
          "status=%d" % s)
    s, body, _ = anon.get("/chat2.htm")
    check("site", "/chat2.htm rooms list 200",
          s == 200 and b"Blue Notes" in body, "status=%d" % s)

    # ---- images that the room pages need
    for img in ["/images/bg/lobby_bg.jpg", "/images/lobby.jpg",
                "/images/bg/speak_bg.jpg", "/images/speakeasy.jpg",
                "/images/bg/denim_bg.jpg", "/images/denim.jpg",
                "/images/bg/classical_bg.jpg", "/images/classical.jpg",
                "/images/blue.jpg", "/images/rock.jpg",
                "/images/jive_talkin.jpg", "/images/paradise.jpg",
                "/images/soul_searching.jpg", "/anything_goes.jpg",
                "/images/bg/home_bg.jpg"]:
        s, _, _ = anon.get(img)
        check("site", "image %s loads" % img, s == 200, "status=%d" % s)
    # known archive gaps (expected 404s — pre-existing, not backend bugs)
    for img in ["/images/bg/blue_bg.jpg", "/images/bg/hard_bg.jpg",
                "/images/bg/jive_bg.jpg", "/images/bg/paradise_bg.jpg",
                "/images/bg/soulsearch_bg.jpg"]:
        s, _, _ = anon.get(img)
        check("site", "known archive gap %s returns 404 (expected)" % img,
              s == 404, "status=%d" % s)

    # ---- member entry page
    s, body, _ = anon.get("/lobby2.cfm")
    check("lobby", "member entry /lobby2.cfm 200",
          s == 200 and b"Enter as Member" in body, "status=%d" % s)

    # ---- per-room walk
    for slug in ROOMS:
        walk_room(base, slug)

    # ---- Lobby guest + member paths in detail (already covered per-room,
    # but verify the two distinct entry forms explicitly)
    guest = Client(base)
    s, _, h = guest.post("/lobby", {"USER": "Guest1251",
                                    "SAYS": "<b>Joins The Lobby...</b>",
                                    "HISTORY": "8"})
    check("lobby", "guest form (archived Guest1251) redirects to /lobby",
          s in (200, 303), "status=%d" % s)
    s, body, _ = guest.get("/api/lobby/messages?since=0",
                           headers={"Accept": "application/json"})
    try:
        data = json.loads(body)
        names = [m["user"] for m in data["messages"]]
        auto = any(re.fullmatch(r"Guest\d+", n) for n in names)
    except Exception:
        auto = False
    check("lobby", "guest gets fresh auto-name GuestNNNN (not literal 1251)",
          auto, "names=%s" % (names if 'names' in dir() else "?"))

    member = Client(base)
    s, _, _ = member.post("/lobby", {"USER": "TestMember", "PASSWORD": "x",
                                     "MEMBER": "1",
                                     "SAYS": "<b>Joins The Lobby...</b>",
                                     "HISTORY": "8"})
    s, body, _ = member.get("/api/lobby/messages?since=0",
                            headers={"Accept": "application/json"})
    try:
        data = json.loads(body)
        pres = data["presence"]
        flagged = any("TestMember (member)" in p for p in pres)
    except Exception:
        flagged = False
    check("lobby", "member entry flagged (member) in presence",
          flagged, "presence=%s" % (pres if 'pres' in dir() else "?"))

    # ---- HISTORY behaviour: post 12 messages, HISTORY=8 shows last 8
    hist = Client(base)
    hist.post("/lobby", {"USER": "HistTest",
                         "SAYS": "<b>Joins The Lobby...</b>",
                         "HISTORY": "8"})
    for i in range(12):
        hist.post("/lobby/post", {"text": "hist-msg-%02d" % i})
        time.sleep(2.1)  # respect the rate limit
    s, body, _ = hist.get("/api/lobby/messages?since=0",
                          headers={"Accept": "application/json"})
    data = json.loads(body)
    shown = [m["text"] for m in data["messages"] if m["text"].startswith("hist-msg")]
    check("lobby", "HISTORY=8 shows exactly last 8 of 12 posted",
          len(shown) == 8 and shown[0] == "hist-msg-04"
          and shown[-1] == "hist-msg-11",
          "shown=%s" % shown)

    # ---- rate limit: two rapid posts, second is 429
    rl = Client(base)
    rl.post("/lobby", {"USER": "RateTest",
                       "SAYS": "<b>Joins The Lobby...</b>", "HISTORY": "8"})
    s1, _, _ = rl.post("/lobby/post", {"text": "first"})
    s2, _, _ = rl.post("/lobby/post", {"text": "second-too-fast"})
    check("lobby", "rate limit: 2nd post within 2s is 429",
          s1 in (200, 303) and s2 == 429, "first=%d second=%d" % (s1, s2))

    # ---- whisper privacy: only sender + recipient see it
    w1, w2, w3 = Client(base), Client(base), Client(base)
    for c, u in ((w1, "WhispA"), (w2, "WhispB"), (w3, "WhispC")):
        c.post("/blue", {"USER": u, "SAYS": "<b>Joins Blue Notes...</b>",
                         "HISTORY": "8"})
    time.sleep(2.1)
    w1.post("/blue/whisper", {"to": "WhispB", "text": "secret-for-b-only"})
    time.sleep(0.2)
    seen = {}
    for label, c in (("sender", w1), ("recipient", w2), ("other", w3)):
        s, body, _ = c.get("/api/blue/messages?since=0",
                           headers={"Accept": "application/json"})
        seen[label] = "secret-for-b-only" in body.decode("utf-8", "replace")
    check("blue", "whisper visible to sender + recipient only, not others",
          seen["sender"] and seen["recipient"] and not seen["other"],
          str(seen))

    # ---- 18+ gate: GET /anything-goes with no session redirects to gate
    s, _, h = raw_get(base, "/anything-goes")
    check("anything-goes", "GET /anything-goes w/o session redirects to gate",
          s in (301, 302, 303) and "anything_goes.cfm" in h.get("Location", ""),
          "status=%d loc=%s" % (s, h.get("Location", "")))

    # ---- word filter (public messages only; whispers never filtered)
    run_filter_tests(base)

    # ---- message board is postable (Paul, 2026-11-09)
    run_board_tests(base)
    # ---- board restore: posts survive restarts via the backup file
    run_board_restore_tests()

    # ---- homepage blurb + monitoring notes
    s, body, _ = anon.get("/")
    check("site", "homepage carries the approved blurb",
          b"Club Gabbay Chat is back" in body, "")
    check("site", "homepage notes monitoring / 18+ / private whispers",
          b"Whispers are private and unmonitored" in body, "")
    # the blocklist itself is never served
    s, _, _ = anon.get("/blocklist.txt")
    check("filter", "blocklist is not served over HTTP (/blocklist.txt 404)",
          s == 404, "status=%d" % s)
    s, _, _ = anon.get("/backend/blocklist.txt")
    check("filter", "blocklist is not served (/backend/blocklist.txt 404)",
          s == 404, "status=%d" % s)

    # ---- broken-link spot check on the homepage + chat directory.
    # The server must agree with the archive: 200 where the file exists
    # in site/, 404 where it was never captured (pre-existing gaps).
    host_dirs = ["www2.clubgabbay.com", "www.clubgabbay.com",
                 "clubgabbay.com", "chat.clubgabbay.com",
                 "members.clubgabbay.com"]

    def expected_status(p):
        rel = p.lstrip("/")
        cands = []
        first = rel.split("/")[0]
        if first in host_dirs:
            cands.append(os.path.join(BASE_DIR, "site", rel))
        else:
            for h in host_dirs:
                cands.append(os.path.join(BASE_DIR, "site", h, rel))
        for cand in cands:
            if os.path.isdir(cand):
                cand = os.path.join(cand, "index.html")
            if os.path.isfile(cand):
                return 200
        return 404

    for page in ["/", "/chat.htm", "/chat2.htm"]:
        s, body, _ = anon.get(page)
        links = re.findall(rb'(?:src|href)="([^"]+)"', body)
        broken, mismatched = [], []
        for link in links:
            href = link.decode("utf-8", "replace")
            if href.startswith(("http://", "https://", "mailto:", "#",
                                "javascript:")):
                continue
            target = urllib.parse.urljoin(base + page, href)
            p = urllib.parse.urlparse(target).path
            st, _, _ = anon.get(p)
            exp = expected_status(p)
            if st != exp:
                mismatched.append("%s -> %s (got %d, expected %d)"
                                  % (href, p, st, exp))
            elif st == 404:
                broken.append(href)
        check("site", "link check %s (%d links): server matches archive"
              % (page, len(links)), not mismatched,
              "; ".join(mismatched) if mismatched else
              ("pre-existing archive gaps (404, expected): %s" % broken
               if broken else "all resolve"))


def run_filter_tests(base):
    """Automated word filter: public messages only. Whispers bypass the
    filter entirely (Paul, 2026-11-07) — never monitored or filtered."""
    # banned word in a public message is blocked, never stored
    f = Client(base)
    f.post("/lobby", {"USER": "FilterTest",
                      "SAYS": "<b>Joins The Lobby...</b>", "HISTORY": "8"})
    s, _, _ = f.post("/lobby/post", {"text": "this is a fuck test"})
    check("filter", "banned word in public message is blocked (403)",
          s == 403, "status=%d" % s)
    s, body, _ = f.get("/api/lobby/messages?since=0",
                       headers={"Accept": "application/json"})
    check("filter", "blocked message never stored/shown",
          b"this is a fuck test" not in body, "")
    # clean message from the same user passes (one strike does not ban)
    s, _, _ = f.post("/lobby/post", {"text": "hello clean world"})
    check("filter", "clean message passes after one strike",
          s in (200, 303), "status=%d" % s)
    s, body, _ = f.get("/api/lobby/messages?since=0",
                       headers={"Accept": "application/json"})
    check("filter", "clean message is stored",
          b"hello clean world" in body, "")
    # innocent word containing a token-only fragment is not blocked
    time.sleep(2.1)  # the clean post above set the rate-limit clock
    s, _, _ = f.post("/lobby/post", {"text": "I love my class"})
    check("filter", "innocent word (class) is not blocked",
          s in (200, 303), "status=%d" % s)
    # spaced-out evasion is still caught
    s, _, _ = f.post("/lobby/post", {"text": "f u c k"})
    check("filter", "spaced-out evasion is still caught (403)",
          s == 403, "status=%d" % s)
    # 3 strikes -> banned from public posting
    b = Client(base)
    b.post("/lobby", {"USER": "StrikeTest",
                      "SAYS": "<b>Joins The Lobby...</b>", "HISTORY": "8"})
    codes = []
    for _ in range(3):
        s, _, _ = b.post("/lobby/post", {"text": "fuck"})
        codes.append(s)
    check("filter", "three blocked posts all return 403",
          codes == [403, 403, 403], "statuses=%s" % codes)
    s, _, _ = b.post("/lobby/post", {"text": "a clean message now"})
    check("filter", "3 strikes -> banned: clean message rejected (403)",
          s == 403, "status=%d" % s)
    s, body, _ = b.get("/api/lobby/messages?since=0",
                       headers={"Accept": "application/json"})
    check("filter", "banned user's clean message never stored",
          b"a clean message now" not in body, "")
    # ban is per-user: someone else can still post
    o = Client(base)
    o.post("/lobby", {"USER": "OtherUser",
                      "SAYS": "<b>Joins The Lobby...</b>", "HISTORY": "8"})
    s, _, _ = o.post("/lobby/post", {"text": "other user is fine"})
    check("filter", "ban is per-user: another user posts fine",
          s in (200, 303), "status=%d" % s)
    # whisper with a banned word passes unfiltered, delivered to recipient
    w1, w2 = Client(base), Client(base)
    for c, u in ((w1, "WhispF1"), (w2, "WhispF2")):
        c.post("/blue", {"USER": u, "SAYS": "<b>Joins Blue Notes...</b>",
                         "HISTORY": "8"})
    s, _, _ = w1.post("/blue/whisper", {"to": "WhispF2", "text": "fuck"})
    check("filter", "whisper with banned word passes unfiltered",
          s in (200, 303), "status=%d" % s)
    s, body, _ = w2.get("/api/blue/messages?since=0",
                        headers={"Accept": "application/json"})
    try:
        data = json.loads(body)
        got = any(m["kind"] == "whisper" and m["text"] == "fuck"
                  for m in data["messages"])
    except Exception:
        got = False
    check("filter", "whisper with banned word is delivered to recipient",
          got, "")


def run_board_tests(base):
    """Message board is postable (Paul, 2026-11-09): anyone can add a
    message; new posts render above the frozen 1997 archive and stay
    up (SQLite, no cap). Same word filter + strikes as public chat."""
    b = Client(base)
    s, body, _ = b.get("/messages/")
    check("board", "board page has post form + 1997 archive",
          s == 200 and b'action="/messages/post"' in body
          and b'name="message"' in body and b"Miss you" in body,
          "status=%d" % s)
    # clean post lands, above the archive
    s, _, _ = b.post("/messages/post",
                     {"to": "ANYONE!!", "from": "BoardPoster",
                      "subject": "hello board",
                      "message": "board-test-hello-12345"})
    check("board", "clean board post accepted",
          s in (200, 303), "status=%d" % s)
    s, body, _ = b.get("/messages/")
    check("board", "new post shows above the 1997 archive",
          b"board-test-hello-12345" in body
          and body.index(b"board-test-hello-12345") < body.index(b"Miss you"),
          "")
    # the backup job reads the board as JSON (Paul, 2026-11-09)
    s, body, _ = b.get("/api/board/posts")
    data = json.loads(body.decode("utf-8"))
    check("board", "GET /api/board/posts returns the new post as JSON",
          s == 200 and any(p.get("message") == "board-test-hello-12345"
                           for p in data.get("posts", [])),
          "status=%d" % s)
    # HTML in a post is escaped, never rendered
    time.sleep(10.1)  # board rate limit: 1 post per 10s per IP
    s, _, _ = b.post("/messages/post",
                     {"to": "", "from": "BoardXSS", "subject": "xss",
                      "message": "<script>alert(1)</script>"})
    check("board", "markup post accepted (stored, escaped at render)",
          s in (200, 303), "status=%d" % s)
    s, body, _ = b.get("/messages/")
    check("board", "markup in a post is escaped, never rendered",
          b"&lt;script&gt;" in body and b"<script>alert(1)" not in body,
          "")
    # blocked word: 403, never stored
    s, _, _ = b.post("/messages/post",
                     {"to": "", "from": "BoardFilter", "subject": "",
                      "message": "this is a fuck test"})
    check("board", "banned word in board post is blocked (403)",
          s == 403, "status=%d" % s)
    s, body, _ = b.get("/messages/")
    check("board", "blocked board post never stored/shown",
          b"this is a fuck test" not in body, "")
    # 3 strikes -> banned from the board
    codes = []
    for _ in range(3):
        s, _, _ = b.post("/messages/post",
                         {"to": "", "from": "BoardStrike", "subject": "",
                          "message": "fuck"})
        codes.append(s)
    check("board", "three blocked board posts all return 403",
          codes == [403, 403, 403], "statuses=%s" % codes)
    s, _, _ = b.post("/messages/post",
                     {"to": "", "from": "BoardStrike", "subject": "",
                      "message": "a clean message now"})
    check("board", "3 strikes -> banned from board: clean post rejected",
          s == 403, "status=%d" % s)
    # empty From / empty message -> back to the board, nothing stored
    s, body, _ = b.post("/messages/post",
                        {"to": "", "from": "", "subject": "",
                         "message": "board-test-no-name-12345"})
    s, body, _ = b.get("/messages/")
    check("board", "post with no From name is not stored",
          b"board-test-no-name-12345" not in body, "")


def run_board_restore_tests():
    """Board restore (Paul, 2026-11-09): an empty board re-seeds from the
    backup file on boot so posts survive restarts/deploys. Tests the
    restore function in-process against a scratch DB + file:// URL."""
    import shutil
    import tempfile
    sys.path.insert(0, HERE)
    import server as srv
    tmp = tempfile.mkdtemp(prefix="board-restore-")
    try:
        db_path = os.path.join(tmp, "restore.db")
        srv.db_init(db_path)
        backup = os.path.join(tmp, "board-posts.json")
        with open(backup, "w", encoding="utf-8") as fh:
            json.dump({"posts": [{"id": 7, "name": "RestoreTest", "to": "",
                                  "subject": "hi",
                                  "message": "restore-marker-12345",
                                  "ts": 1794240000.0}]}, fh)
        url = "file://" + backup
        n = srv.restore_board_posts(url)
        got = [p["message"] for p in srv.db_board_posts()]
        check("board", "restore seeds an empty board from the backup file",
              n == 1 and "restore-marker-12345" in got, "restored=%d" % n)
        n = srv.restore_board_posts(url)
        check("board", "restore is idempotent (second run restores 0)",
              n == 0 and len(srv.db_board_posts()) == 1, "restored=%d" % n)
        # non-empty board: restore does nothing (live posts never clobbered)
        srv.db_add_board_post("LivePoster", "", "", "live-marker-12345")
        other = os.path.join(tmp, "other.json")
        with open(other, "w", encoding="utf-8") as fh:
            json.dump({"posts": [{"id": 99, "name": "Other", "to": "",
                                  "subject": "",
                                  "message": "other-marker-12345",
                                  "ts": 1794240001.0}]}, fh)
        n = srv.restore_board_posts("file://" + other)
        msgs = [p["message"] for p in srv.db_board_posts()]
        check("board", "restore skips a non-empty board (live posts kept)",
              n == 0 and "live-marker-12345" in msgs
              and "other-marker-12345" not in msgs, "restored=%d" % n)
        # unreachable URL: returns 0, never raises
        try:
            n = srv.restore_board_posts("http://127.0.0.1:1/nope.json")
            ok = (n == 0)
        except Exception:
            ok = False
        check("board", "restore with an unreachable URL returns 0, no crash",
              ok, "")
        # no URL configured: no-op
        check("board", "restore with no URL configured is a no-op",
              srv.restore_board_posts("") == 0, "")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def walk_room(base, slug):
    c = Client(base)
    # entry page serves
    s, body, _ = c.get(ENTRY_PAGE[slug])
    check(slug, "entry page %s 200" % ENTRY_PAGE[slug],
          s == 200, "status=%d" % s)
    # room without a session redirects to its entry page
    s, _, h = raw_get(base, "/" + slug)
    check(slug, "GET /%s w/o session redirects to entry page" % slug,
          s in (301, 302, 303) and ENTRY_PAGE[slug].split("/")[-1] in
          h.get("Location", ""),
          "status=%d loc=%s" % (s, h.get("Location", "")))
    # guest entry
    name = "T" + slug[:9].replace("-", "")
    s, _, h = c.post("/" + slug, {"USER": name,
                                  "SAYS": "<b>%s</b>" % JOIN_TEXT[slug],
                                  "HISTORY": "8"})
    check(slug, "guest entry POST redirects to /%s" % slug,
          s in (200, 303), "status=%d" % s)
    s, body, _ = c.get("/" + slug)
    check(slug, "chat pane shows join line + room name",
          s == 200 and JOIN_TEXT[slug].encode() in body
          and ROOMS and name.encode() in body, "status=%d" % s)
    # post a message, then see it via the poll API
    s, _, _ = c.post("/" + slug + "/post", {"text": "hello from %s test" % slug})
    check(slug, "post a message (303 back to room)",
          s in (200, 303), "status=%d" % s)
    s, body, _ = c.get("/api/%s/messages?since=0" % slug,
                       headers={"Accept": "application/json"})
    try:
        data = json.loads(body)
        mine = [m for m in data["messages"]
                if m["text"] == "hello from %s test" % slug]
        pres = name in " ".join(data["presence"])
        hist_ok = len(data["messages"]) <= 8
    except Exception as e:
        mine, pres, hist_ok = [], False, False
    check(slug, "poll API returns posted message",
          bool(mine), "found=%d" % len(mine))
    check(slug, "presence lists the chatter", pres, "")
    check(slug, "HISTORY=8 caps initial pane at 8", hist_ok,
          "n=%d" % (len(data["messages"]) if 'data' in dir() else -1))
    # jump to the next room with the same name
    nxt = ROOMS[(ROOMS.index(slug) + 1) % len(ROOMS)]
    s, _, h = c.get("/%s?jump=1" % nxt)
    check(slug, "jump to /%s keeps session, redirects" % nxt,
          s in (200, 303), "status=%d" % s)
    s, body, _ = c.get("/api/%s/messages?since=0" % nxt,
                       headers={"Accept": "application/json"})
    try:
        data = json.loads(body)
        joined = any(m["kind"] == "join" and m["user"] == name
                     for m in data["messages"])
    except Exception:
        joined = False
    check(slug, "jump posts join line in %s" % nxt, joined, "")
    # leave
    s, _, _ = c.get("/%s/leave" % nxt)
    check(slug, "leave %s redirects to chat directory" % nxt,
          s in (200, 303), "status=%d" % s)


def persistence_check(proc, base):
    """Restart the server; a message posted before the restart must still
    be in the room history (SQLite persistence)."""
    c = Client(base)
    c.post("/lobby", {"USER": "Persist", "SAYS": "<b>Joins The Lobby...</b>",
                      "HISTORY": "8"})
    c.post("/lobby/post", {"text": "persist-marker-12345"})
    stop_server(proc)
    proc2, base2 = start_server(fresh=False)
    c2 = Client(base2)
    c2.post("/lobby", {"USER": "Persist2", "SAYS": "<b>Joins The Lobby...</b>",
                       "HISTORY": "8"})
    s, body, _ = c2.get("/api/lobby/messages?since=0",
                        headers={"Accept": "application/json"})
    ok = b"persist-marker-12345" in body
    check("site", "message survives server restart (SQLite persistence)",
          ok, "found=%s" % ok)
    # board posts survive the restart too — they stay up
    s, body, _ = c2.get("/messages/")
    ok = b"board-test-hello-12345" in body
    check("board", "board post survives server restart (stays up)",
          ok, "found=%s" % ok)
    return proc2, base2


def write_report():
    fails = [r for r in results if r[2] == "FAIL"]
    passes = [r for r in results if r[2] == "PASS"]
    lines = []
    lines.append("# Club Gabbay mirror — backend test report (spec step 5)")
    lines.append("")
    lines.append("Test run: %s (local only, http://127.0.0.1:%d, "
                 "scratch DB test-chat.db)" %
                 (time.strftime("%Y-%m-%d %H:%M %Z"), PORT))
    lines.append("Backend: `backend/server.py` (stdlib-only Python), "
                 "test: `backend/test_backend.py`.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("- Checks run: %d — **%d PASS, %d FAIL**"
                 % (len(results), len(passes), len(fails)))
    lines.append("- Rooms walked: %d of 11 (%s)"
                 % (len(ROOMS), ", ".join(ROOMS)))
    lines.append("")
    lines.append("## Per-room results")
    lines.append("")
    lines.append("| Room | Check | Result | Detail |")
    lines.append("|---|---|---|---|")
    for room, name, status, detail in results:
        if room == "site":
            continue
        lines.append("| %s | %s | %s | %s |"
                     % (room, name, status, detail.replace("|", "/")))
    lines.append("")
    lines.append("## Site / cross-cutting results")
    lines.append("")
    lines.append("| Check | Result | Detail |")
    lines.append("|---|---|---|")
    for room, name, status, detail in results:
        if room != "site":
            continue
        lines.append("| %s | %s | %s |" % (name, status,
                                            detail.replace("|", "/")))
    lines.append("")
    lines.append("## What passed")
    lines.append("")
    for room, name, status, detail in results:
        if status == "PASS":
            lines.append("- %s — %s" % (room, name))
    lines.append("")
    lines.append("## What failed")
    lines.append("")
    if fails:
        for room, name, status, detail in fails:
            lines.append("- %s — %s (%s)" % (room, name, detail))
    else:
        lines.append("Nothing — all checks passed.")
    lines.append("")
    lines.append("## Known archive gaps (not backend bugs)")
    lines.append("")
    lines.append("- Room backgrounds never captured by Wayback, so the chat "
                 "pane falls back to a plain background for: blue, hard, "
                 "jive, paradise, soul (`images/bg/*_bg.jpg` 404). Room art "
                 "images all exist.")
    lines.append("- `jakies_jokeland_sm.gif` (JokeLand thumbnail) never "
                 "captured — JokeLand pane shows no art image.")
    lines.append("- `lobby2.cfm` (member entry) was never archived; the "
                 "backend serves a new member-entry page at that URL instead.")
    lines.append("- Themed-room `.cfm` pages (blue.cfm etc.) open a "
                 "`login.cfm` popup that was never archived; the backend "
                 "serves a member-login page at `/login.cfm` so the popup "
                 "works instead of 404ing.")
    lines.append("- Anything Goes keeps its 18+ certify gate: GET "
                 "`/anything-goes` without a session redirects to the "
                 "archived gate page; the certify POST is the entry.")
    lines.append("")
    lines.append("## What remains")
    lines.append("")
    lines.append("- Host DECIDED 2026-11-07: Render free tier (render.yaml at "
                 "the repo root; start: `python backend/server.py "
                 "--host 0.0.0.0`, port from $PORT, default 8124). Nothing "
                 "is deployed yet — deploy is the parent lane's step; "
                 "locally the server still binds 127.0.0.1 by default. "
                 "Domain: free Render subdomain to start "
                 "(clubgabbay.onrender.com); a real domain later only if "
                 "the proof of concept earns it.")
    lines.append("- Moderation: automated word filter live on public "
                 "messages (backend/blocklist.txt, private, never served; "
                 "3 strikes -> banned from public posting). Whispers are "
                 "never monitored or filtered, in any room (Paul, "
                 "2026-11-07). Report endpoint exists (`POST "
                 "`/api/<room>/report`, stored in SQLite `reports` table); "
                 "Mira reviews the report queue.")
    lines.append("- Landing page carries the approved blurb above Enter "
                 "(plus the monitoring / 18+ / private-whisper notes) on "
                 "all three homepage variants.")
    lines.append("- 2026-11-09 (Paul): Enter ClubGabbay on the landing page "
                 "now links straight to /chat.htm; /main.htm, /welcome.htm, "
                 "/menu.cfm and /webdates.cfm are removed from the live "
                 "site; the email line and WebDates block are off the "
                 "landing page. The landing page is now just a link to "
                 "the chat. (Also 2026-11-09: the dead LinkExchange banner "
                 "at the top of the landing page is gone — the ad server "
                 "is long dead and it rendered as a broken-image box.)")
    lines.append("- 2026-11-09 (Paul): the bulletin board is postable — "
                 "anyone can add a message (To / From / Subject / Message); "
                 "new posts render above the frozen 1997 archive and stay "
                 "up (SQLite `board_posts`, no cap; same word filter and "
                 "3-strike ban as public chat; no Host/IP shown on new "
                 "posts). Caveat: the free tier's disk is ephemeral, so a "
                 "restart or redeploy resets board posts, same as chat "
                 "history — true permanence needs persistent disk.")
    lines.append("- Member accounts are not provisioned (v1 accepts any "
                 "password on `/lobby2.cfm` and flags the session as a "
                 "member). Real member auth is a later decision.")
    lines.append("- The 29 unarchived absolute URLs from step 3 (webdates "
                 "images, queue CGI, club store, etc.) are unchanged — "
                 "still unarchived targets, not backend issues.")
    lines.append("- Browser-level visual check (1996 look pixel-for-pixel) "
                 "was not done in this VM-only run — needs a human or a "
                 "browser lane to eyeball the pane against the archived pages.")
    with open(REPORT, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("report written to", REPORT)


if __name__ == "__main__":
    sys.exit(main())
