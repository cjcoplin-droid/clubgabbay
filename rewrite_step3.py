#!/usr/bin/env python3
"""Club Gabbay mirror — spec step 3: rewrite absolute clubgabbay.com links
to relative paths inside the mirror tree (site/).

Rules (from mirror-build-spec.md step 3 + chat-backend-design.md room routing):
- clubgabbay.com-host URLs (any subdomain, port 80/None) resolve via the
  inventory (mirror-inventory.json) to a site_path; rewrite to a path
  relative to the containing file. Query strings and fragments preserved.
- Directory URLs (trailing /) resolve to that dir's index.html/index.htm.
- Chat-server endpoints (form actions to ports 2000-2080, or the two chat
  IPs 198.147.75.30 / 204.7.247.51) are NOT static files: rewrite to the
  backend room route /<slug> per chat-backend-design.md, with the slug taken
  from the containing room page's filename (anything_goes -> anything-goes).
- chat.clubgabbay.com:88/cgi-bin/guestbook is the guestbook: rewrite to the
  archived guestbook file (manual alias).
- cgi-bin queue/queue?forum=... has no archived file: left as-is, logged.
- External hosts (linkexchange, bookshop, nethaus, ...) are NOT touched.
- Unresolvable clubgabbay.com URLs are left as-is and logged.

Outputs: rewrites site/ in place; writes rewrite_step3_report.json.
"""
import json, os, re, sys

BASE = os.path.expanduser("~/workspace/geocities-revival")
SITE = os.path.join(BASE, "site")
INV = os.path.join(BASE, "mirror-inventory.json")

inv = json.load(open(INV))
lookup = {}
for e in inv:
    u = e["url"]
    m = re.match(r"https?://([^/:]+)(?::\d+)?(/.*)$", u)
    if not m:
        continue
    host, path = m.group(1).lower(), m.group(2)
    lookup[(host, path)] = e["site_path"]

ALIASES = {
    ("chat.clubgabbay.com", "/cgi-bin/guestbook"):
        "www.clubgabbay.com/cgi-bin/clubgabbay/guestbook",
}

ROOM_SLUGS = {
    "blue": "blue", "classical": "classical", "denim": "denim",
    "hard": "hard", "jive": "jive", "lobby": "lobby",
    "paradise": "paradise", "soul": "soul", "speakeasy": "speakeasy",
    "jokeland": "jokeland", "anything_goes": "anything-goes",
    "anything-goes": "anything-goes",
}

CHAT_IPS = {"198.147.75.30", "204.7.247.51"}
CHAT_PORTS = set(range(2000, 2081)) | {88}

URL_RE = re.compile(
    r"https?://[A-Za-z0-9._:-]+(?:/[^\s\"'<>]*)?")

def is_mirror_host(host):
    h = host.lower()
    return h == "clubgabbay.com" or h.endswith(".clubgabbay.com") or h in CHAT_IPS

def parse_url(u):
    m = re.match(r"(https?)://([^/:?#]+)(?::(\d+))?([^?#]*)(\?[^#]*)?(#.*)?$", u)
    if not m:
        return None
    scheme, host, port, path, query, frag = m.groups()
    return {"scheme": scheme, "host": host.lower(), "port": int(port) if port else None,
            "path": path or "/", "query": query or "", "frag": frag or ""}

def resolve(host, path):
    """Return (site_path, note) or (None, reason). note='cross-host' when the
    file was found under a different host than the link named (1996-era
    host moves: the archived copy lives under the bare host while the link
    names www). 'ambiguous' when the same path exists under >1 host."""
    if (host, path) in lookup:
        return lookup[(host, path)], None
    if (host, path) in ALIASES:
        return ALIASES[(host, path)], "alias"
    for p in ([path] if path.endswith("/") else [path, path + "/"]):
        for idx in ("index.html", "index.htm"):
            if (host, p + idx) in lookup:
                return lookup[(host, p + idx)], None
        cand = os.path.join(SITE, host, p.lstrip("/"))
        if os.path.isfile(cand):
            return host + "/" + p.lstrip("/"), None
        for idx in ("index.html", "index.htm"):
            if os.path.isfile(os.path.join(cand, idx)):
                return host + "/" + p.lstrip("/") + idx, None
    cands = {v for (h, p), v in lookup.items() if p == path}
    if len(cands) == 1:
        return next(iter(cands)), "cross-host"
    if len(cands) > 1:
        return None, "ambiguous across hosts: " + ", ".join(sorted(cands))
    return None, "no inventory entry and no file on disk"

def room_slug_for(path):
    stem = os.path.splitext(os.path.basename(path))[0].lower()
    return ROOM_SLUGS.get(stem)

report = {"files_changed": [], "rewritten": 0, "unresolved": [],
          "chat_routes": [], "left_external": 0, "per_file": {}}
TEXT_EXTS = None  # content-based: skip known binaries, skip NUL-containing files
BINARY_EXTS = {".jpg", ".jpeg", ".gif", ".png", ".JPG", ".ico", ".pdf", ".zip", ".gz"}

for root, dirs, files in os.walk(SITE):
    for fn in files:
        fpath = os.path.join(root, fn)
        ext = os.path.splitext(fn)[1].lower()
        if ext in BINARY_EXTS:
            continue
        try:
            with open(fpath, "rb") as f:
                raw = f.read()
        except OSError:
            continue
        if b"\x00" in raw[:4096]:
            continue
        try:
            text = raw.decode("utf-8")
            enc = "utf-8"
        except UnicodeDecodeError:
            try:
                text = raw.decode("latin-1")
                enc = "latin-1"
            except Exception:
                continue
        if "clubgabbay.com" not in text and "198.147.75.30" not in text \
                and "204.7.247.51" not in text:
            continue

        changed = [0]
        def repl(m):
            u = m.group(0)
            p = parse_url(u)
            if not p or not is_mirror_host(p["host"]):
                report["left_external"] += 1
                return u
            # chat endpoint: port in chat range or chat IP
            if (p["port"] in CHAT_PORTS) or (p["host"] in CHAT_IPS):
                # guestbook alias on :88
                if (p["host"], p["path"]) in ALIASES:
                    tgt = ALIASES[(p["host"], p["path"])]
                    rel = os.path.relpath(os.path.join(SITE, tgt),
                                          start=os.path.dirname(fpath))
                    changed[0] += 1
                    report["chat_routes"].append(
                        {"file": os.path.relpath(fpath, SITE), "url": u,
                         "to": rel.replace(os.sep, "/") + p["query"] + p["frag"]})
                    return rel.replace(os.sep, "/") + p["query"] + p["frag"]
                slug = room_slug_for(fpath)
                if slug:
                    rel = os.path.relpath(os.path.join(SITE, slug),
                                          start=os.path.dirname(fpath))
                    changed[0] += 1
                    report["chat_routes"].append(
                        {"file": os.path.relpath(fpath, SITE), "url": u,
                         "to": rel.replace(os.sep, "/")})
                    return rel.replace(os.sep, "/")
                report["unresolved"].append(
                    {"file": os.path.relpath(fpath, SITE), "url": u,
                     "why": "chat endpoint, no room slug for this file"})
                return u
            tgt, note = resolve(p["host"], p["path"])
            if tgt is None:
                report["unresolved"].append(
                    {"file": os.path.relpath(fpath, SITE), "url": u,
                     "why": note})
                return u
            if note == "cross-host":
                report.setdefault("cross_host", []).append(
                    {"file": os.path.relpath(fpath, SITE), "url": u,
                     "to": tgt})
            rel = os.path.relpath(os.path.join(SITE, tgt),
                                  start=os.path.dirname(fpath))
            rel = rel.replace(os.sep, "/")
            q = p["query"]
            if q == "?":
                q = ""
            changed[0] += 1
            return rel + q + p["frag"]

        new_text = URL_RE.sub(repl, text)
        if changed[0]:
            with open(fpath, "w", encoding=enc, newline="") as f:
                f.write(new_text)
            rel_f = os.path.relpath(fpath, SITE)
            report["files_changed"].append(rel_f)
            report["per_file"][rel_f] = changed[0]
            report["rewritten"] += changed[0]

with open(os.path.join(BASE, "rewrite_step3_report.json"), "w") as f:
    json.dump(report, f, indent=1)

print(f"files_changed={len(report['files_changed'])} links_rewritten={report['rewritten']}")
print(f"chat_routes={len(report['chat_routes'])} unresolved={len(report['unresolved'])} external_left={report['left_external']} cross_host={len(report.get('cross_host', []))}")
for u in report["unresolved"]:
    print("UNRESOLVED", u["file"], "|", u["url"], "|", u["why"])
for c in report["chat_routes"]:
    print("CHAT", c["file"], "|", c["url"], "->", c["to"])
