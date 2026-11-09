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

# Third-person actions (Paul, 2026-11-09): the 90s chat-room dropdown --
# pick a verb and a person in the room; posts "* user winks at target *".
# The verb is whitelisted and the target must be in the room, so no word
# filter is needed. "kisses" is left out on purpose -- keep it clean.
ACTION_VERBS = ["laughs at", "winks at", "waves at", "smiles at", "hugs",
                "pokes", "dances with", "high-fives", "bows to",
                "cheers for"]

# AOL message colors/fonts, basic level (Paul, 2026-11-09): a color and a
# font picker on the AOL chat box; the choice rides on the message and
# sticks in the session. Server-side whitelists only -- anything else
# falls back to black/Arial. AOL room only.
AOL_COLORS = ["black", "red", "blue", "green", "purple", "orange",
              "teal", "maroon", "navy"]
AOL_FONTS = ["Arial", "Times New Roman", "Courier New", "Verdana",
             "Comic Sans MS"]

# Retro chat services (Paul, 2026-11-09): the other services from the
# old days -- MSN, Yahoo, ICQ, mIRC and the rest -- each with its own
# room on the same engine, same setup as AOL Chat (landing page + age
# gate + room). The landing pages are built by backend/build_services.py,
# which imports this table -- one source of truth, keep it here.
SERVICES = [
    {"slug": "msn", "name": "MSN Messenger", "room": "MSN Chat",
     "bgcolor": "#0078D7",
     "desc": "Microsoft's buddy-list messenger -- nudges, winks, custom "
             "display pictures, and adding friends by email. The sound "
             "of a friend coming online.",
     "join": "Joins MSN Chat...",
     "skin": {'nudge': 'Nudge', 'title_style': 'background:linear-gradient(#3A7BD5, #7FB5E8);', 'dp': True}},
    {"slug": "yahoo", "name": "Yahoo! Chat", "room": "Yahoo! Chat",
     "bgcolor": "#6001D2",
     "desc": "Public chat rooms divided by interests, age groups, places "
             "and topics -- walk in, pick a room, talk to strangers.",
     "join": "Joins Yahoo! Chat...",
     "skin": {'nudge': 'BUZZ!', 'smiley': True}},
    {"slug": "icq", "name": "ICQ", "room": "ICQ Chat",
     "bgcolor": "#00A000",
     "desc": "One of the first instant messengers -- number-based "
             "usernames, the famous 'Uh-oh!' sound, and a flower that "
             "told you who was online.",
     "join": "Joins ICQ Chat...",
     "skin": {'win': '#E8F5E8', 'body': '#C8E6C8', 'channel': '#icq_usa', 'flower': True, 'footer_note': 'Uh-oh!'}},
    {"slug": "mirc", "name": "mIRC", "room": "mIRC Chat",
     "bgcolor": "#000080",
     "desc": "The old IRC network -- channels like #Canada, #Gaming and "
             "#Singles, where a nickname and a channel were all you "
             "needed.",
     "join": "Joins mIRC Chat...",
     "skin": {'channel': '#Canada', 'chat_font': 'Courier New', 'join': '#808080', 'quit': '#808080', 'topic': True, 'statusbar': True}},
    {"slug": "excite", "name": "Excite Chat", "room": "Excite Chat",
     "bgcolor": "#CC0000",
     "desc": "Public chat rooms where strangers could meet and talk -- "
             "one of the web's early meeting places.",
     "join": "Joins Excite Chat...",
     "skin": {'win': '#FFF0F0', 'body': '#F0C8C8', 'masthead': {'bg': '#CC0000', 'fg': 'white', 'text': 'Excite - Home | Chat | Mail'}}},
    {"slug": "paltalk", "name": "Paltalk", "room": "Paltalk Chat",
     "bgcolor": "#0099CC",
     "desc": "Voice and video chat rooms -- talk instead of type, with "
             "rooms for every interest.",
     "join": "Joins Paltalk Chat...",
     "skin": {'win': '#E0F0F8', 'body': '#C8DCE8', 'video_strip': True}},
    {"slug": "lycos", "name": "Lycos Chat", "room": "Lycos Chat",
     "bgcolor": "#FF6600",
     "desc": "Web-based chat rooms from the search-engine days -- no "
             "download, just a browser and a nickname.",
     "join": "Joins Lycos Chat...",
     "skin": {'win': '#FFF5E8', 'body': '#F0D8B8', 'masthead': {'bg': '#000000', 'fg': '#FFCC00', 'text': 'Lycos - Go get it'}}},
    {"slug": "palace", "name": "The Palace", "room": "The Palace Chat",
     "bgcolor": "#993399",
     "desc": "2D graphical chat rooms with avatars -- walk your little "
             "figure around the room and talk in bubbles.",
     "join": "Joins The Palace Chat...",
     "skin": {'win': '#F5E8F5', 'body': '#E0C8E0', 'chat_bg': '#87CEEB', 'chat_font': 'Comic Sans MS', 'chat_bg_css': 'linear-gradient(#87CEEB 0%, #87CEEB 60%, #90EE90 60%, #90EE90 100%)', 'avatars': True}},
    {"slug": "habbo", "name": "Habbo Hotel", "room": "Habbo Hotel Chat",
     "bgcolor": "#E6B800",
     "desc": "A virtual hotel to hang out in -- your own little avatar, "
             "rooms to visit, people to meet.",
     "join": "Joins Habbo Hotel Chat...",
     "skin": {'fg': 'black', 'win': '#FFF8D0', 'body': '#F0E0A0', 'chat_bg': '#003399', 'chat_fg': 'white', 'chat_font': 'Verdana', 'room_bg_css': 'repeating-conic-gradient(#E8C860 0% 25%, #F5D878 0% 50%) 0 0 / 32px 32px', 'habbo_room': True}},
    {"slug": "powwow", "name": "PowWow", "room": "PowWow Chat",
     "bgcolor": "#006666",
     "desc": "Early group messaging and voice chat -- one of the first "
             "programs that let a group talk together online.",
     "join": "Joins PowWow Chat...",
     "skin": {'win': '#E0F0F0', 'body': '#C8E0E0', 'voice_dot': True}},
    {"slug": "compuserve", "name": "CompuServe", "room": "CompuServe Chat",
     "bgcolor": "#003366",
     "desc": "One of the first online services -- forums and chat before "
             "the web took over.",
     "join": "Joins CompuServe Chat...",
     "skin": {'win': '#E8EEF5', 'body': '#C8D8E8', 'channel': 'CB Channel 1', 'chat_bg': '#000000', 'chat_fg': '#00FF00', 'chat_font': 'Courier New', 'send': 'GO'}},
    {"slug": "prodigy", "name": "Prodigy", "room": "Prodigy Chat",
     "bgcolor": "#800000",
     "desc": "An early online service with public chat -- a whole world "
             "behind a dial-up number.",
     "join": "Joins Prodigy Chat...",
     "skin": {'win': '#F8E8E8', 'body': '#E8C8C8', 'notice': 'Welcome to Prodigy Chat', 'sidebar': '#0000CC', 'side_fg': 'white', 'side_link': '#FFCC00'}},
    {"slug": "xfire", "name": "Xfire", "room": "Xfire Chat",
     "bgcolor": "#999999",
     "desc": "Gaming friends and chat -- see what your friends are "
             "playing and jump in with them.",
     "join": "Joins Xfire Chat...",
     "skin": {'title': '#000000', 'win': '#333333', 'body': '#222222', 'text': 'white', 'link': '#66CCFF', 'vlink': '#99CCFF', 'chat_bg': '#1A1A1A', 'chat_fg': '#CCCCCC'}},
    {"slug": "myspace", "name": "MySpace", "room": "MySpace Chat",
     "bgcolor": "#003399",
     "desc": "Profiles, friends, messages and comments -- the place "
             "where everyone's page had a song that started playing.",
     "join": "Joins MySpace Chat...",
     "skin": {'win': '#E8EEF8', 'body': '#C8D8F0', 'top8': True}},
]
SKIN_DEFAULT = {"fg": "white", "win": "#D4D0C8", "body": "#C0C0C0",
                "text": "black", "link": "blue", "vlink": "purple",
                # messenger look, v2 (Paul, 2026-11-09, ICQ screenshot):
                # the web-chat chrome -- chat area colors/font, join/quit
                # line colors, the channel tab, the Send label, and the
                # per-service signature bits (nudge/BUZZ button, notice
                # strip, masthead band, flower mark, video strip, Top 8,
                # voice dot, footer note). Defaults are the ICQ screenshot.
                "chat_bg": "white", "chat_fg": "black",
                "chat_font": "Tahoma",
                "join": "#008000", "quit": "#FF0000",
                "channel": None, "send": "Send",
                "nudge": None, "notice": None, "masthead": None,
                "flower": False, "video_strip": False, "top8": False,
                "voice_dot": False, "footer_note": None,
                # v3 (Paul, 2026-11-09): the look drawn properly -- a
                # gradient title bar, display pictures, the Yahoo smiley,
                # mIRC topic + status bar, a Prodigy blue sidebar, the
                # Palace backdrop + avatars, the Habbo pixel room.
                "title_style": "", "dp": False, "smiley": False,
                "topic": False, "statusbar": False,
                "sidebar": None, "side_fg": None, "side_link": None,
                "chat_bg_css": None, "room_bg_css": None,
                "avatars": False, "habbo_room": False}
for _s in SERVICES:
    _skin = dict(SKIN_DEFAULT)
    _skin["title"] = _s["bgcolor"]
    _skin.update(_s.get("skin") or {})
    if not _skin["channel"]:
        _skin["channel"] = _s["room"]
    ROOMS[_s["slug"] + "-chat"] = {
        "name": _s["room"],
        "service": _s["name"],
        "bg": None, "bgcolor": _s["bgcolor"],
        "art": None,
        "desc": _s["desc"],
        "entry": "/%s.html" % _s["slug"],
        "join": _s["join"],
        "messenger": True,
        "skin": _skin,
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
        # AOL message colors/fonts (Paul, 2026-11-09): nullable columns;
        # old rows read back with None = default rendering.
        for col in ("color TEXT", "font TEXT"):
            try:
                db.execute("ALTER TABLE messages ADD COLUMN %s" % col)
            except sqlite3.OperationalError:
                pass  # column already there
        db.commit()


def db_add_message(room, user, kind, text, to_user=None, color=None,
                   font=None):
    with db_lock:
        cur = db.execute(
            "INSERT INTO messages (room, user, kind, text, to_user, ts,"
            " color, font) VALUES (?,?,?,?,?,?,?,?)",
            (room, user, kind, text, to_user, time.time(), color, font))
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
                "SELECT id, user, kind, text, to_user, ts, color, font"
                " FROM messages"
                " WHERE room=? AND id>? ORDER BY id ASC LIMIT 200",
                (room, since_id)).fetchall()
        else:
            rows = db.execute(
                "SELECT id, user, kind, text, to_user, ts, color, font"
                " FROM messages"
                " WHERE room=? ORDER BY id DESC LIMIT ?",
                (room, limit)).fetchall()
            rows.reverse()
    out = []
    for mid, muser, kind, text, to_user, ts, color, font in rows:
        if kind == "whisper" and user not in (muser, to_user):
            continue
        out.append({"id": mid, "user": muser, "kind": kind, "text": text,
                    "to": to_user, "ts": ts, "color": color, "font": font,
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
            if s.get("room") == room and now - s["last_seen"] < PRESENCE_TIMEOUT:
                label = s["user"] + (" (member)" if s.get("member") else "")
                names.append(label)
    return sorted(set(names))


def guest_name(room):
    with sessions_lock:
        taken = {s["user"] for s in sessions.values()
                 if s.get("room") == room}
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


def render_msg(m, join_c=None, quit_c=None):
    """One message as an HTML line (user content always escaped).
    join_c/quit_c color the join/leave lines -- the messenger skins
    pass their own (ICQ green/red from Paul's screenshot, mIRC grey);
    None keeps the plain bold/italic rendering every other room uses."""
    if m["kind"] == "join":
        if join_c:
            return ('<b><font color="%s">%s %s</font></b><br>'
                    % (join_c, esc(m["user"]), esc(m["text"])))
        return ('<b>%s %s</b><br>' % (esc(m["user"]), esc(m["text"])))
    if m["kind"] == "leave":
        if quit_c:
            return ('<i><font color="%s"><b>%s</b> %s</font></i><br>'
                    % (quit_c, esc(m["user"]), esc(m["text"])))
        return ('<i><b>%s</b> %s</i><br>' % (esc(m["user"]), esc(m["text"])))
    if m["kind"] == "whisper":
        return ('<i><font color="#800080"><b>%s</b> whispers to '
                '<b>%s</b>: %s</font></i><br>'
                % (esc(m["user"]), esc(m["to"]), esc(m["text"])))
    if m["kind"] == "action":
        return ('<i>* <b>%s</b> %s *</i><br>'
                % (esc(m["user"]), esc(m["text"])))
    # a plain say, possibly with an AOL color/font (basic level)
    attrs = ""
    if m.get("color") and m["color"] != "black":
        attrs += ' color="%s"' % esc(m["color"])
    if m.get("font") and m["font"] != "Arial":
        attrs += ' face="%s"' % esc(m["font"])
    if attrs:
        return ('<b>%s:</b> <font%s>%s</font><br>'
                % (esc(m["user"]), attrs, esc(m["text"])))
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
    action_opts = "".join('<option>%s</option>' % v for v in ACTION_VERBS)
    lines = "".join(render_msg(m) for m in initial_msgs)
    last_id = initial_msgs[-1]["id"] if initial_msgs else 0
    return """<html><head><title>ClubGabbay: %s</title></head>
<body%s>
<center><h2>ClubGabbay: %s</h2></center>
%s
<blockquote>%s</blockquote>
<p><font size="-1"><i>This room is intended for adults 21 and over.</i></font></p>
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
<form action="/%s/action" method="post">
<select name="action">%s</select>
<select name="to">%s</select>
<input type="submit" value="Do it!">
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
  if(m.kind==='action') return '<i>* <b>'+escHtml(m.user)+'</b> '+escHtml(m.text)+' *</i><br>';
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
       slug, slug, user_opts, slug, action_opts, user_opts,
       slug, history_opts,
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
    color = sess.get("color", "black")
    font = sess.get("font", "Arial")
    color_opts = "".join('<option value="%s"%s>%s</option>'
                         % (c, " selected" if c == color else "", c)
                         for c in AOL_COLORS)
    font_opts = "".join('<option%s>%s</option>'
                        % (" selected" if f == font else "", f)
                        for f in AOL_FONTS)
    action_opts = "".join('<option>%s</option>' % v for v in ACTION_VERBS)
    aol_user_opts = "".join('<option>%s</option>'
                            % esc(u.split(" (member)")[0])
                            for u in users
                            if u.split(" (member)")[0] != me)
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
<font size="-1"><i>This room is intended for adults 21 and over.</i></font><br>
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
<input type="submit" value="Send"><br>
<font size="-1">Color: <select name="color">%s</select>
Font: <select name="font">%s</select></font>
</form>
</td></tr>
<tr><td colspan="2">
<form action="/%s/action" method="post">
<select name="action">%s</select>
<select name="to">%s</select>
<input type="submit" value="Do it!">
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
  if(m.kind==='action') return '<i>* <b>'+escHtml(m.user)+'</b> '+escHtml(m.text)+' *</i><br>';
  return '<b>'+escHtml(m.user)+':</b> '+fontWrap(m)+'<br>';
}
function fontWrap(m){
  var attrs='';
  if(m.color && m.color!=='black') attrs+=' color="'+escHtml(m.color)+'"';
  if(m.font && m.font!=='Arial') attrs+=' face="'+escHtml(m.font)+'"';
  if(!attrs) return escHtml(m.text);
  return '<font'+attrs+'>'+escHtml(m.text)+'</font>';
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
""" % (lines, members, slug, color_opts, font_opts,
       slug, action_opts, aol_user_opts, slug, slug, history_opts,
       slug, esc(info["name"]),
       esc(sess["user"]), " (member)" if sess.get("member") else "",
       last_id, slug, esc(sess["user"]))


# Messenger skins v3 (Paul, 2026-11-09): the look, drawn properly.
# The ICQ flower is the real flower shape (8 green petals, yellow
# center) as an inline SVG, not a circle; MSN gets its blue gradient
# title bar and display-picture squares; Yahoo gets its yellow smiley;
# mIRC gets its topic line and live status bar; Prodigy gets its blue
# sidebar; The Palace gets its backdrop with smiley avatars and speech
# bubbles; Habbo gets its pixel room with block avatars and the HC sofa.
# Still just a skin -- no new engine, no invented data (no UINs, no
# game status, no moods, no fake buttons).
FLOWER_SVG = ('<svg width="16" height="16" viewBox="0 0 24 24">'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(0 12 12)"/>'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(45 12 12)"/>'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(90 12 12)"/>'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(135 12 12)"/>'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(180 12 12)"/>'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(225 12 12)"/>'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(270 12 12)"/>'
              '<ellipse cx="12" cy="6" rx="3" ry="5" fill="#00A651" transform="rotate(315 12 12)"/>'
              '<circle cx="12" cy="12" r="3.5" fill="#FFD700"/></svg>')


def smiley_svg(size):
    """Yahoo's yellow smiley (and The Palace's default avatar)."""
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24">'
            '<circle cx="12" cy="12" r="10" fill="#FFD700" stroke="#000" stroke-width="1"/>'
            '<circle cx="9" cy="10" r="1.5" fill="#000"/>'
            '<circle cx="15" cy="10" r="1.5" fill="#000"/>'
            '<path d="M8 14 Q12 18 16 14" stroke="#000" stroke-width="1.5" fill="none"/>'
            '</svg>' % (size, size))


AVATAR_COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A",
                 "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"]


def avatar_color(name):
    """A deterministic display-picture color per user (MSN squares,
    Habbo block avatars). Not a photo -- just a colored square."""
    return AVATAR_COLORS[sum(name.encode("utf-8", "ignore"))
                         % len(AVATAR_COLORS)]


def render_messenger_room_page(slug, sess, initial_msgs):
    """Messenger skins v3 (Paul, 2026-11-09): each retro service wears
    the look its own messenger had -- the AOL Chat window, re-skinned,
    now with the real shapes drawn in (ICQ flower, Yahoo smiley, MSN
    gradient + display pictures, mIRC topic + status bar, Prodigy blue
    sidebar, Palace backdrop + smiley avatars + speech bubbles, Habbo
    pixel room + block avatars + HC sofa). Same engine underneath:
    poll, filter, whispers (click a name or an avatar to IM them),
    actions, history. No color/font pickers -- those stay AOL-only."""
    info = ROOMS[slug]
    skin = info["skin"]
    history_opts = "".join(
        '<option value="%d"%s>%d</option>' % (n, " selected" if n == sess["history"] else "", n)
        for n in (8, 16, 32))
    users = presence(slug)
    me = sess["user"]
    others = [u.split(" (member)")[0] for u in users
              if u.split(" (member)")[0] != me]
    side_bg = skin["sidebar"] or skin["win"]
    side_fg = skin["side_fg"] or skin["text"]
    side_link = skin["side_link"] or skin["link"]

    def jsq(s):
        return ("'" + s.replace("\\", "\\\\").replace("'", "\\'")
                .replace('"', "&quot;") + "'")
    dot = ('<span style="display:inline-block;width:8px;height:8px;'
           'background:#663399;border-radius:50%;"></span> '
           if skin["voice_dot"] else "")
    members = "".join(
        (('<span style="display:inline-block;width:16px;height:16px;'
          'background:%s;border:1px solid #808080;vertical-align:middle;">'
          '</span> ' % avatar_color(u)) if skin["dp"] else "")
        + dot
        + ('<a href="#" onclick="return pmUser(this.textContent);" '
           'style="color:%s;">%s</a><br>' % (side_link, esc(u)))
        for u in others)
    # MySpace Top 8 strip: the first 8 others as small squares, click
    # to IM (the name rides in the onclick, the square shows the initial).
    top8_html = ""
    if skin["top8"] and others:
        squares = "".join(
            '<a href="#" onclick="return pmUser(%s);">'
            '<span style="display:inline-block;width:24px;height:24px;'
            'border:1px solid #808080;background:white;text-align:center;">'
            '%s</span></a> ' % (jsq(u), esc(u[0]))
            for u in others[:8])
        top8_html = '<b>Top 8:</b><br>' + squares + '<br>'
    action_opts = "".join('<option>%s</option>' % v for v in ACTION_VERBS)
    user_opts = "".join('<option>%s</option>' % esc(u) for u in others)
    more = " | ".join(
        '<a href="/%s.html">%s</a>' % (sv["slug"], sv["name"])
        for sv in SERVICES)
    # Chat Rooms panel (ICQ screenshot): the other services, linked.
    my_svc = slug[:-len("-chat")]
    rooms_html = ('<p><b>Chat Rooms:</b><br>'
                  '<div style="height:120px;overflow:auto;">'
                  + "".join(
                      '<a href="/%s.html" style="color:%s;">%s</a><br>'
                      % (sv["slug"], side_link, sv["name"])
                      for sv in SERVICES if sv["slug"] != my_svc)
                  + '</div></p>')
    lines = "".join(render_msg(m, skin["join"], skin["quit"])
                    for m in initial_msgs)
    last_id = initial_msgs[-1]["id"] if initial_msgs else 0
    # Portal masthead band (Excite red, Lycos black/yellow).
    masthead_html = ""
    if skin["masthead"]:
        mh = skin["masthead"]
        masthead_html = ('<table width="640" border="0" cellpadding="4" '
                         'cellspacing="0" bgcolor="%s"><tr><td>'
                         '<font color="%s"><b>%s</b></font></td></tr></table>'
                         % (mh["bg"], mh["fg"], esc(mh["text"])))
    # Title-bar marks: the ICQ flower (real shape, SVG) and the Yahoo
    # smiley, before the room name.
    title_marks = ""
    if skin["flower"]:
        title_marks += FLOWER_SVG + " "
    if skin["smiley"]:
        title_marks += smiley_svg(16) + " "
    title_style_attr = (' style="%s"' % skin["title_style"]
                        if skin["title_style"] else "")
    tab_html = ('<tr><td colspan="2"><font size="-1">&nbsp;'
                '<span style="border:1px solid #808080;background:#E0E0E0;">'
                '&nbsp;Status: Online&nbsp;</span> &nbsp;'
                '<span style="border:1px solid #808080;background:#E0E0E0;">'
                '&nbsp;%s&nbsp;</span></font></td></tr>'
                % esc(skin["channel"]))
    # mIRC topic line (the room's own description is the topic).
    topic_html = ""
    if skin["topic"]:
        topic_html = ('<font size="-1"><b>Topic:</b> %s</font><br>'
                      % esc(info["desc"]))
    # Prodigy welcome strip above the chat.
    notice_html = ""
    if skin["notice"]:
        notice_html = ('<table width="100%%" bgcolor="#FFFFCC"><tr><td>'
                       '<font size="-1"><b>%s</b></font></td></tr></table>'
                       % esc(skin["notice"]))
    # Paltalk video strip: grey placeholder tiles above the chat.
    video_html = ""
    if skin["video_strip"]:
        video_html = ('<table width="100%%" cellpadding="2" cellspacing="0">'
                      '<tr><td colspan="3"><font size="-1"><b>Video</b>'
                      '</font></td></tr><tr>'
                      '<td width="33%%" height="40" bgcolor="#C0C0C0" '
                      'align="center"><font size="-1">video</font></td>'
                      '<td width="33%%" height="40" bgcolor="#C0C0C0" '
                      'align="center"><font size="-1">video</font></td>'
                      '<td width="34%%" height="40" bgcolor="#C0C0C0" '
                      'align="center"><font size="-1">video</font></td>'
                      '</tr></table>')
    # The Palace: smiley avatars standing on the backdrop, each with a
    # speech bubble holding their last message (the poll keeps the
    # bubbles live). Click an avatar to IM them.
    avatars_html = ""
    if skin["avatars"]:
        last_said = {}
        for m in initial_msgs:
            if m["kind"] in ("say", "action"):
                last_said[m["user"]] = m["text"]
        blocks = []
        for u in [x.split(" (member)")[0] for x in users]:
            txt = last_said.get(u, "")
            if len(txt) > 60:
                txt = txt[:60] + "..."
            bubble = ('<div data-bubble="%s" style="display:%s;'
                      'background:white;border:1px solid #808080;'
                      'border-radius:6px;padding:2px;font-size:11px;'
                      'word-wrap:break-word;">%s</div>'
                      % (esc(u), "block" if txt else "none", esc(txt)))
            inner = ('%s%s<br><font size="-1">%s</font>'
                     % (bubble, smiley_svg(24), esc(u)))
            if u == me:
                blocks.append('<div style="display:inline-block;width:64px;'
                              'text-align:center;vertical-align:top;margin:2px;">'
                              + inner + '</div>')
            else:
                blocks.append('<a href="#" onclick="return pmUser(%s);">'
                              '<div style="display:inline-block;width:64px;'
                              'text-align:center;vertical-align:top;margin:2px;">'
                              % jsq(u) + inner + '</div></a>')
        avatars_html = ('<div id="avatars">' + "".join(blocks) + '</div>')
    # Habbo: the pixel room -- checker floor, block avatars standing on
    # it, the HC sofa in the corner -- with the dark blue chat log below.
    habbo_room_html = ""
    if skin["habbo_room"]:
        blocks = []
        for u in others:
            inner = ('<span style="display:block;width:12px;height:12px;'
                     'background:#FFDBAC;margin:0 auto;"></span>'
                     '<span style="display:block;width:20px;height:24px;'
                     'background:%s;margin:0 auto;"></span>'
                     '<font size="-1" color="#000000">%s</font>'
                     % (avatar_color(u), esc(u)))
            blocks.append('<a href="#" onclick="return pmUser(%s);">'
                          '<span style="display:inline-block;width:28px;'
                          'text-align:center;margin:0 4px;">'
                          % jsq(u) + inner + '</span></a>')
        habbo_room_html = ('<div style="height:140px;position:relative;'
                           'background:%s;display:flex;align-items:flex-end;'
                           'padding:4px;">' % skin["room_bg_css"]
                           + "".join(blocks)
                           + '<span style="position:absolute;right:8px;bottom:8px;'
                           'width:48px;height:28px;background:#8B4513;color:white;'
                           'text-align:center;font-size:11px;line-height:28px;">'
                           'HC</span></div>')
    chat_bg_css = skin["chat_bg_css"] or skin["chat_bg"]
    chat_style = ('height:300px;overflow:auto;background:%s;color:%s;'
                  'font-family:%s;'
                  % (chat_bg_css, skin["chat_fg"], skin["chat_font"]))
    # mIRC status bar (live user count, updated by the poll).
    statusbar_html = ""
    if skin["statusbar"]:
        statusbar_html = ('<div style="background:#C0C0C0;padding:2px;">'
                          '<font size="-1">Channel: %s | Users: '
                          '<span id="status-users">%d</span></font></div>'
                          % (esc(skin["channel"]), len(users)))
    send_btn = ('<input type="submit" value="%s" '
                'style="background:%s;color:%s;">'
                % (esc(skin["send"]), skin["title"], skin["fg"]))
    nudge_html = ""
    if skin["nudge"]:
        nudge_html = (' <input type="button" value="%s" '
                      'onclick="shakePane();">' % esc(skin["nudge"]))
    footer_html = esc(info["service"])
    if skin["footer_note"]:
        footer_html += " -- " + esc(skin["footer_note"])
    footer_html += " -- a fan-made tribute to the 1990s."
    return """<html><head><title>%s</title></head>
<body bgcolor="%s" text="%s" link="%s" vlink="%s">
<center>
%s
<table width="640" border="2" cellpadding="0" cellspacing="0" bgcolor="%s">
<tr><td bgcolor="%s"%s><font color="%s"><b>&nbsp;%s%s</b></font></td>
<td bgcolor="%s"%s align="right"><font color="%s"><b>X&nbsp;</b></font></td></tr>
%s
<tr><td colspan="2">
<table width="620" cellpadding="4" cellspacing="0"><tr>
<td width="460" valign="top" bgcolor="%s">
<font size="-1" color="%s"><i>This room is intended for adults 21 and over.</i></font><br>
%s%s%s%s%s
<div id="chat" style="%s">%s</div>
%s
</td>
<td width="150" valign="top" bgcolor="%s">
<font color="%s">
<b>People in this room:</b><br>
%s
<div id="members">%s</div>
%s
</font>
</td>
</tr></table>
</td></tr>
<tr><td colspan="2">
<form action="/%s/post" method="post">
<input type="text" name="text" size="50" maxlength="500">
%s%s
</form>
</td></tr>
<tr><td colspan="2">
<form action="/%s/action" method="post">
<select name="action">%s</select>
<select name="to">%s</select>
<input type="submit" value="Do it!">
</form>
</td></tr>
<tr><td colspan="2">
<div id="imbox" style="display:none;">
<table width="620" border="1" cellpadding="2" cellspacing="0" bgcolor="%s">
<tr><td bgcolor="%s"><font color="%s"><b>Instant Message to <span id="im-to-name"></span></b></font></td>
<td bgcolor="%s" align="right"><a href="#" onclick="return closeIm();"><font color="%s">X</font></a></td></tr>
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
<a href="/%s.html">Back to %s</a> |
<a href="/">Club Gabbay Home</a> |
<a href="#" onclick="location.reload(); return false;">Refresh</a>
</font></p>
<p><font size="-1">More retro chat: %s</font></p>
<p><font size="-1">You are chatting as <b>%s</b>%s.
Messages refresh automatically every few seconds.
Click a name on the right to send them a private message.</font></p>
<hr noshade>
%s
</td></tr>
</table>
</center>
<script>
var lastId = %d;
var room = "%s";
var me = "%s";
var joinColor = "%s";
var quitColor = "%s";
var voiceDot = %s;
var showDP = %s;
var sideLink = "%s";
var AVATAR_COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"];
function avatarColor(name){ var s=0; for(var i=0;i<name.length;i++){ s+=name.charCodeAt(i); } return AVATAR_COLORS[s %% AVATAR_COLORS.length]; }
function escHtml(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function lineHtml(m){
  if(m.kind==='join') return '<b><font color="'+joinColor+'">'+escHtml(m.user)+' '+escHtml(m.text)+'</font></b><br>';
  if(m.kind==='leave') return '<i><font color="'+quitColor+'"><b>'+escHtml(m.user)+'</b> '+escHtml(m.text)+'</font></i><br>';
  if(m.kind==='whisper') return '<i><font color="#800080"><b>'+escHtml(m.user)+'</b> whispers to <b>'+escHtml(m.to)+'</b>: '+escHtml(m.text)+'</font></i><br>';
  if(m.kind==='action') return '<i>* <b>'+escHtml(m.user)+'</b> '+escHtml(m.text)+' *</i><br>';
  return '<b>'+escHtml(m.user)+':</b> '+escHtml(m.text)+'<br>';
}
function membersHtml(list){
  var others = list.map(function(u){return u.split(' (member)')[0];})
    .filter(function(u){return u !== me;});
  if(!others.length) return '(just you)';
  return others.map(function(u){
    var dot = voiceDot ? '<span style="display:inline-block;width:8px;height:8px;background:#663399;border-radius:50%%;"></span> ' : '';
    var pic = showDP ? '<span style="display:inline-block;width:16px;height:16px;background:'+avatarColor(u)+';border:1px solid #808080;vertical-align:middle;"></span> ' : '';
    return dot+pic+'<a href="#" onclick="return pmUser(this.textContent);" style="color:'+sideLink+';">'+escHtml(u)+'</a>';
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
function shakePane(){
  var c = document.getElementById('chat');
  var n = 0;
  var t = setInterval(function(){
    c.style.marginLeft = (n %% 2 ? '-4px' : '4px');
    if(++n > 5){ clearInterval(t); c.style.marginLeft = '0'; }
  }, 60);
}
var bubbles = {};
document.querySelectorAll('[data-bubble]').forEach(function(el){
  bubbles[el.getAttribute('data-bubble')] = el;
});
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
        if((m.kind==='say' || m.kind==='action') && bubbles[m.user]){
          var b = bubbles[m.user];
          b.textContent = m.text.length > 60 ? m.text.slice(0,60)+'...' : m.text;
          b.style.display = 'block';
        }
      });
      document.getElementById('members').innerHTML = membersHtml(data.presence);
      var su = document.getElementById('status-users');
      if(su) su.textContent = data.presence.length;
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
""" % (esc(info["name"]), skin["body"], skin["text"], skin["link"],
       skin["vlink"], masthead_html, skin["win"],
       skin["title"], title_style_attr, skin["fg"], title_marks,
       esc(info["name"]),
       skin["title"], title_style_attr, skin["fg"], tab_html,
       skin["chat_bg"], skin["chat_fg"], topic_html, notice_html,
       video_html, avatars_html, habbo_room_html,
       chat_style, lines, statusbar_html,
       side_bg, side_fg, top8_html, members, rooms_html,
       slug, send_btn, nudge_html,
       slug, action_opts, user_opts,
       skin["win"], skin["title"], skin["fg"], skin["title"], skin["fg"],
       slug,
       slug, history_opts,
       slug, esc(info["name"]),
       slug, esc(info["service"]), more,
       esc(sess["user"]), " (member)" if sess.get("member") else "",
       footer_html,
       last_id, slug, esc(sess["user"]),
       skin["join"], skin["quit"],
       "true" if skin["voice_dot"] else "false",
       "true" if skin["dp"] else "false",
       side_link)


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
<p><font size="-1"><i>This room is intended for adults 21 and over.</i></font></p>
<center>
<form action="/lobby" method="post">
Name: <input type="text" name="USER" size="12" maxlength="12"><br>
Password: <input type="password" name="PASSWORD" size="12" maxlength="12"><br>
<input type="hidden" name="MEMBER" value="1">
<input type="hidden" name="SAYS" value="<b>Joins The Lobby...</b>">
<input type="hidden" name="HISTORY" value="8">
<input type="checkbox" name="confirm" value="21"> I am 21 or older<br>
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
    def _handle_age_gate(self, form):
        """POST /age-gate -- the landing-page age gate (Paul, 2026-11-09):
        confirming 21+ sets the age_ok flag on the session (created if
        needed) and sends you to the chat directory. No age is stored,
        no ID is asked for -- a self-declared confirmation, the same
        as the original's certify button."""
        if form.get("confirm") != "21":
            self._redirect("/")
            return
        sid, sess = get_session(self)
        if sess is None:
            sid = new_sid()
            sess = {}
            with sessions_lock:
                sessions[sid] = sess
        sess["age_ok"] = True
        touch(sess)
        self._redirect("/chat.htm", sid=sid)

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
        # Age gate (Paul, 2026-11-09): entering a room confirms you are
        # 21 or older -- either you already passed the landing-page gate
        # (age_ok on the session) or this entry form's confirm checkbox
        # is checked. No age is stored, no ID is asked for.
        if not sess or not sess.get("age_ok"):
            if form.get("confirm") != "21":
                self._redirect("/")
                return
        if sess is None or sess.get("room") != slug:
            sid = new_sid()
            sess = {}
            with sessions_lock:
                sessions[sid] = sess
        sess.update(user=user, room=slug, member=member, history=history,
                    certified=(slug == "anything-goes" or
                               sess.get("certified", False)),
                    age_ok=True,
                    last_seen=time.time(), last_msg=0.0)
        db_add_message(slug, user, "join", says)
        self._redirect("/" + slug, sid=sid)

    # -- chat pane (GET /<room>)
    def _handle_room(self, slug, query):
        info = ROOMS[slug]
        sid, sess = get_session(self)
        if sess and sess.get("room") != slug and sess.get("user") \
                and "jump" in query:
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
        elif info.get("messenger"):
            self._send(200, render_messenger_room_page(slug, sess, msgs))
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
            # AOL colors/fonts (Paul, 2026-11-09, basic level): the
            # choice rides on the message and sticks in the session.
            # AOL room only -- other rooms never see these fields.
            color = font = None
            if ROOMS[slug].get("aol"):
                color = (form.get("color") or sess.get("color")
                         or "black").strip()
                font = (form.get("font") or sess.get("font")
                        or "Arial").strip()
                if color not in AOL_COLORS:
                    color = "black"
                if font not in AOL_FONTS:
                    font = "Arial"
                sess["color"] = color
                sess["font"] = font
                if color == "black" and font == "Arial":
                    color = font = None
            db_add_message(slug, sess["user"], "say", text,
                           color=color, font=font)
        if self._wants_json():
            self._json(200, {"ok": True})
        else:
            self._redirect("/" + slug)

    def _handle_action(self, slug, form):
        """POST /<room>/action -- a third-person action (Paul, 2026-11-09):
        pick a verb and a person in the room; posts
        "* user winks at target *". The verb is whitelisted and the
        target must be in the room (and not yourself), so no word filter
        is needed; a banned user still cannot act."""
        sid, sess = get_session(self)
        if not sess or sess.get("room") != slug:
            if self._wants_json():
                self._json(403, {"error": "not in this room"})
            else:
                self._redirect(ROOMS[slug]["entry"])
            return
        _, banned = strike_status(sess["user"])
        if banned:
            self._blocked_response(slug, banned=True)
            return
        verb = (form.get("action") or "").strip()
        target = (form.get("to") or "").strip()[:MAX_NAME]
        if verb not in ACTION_VERBS:
            self._redirect("/" + slug)
            return
        here = [u.split(" (member)")[0] for u in presence(slug)]
        if not target or target == sess["user"] or target not in here:
            self._redirect("/" + slug)
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
        db_add_message(slug, sess["user"], "action", verb + " " + target,
                       to_user=target)
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
        if path in ("/chat.htm", "/chat2.htm"):
            # the chat directories sit behind the age gate (Paul,
            # 2026-11-09): the landing page is the front door.
            _, sess = get_session(self)
            if not sess or not sess.get("age_ok"):
                self._redirect("/")
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
        if parts == ["age-gate"]:
            self._handle_age_gate(form)
            return
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
        if len(parts) >= 2 and parts[1] == "action" and self._room_or_none(parts[0]):
            self._handle_action(ALIASES.get(parts[0], parts[0]), form)
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
