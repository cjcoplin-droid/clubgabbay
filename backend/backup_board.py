#!/usr/bin/env python3
"""Back up Club Gabbay board posts to the repo (GitHub is the store).

The free host's disk is ephemeral: every restart/deploy wipes chat.db,
board posts included (Paul lost a post this way, 2026-11-09). This script
is the other half of the fix — it pulls GET /api/board/posts, merges new
posts into site-data/board-posts.json by id, and commits + pushes. The
server re-seeds an empty board from that file on boot
(BOARD_RESTORE_URL), so posts survive restarts.

Run by the board-backup hook every 5 minutes (and before any deploy).
Idempotent: no new posts -> no commit, exit 0. Exit 2 on failure
(fetch / git error) so the hook can count consecutive failures.

Stdlib only. No secrets: plain git push using the repo's existing auth.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

API_URL = "https://clubgabbay.onrender.com/api/board/posts"
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BACKUP_REL = os.path.join("site-data", "board-posts.json")


def fetch_posts(api_url):
    """GET the board posts; retry once (the free instance may be waking
    from sleep — first fetch can take ~50s)."""
    last_err = None
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(
                api_url, headers={"User-Agent": "ClubGabbay-board-backup/1.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.load(resp)["posts"]
        except Exception as e:  # noqa: BLE001 - retry once, then report
            last_err = e
            if attempt == 1:
                time.sleep(5)
    raise RuntimeError("board API fetch failed: %s" % last_err)


def load_backup(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("posts", data) if isinstance(data, dict) else data


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
        live = fetch_posts(args.api)
    except Exception as e:  # noqa: BLE001 - exit 2 so the hook counts it
        print("board backup FAILED: %s" % e)
        return 2
    saved = load_backup(backup_path)
    saved_ids = {p["id"] for p in saved if isinstance(p, dict)
                 and "id" in p}
    new = [p for p in live if p.get("id") not in saved_ids]
    if not new:
        print("board backup: no new posts (%d saved)" % len(saved))
        return 0
    # merge by id, live wins on refresh (a post's stored copy stays
    # current if its board or text ever changes server-side)
    by_id = {p["id"]: p for p in saved if isinstance(p, dict)
             and "id" in p}
    by_id.update({p["id"]: p for p in live if isinstance(p, dict)
                  and "id" in p})
    merged = sorted(by_id.values(), key=lambda p: p["id"])
    if args.dry_run:
        print("board backup DRY RUN: would add %d post(s), %d total"
              % (len(new), len(merged)))
        return 0
    # Sync just the backup file with the remote first. The hook is the
    # only writer of this file, but the working tree is often dirty with
    # unrelated work — a plain `git pull --rebase` would refuse, so sync
    # the one file instead (a failed sync just means the next run retries).
    try:
        git(repo, "fetch", "origin", "main")
        git(repo, "checkout", "origin/main", "--", BACKUP_REL)
    except Exception:
        pass  # remote file may not exist yet; continue with local copy
    saved = load_backup(backup_path)  # re-read after the sync
    saved_ids = {p["id"] for p in saved if isinstance(p, dict)
                 and "id" in p}
    new = [p for p in live if p.get("id") not in saved_ids]
    if not new:
        print("board backup: no new posts after sync (%d saved)"
              % len(saved))
        return 0
    by_id = {p["id"]: p for p in saved if isinstance(p, dict)
             and "id" in p}
    by_id.update({p["id"]: p for p in live if isinstance(p, dict)
                  and "id" in p})
    merged = sorted(by_id.values(), key=lambda p: p["id"])
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump({"posts": merged}, fh, indent=2, ensure_ascii=True)
        fh.write("\n")
    try:
        git(repo, "add", BACKUP_REL)
        git(repo, "commit", "-m",
            "board backup: %d new post(s), %d total"
            % (len(new), len(merged)))
        git(repo, "push", "origin", "main")
    except Exception as e:  # noqa: BLE001 - file is written; next run retries
        print("board backup FAILED: %s" % e)
        return 2
    print("board backup: saved %d new post(s), %d total"
          % (len(new), len(merged)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
