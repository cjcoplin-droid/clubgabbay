#!/usr/bin/env python3
"""Back up the Club Gabbay visitor counter to the repo (GitHub is the
store).

The free host's disk is ephemeral: every restart/deploy wipes chat.db,
the visits table included — the unique count would reset to the last
committed baseline. This script is the other half of the fix — it pulls
GET /api/visits, writes the unique count into site-data/visits.json,
and commits + pushes when the count grew. The server re-seeds its
baseline from that file on boot, so the counter survives restarts.

Run by the visits-backup hook every 5 minutes (and before any deploy).
Idempotent: count unchanged -> no commit, exit 0. Exit 2 on failure
(fetch / git error) so the hook can count consecutive failures.

Stdlib only. No secrets: plain git push using the repo's existing auth.
Only the total count is stored — never visitor IPs (those live only in
the server's ephemeral visits table, salted + hashed).
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

API_URL = "https://clubgabbay.onrender.com/api/visits"
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BACKUP_REL = os.path.join("site-data", "visits.json")


def fetch_visits(api_url):
    """GET the visit counts; retry once (the free instance may be waking
    from sleep — first fetch can take ~50s)."""
    last_err = None
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(
                api_url, headers={"User-Agent": "ClubGabbay-visits-backup/1.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.load(resp)
        except Exception as e:  # noqa: BLE001 - retry once, then report
            last_err = e
            if attempt == 1:
                time.sleep(5)
    raise RuntimeError("visits API fetch failed: %s" % last_err)


def load_backup(path):
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    try:
        return int(data.get("unique", 0))
    except (TypeError, ValueError):
        return 0


def git(repo, *args):
    r = subprocess.run(["git", "-c", "user.name=Paul Orbeck",
                        "-c", "user.email=cjcoplin@gmail.com"] + list(args),
                       cwd=repo, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (
            " ".join(args), (r.stderr or r.stdout).strip()[-300:]))
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api", default=API_URL)
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--dry-run", action="store_true",
                    help="fetch + compare only; write nothing, commit nothing")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    backup_path = os.path.join(repo, BACKUP_REL)

    try:
        live = fetch_visits(args.api)
    except Exception as e:  # noqa: BLE001 - exit 2 so the hook counts it
        print("visits backup FAILED: %s" % e)
        return 2
    try:
        live_unique = int(live.get("unique", 0))
    except (TypeError, ValueError):
        print("visits backup FAILED: bad API payload %r" % (live,))
        return 2
    saved = load_backup(backup_path)
    if live_unique <= saved:
        print("visits backup: no growth (%d unique saved)" % saved)
        return 0
    if args.dry_run:
        print("visits backup DRY RUN: would save %d unique (was %d)"
              % (live_unique, saved))
        return 0
    # Sync just the backup file with the remote first (same as the board
    # backup — the working tree is often dirty with unrelated work).
    try:
        git(repo, "fetch", "origin", "main")
        git(repo, "checkout", "origin/main", "--", BACKUP_REL)
    except Exception:
        pass  # remote file may not exist yet; continue with local copy
    saved = load_backup(backup_path)  # re-read after the sync
    if live_unique <= saved:
        print("visits backup: no growth after sync (%d unique saved)" % saved)
        return 0
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump({"unique": live_unique}, fh, indent=2)
        fh.write("\n")
    try:
        git(repo, "add", BACKUP_REL)
        git(repo, "commit", "-m",
            "visits backup: %d unique visitor(s)" % live_unique)
        git(repo, "push", "origin", "main")
    except Exception as e:  # noqa: BLE001 - file is written; next run retries
        print("visits backup FAILED: %s" % e)
        return 2
    print("visits backup: saved %d unique visitor(s) (was %d)"
          % (live_unique, saved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
