# Club Gabbay mirror — backend test report (spec step 5)

Test run: 2026-11-09 09:50 MST (local only, http://127.0.0.1:8124, scratch DB test-chat.db)
Backend: `backend/server.py` (stdlib-only Python), test: `backend/test_backend.py`.

## Summary

- Checks run: 190 — **190 PASS, 0 FAIL**
- Rooms walked: 11 of 11 (lobby, blue, speakeasy, denim, hard, soul, jive, classical, paradise, anything-goes, jokeland)

## Per-room results

| Room | Check | Result | Detail |
|---|---|---|---|
| lobby | member entry /lobby2.cfm 200 | PASS | status=200 |
| lobby | entry page /www2.clubgabbay.com/lobby.cfm 200 | PASS | status=200 |
| lobby | GET /lobby w/o session redirects to entry page | PASS | status=303 loc=/www2.clubgabbay.com/lobby.cfm |
| lobby | guest entry POST redirects to /lobby | PASS | status=200 |
| lobby | chat pane shows join line + room name | PASS | status=200 |
| lobby | post a message (303 back to room) | PASS | status=200 |
| lobby | poll API returns posted message | PASS | found=1 |
| lobby | presence lists the chatter | PASS |  |
| lobby | HISTORY=8 caps initial pane at 8 | PASS | n=2 |
| lobby | jump to /blue keeps session, redirects | PASS | status=200 |
| lobby | jump posts join line in blue | PASS |  |
| lobby | leave blue redirects to chat directory | PASS | status=200 |
| blue | entry page /www.clubgabbay.com/htmls/blue.html 200 | PASS | status=200 |
| blue | GET /blue w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/blue.html |
| blue | guest entry POST redirects to /blue | PASS | status=200 |
| blue | chat pane shows join line + room name | PASS | status=200 |
| blue | post a message (303 back to room) | PASS | status=200 |
| blue | poll API returns posted message | PASS | found=1 |
| blue | presence lists the chatter | PASS |  |
| blue | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| blue | jump to /speakeasy keeps session, redirects | PASS | status=200 |
| blue | jump posts join line in speakeasy | PASS |  |
| blue | leave speakeasy redirects to chat directory | PASS | status=200 |
| speakeasy | entry page /www.clubgabbay.com/htmls/speakeasy.html 200 | PASS | status=200 |
| speakeasy | GET /speakeasy w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/speakeasy.html |
| speakeasy | guest entry POST redirects to /speakeasy | PASS | status=200 |
| speakeasy | chat pane shows join line + room name | PASS | status=200 |
| speakeasy | post a message (303 back to room) | PASS | status=200 |
| speakeasy | poll API returns posted message | PASS | found=1 |
| speakeasy | presence lists the chatter | PASS |  |
| speakeasy | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| speakeasy | jump to /denim keeps session, redirects | PASS | status=200 |
| speakeasy | jump posts join line in denim | PASS |  |
| speakeasy | leave denim redirects to chat directory | PASS | status=200 |
| denim | entry page /www.clubgabbay.com/htmls/denim.html 200 | PASS | status=200 |
| denim | GET /denim w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/denim.html |
| denim | guest entry POST redirects to /denim | PASS | status=200 |
| denim | chat pane shows join line + room name | PASS | status=200 |
| denim | post a message (303 back to room) | PASS | status=200 |
| denim | poll API returns posted message | PASS | found=1 |
| denim | presence lists the chatter | PASS |  |
| denim | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| denim | jump to /hard keeps session, redirects | PASS | status=200 |
| denim | jump posts join line in hard | PASS |  |
| denim | leave hard redirects to chat directory | PASS | status=200 |
| hard | entry page /www.clubgabbay.com/htmls/hard.html 200 | PASS | status=200 |
| hard | GET /hard w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/hard.html |
| hard | guest entry POST redirects to /hard | PASS | status=200 |
| hard | chat pane shows join line + room name | PASS | status=200 |
| hard | post a message (303 back to room) | PASS | status=200 |
| hard | poll API returns posted message | PASS | found=1 |
| hard | presence lists the chatter | PASS |  |
| hard | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| hard | jump to /soul keeps session, redirects | PASS | status=200 |
| hard | jump posts join line in soul | PASS |  |
| hard | leave soul redirects to chat directory | PASS | status=200 |
| soul | entry page /www.clubgabbay.com/htmls/soul.html 200 | PASS | status=200 |
| soul | GET /soul w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/soul.html |
| soul | guest entry POST redirects to /soul | PASS | status=200 |
| soul | chat pane shows join line + room name | PASS | status=200 |
| soul | post a message (303 back to room) | PASS | status=200 |
| soul | poll API returns posted message | PASS | found=1 |
| soul | presence lists the chatter | PASS |  |
| soul | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| soul | jump to /jive keeps session, redirects | PASS | status=200 |
| soul | jump posts join line in jive | PASS |  |
| soul | leave jive redirects to chat directory | PASS | status=200 |
| jive | entry page /www.clubgabbay.com/htmls/jive.html 200 | PASS | status=200 |
| jive | GET /jive w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/jive.html |
| jive | guest entry POST redirects to /jive | PASS | status=200 |
| jive | chat pane shows join line + room name | PASS | status=200 |
| jive | post a message (303 back to room) | PASS | status=200 |
| jive | poll API returns posted message | PASS | found=1 |
| jive | presence lists the chatter | PASS |  |
| jive | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| jive | jump to /classical keeps session, redirects | PASS | status=200 |
| jive | jump posts join line in classical | PASS |  |
| jive | leave classical redirects to chat directory | PASS | status=200 |
| classical | entry page /www.clubgabbay.com/htmls/classical.html 200 | PASS | status=200 |
| classical | GET /classical w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/classical.html |
| classical | guest entry POST redirects to /classical | PASS | status=200 |
| classical | chat pane shows join line + room name | PASS | status=200 |
| classical | post a message (303 back to room) | PASS | status=200 |
| classical | poll API returns posted message | PASS | found=1 |
| classical | presence lists the chatter | PASS |  |
| classical | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| classical | jump to /paradise keeps session, redirects | PASS | status=200 |
| classical | jump posts join line in paradise | PASS |  |
| classical | leave paradise redirects to chat directory | PASS | status=200 |
| paradise | entry page /www.clubgabbay.com/htmls/paradise.html 200 | PASS | status=200 |
| paradise | GET /paradise w/o session redirects to entry page | PASS | status=303 loc=/www.clubgabbay.com/htmls/paradise.html |
| paradise | guest entry POST redirects to /paradise | PASS | status=200 |
| paradise | chat pane shows join line + room name | PASS | status=200 |
| paradise | post a message (303 back to room) | PASS | status=200 |
| paradise | poll API returns posted message | PASS | found=1 |
| paradise | presence lists the chatter | PASS |  |
| paradise | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| paradise | jump to /anything-goes keeps session, redirects | PASS | status=200 |
| paradise | jump posts join line in anything-goes | PASS |  |
| paradise | leave anything-goes redirects to chat directory | PASS | status=200 |
| anything-goes | entry page /www2.clubgabbay.com/anything_goes.cfm 200 | PASS | status=200 |
| anything-goes | GET /anything-goes w/o session redirects to entry page | PASS | status=303 loc=/www2.clubgabbay.com/anything_goes.cfm |
| anything-goes | guest entry POST redirects to /anything-goes | PASS | status=200 |
| anything-goes | chat pane shows join line + room name | PASS | status=200 |
| anything-goes | post a message (303 back to room) | PASS | status=200 |
| anything-goes | poll API returns posted message | PASS | found=1 |
| anything-goes | presence lists the chatter | PASS |  |
| anything-goes | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| anything-goes | jump to /jokeland keeps session, redirects | PASS | status=200 |
| anything-goes | jump posts join line in jokeland | PASS |  |
| anything-goes | leave jokeland redirects to chat directory | PASS | status=200 |
| jokeland | entry page /www2.clubgabbay.com/jokeland.cfm 200 | PASS | status=200 |
| jokeland | GET /jokeland w/o session redirects to entry page | PASS | status=303 loc=/www2.clubgabbay.com/jokeland.cfm |
| jokeland | guest entry POST redirects to /jokeland | PASS | status=200 |
| jokeland | chat pane shows join line + room name | PASS | status=200 |
| jokeland | post a message (303 back to room) | PASS | status=200 |
| jokeland | poll API returns posted message | PASS | found=1 |
| jokeland | presence lists the chatter | PASS |  |
| jokeland | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| jokeland | jump to /lobby keeps session, redirects | PASS | status=200 |
| jokeland | jump posts join line in lobby | PASS |  |
| jokeland | leave lobby redirects to chat directory | PASS | status=200 |
| lobby | guest form (archived Guest1251) redirects to /lobby | PASS | status=200 |
| lobby | guest gets fresh auto-name GuestNNNN (not literal 1251) | PASS | names=['Tlobby', 'Tlobby', 'Tjokeland', 'Tjokeland', 'Guest4178'] |
| lobby | member entry flagged (member) in presence | PASS | presence=['Guest4178', 'TestMember (member)'] |
| lobby | HISTORY=8 shows exactly last 8 of 12 posted | PASS | shown=['hist-msg-04', 'hist-msg-05', 'hist-msg-06', 'hist-msg-07', 'hist-msg-08', 'hist-msg-09', 'hist-msg-10', 'hist-msg-11'] |
| lobby | rate limit: 2nd post within 2s is 429 | PASS | first=200 second=429 |
| blue | whisper visible to sender + recipient only, not others | PASS | {'sender': True, 'recipient': True, 'other': False} |
| anything-goes | GET /anything-goes w/o session redirects to gate | PASS | status=303 loc=/www2.clubgabbay.com/anything_goes.cfm |
| filter | banned word in public message is blocked (403) | PASS | status=403 |
| filter | blocked message never stored/shown | PASS |  |
| filter | clean message passes after one strike | PASS | status=200 |
| filter | clean message is stored | PASS |  |
| filter | innocent word (class) is not blocked | PASS | status=200 |
| filter | spaced-out evasion is still caught (403) | PASS | status=403 |
| filter | three blocked posts all return 403 | PASS | statuses=[403, 403, 403] |
| filter | 3 strikes -> banned: clean message rejected (403) | PASS | status=403 |
| filter | banned user's clean message never stored | PASS |  |
| filter | ban is per-user: another user posts fine | PASS | status=200 |
| filter | whisper with banned word passes unfiltered | PASS | status=200 |
| filter | whisper with banned word is delivered to recipient | PASS |  |
| board | board page has post form + 1997 archive | PASS | status=200 |
| board | clean board post accepted | PASS | status=200 |
| board | new post shows above the 1997 archive | PASS |  |
| board | markup post accepted (stored, escaped at render) | PASS | status=200 |
| board | markup in a post is escaped, never rendered | PASS |  |
| board | banned word in board post is blocked (403) | PASS | status=403 |
| board | blocked board post never stored/shown | PASS |  |
| board | three blocked board posts all return 403 | PASS | statuses=[403, 403, 403] |
| board | 3 strikes -> banned from board: clean post rejected | PASS | status=403 |
| board | post with no From name is not stored | PASS |  |
| filter | blocklist is not served over HTTP (/blocklist.txt 404) | PASS | status=404 |
| filter | blocklist is not served (/backend/blocklist.txt 404) | PASS | status=404 |
| board | board post survives server restart (stays up) | PASS | found=True |

## Site / cross-cutting results

| Check | Result | Detail |
|---|---|---|
| homepage / returns 200 + Enter ClubGabbay -> /chat.htm, no webdates/email/linkexchange (Paul 2026-11-09) | PASS | status=200 |
| /main.htm removed 404 (Paul 2026-11-09) | PASS | status=404 |
| /welcome.htm removed 404 (Paul 2026-11-09) | PASS | status=404 |
| /menu.cfm removed 404 (Paul 2026-11-09) | PASS | status=404 |
| /webdates.cfm removed 404 (Paul 2026-11-09) | PASS | status=404 |
| bulletin board 200, no linkexchange (Paul 2026-11-09) | PASS | status=200 |
| calendar footer has no webdates/mall links | PASS | status=200 |
| /htmls/webdates.html removed 404 (Paul 2026-11-09) | PASS | status=404 |
| /chat.htm directory 200 | PASS | status=200 |
| /chat2.htm rooms list 200 | PASS | status=200 |
| image /images/bg/lobby_bg.jpg loads | PASS | status=200 |
| image /images/lobby.jpg loads | PASS | status=200 |
| image /images/bg/speak_bg.jpg loads | PASS | status=200 |
| image /images/speakeasy.jpg loads | PASS | status=200 |
| image /images/bg/denim_bg.jpg loads | PASS | status=200 |
| image /images/denim.jpg loads | PASS | status=200 |
| image /images/bg/classical_bg.jpg loads | PASS | status=200 |
| image /images/classical.jpg loads | PASS | status=200 |
| image /images/blue.jpg loads | PASS | status=200 |
| image /images/rock.jpg loads | PASS | status=200 |
| image /images/jive_talkin.jpg loads | PASS | status=200 |
| image /images/paradise.jpg loads | PASS | status=200 |
| image /images/soul_searching.jpg loads | PASS | status=200 |
| image /anything_goes.jpg loads | PASS | status=200 |
| image /images/bg/home_bg.jpg loads | PASS | status=200 |
| known archive gap /images/bg/blue_bg.jpg returns 404 (expected) | PASS | status=404 |
| known archive gap /images/bg/hard_bg.jpg returns 404 (expected) | PASS | status=404 |
| known archive gap /images/bg/jive_bg.jpg returns 404 (expected) | PASS | status=404 |
| known archive gap /images/bg/paradise_bg.jpg returns 404 (expected) | PASS | status=404 |
| known archive gap /images/bg/soulsearch_bg.jpg returns 404 (expected) | PASS | status=404 |
| homepage carries the approved blurb | PASS |  |
| homepage notes monitoring / 18+ / private whispers | PASS |  |
| link check / (2 links): server matches archive | PASS | all resolve |
| link check /chat.htm (8 links): server matches archive | PASS | pre-existing archive gaps (404, expected): ['lobby_sm.jpg'] |
| link check /chat2.htm (33 links): server matches archive | PASS | all resolve |
| message survives server restart (SQLite persistence) | PASS | found=True |

## What passed

- site — homepage / returns 200 + Enter ClubGabbay -> /chat.htm, no webdates/email/linkexchange (Paul 2026-11-09)
- site — /main.htm removed 404 (Paul 2026-11-09)
- site — /welcome.htm removed 404 (Paul 2026-11-09)
- site — /menu.cfm removed 404 (Paul 2026-11-09)
- site — /webdates.cfm removed 404 (Paul 2026-11-09)
- site — bulletin board 200, no linkexchange (Paul 2026-11-09)
- site — calendar footer has no webdates/mall links
- site — /htmls/webdates.html removed 404 (Paul 2026-11-09)
- site — /chat.htm directory 200
- site — /chat2.htm rooms list 200
- site — image /images/bg/lobby_bg.jpg loads
- site — image /images/lobby.jpg loads
- site — image /images/bg/speak_bg.jpg loads
- site — image /images/speakeasy.jpg loads
- site — image /images/bg/denim_bg.jpg loads
- site — image /images/denim.jpg loads
- site — image /images/bg/classical_bg.jpg loads
- site — image /images/classical.jpg loads
- site — image /images/blue.jpg loads
- site — image /images/rock.jpg loads
- site — image /images/jive_talkin.jpg loads
- site — image /images/paradise.jpg loads
- site — image /images/soul_searching.jpg loads
- site — image /anything_goes.jpg loads
- site — image /images/bg/home_bg.jpg loads
- site — known archive gap /images/bg/blue_bg.jpg returns 404 (expected)
- site — known archive gap /images/bg/hard_bg.jpg returns 404 (expected)
- site — known archive gap /images/bg/jive_bg.jpg returns 404 (expected)
- site — known archive gap /images/bg/paradise_bg.jpg returns 404 (expected)
- site — known archive gap /images/bg/soulsearch_bg.jpg returns 404 (expected)
- lobby — member entry /lobby2.cfm 200
- lobby — entry page /www2.clubgabbay.com/lobby.cfm 200
- lobby — GET /lobby w/o session redirects to entry page
- lobby — guest entry POST redirects to /lobby
- lobby — chat pane shows join line + room name
- lobby — post a message (303 back to room)
- lobby — poll API returns posted message
- lobby — presence lists the chatter
- lobby — HISTORY=8 caps initial pane at 8
- lobby — jump to /blue keeps session, redirects
- lobby — jump posts join line in blue
- lobby — leave blue redirects to chat directory
- blue — entry page /www.clubgabbay.com/htmls/blue.html 200
- blue — GET /blue w/o session redirects to entry page
- blue — guest entry POST redirects to /blue
- blue — chat pane shows join line + room name
- blue — post a message (303 back to room)
- blue — poll API returns posted message
- blue — presence lists the chatter
- blue — HISTORY=8 caps initial pane at 8
- blue — jump to /speakeasy keeps session, redirects
- blue — jump posts join line in speakeasy
- blue — leave speakeasy redirects to chat directory
- speakeasy — entry page /www.clubgabbay.com/htmls/speakeasy.html 200
- speakeasy — GET /speakeasy w/o session redirects to entry page
- speakeasy — guest entry POST redirects to /speakeasy
- speakeasy — chat pane shows join line + room name
- speakeasy — post a message (303 back to room)
- speakeasy — poll API returns posted message
- speakeasy — presence lists the chatter
- speakeasy — HISTORY=8 caps initial pane at 8
- speakeasy — jump to /denim keeps session, redirects
- speakeasy — jump posts join line in denim
- speakeasy — leave denim redirects to chat directory
- denim — entry page /www.clubgabbay.com/htmls/denim.html 200
- denim — GET /denim w/o session redirects to entry page
- denim — guest entry POST redirects to /denim
- denim — chat pane shows join line + room name
- denim — post a message (303 back to room)
- denim — poll API returns posted message
- denim — presence lists the chatter
- denim — HISTORY=8 caps initial pane at 8
- denim — jump to /hard keeps session, redirects
- denim — jump posts join line in hard
- denim — leave hard redirects to chat directory
- hard — entry page /www.clubgabbay.com/htmls/hard.html 200
- hard — GET /hard w/o session redirects to entry page
- hard — guest entry POST redirects to /hard
- hard — chat pane shows join line + room name
- hard — post a message (303 back to room)
- hard — poll API returns posted message
- hard — presence lists the chatter
- hard — HISTORY=8 caps initial pane at 8
- hard — jump to /soul keeps session, redirects
- hard — jump posts join line in soul
- hard — leave soul redirects to chat directory
- soul — entry page /www.clubgabbay.com/htmls/soul.html 200
- soul — GET /soul w/o session redirects to entry page
- soul — guest entry POST redirects to /soul
- soul — chat pane shows join line + room name
- soul — post a message (303 back to room)
- soul — poll API returns posted message
- soul — presence lists the chatter
- soul — HISTORY=8 caps initial pane at 8
- soul — jump to /jive keeps session, redirects
- soul — jump posts join line in jive
- soul — leave jive redirects to chat directory
- jive — entry page /www.clubgabbay.com/htmls/jive.html 200
- jive — GET /jive w/o session redirects to entry page
- jive — guest entry POST redirects to /jive
- jive — chat pane shows join line + room name
- jive — post a message (303 back to room)
- jive — poll API returns posted message
- jive — presence lists the chatter
- jive — HISTORY=8 caps initial pane at 8
- jive — jump to /classical keeps session, redirects
- jive — jump posts join line in classical
- jive — leave classical redirects to chat directory
- classical — entry page /www.clubgabbay.com/htmls/classical.html 200
- classical — GET /classical w/o session redirects to entry page
- classical — guest entry POST redirects to /classical
- classical — chat pane shows join line + room name
- classical — post a message (303 back to room)
- classical — poll API returns posted message
- classical — presence lists the chatter
- classical — HISTORY=8 caps initial pane at 8
- classical — jump to /paradise keeps session, redirects
- classical — jump posts join line in paradise
- classical — leave paradise redirects to chat directory
- paradise — entry page /www.clubgabbay.com/htmls/paradise.html 200
- paradise — GET /paradise w/o session redirects to entry page
- paradise — guest entry POST redirects to /paradise
- paradise — chat pane shows join line + room name
- paradise — post a message (303 back to room)
- paradise — poll API returns posted message
- paradise — presence lists the chatter
- paradise — HISTORY=8 caps initial pane at 8
- paradise — jump to /anything-goes keeps session, redirects
- paradise — jump posts join line in anything-goes
- paradise — leave anything-goes redirects to chat directory
- anything-goes — entry page /www2.clubgabbay.com/anything_goes.cfm 200
- anything-goes — GET /anything-goes w/o session redirects to entry page
- anything-goes — guest entry POST redirects to /anything-goes
- anything-goes — chat pane shows join line + room name
- anything-goes — post a message (303 back to room)
- anything-goes — poll API returns posted message
- anything-goes — presence lists the chatter
- anything-goes — HISTORY=8 caps initial pane at 8
- anything-goes — jump to /jokeland keeps session, redirects
- anything-goes — jump posts join line in jokeland
- anything-goes — leave jokeland redirects to chat directory
- jokeland — entry page /www2.clubgabbay.com/jokeland.cfm 200
- jokeland — GET /jokeland w/o session redirects to entry page
- jokeland — guest entry POST redirects to /jokeland
- jokeland — chat pane shows join line + room name
- jokeland — post a message (303 back to room)
- jokeland — poll API returns posted message
- jokeland — presence lists the chatter
- jokeland — HISTORY=8 caps initial pane at 8
- jokeland — jump to /lobby keeps session, redirects
- jokeland — jump posts join line in lobby
- jokeland — leave lobby redirects to chat directory
- lobby — guest form (archived Guest1251) redirects to /lobby
- lobby — guest gets fresh auto-name GuestNNNN (not literal 1251)
- lobby — member entry flagged (member) in presence
- lobby — HISTORY=8 shows exactly last 8 of 12 posted
- lobby — rate limit: 2nd post within 2s is 429
- blue — whisper visible to sender + recipient only, not others
- anything-goes — GET /anything-goes w/o session redirects to gate
- filter — banned word in public message is blocked (403)
- filter — blocked message never stored/shown
- filter — clean message passes after one strike
- filter — clean message is stored
- filter — innocent word (class) is not blocked
- filter — spaced-out evasion is still caught (403)
- filter — three blocked posts all return 403
- filter — 3 strikes -> banned: clean message rejected (403)
- filter — banned user's clean message never stored
- filter — ban is per-user: another user posts fine
- filter — whisper with banned word passes unfiltered
- filter — whisper with banned word is delivered to recipient
- board — board page has post form + 1997 archive
- board — clean board post accepted
- board — new post shows above the 1997 archive
- board — markup post accepted (stored, escaped at render)
- board — markup in a post is escaped, never rendered
- board — banned word in board post is blocked (403)
- board — blocked board post never stored/shown
- board — three blocked board posts all return 403
- board — 3 strikes -> banned from board: clean post rejected
- board — post with no From name is not stored
- site — homepage carries the approved blurb
- site — homepage notes monitoring / 18+ / private whispers
- filter — blocklist is not served over HTTP (/blocklist.txt 404)
- filter — blocklist is not served (/backend/blocklist.txt 404)
- site — link check / (2 links): server matches archive
- site — link check /chat.htm (8 links): server matches archive
- site — link check /chat2.htm (33 links): server matches archive
- site — message survives server restart (SQLite persistence)
- board — board post survives server restart (stays up)

## What failed

Nothing — all checks passed.

## Known archive gaps (not backend bugs)

- Room backgrounds never captured by Wayback, so the chat pane falls back to a plain background for: blue, hard, jive, paradise, soul (`images/bg/*_bg.jpg` 404). Room art images all exist.
- `jakies_jokeland_sm.gif` (JokeLand thumbnail) never captured — JokeLand pane shows no art image.
- `lobby2.cfm` (member entry) was never archived; the backend serves a new member-entry page at that URL instead.
- Themed-room `.cfm` pages (blue.cfm etc.) open a `login.cfm` popup that was never archived; the backend serves a member-login page at `/login.cfm` so the popup works instead of 404ing.
- Anything Goes keeps its 18+ certify gate: GET `/anything-goes` without a session redirects to the archived gate page; the certify POST is the entry.

## What remains

- Host DECIDED 2026-11-07: Render free tier (render.yaml at the repo root; start: `python backend/server.py --host 0.0.0.0`, port from $PORT, default 8124). Nothing is deployed yet — deploy is the parent lane's step; locally the server still binds 127.0.0.1 by default. Domain: free Render subdomain to start (clubgabbay.onrender.com); a real domain later only if the proof of concept earns it.
- Moderation: automated word filter live on public messages (backend/blocklist.txt, private, never served; 3 strikes -> banned from public posting). Whispers are never monitored or filtered, in any room (Paul, 2026-11-07). Report endpoint exists (`POST `/api/<room>/report`, stored in SQLite `reports` table); Mira reviews the report queue.
- Landing page carries the approved blurb above Enter (plus the monitoring / 18+ / private-whisper notes) on all three homepage variants.
- 2026-11-09 (Paul): Enter ClubGabbay on the landing page now links straight to /chat.htm; /main.htm, /welcome.htm, /menu.cfm and /webdates.cfm are removed from the live site; the email line and WebDates block are off the landing page. The landing page is now just a link to the chat. (Also 2026-11-09: the dead LinkExchange banner at the top of the landing page is gone — the ad server is long dead and it rendered as a broken-image box.)
- 2026-11-09 (Paul): the bulletin board is postable — anyone can add a message (To / From / Subject / Message); new posts render above the frozen 1997 archive and stay up (SQLite `board_posts`, no cap; same word filter and 3-strike ban as public chat; no Host/IP shown on new posts). Caveat: the free tier's disk is ephemeral, so a restart or redeploy resets board posts, same as chat history — true permanence needs persistent disk.
- Member accounts are not provisioned (v1 accepts any password on `/lobby2.cfm` and flags the session as a member). Real member auth is a later decision.
- The 29 unarchived absolute URLs from step 3 (webdates images, queue CGI, club store, etc.) are unchanged — still unarchived targets, not backend issues.
- Browser-level visual check (1996 look pixel-for-pixel) was not done in this VM-only run — needs a human or a browser lane to eyeball the pane against the archived pages.
