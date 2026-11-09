#!/usr/bin/env python3
"""Build the retro chat service landing pages, one per service (Paul,
2026-11-09: the same setup for each one -- a clear landing page with a
21+ age gate and a handle form, then a chat room on the same engine).

The service data lives in server.py (SERVICES) -- one source of truth.
Run from the repo root: python3 backend/build_services.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server import SERVICES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "www2.clubgabbay.com")


def page(s, all_services):
    links = " | ".join(
        '<a href="/%s.html">%s</a>' % (t["slug"], t["name"])
        for t in all_services)
    return """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>

<head>
<meta http-equiv="Content-Type"
content="text/html; charset=iso-8859-1">
<title>%(name)s Chat</title>
</head>

<body background="../clubgabbay.com/images/bg/home_bg.jpg">
<center><font size="+3"><strong>%(name)s</strong></font></center>
<center><font size="+1">%(desc)s</font></center>
<p>
<center>
<font size="+1"><strong>This room is intended for adults 21 and over.</strong></font><br>
<font size="-1">By entering, you confirm that you are at least 21 years of age.
If you are under 21, please do not enter.</font>
</center>
<p>
<center>
<form action="/%(slug)s-chat" method="post">
Your handle: <input type="text" name="USER" size="12" maxlength="12"><br>
Show last <select name="HISTORY"><option value="8" selected>8</option><option value="16">16</option><option value="32">32</option></select> messages<br>
<input type="hidden" name="SAYS" value="%(join)s">
<input type="checkbox" name="confirm" value="21"> I am 21 or older<br>
<input type="submit" value="Enter the chat">
</form>
</center>
<center><font size="-1"><i>This room is intended for adults 21 and over.</i></font></center>
<hr noshade>
<center><font size="-1">More retro chat: %(links)s<br>
<a href="/">Club Gabbay Home</a> | <a href="/fine-print.html">Fine print</a></font></center>
<hr noshade>
<center><font color=gray size=2>%(name)s Chat -- a fan-made tribute to the 1990s. Not affiliated with the original owners.</font></center>
</body>
</html>
""" % {"slug": s["slug"], "name": s["name"], "desc": s["desc"],
       "join": s["join"], "links": links}


def main():
    for s in SERVICES:
        path = os.path.join(OUT, s["slug"] + ".html")
        text = page(s, SERVICES)
        assert all(ord(ch) < 128 for ch in text), s["slug"]
        with open(path, "w", encoding="latin-1", newline="") as fh:
            fh.write(text)
        print("wrote", path)


if __name__ == "__main__":
    main()
