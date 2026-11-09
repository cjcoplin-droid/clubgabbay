#!/usr/bin/env python3
"""
Club Gabbay mirror — chat backend (step 4 of mirror-build-spec.md).

Stdlib-only Python server. Serves the archived site/ tree as-is and
implements the 11 chat rooms (Lobby + 10 themed) as paths /lobby, /blue,
... /anything-goes, /jokeland, with the original 1996 entry flow:

  POST /<room>  with USER (max 12 chars), SAYS (join announcement),
                 HISTORY (default 8, how many previous messages to see)

Live updates are plain HTTP short polling (the 90s original effectively
polled via refresh; no WebSocket dependency, so this runs on any host).

Features: guest auto-names (GuestNNNN), member entry path (/lobby2.cfm),
per-room history capped at 200 in SQLite, presence, whispers, rate
limit ~1 msg / 2s per user, 18+ certify gate on Anything Goes, multi-room
jumping, message reporting (mod queue hook), automated word filter on
PUBLIC messages only (whispers are never monitored or filtered).

The archived pages are served untouched, except the bulletin board,
which is server-rendered so people can post: the 1997 archive stays
frozen in site/ and new posts (SQLite, same word filter as public
chat) render above it. Only the chat pane, the board, and the
member-login pages are new code.

Run:  python3 server.py [--port 8124] [--host 127.0.0.1]
        [--db chat.db] [--site ../site]
     On Render: python3 server.py --host 0.0.0.0  (port from $PORT,
        default 8124 when unset)
"""
import argparse
import datetime
import html
import json
import mimetypes
import os
import random
import re
import sqlite3
import sys
import threading
import time
import urllib.request
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

# ---------------------------------------------------------------- rooms
# bg / art paths are root-relative URLs as the archived pages use them
# (/images/... resolves through the static file resolver to
# clubgabbay.com/images/...). bg=None means the archived background was
# never captured (known archive gap — see backend-test-report.md).
ROOMS = {
    "lobby": {
        "name": "The Lobby", "bg": "/images/bg/lobby_bg.jpg",
        "art": "/images/lobby.jpg",
        "desc": "Any concern that the interior couldn't live up to expectations "
                "fade away as you enter the sprawling foyer. This place is classy "
                "and cool, from its oak-lined walls and vaulted ceiling to the "
                "overstuffed furniture and tasteful floral displays. Complimentary "
                "cocktails await to the left, and behind them a delicious "
                "assortment of appetizers.",
        "entry": "/www2.clubgabbay.com/lobby.cfm",
        "join": "Joins The Lobby...",
    },
    "blue": {
        "name": "Blue Notes", "bg": "/images/bg/blue_bg.jpg",
        "art": "/images/blue.jpg",
        "desc": "Are you bluer than blue? Got nothin' to do? See you in the "
                "Blue Notes room!!!",
        "entry": "/www.clubgabbay.com/htmls/blue.html",
        "join": "Joins Blue Notes...",
    },
    "speakeasy": {
        "name": "Speak Easy", "bg": "/images/bg/speak_bg.jpg",
        "art": "/images/speakeasy.jpg",
        "desc": "Bird lives!!! He's puttin' on the ritz, don't get too "
                "excited... Speak Easy in the jazz room.",
        "entry": "/www.clubgabbay.com/htmls/speakeasy.html",
        "join": "Joins The Speak Easy...",
    },
    "denim": {
        "name": "Denim & Dialog", "bg": "/images/bg/denim_bg.jpg",
        "art": "/images/denim.jpg",
        "desc": "What do country and chat have in common? Just a bunch of kind "
                "folks gettin together in the Denim & Dialog room!!!",
        "entry": "/www.clubgabbay.com/htmls/denim.html",
        "join": "Joins Denim & Dialog...",
    },
    "hard": {
        "name": "Hard Rock Gabbay", "bg": "/images/bg/hard_bg.jpg",
        "art": "/images/rock.jpg",
        "desc": "Rock till you drop!!! What else is there to say about the "
                "Hard Rock Gabbay!!!",
        "entry": "/www.clubgabbay.com/htmls/hard.html",
        "join": "Joins Hard Rock Gabbay...",
    },
    "soul": {
        "name": "Soul Searching", "bg": "/images/bg/soulsearch_bg.jpg",
        "art": "/images/soul_searching.jpg",
        "desc": "I'm so tired of being alone, so tired of being alone!!! Find "
                "someone to hold in the Soul Searching room!!!",
        "entry": "/www.clubgabbay.com/htmls/soul.html",
        "join": "Joins Soul Searching...",
    },
    "jive": {
        "name": "Jive Talkin'", "bg": "/images/bg/jive_bg.jpg",
        "art": "/images/jive_talkin.jpg",
        "desc": "Dance, dance, dance, chat!!! You can do all that and more, "
                "in the Jive Talkin' room!!!",
        "entry": "/www.clubgabbay.com/htmls/jive.html",
        "join": "Joins Jive Talkin'...",
    },
    "classical": {
        "name": "Classical Comment", "bg": "/images/bg/classical_bg.jpg",
        "art": "/images/classical.jpg",
        "desc": "What's that you say, \"too many notes for the royal ear to "
                "hear???\" That sounds like a Classical Comment to me!!!",
        "entry": "/www.clubgabbay.com/htmls/classical.html",
        "join": "Joins Classical Comment...",
    },
    "paradise": {
        "name": "Paradise Patio", "bg": "/images/bg/paradise_bg.jpg",
        "art": "/images/paradise.jpg",
        "desc": "Join us for happy hour on the patio everyday. Come hear our "
                "reggae band, drinks are always on the house. Bring all the "
                "love you got to the Paradise Patio. See you there, mon!",
        "entry": "/www.clubgabbay.com/htmls/paradise.html",
        "join": "Joins Paradise Patio...",
    },
    "anything-goes": {
        "name": "Anything Goes", "bg": None, "bgcolor": "black",
        "textcolor": "white", "art": "/anything_goes.jpg",
        "desc": "WARNING THIS ROOM MAY CONTAIN LANGUAGE AND ADULT MATERIAL "
                "NOT SUITABLE FOR MINORS. TO ENTER THIS ROOM YOU MUST BE AT "
                "LEAST 18. ENTER AT YOUR OWN RISK...AND REMEMBER ANYTHING GOES!",
        "entry": "/www2.clubgabbay.com/anything_goes.cfm",
        "join": "Joins Anything Goes...",
    },
    "jokeland": {
        "name": "Jackie's JokeLand", "bg": None, "bgcolor": "lightyellow",
        "art": None,
        "desc": "Are you good for a joke and a light of your smoke? Show off "
                "your comedy prowers in the Jackie's JokeLand Chat Room.",
        "entry": "/www2.clubgabbay.com/jokeland.cfm",
        "join": "Joins Jackie's JokeLand...",
    },
    # GeoCities neighborhood chat rooms (Paul, 2026-11-09): every
    # neighborhood had its own chat room, entered from its main page
    # (e.g. geocities.com/chat/Entry/Silicon.html). Same engine as the
    # Gabbay rooms: live poll, handles, whispers, same word filter +
    # strikes. Art is the neighborhood's own 88x31 button (Chaz Boston
    # Baden, freely given away; via Blade's Place). Backgrounds are the
    # originals, checked on the Wayback Machine Dec 1996: Hollywood,
    # SiliconValley, SunsetStrip and WestHollywood all used GeoCities'
    # shared background.gif; Area51 had its own area_glow.gif on a black
    # page with white text and red links (Paul, 2026-11-09: the Gabbay
    # home background -- the Hollywood sign -- was wrong on Area51).
    "hollywood-chat": {
        "name": "Hollywood Chat",
        "bg": "/images/neighborhoods/background.gif", "bgcolor": "white",
        "art": "/images/neighborhoods/hollywood.gif",
        "desc": "Lights, camera, chat!!! Talk movies, TV and stars with "
                "your fellow Hollywood homesteaders!!!",
        "entry": "/neighborhoods/chat/hollywood.html",
        "join": "Joins The Hollywood Chat...",
    },
    "siliconvalley-chat": {
        "name": "SiliconValley Chat",
        "bg": "/images/neighborhoods/background.gif", "bgcolor": "white",
        "art": "/images/neighborhoods/siliconvalley.gif",
        "desc": "Log on and talk tech!!! Hardware, software, programming -- "
                "the SiliconValley homesteaders are online!!!",
        "entry": "/neighborhoods/chat/siliconvalley.html",
        "join": "Joins The SiliconValley Chat...",
    },
    "sunsetstrip-chat": {
        "name": "SunsetStrip Chat",
        "bg": "/images/neighborhoods/background.gif", "bgcolor": "white",
        "art": "/images/neighborhoods/sunsetstrip.gif",
        "desc": "Turn it up!!! Talk rock, grunge, punk and the club scene "
                "with your SunsetStrip neighbors!!!",
        "entry": "/neighborhoods/chat/sunsetstrip.html",
        "join": "Joins The SunsetStrip Chat...",
    },
    "area51-chat": {
        "name": "Area51 Chat",
        "bg": "/images/neighborhoods/area_glow.gif", "bgcolor": "black",
        "textcolor": "white", "link": "red", "vlink": "#9932CC",
        "art": "/images/neighborhoods/area51.gif",
        "desc": "The truth is in here!!! Talk sci-fi, fantasy and conspiracy "
                "theories with your fellow Area51 homesteaders!!!",
        "entry": "/neighborhoods/chat/area51.html",
        "join": "Joins The Area51 Chat...",
    },
    "westhollywood-chat": {
        "name": "WestHollywood Chat",
        "bg": "/images/neighborhoods/background.gif", "bgcolor": "white",
        "art": "/images/neighborhoods/westhollywood.gif",
        "desc": "Come as you are!!! Talk life, love and community with your "
                "WestHollywood neighbors!!!",
        "entry": "/neighborhoods/chat/westhollywood.html",
        "join": "Joins The WestHollywood Chat...",
    },
    # AOL-style chat (Paul, 2026-11-09): a landing page with a chat box
    # that looks like AOL -- click a name in the member list to PM them,
    # otherwise just read along. Same engine as every other room (live
    # poll, handles, whispers, same word filter + strikes); only the
    # skin is different (render_aol_room_page, AOL 4.0 chat-room look).
    "aol": {
        "name": "AOL Chat",
        "aol": True,
        "bg": None, "bgcolor": "#C0C0C0",
        "art": None,
        "desc": "You've got chat!!! Talk with your old AOL neighbors -- "
                "click a name on the right to send them a private message.",
        "entry": "/aol.html",
        "join": "Joins AOL Chat...",
    },
}
# The archived Anything Goes form posts to /anything-goes; accept the
# underscore spelling too.
ALIASES = {"anything_goes": "anything-goes"}

HOST_DIRS = ["www2.clubgabbay.com", "www.clubgabbay.com", "clubgabbay.com",
             "chat.clubgabbay.com", "members.clubgabbay.com"]
HISTORY_CAP = 200          # messages kept per room in SQLite
BOARD_MAX_NAME = 30        # board post fields
BOARD_MAX_SUBJECT = 100
BOARD_MAX_MSG = 1000
BOARD_RATE_LIMIT_SECS = 10.0  # one board post per 10s per IP
PRESENCE_TIMEOUT = 120     # seconds without a poll/post before you drop off
RATE_LIMIT_SECS = 2.0      # ~1 message per 2s per user
MAX_NAME = 12
MAX_MSG = 500

SITE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat.db")

# ---------------------------------------------------------------- storage
db_lock = threading.Lock()
db = None


def db_init(path):
    global db
    db = sqlite3.connect(path, check_same_thread=False)
    with db_lock:
        db.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT NOT NULL, user TEXT NOT NULL, kind TEXT NOT NULL,
            text TEXT NOT NULL, to_user TEXT, ts REAL NOT NULL)""")
        db.execute("""CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT NOT NULL, msg_id INTEGER NOT NULL,
            reporter TEXT NOT NULL, reason TEXT NOT NULL, ts REAL NOT NULL)""")
        # word-filter strikes: 3 blocked public messages -> banned from
        # public posting (whispers are never filtered or banned).
        db.execute("""CREATE TABLE IF NOT EXISTS strikes (
            user TEXT PRIMARY KEY, strikes INTEGER NOT NULL DEFAULT 0,
            banned INTEGER NOT NULL DEFAULT 0, updated REAL NOT NULL)""")
        # Message board posts (Paul, 2026-11-09): the 1997 archive is
        # frozen in site/; new posts live here. NO cap — a board message
        # stays up. Same word filter + strikes as public chat.
        # board column (Paul, 2026-11-09, neighborhoods): 'clubgabbay'
        # for the main board, a neighborhood slug for the five portals.
        db.execute("""CREATE TABLE IF NOT EXISTS board_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board TEXT NOT NULL DEFAULT 'clubgabbay',
            name TEXT NOT NULL, to_name TEXT, subject TEXT,
            message TEXT NOT NULL, ts REAL NOT NULL)""")
        try:
            # existing DBs predate the board column
            db.execute("ALTER TABLE board_posts ADD COLUMN board TEXT "
                       "NOT NULL DEFAULT 'clubgabbay'")
        except sqlite3.OperationalError:
            pass  # column already there
        db.execute("CREATE INDEX IF NOT EXISTS idx_msg_room ON messages(room, id)")
        db.commit()


def db_add_message(room, user, kind, text, to_user=None):
    with db_lock:
        cur = db.execute(
            "INSERT INTO messages (room, user, kind, text, to_user, ts)"
            " VALUES (?,?,?,?,?,?)",
            (room, user, kind, text, to_user, time.time()))
        mid = cur.lastrowid
        # cap history at HISTORY_CAP per room
        db.execute(
            "DELETE FROM messages WHERE room=? AND id NOT IN "
            "(SELECT id FROM messages WHERE room=? ORDER BY id DESC LIMIT ?)",
            (room, room, HISTORY_CAP))
        db.commit()
    return mid


def db_messages(room, limit, since_id=0, user=None):
    """Last `limit` messages (or all with id > since_id), newest last.
    Whispers are visible only to sender/recipient."""
    with db_lock:
        if since_id:
            rows = db.execute(
                "SELECT id, user, kind, text, to_user, ts FROM messages"
                " WHERE room=? AND id>? ORDER BY id ASC LIMIT 200",
                (room, since_id)).fetchall()
        else:
            rows = db.execute(
                "SELECT id, user, kind, text, to_user, ts FROM messages"
                " WHERE room=? ORDER BY id DESC LIMIT ?",
                (room, limit)).fetchall()
            rows.reverse()
    out = []
    for mid, muser, kind, text, to_user, ts in rows:
        if kind == "whisper" and user not in (muser, to_user):
            continue
        out.append({"id": mid, "user": muser, "kind": kind, "text": text,
                    "to": to_user, "ts": ts,
                    "time": time.strftime("%H:%M", time.localtime(ts))})
    return out


def db_last_id(room):
    with db_lock:
        row = db.execute("SELECT MAX(id) FROM messages WHERE room=?",
                         (room,)).fetchone()
    return row[0] or 0


def db_add_board_post(name, to_name, subject, message, board="clubgabbay"):
    """Store a board post. No cap: board messages stay up."""
    with db_lock:
        cur = db.execute(
            "INSERT INTO board_posts (board, name, to_name, subject, message, ts)"
            " VALUES (?,?,?,?,?,?)",
            (board, name, to_name, subject, message, time.time()))
        db.commit()
    return cur.lastrowid


def db_board_posts(limit=200, board=None):
    """Board posts, newest first. board=None returns every board (the
    backup job reads that); a board slug returns just that board."""
    with db_lock:
        if board is None:
            rows = db.execute(
                "SELECT id, board, name, to_name, subject, message, ts FROM board_posts"
                " ORDER BY id DESC LIMIT ?",
                (limit,)).fetchall()
        else:
            rows = db.execute(
                "SELECT id, board, name, to_name, subject, message, ts FROM board_posts"
                " WHERE board=? ORDER BY id DESC LIMIT ?",
                (board, limit)).fetchall()
    return [{"id": r[0], "board": r[1], "name": r[2], "to": r[3],
             "subject": r[4], "message": r[5], "ts": r[6]} for r in rows]


def restore_board_posts(url=None):
    """Re-seed board_posts from the backup file when the local board is
    empty. The free host's disk is ephemeral: every restart/deploy wipes
    chat.db, board posts included (Paul lost a post this way, 2026-11-09).
    Posts are backed up to the repo (site-data/board-posts.json — GitHub
    is the store) by an external job; on boot, an empty board is re-seeded
    from that file. Gated on BOARD_RESTORE_URL so tests and local runs
    (env var unset) never touch the network. Returns the number of posts
    restored. Never raises — a failed restore must never block startup."""
    if url is None:
        url = os.environ.get("BOARD_RESTORE_URL", "")
    if not url:
        return 0
    try:
        with db_lock:
            n = db.execute("SELECT COUNT(*) FROM board_posts").fetchone()[0]
        if n:
            return 0
        req = urllib.request.Request(
            url, headers={"User-Agent": "ClubGabbay/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
        posts = data.get("posts", data) if isinstance(data, dict) else data
        restored = 0
        with db_lock:
            for p in posts:
                try:
                    db.execute(
                        "INSERT OR IGNORE INTO board_posts"
                        " (id, board, name, to_name, subject, message, ts)"
                        " VALUES (?,?,?,?,?,?,?)",
                        (p["id"], p.get("board", "clubgabbay"), p["name"],
                         p.get("to"), p.get("subject"),
                         p["message"], p["ts"]))
                    restored += 1
                except (KeyError, TypeError):
                    continue
            db.commit()
        return restored
    except Exception as e:  # noqa: BLE001 - restore must never block startup
        sys.stderr.write("board restore failed: %s\n" % e)
        return 0


# ---------------------------------------------------------------- sessions
sessions = {}   # sid -> dict(user, room, member, history, certified, last_seen, last_msg)
sessions_lock = threading.Lock()


def new_sid():
    import secrets
    return secrets.token_hex(16)


def get_session(handler):
    cookie = SimpleCookie(handler.headers.get("Cookie") or "")
    morsel = cookie.get("gabbay_sid")
    if not morsel:
        return None, None
    sid = morsel.value
    with sessions_lock:
        sess = sessions.get(sid)
    return sid, sess


def touch(sess):
    sess["last_seen"] = time.time()


def presence(room):
    now = time.time()
    with sessions_lock:
        names = []
        for s in sessions.values():
            if s["room"] == room and now - s["last_seen"] < PRESENCE_TIMEOUT:
                label = s["user"] + (" (member)" if s.get("member") else "")
                names.append(label)
    return sorted(set(names))


def guest_name(room):
    with sessions_lock:
        taken = {s["user"] for s in sessions.values() if s["room"] == room}
    for _ in range(50):
        name = "Guest%d" % random.randint(1000, 9999)
        if name not in taken:
            return name
    return "Guest%d" % random.randint(10000, 99999)


def strip_tags(s):
    return re.sub(r"<[^>]*>", "", s or "")


# ---------------------------------------------------------------- word filter
# Automated moderation for PUBLIC room messages only. Whispers are never
# monitored or filtered (Paul, 2026-11-07) — they bypass this entirely,
# and a ban only blocks public posting. blocklist.txt is private: it
# lives under backend/, the static resolver only serves site/, and it is
# never rendered in any page.
BLOCKLIST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "blocklist.txt")
BLOCK_STRIKES = 3            # strikes -> banned from public posting
_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s",
                       "7": "t", "@": "a", "$": "s", "!": "i"})
# Words that appear inside innocent words (class, peacock, analysis,
# cucumber, raccoon, spice) are matched as whole tokens only, never as
# substrings — otherwise "I love my class" would be blocked.
TOKEN_ONLY = {"ass", "fag", "dick", "cock", "cum", "anal", "spic", "coon"}
_block_sub = set()     # normalised entries, substring-matched
_block_tok = set()     # normalised entries, whole-token matched
_block_phrase = set()  # normalised multi-word entries ("click here")


def _normalize(s):
    """Lowercase, map leet digits to letters, strip all non-letters."""
    return re.sub(r"[^a-z]+", "", s.lower().translate(_LEET))


def load_blocklist(path=BLOCKLIST_PATH):
    global _block_sub, _block_tok, _block_phrase
    sub, tok, phrase = set(), set(), set()
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                w = line.strip().lower()
                if not w or w.startswith("#"):
                    continue
                n = _normalize(w)
                if not n:
                    continue
                if " " in w:
                    # a phrase ("click here"): its words legitimately
                    # span a space, so it is never a boundary false
                    # positive -- substring-match it as-is
                    phrase.add(n)
                    sub.add(n)
                elif n in TOKEN_ONLY or len(n) < 4:
                    tok.add(n)
                else:
                    sub.add(n)
    except OSError:
        pass
    _block_sub, _block_tok, _block_phrase = sub, tok, phrase


load_blocklist()


def _sub_spans_words(low_leet, w):
    """True if the leftmost occurrence of w in low_leet (letters may be
    separated by non-letters) spans two whole words -- the first and
    last letter-runs inside the match are each at least two letters.
    An innocent phrase like "who remembers" squashes to "whoremembers"
    and would otherwise trip "whore" (Paul, 2026-11-09: two strikes on
    his own handle from a handles-board test post). Spaced-out single
    letters ("f u c k") are still caught: their runs are one letter."""
    pat = "[^a-z]*".join(re.escape(ch) for ch in w)
    m = re.search(pat, low_leet)
    if not m:
        return False
    runs = re.findall(r"[a-z]+", m.group(0))
    return len(runs) >= 2 and len(runs[0]) >= 2 and len(runs[-1]) >= 2


def text_blocked(text):
    """Return the matched blocklist entry, or None. Public messages only."""
    if not text:
        return None
    low = text.lower()
    # link abuse: raw URLs in a public message
    if "http://" in low or "https://" in low or "www." in low:
        return "link"
    squashed = _normalize(text)
    low_leet = text.lower().translate(_LEET)
    for w in _block_sub:
        if w not in squashed:
            continue
        if w in _block_phrase:
            return w
        # A substring hit that spans two whole words in the original is
        # an innocent phrase, not the blocked word -- skip it.
        if _sub_spans_words(low_leet, w):
            continue
        return w
    for tok in re.split(r"[^a-z]+", low.translate(_LEET)):
        if tok and tok in _block_tok:
            return tok
    return None


def strike_status(user):
    """(strikes, banned) for a user name."""
    with db_lock:
        row = db.execute("SELECT strikes, banned FROM strikes WHERE user=?",
                         (user,)).fetchone()
    if not row:
        return 0, False
    return row[0], bool(row[1])


def record_strike(user):
    """Record one blocked public message. Returns (strikes, banned)."""
    with db_lock:
        row = db.execute("SELECT strikes FROM strikes WHERE user=?",
                         (user,)).fetchone()
        strikes = (row[0] if row else 0) + 1
        banned = 1 if strikes >= BLOCK_STRIKES else 0
        db.execute("INSERT OR REPLACE INTO strikes"
                   " (user, strikes, banned, updated) VALUES (?,?,?,?)",
                   (user, strikes, banned, time.time()))
        db.commit()
    return strikes, bool(banned)


# ---------------------------------------------------------------- static
def resolve_static(path):
    """Map a URL path onto a file inside site/. Returns abspath or None.
    First segment may be a host dir (e.g. /clubgabbay.com/images/...);
    otherwise try each host dir in priority order (www2 first — the
    main site). Directory -> its index.html."""
    path = unquote(path)
    if not path or path == "/":
        path = "/index.html"
    rel = path.lstrip("/")
    if ".." in rel.split("/"):
        return None
    candidates = []
    first = rel.split("/")[0]
    if first in HOST_DIRS:
        candidates.append(os.path.join(SITE_ROOT, rel))
    else:
        for host in HOST_DIRS:
            candidates.append(os.path.join(SITE_ROOT, host, rel))
    for cand in candidates:
        if os.path.isdir(cand):
            idx = os.path.join(cand, "index.html")
            if os.path.isfile(idx):
                return idx
        elif os.path.isfile(cand):
            return cand
    return None


def static_exists(urlpath):
    return resolve_static(urlpath) is not None


def content_type(path):
    if path.endswith(".cfm") or path.endswith(".cgi"):
        return "text/html; charset=iso-8859-1"
    ctype, _ = mimetypes.guess_type(path)
    return ctype or "application/octet-stream"


# ---------------------------------------------------------------- HTML
def esc(s):
    return html.escape(s or "", quote=True)


def room_jump_links(current):
    links = []
    for slug, info in ROOMS.items():
        if slug == current:
            links.append("<b>%s</b>" % esc(info["name"]))
        else:
            links.append('<a href="/%s?jump=1">%s</a>'
                         % (slug, esc(info["name"])))
    return " | ".join(links)


def render_msg(m):
    """One message as an HTML line (user content always escaped)."""
    if m["kind"] == "join":
        return ('<b>%s %s</b><br>' % (esc(m["user"]), esc(m["text"])))
    if m["kind"] == "leave":
        return ('<i><b>%s</b> %s</i><br>' % (esc(m["user"]), esc(m["text"])))
    if m["kind"] == "whisper":
        return ('<i><font color="#800080"><b>%s</b> whispers to '
                '<b>%s</b>: %s</font></i><br>'
                % (esc(m["user"]), esc(m["to"]), esc(m["text"])))
    return ('<b>%s:</b> %s<br>' % (esc(m["user"]), esc(m["text"])))


def render_room_page(slug, sess, initial_msgs):
    info = ROOMS[slug]
    bg_attr = ""
    if info.get("bg") and static_exists(info["bg"]):
        bg_attr = ' background="%s"' % info["bg"]
    body_attrs = bg_attr
    if info.get("bgcolor"):
        body_attrs += ' bgcolor="%s"' % info["bgcolor"]
    if info.get("textcolor"):
        body_attrs += ' text="%s"' % info["textcolor"]
    if info.get("link"):
        body_attrs += ' link="%s"' % info["link"]
    if info.get("vlink"):
        body_attrs += ' vlink="%s"' % info["vlink"]
    art = ""
    if info.get("art") and static_exists(info["art"]):
        art = '<center><img src="%s"></center><p>' % info["art"]
    history_opts = "".join(
        '<option value="%d"%s>%d</option>' % (n, " selected" if n == sess["history"] else "", n)
        for n in (8, 16, 32))
    users = presence(slug)
    user_opts = "".join('<option>%s</option>' % esc(u.split(" (member)")[0])
                        for u in users if u.split(" (member)")[0] != sess["user"])
    lines = "".join(render_msg(m) for m in initial_msgs)
    last_id = initial_msgs[-1]["id"] if initial_msgs else 0
    return """<html><head><title>ClubGabbay: %s</title></head>
<body%s>
<center><h2>ClubGabbay: %s</h2></center>
%s
<blockquote>%s</blockquote>
<center>
<font size="-1">Jump to another room:<br>%s</font>
</center>
<hr noshade>
<p><b>Who's here:</b> <span id="presence">%s</span></p>
<div id="chat">%s</div>
<hr noshade>
<form action="/%s/post" method="post">
<input type="text" name="text" size="60" maxlength="500">
<input type="submit" value="Say It!">
</form>
<form action="/%s/whisper" method="post">
Whisper to <select name="to">%s</select>
<input type="text" name="text" size="40" maxlength="500">
<input type="submit" value="Whisper">
</form>
<form action="/%s/history" method="post">
Show last
<select name="HISTORY">%s</select> messages
<input type="submit" value="Change">
</form>
<p><font size="-1">
<a href="/%s/leave">Leave %s</a> |
<a href="/chat.htm">Chat Directory</a> |
<a href="#" onclick="location.reload(); return false;">Refresh</a>
</font></p>
<p><font size="-1">You are chatting as <b>%s</b>%s.
Messages refresh automatically every few seconds.</font></p>
<hr noshade>
Club Gabbay -- a fan-run homage to the 1996-1999 original.
<script>
var lastId = %d;
var room = "%s";
function escHtml(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function lineHtml(m){
  if(m.kind==='join') return '<b>'+escHtml(m.user)+' '+escHtml(m.text)+'</b><br>';
  if(m.kind==='leave') return '<i><b>'+escHtml(m.user)+'</b> '+escHtml(m.text)+'</i><br>';
  if(m.kind==='whisper') return '<i><font color="#800080"><b>'+escHtml(m.user)+'</b> whispers to <b>'+escHtml(m.to)+'</b>: '+escHtml(m.text)+'</font></i><br>';
  return '<b>'+escHtml(m.user)+':</b> '+escHtml(m.text)+'<br>';
}
function poll(){
  fetch('/api/'+room+'/messages?since='+lastId, {credentials:'same-origin'})
    .then(function(r){return r.json();})
    .then(function(data){
      var chat=document.getElementById('chat');
      var added=0;
      data.messages.forEach(function(m){
        chat.innerHTML += lineHtml(m);
        if(m.id>lastId) lastId=m.id;
        added++;
      });
      document.getElementById('presence').textContent =
        data.presence.length ? data.presence.join(', ') : '(just you)';
      // Only follow new messages when the reader is already near the
      // bottom. Never yank the page while someone is typing or reading
      // back — the old unconditional scroll dropped the keyboard on
      // phones every 4 seconds (Paul, 2026-11-09).
      if(added>0){
        var nearBottom = (window.innerHeight + window.scrollY) >= (document.body.scrollHeight - 120);
        if(nearBottom) window.scrollTo(0, document.body.scrollHeight);
      }
    })
    .catch(function(){});
}
setInterval(poll, 4000);
</script>
</body></html>
""" % (esc(info["name"]), body_attrs, esc(info["name"]), art,
       esc(info["desc"]), room_jump_links(slug),
       esc(", ".join(users) if users else "(just you)"), lines,
       slug, slug, user_opts, slug, history_opts,
       slug, esc(info["name"]),
       esc(sess["user"]), " (member)" if sess.get("member") else "",
       last_id, slug)


def render_aol_room_page(slug, sess, initial_msgs):
    """AOL Chat (Paul, 2026-11-09): the same room engine in an AOL 4.0
    chat-room skin -- blue title bar, chat on the left, member list on
    the right, click a name to open a private-message box to them. The
    poll, the filter and the whisper delivery are the shared ones."""
    info = ROOMS[slug]
    history_opts = "".join(
        '<option value="%d"%s>%d</option>' % (n, " selected" if n == sess["history"] else "", n)
        for n in (8, 16, 32))
    users = presence(slug)
    me = sess["user"]
    members = "".join(
        '<a href="#" onclick="return pmUser(this.textContent);">%s</a><br>'
        % esc(u.split(" (member)")[0])
        for u in users if u.split(" (member)")[0] != me)
    lines = "".join(render_msg(m) for m in initial_msgs)
    last_id = initial_msgs[-1]["id"] if initial_msgs else 0
    return """<html><head><title>AOL Chat</title></head>
<body bgcolor="#C0C0C0" text="black" link="blue" vlink="purple">
<center>
<table width="640" border="2" cellpadding="0" cellspacing="0" bgcolor="#D4D0C8">
<tr><td bgcolor="#000080"><font color="white"><b>&nbsp;AOL Chat</b></font></td>
<td bgcolor="#000080" align="right"><font color="white"><b>X&nbsp;</b></font></td></tr>
<tr><td colspan="2">
<table width="620" cellpadding="4" cellspacing="0"><tr>
<td width="460" valign="top" bgcolor="white">
<div id="chat" style="height:300px;overflow:auto;background:white;">%s</div>
</td>
<td width="150" valign="top" bgcolor="#D4D0C8">
<b>People in this room:</b><br>
<div id="members">%s</div>
</td>
</tr></table>
</td></tr>
<tr><td colspan="2">
<form action="/%s/post" method="post">
<input type="text" name="text" size="50" maxlength="500">
<input type="submit" value="Send">
</form>
</td></tr>
<tr><td colspan="2">
<div id="imbox" style="display:none;">
<table width="620" border="1" cellpadding="2" cellspacing="0" bgcolor="#D4D0C8">
<tr><td bgcolor="#000080"><font color="white"><b>Instant Message to <span id="im-to-name"></span></b></font></td>
<td bgcolor="#000080" align="right"><a href="#" onclick="return closeIm();"><font color="white">X</font></a></td></tr>
<tr><td colspan="2">
<form action="/%s/whisper" method="post">
<input type="hidden" name="to" id="im-to" value="">
<input type="text" name="text" id="im-text" size="45" maxlength="500">
<input type="submit" value="Send">
</form>
</td></tr>
</table>
</div>
</td></tr>
<tr><td colspan="2">
<form action="/%s/history" method="post">
Show last
<select name="HISTORY">%s</select> messages
<input type="submit" value="Change">
</form>
<p><font size="-1">
<a href="/%s/leave">Leave %s</a> |
<a href="/aol-handles/board/">Old AOL handles board</a> |
<a href="#" onclick="location.reload(); return false;">Refresh</a>
</font></p>
<p><font size="-1">You are chatting as <b>%s</b>%s.
Messages refresh automatically every few seconds.
Click a name on the right to send them a private message.</font></p>
<hr noshade>
AOL Chat -- a fan-made tribute to the 1990s.
</td></tr>
</table>
</center>
<script>
var lastId = %d;
var room = "%s";
var me = "%s";
function escHtml(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function lineHtml(m){
  if(m.kind==='join') return '<b>'+escHtml(m.user)+' '+escHtml(m.text)+'</b><br>';
  if(m.kind==='leave') return '<i><b>'+escHtml(m.user)+'</b> '+escHtml(m.text)+'</i><br>';
  if(m.kind==='whisper') return '<i><font color="#800080"><b>'+escHtml(m.user)+'</b> whispers to <b>'+escHtml(m.to)+'</b>: '+escHtml(m.text)+'</font></i><br>';
  return '<b>'+escHtml(m.user)+':</b> '+escHtml(m.text)+'<br>';
}
function membersHtml(list){
  var others = list.map(function(u){return u.split(' (member)')[0];})
    .filter(function(u){return u !== me;});
  if(!others.length) return '(just you)';
  return others.map(function(u){
    return '<a href="#" onclick="return pmUser(this.textContent);">'+escHtml(u)+'</a>';
  }).join('<br>');
}
function pmUser(name){
  document.getElementById('im-to').value = name;
  document.getElementById('im-to-name').textContent = name;
  document.getElementById('imbox').style.display = 'block';
  document.getElementById('im-text').focus();
  return false;
}
function closeIm(){
  document.getElementById('imbox').style.display = 'none';
  return false;
}
function poll(){
  fetch('/api/'+room+'/messages?since='+lastId, {credentials:'same-origin'})
    .then(function(r){return r.json();})
    .then(function(data){
      var chat=document.getElementById('chat');
      var added=0;
      data.messages.forEach(function(m){
        chat.innerHTML += lineHtml(m);
        if(m.id>lastId) lastId=m.id;
        added++;
      });
      document.getElementById('members').innerHTML = membersHtml(data.presence);
      // Only follow new messages when the reader is already near the
      // bottom of the chat box. Never yank it while someone is typing
      // or reading back (Paul, 2026-11-09).
      if(added>0){
        var nearBottom = (chat.scrollHeight - chat.scrollTop - chat.clientHeight) < 120;
        if(nearBottom) chat.scrollTop = chat.scrollHeight;
      }
    })
    .catch(function(){});
}
setInterval(poll, 4000);
</script>
</body></html>
""" % (lines, members, slug, slug, slug, history_opts,
       slug, esc(info["name"]),
       esc(sess["user"]), " (member)" if sess.get("member") else "",
       last_id, slug, esc(sess["user"]))


def render_member_page():
    """Member entry (lobby2.cfm / login.cfm) — new code, lobby look.
    v1: any password is accepted; no member accounts are provisioned yet."""
    return """<html><head><title>ClubGabbay: Members Enter</title></head>
<body background="/images/bg/lobby_bg.jpg">
<center><img src="/images/lobby.jpg"></center>
<blockquote>
Members enter here. Type your member name and password to join the Lobby
as a member. Guests, please use the Guest Entrance on the Lobby page.
</blockquote>
<center>
<form action="/lobby" method="post">
Name: <input type="text" name="USER" size="12" maxlength="12"><br>
Password: <input type="password" name="PASSWORD" size="12" maxlength="12"><br>
<input type="hidden" name="MEMBER" value="1">
<input type="hidden" name="SAYS" value="<b>Joins The Lobby...</b>">
<input type="hidden" name="HISTORY" value="8">
<input type="submit" value="Enter as Member">
</form>
</center>
<p><font size="-1">Members' preview: the themed rooms are listed on the
<a href="/chat2.htm">Chat Directory</a>. (v1 note: member accounts are not
provisioned yet — any password is accepted and you are flagged as a member
for this visit.)</font></p>
<hr noshade>
Club Gabbay -- a fan-run homage to the 1996-1999 original.
</body></html>
"""


def render_404(path):
    return """<html><head><title>ClubGabbay: Not Found</title></head>
<body background="/images/bg/lobby_bg.jpg">
<center><h2>Sorry — that page isn't in the archive.</h2></center>
<p>The page <b>%s</b> was not captured in the ClubGabbay archive
(1996–1999). Try the <a href="/">ClubGabbay homepage</a> or the
<a href="/chat.htm">Chat Directory</a>.</p>
<hr noshade>
Club Gabbay -- a fan-run homage to the 1996-1999 original.
</body></html>""" % esc(path)


# GeoCities neighborhoods revival (Paul, 2026-11-09): the top 5, each a
# fan-made portal with its own message board, same setup for all, linked
# to each other and to Club Gabbay. Slug -> display name.
NEIGHBORHOODS = {
    "hollywood": "Hollywood",
    "siliconvalley": "SiliconValley",
    "sunsetstrip": "SunsetStrip",
    "area51": "Area51",
    "westhollywood": "WestHollywood",
}


# Standalone boards (Paul, 2026-11-09): boards that are not a
# neighborhood's -- same form + posts + filter + backup as the rest.
STANDALONE_BOARDS = {
    "aol-handles": {
        "name": "Old AOL handles",
        "intro": ("Were you on AOL back in the day? Leave your old screen "
                  "name -- say what your handle was, what rooms you hung "
                  "out in, and who you remember."),
        "back": "/aol.html",
        "back_label": "Back to AOL Chat",
        "bg": "/images/neighborhoods/background.gif",
        "footer": "AOL Chat -- a fan-made tribute to the 1990s.",
    },
}


def board_url(board):
    """Public URL of a board page."""
    if board == "clubgabbay":
        return "/messages/"
    if board in STANDALONE_BOARDS:
        return "/%s/board/" % board
    return "/neighborhoods/%s/board/" % board


def board_post_url(board):
    if board == "clubgabbay":
        return "/messages/post"
    if board in STANDALONE_BOARDS:
        return "/%s/board/post" % board
    return "/neighborhoods/%s/board/post" % board


# ---------------------------------------------------------------- message board
# The 1997 bulletin board is a frozen archive file in site/; new posts live
# in SQLite (board_posts) and render ABOVE the archive, newest first, in
# the archive's own Date/To/From/Subject format — minus Host/IP, which the
# 1997 board printed and we do not. Same word filter + strikes as public
# chat (Paul, 2026-11-07); board posts are public, so they are filtered.
# Neighborhood boards (Paul, 2026-11-09) are the same form + posts with
# no archive — they are new pages, not frozen files.
_board_last_post = {}  # ip -> time of last accepted board post


def board_file():
    return os.path.join(SITE_ROOT, "www.clubgabbay.com", "messages",
                        "index.html")


def is_board_file(fpath):
    return os.path.abspath(fpath) == os.path.abspath(board_file())


def board_date(ts):
    """Archive-style date: 'Wed Jul 30 4:54 (PT)', Pacific time."""
    try:
        from zoneinfo import ZoneInfo
        dt = datetime.datetime.fromtimestamp(ts, ZoneInfo("America/Vancouver"))
    except Exception:
        dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%a %b %d %H:%M (PT)")


def render_board_post(p):
    to = ('<b>To:</b> %s<br>\n' % esc(p["to"])) if p["to"] else ""
    subj = ('<b>Subject:</b> %s<br>\n' % esc(p["subject"])) \
        if p["subject"] else ""
    return ('<b>Date:</b> %s<br>\n%s<b>From:</b> %s<br>\n%s<p>%s<p>\n<hr>\n'
            % (esc(board_date(p["ts"])), to, esc(p["name"]), subj,
               esc(p["message"])))


def render_board_page(board="clubgabbay"):
    """Club Gabbay board: archived board file + post form + new posts
    above the frozen 1997 archive. Neighborhood boards: the same form +
    posts on a fresh page (no archive), with a link back to the portal."""
    form = ('<center><b>Post a message:</b></center>\n'
            '<form action="__POST_URL__" method="post">\n'
            'To: <input type="text" name="to" size="20" maxlength="30">\n'
            'From: <input type="text" name="from" size="20" maxlength="30">'
            '<br>\n'
            'Subject: <input type="text" name="subject" size="40" '
            'maxlength="100"><br>\n'
            '<textarea name="message" rows="4" cols="60" maxlength="1000">'
            '</textarea><br>\n'
            '<input type="submit" value="Post It!">\n'
            '</form>\n<hr noshade>\n').replace("__POST_URL__",
                                                board_post_url(board))
    posts = db_board_posts(board=board)
    new_html = ""
    if posts:
        new_html = ('<center><b>— New messages —</b></center>\n'
                    + "".join(render_board_post(p) for p in posts))
    if board == "clubgabbay":
        try:
            with open(board_file(), encoding="latin-1") as fh:
                raw = fh.read()
        except OSError:
            return render_404("/messages/")
        head, sep, archive = raw.partition("<hr noshade>")
        if not sep:
            head, archive = raw, ""
        if posts:
            new_html += '<center><b>— Messages from 1997 —</b></center>\n'
        return head + sep + "\n" + form + new_html + archive + "</body></html>\n"
    if board in STANDALONE_BOARDS:
        info = STANDALONE_BOARDS[board]
        body = new_html or ('<center><i>No messages yet — be the first to '
                            'leave one.</i></center>\n')
        return ('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n<html>\n<head>\n'
                '<meta http-equiv="Content-Type" content="text/html; '
                'charset=iso-8859-1">\n'
                '<title>%s message board</title>\n</head>\n'
                '<body background="%s">\n'
                '<center><font size="+2"><strong>%s message board</strong>'
                '</font></center>\n'
                '<p><font size="+1">%s</font></p>\n'
                '%s%s'
                '<hr>\n<p><a href="%s">%s</a> | '
                '<a href="/fine-print.html">Fine print</a></p>\n'
                '<font color=gray size=2>%s</font>\n'
                '</body></html>\n'
                % (info["name"], info["bg"], info["name"], info["intro"],
                   form, body, info["back"], info["back_label"],
                   info["footer"]))
    name = NEIGHBORHOODS[board]
    body = new_html or ('<center><i>No messages yet — be the first to '
                        'leave one.</i></center>\n')
    return ('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n<html>\n<head>\n'
            '<meta http-equiv="Content-Type" content="text/html; '
            'charset=iso-8859-1">\n'
            '<title>%s message board -- Club Gabbay</title>\n</head>\n'
            '<body background="/clubgabbay.com/images/bg/home_bg.jpg">\n'
            '<center><font size="+2"><strong>%s message board</strong>'
            '</font></center>\n'
            '<p><font size="+1">Were you a %s homesteader? Leave a message '
            '-- say what your address was, who you remember, and where life '
            'took you.</font></p>\n'
            '%s%s'
            '<hr>\n<p><a href="/neighborhoods/%s.html">Back to %s</a> | '
            '<a href="/">Club Gabbay Home</a> | '
            '<a href="/fine-print.html">Fine print</a></p>\n'
            '<font color=gray size=2>Club Gabbay -- a fan-run homage to the '
            '1996-1999 original.</font>\n'
            '</body></html>\n'
            % (name, name, name, form, body, board, name))


# ---------------------------------------------------------------- handler
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "ClubGabbay/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    # -- helpers
    def _send(self, status, body, ctype="text/html; charset=utf-8",
              extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8", "replace")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _redirect(self, location, sid=None):
        extra = {}
        if sid:
            extra["Set-Cookie"] = "gabbay_sid=%s; Path=/; HttpOnly" % sid
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        for k, v in extra.items():
            self.send_header(k, v)
        self.end_headers()

    def _json(self, status, obj):
        self._send(status, json.dumps(obj), "application/json")

    def _wants_json(self):
        return ("application/json" in (self.headers.get("Accept") or "")
                or self.headers.get("X-Requested-With") == "fetch")

    def _read_form(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        return {k: v[0] for k, v in
                parse_qs(raw.decode("utf-8", "replace"),
                         keep_blank_values=True).items()}

    def _room_or_none(self, slug):
        return ROOMS.get(ALIASES.get(slug, slug))

    # -- entry (POST /<room>)
    def _handle_entry(self, slug, form):
        info = ROOMS[slug]
        user = (form.get("USER") or "").strip()[:MAX_NAME]
        # The archived guest form hardcodes Guest1251; treat it (and a
        # blank name) as "give me a fresh guest name".
        if not user or re.fullmatch(r"Guest\d+", user, re.I):
            user = guest_name(slug)
        history = 8
        try:
            history = int(form.get("HISTORY") or 8)
        except ValueError:
            pass
        history = max(1, min(50, history))
        says = strip_tags(form.get("SAYS") or info["join"]).strip()
        if not says:
            says = info["join"]
        member = form.get("MEMBER") == "1"
        sid, sess = get_session(self)
        if sess is None or sess["room"] != slug:
            sid = new_sid()
            sess = {}
            with sessions_lock:
                sessions[sid] = sess
        sess.update(user=user, room=slug, member=member, history=history,
                    certified=(slug == "anything-goes" or
                               sess.get("certified", False)),
                    last_seen=time.time(), last_msg=0.0)
        db_add_message(slug, user, "join", says)
        self._redirect("/" + slug, sid=sid)

    # -- chat pane (GET /<room>)
    def _handle_room(self, slug, query):
        info = ROOMS[slug]
        sid, sess = get_session(self)
        if sess and sess.get("room") != slug and "jump" in query:
            # multi-room jumping: same name, new room, join announcement
            sess["room"] = slug
            sess["certified"] = sess.get("certified", False) or \
                slug != "anything-goes"
            touch(sess)
            db_add_message(slug, sess["user"], "join", info["join"])
            self._redirect("/" + slug, sid=sid)
            return
        if not sess or sess.get("room") != slug:
            self._redirect(info["entry"])
            return
        if slug == "anything-goes" and not sess.get("certified"):
            self._redirect(info["entry"])
            return
        touch(sess)
        msgs = db_messages(slug, sess["history"], user=sess["user"])
        if info.get("aol"):
            self._send(200, render_aol_room_page(slug, sess, msgs))
        else:
            self._send(200, render_room_page(slug, sess, msgs))

    def _handle_leave(self, slug):
        sid, sess = get_session(self)
        if sess and sess.get("room") == slug:
            db_add_message(slug, sess["user"], "leave",
                           "Leaves %s..." % ROOMS[slug]["name"])
            with sessions_lock:
                sessions.pop(sid, None)
        self._redirect("/chat.htm")

    def _blocked_response(self, slug, strikes=0, banned=False):
        """403 for a filtered public message or a banned poster."""
        if banned:
            msg = ("You are banned from posting in public chat here — "
                   "three blocked messages.")
        else:
            msg = ("That message was blocked — it contains language that "
                   "isn't allowed in public chat here. (Strike %d of %d.)"
                   % (strikes, BLOCK_STRIKES))
        if self._wants_json():
            self._json(403, {"error": msg, "strikes": strikes,
                             "banned": banned})
        else:
            self._send(403, "<html><body>%s<br><a href=\"/%s\">Back to %s"
                            "</a></body></html>"
                       % (esc(msg), slug, esc(ROOMS[slug]["name"])))

    def _handle_post(self, slug, form, whisper=False):
        sid, sess = get_session(self)
        if not sess or sess.get("room") != slug:
            if self._wants_json():
                self._json(403, {"error": "not in this room"})
            else:
                self._redirect(ROOMS[slug]["entry"])
            return
        text = (form.get("text") or form.get("SAYS") or "").strip()
        if not text:
            self._redirect("/" + slug)
            return
        text = text[:MAX_MSG]
        if not whisper:
            # automated word filter — public messages only. Whispers
            # bypass the filter (and the ban) entirely: they are private
            # between the two people and are never monitored.
            _, banned = strike_status(sess["user"])
            if banned:
                self._blocked_response(slug, banned=True)
                return
            hit = text_blocked(text)
            if hit:
                strikes, now_banned = record_strike(sess["user"])
                self._blocked_response(slug, strikes=strikes,
                                       banned=now_banned)
                return
        now = time.time()
        if now - sess.get("last_msg", 0) < RATE_LIMIT_SECS:
            if self._wants_json():
                self._json(429, {"error": "slow down — one message every "
                                          "couple of seconds"})
            else:
                self._send(429, "<html><body>Slow down — one message every "
                                "couple of seconds. "
                                '<a href="/%s">Back to %s</a></body></html>'
                           % (slug, esc(ROOMS[slug]["name"])))
            return
        sess["last_msg"] = now
        touch(sess)
        if whisper:
            to = (form.get("to") or "").strip()[:MAX_NAME]
            db_add_message(slug, sess["user"], "whisper", text, to_user=to)
        else:
            db_add_message(slug, sess["user"], "say", text)
        if self._wants_json():
            self._json(200, {"ok": True})
        else:
            self._redirect("/" + slug)

    # -- message board
    def _handle_board_post(self, form, board="clubgabbay"):
        """POST /messages/post (or /neighborhoods/<slug>/board/post) — a
        new board message. Same word filter + strikes as public chat;
        board posts are public, so they are filtered. No login: the
        poster types their own From name."""
        if board != "clubgabbay" and board not in NEIGHBORHOODS \
                and board not in STANDALONE_BOARDS:
            self._send(404, render_404(self.path))
            return
        back = board_url(board)
        name = (form.get("from") or "").strip()[:BOARD_MAX_NAME]
        to_name = (form.get("to") or "").strip()[:BOARD_MAX_NAME]
        subject = (form.get("subject") or "").strip()[:BOARD_MAX_SUBJECT]
        message = (form.get("message") or "").strip()[:BOARD_MAX_MSG]
        if not name or not message:
            self._redirect(back)
            return
        _, banned = strike_status(name)
        if banned:
            self._send(403, "<html><body>You are banned from posting on "
                            "the message board here — three blocked "
                            "messages.<br><a href=\"%s\">Back to "
                            "the board</a></body></html>" % back)
            return
        hit = text_blocked(" ".join(
            x for x in (name, to_name, subject, message) if x))
        if hit:
            strikes, now_banned = record_strike(name)
            if now_banned:
                msg = ("You are banned from posting on the message board "
                       "here — three blocked messages.")
            else:
                msg = ("That message was blocked — it contains language "
                       "that isn't allowed here. (Strike %d of %d.)"
                       % (strikes, BLOCK_STRIKES))
            self._send(403, "<html><body>%s<br><a href=\"%s\">"
                            "Back to the board</a></body></html>"
                       % (esc(msg), back))
            return
        ip = self.client_address[0]
        now = time.time()
        if now - _board_last_post.get(ip, 0) < BOARD_RATE_LIMIT_SECS:
            self._send(429, "<html><body>Slow down — one board message "
                            "every few seconds. <a href=\"%s\">"
                            "Back to the board</a></body></html>" % back)
            return
        _board_last_post[ip] = now
        db_add_board_post(name, to_name, subject, message, board)
        self._redirect(back)

    # -- API
    def _handle_api_messages(self, slug, query):
        sid, sess = get_session(self)
        if not sess or sess.get("room") != slug:
            self._json(403, {"error": "not in this room"})
            return
        touch(sess)
        try:
            since = int(query.get("since", ["0"])[0])
        except ValueError:
            since = 0
        if since:
            msgs = db_messages(slug, 200, since_id=since, user=sess["user"])
        else:
            msgs = db_messages(slug, sess["history"], user=sess["user"])
        self._json(200, {"room": slug, "messages": msgs,
                         "presence": presence(slug),
                         "last_id": db_last_id(slug)})

    def _handle_api_report(self, slug, form):
        sid, sess = get_session(self)
        if not sess:
            self._json(403, {"error": "enter a room first"})
            return
        try:
            msg_id = int(form.get("msg_id") or 0)
        except ValueError:
            msg_id = 0
        reason = (form.get("reason") or "reported").strip()[:200]
        with db_lock:
            db.execute("INSERT INTO reports (room, msg_id, reporter, reason, ts)"
                       " VALUES (?,?,?,?,?)",
                       (slug, msg_id, sess["user"], reason, time.time()))
            db.commit()
        self._json(200, {"ok": True,
                         "note": "Report noted — a moderator reviews it."})

    # -- routing
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        slug = path.strip("/").split("/")[0]
        if path in ("/lobby2.cfm", "/login.cfm") or \
                path.endswith("/lobby2.cfm") or path.endswith("/login.cfm"):
            self._send(200, render_member_page())
            return
        if path == "/api/rooms":
            self._json(200, {"rooms": [
                {"slug": s, "name": i["name"]} for s, i in ROOMS.items()]})
            return
        if path == "/api/board/posts":
            # public data (same posts the board pages render); the backup
            # job reads this (Paul, 2026-11-09: board posts must stay up).
            # ?board=<slug> filters to one board; no param returns all.
            b = query.get("board", [None])[0]
            if b is not None and b != "clubgabbay" \
                    and b not in NEIGHBORHOODS \
                    and b not in STANDALONE_BOARDS:
                self._json(404, {"error": "no such board"})
                return
            self._json(200, {"posts": db_board_posts(board=b)})
            return
        if path.startswith("/api/") and "/messages" in path:
            parts = [p for p in path.split("/") if p]
            if len(parts) >= 3 and self._room_or_none(parts[1]):
                self._handle_api_messages(ALIASES.get(parts[1], parts[1]),
                                          query)
                return
        room = self._room_or_none(slug)
        if room and path in ("/" + slug, "/" + ALIASES.get(slug, slug)):
            self._handle_room(ALIASES.get(slug, slug), query)
            return
        if path.endswith("/leave"):
            base = path.strip("/").split("/")[0]
            if self._room_or_none(base):
                self._handle_leave(ALIASES.get(base, base))
                return
        parts = [p for p in path.split("/") if p]
        if len(parts) == 2 and parts[1] == "board" \
                and parts[0] in STANDALONE_BOARDS:
            # a standalone board (Paul, 2026-11-09, AOL handles): same
            # form + posts as the rest, no archive
            self._send(200, render_board_page(parts[0]))
            return
        if len(parts) == 3 and parts[0] == "neighborhoods" \
                and parts[2] == "board" and parts[1] in NEIGHBORHOODS:
            # a neighborhood's own board (Paul, 2026-11-09): same form +
            # posts as the main board, no archive
            self._send(200, render_board_page(parts[1]))
            return
        fpath = resolve_static(path)
        if fpath and is_board_file(fpath):
            # the bulletin board is server-rendered: post form + new
            # posts above the frozen 1997 archive (Paul, 2026-11-09)
            self._send(200, render_board_page())
            return
        if fpath:
            try:
                with open(fpath, "rb") as fh:
                    data = fh.read()
            except OSError:
                self._send(404, render_404(path))
                return
            self._send(200, data, content_type(fpath))
            return
        self._send(404, render_404(path))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        parts = [p for p in path.split("/") if p]
        form = self._read_form()
        if parts == ["messages", "post"]:
            self._handle_board_post(form, "clubgabbay")
            return
        if len(parts) == 3 and parts[1] == "board" and parts[2] == "post" \
                and parts[0] in STANDALONE_BOARDS:
            self._handle_board_post(form, parts[0])
            return
        if len(parts) == 4 and parts[0] == "neighborhoods" \
                and parts[2] == "board" and parts[3] == "post" \
                and parts[1] in NEIGHBORHOODS:
            self._handle_board_post(form, parts[1])
            return
        if len(parts) >= 2 and parts[1] == "post" and self._room_or_none(parts[0]):
            self._handle_post(ALIASES.get(parts[0], parts[0]), form)
            return
        if len(parts) >= 2 and parts[1] == "whisper" and self._room_or_none(parts[0]):
            self._handle_post(ALIASES.get(parts[0], parts[0]), form,
                              whisper=True)
            return
        if len(parts) >= 2 and parts[1] == "history" and self._room_or_none(parts[0]):
            sid, sess = get_session(self)
            slug = ALIASES.get(parts[0], parts[0])
            if sess and sess.get("room") == slug:
                try:
                    sess["history"] = max(1, min(50, int(form.get("HISTORY") or 8)))
                except ValueError:
                    pass
                touch(sess)
            self._redirect("/" + slug)
            return
        if len(parts) >= 3 and parts[0] == "api" and parts[2] == "report" \
                and self._room_or_none(parts[1]):
            self._handle_api_report(ALIASES.get(parts[1], parts[1]), form)
            return
        if len(parts) == 1 and self._room_or_none(parts[0]):
            self._handle_entry(ALIASES.get(parts[0], parts[0]), form)
            return
        self._send(404, render_404(path))

    def do_HEAD(self):
        self.do_GET()


def main():
    global SITE_ROOT, DB_PATH
    ap = argparse.ArgumentParser(description="Club Gabbay mirror backend")
    ap.add_argument("--host", default="127.0.0.1")
    # Render provides $PORT; fall back to 8124 when unset (local runs).
    ap.add_argument("--port", type=int,
                    default=int(os.environ.get("PORT", "8124")))
    ap.add_argument("--site", default=SITE_ROOT)
    ap.add_argument("--db", default=DB_PATH)
    args = ap.parse_args()
    SITE_ROOT = os.path.abspath(args.site)
    DB_PATH = os.path.abspath(args.db)
    if not os.path.isdir(SITE_ROOT):
        sys.exit("site tree not found: %s" % SITE_ROOT)
    db_init(DB_PATH)
    restored = restore_board_posts()
    if restored:
        sys.stderr.write("board restore: %d post(s) re-seeded from backup\n"
                         % restored)
    # warn about room backgrounds the archive never captured
    for slug, info in ROOMS.items():
        if info.get("bg") and not static_exists(info["bg"]):
            sys.stderr.write("note: room %s background %s not in archive "
                             "(pane falls back to plain background)\n"
                             % (slug, info["bg"]))
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    sys.stderr.write("Club Gabbay mirror up on http://%s:%d/ "
                     "(site=%s, db=%s)\n"
                     % (args.host, args.port, SITE_ROOT, DB_PATH))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
