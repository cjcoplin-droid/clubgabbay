# Club Gabbay mirror — backend test report (spec step 5)

Test run: 2026-11-10 07:48 UTC (local only, http://127.0.0.1:8124, scratch DB test-chat.db)
Backend: `backend/server.py` (stdlib-only Python), test: `backend/test_backend.py`.

## Summary

- Checks run: 640 — **640 PASS, 0 FAIL**
- Rooms walked: 31 of 11 (lobby, blue, speakeasy, denim, hard, soul, jive, classical, paradise, anything-goes, jokeland, hollywood-chat, siliconvalley-chat, sunsetstrip-chat, area51-chat, westhollywood-chat, aol, msn-chat, yahoo-chat, icq-chat, mirc-chat, excite-chat, paltalk-chat, lycos-chat, palace-chat, habbo-chat, powwow-chat, compuserve-chat, prodigy-chat, xfire-chat, myspace-chat)

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
| jokeland | jump to /hollywood-chat keeps session, redirects | PASS | status=200 |
| jokeland | jump posts join line in hollywood-chat | PASS |  |
| jokeland | leave hollywood-chat redirects to chat directory | PASS | status=200 |
| hollywood-chat | entry page /neighborhoods/chat/hollywood.html 200 | PASS | status=200 |
| hollywood-chat | GET /hollywood-chat w/o session redirects to entry page | PASS | status=303 loc=/neighborhoods/chat/hollywood.html |
| hollywood-chat | guest entry POST redirects to /hollywood-chat | PASS | status=200 |
| hollywood-chat | chat pane shows join line + room name | PASS | status=200 |
| hollywood-chat | room page uses its own background | PASS |  |
| hollywood-chat | post a message (303 back to room) | PASS | status=200 |
| hollywood-chat | poll API returns posted message | PASS | found=1 |
| hollywood-chat | presence lists the chatter | PASS |  |
| hollywood-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| hollywood-chat | jump to /siliconvalley-chat keeps session, redirects | PASS | status=200 |
| hollywood-chat | jump posts join line in siliconvalley-chat | PASS |  |
| hollywood-chat | leave siliconvalley-chat redirects to chat directory | PASS | status=200 |
| siliconvalley-chat | entry page /neighborhoods/chat/siliconvalley.html 200 | PASS | status=200 |
| siliconvalley-chat | GET /siliconvalley-chat w/o session redirects to entry page | PASS | status=303 loc=/neighborhoods/chat/siliconvalley.html |
| siliconvalley-chat | guest entry POST redirects to /siliconvalley-chat | PASS | status=200 |
| siliconvalley-chat | chat pane shows join line + room name | PASS | status=200 |
| siliconvalley-chat | room page uses its own background | PASS |  |
| siliconvalley-chat | post a message (303 back to room) | PASS | status=200 |
| siliconvalley-chat | poll API returns posted message | PASS | found=1 |
| siliconvalley-chat | presence lists the chatter | PASS |  |
| siliconvalley-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| siliconvalley-chat | jump to /sunsetstrip-chat keeps session, redirects | PASS | status=200 |
| siliconvalley-chat | jump posts join line in sunsetstrip-chat | PASS |  |
| siliconvalley-chat | leave sunsetstrip-chat redirects to chat directory | PASS | status=200 |
| sunsetstrip-chat | entry page /neighborhoods/chat/sunsetstrip.html 200 | PASS | status=200 |
| sunsetstrip-chat | GET /sunsetstrip-chat w/o session redirects to entry page | PASS | status=303 loc=/neighborhoods/chat/sunsetstrip.html |
| sunsetstrip-chat | guest entry POST redirects to /sunsetstrip-chat | PASS | status=200 |
| sunsetstrip-chat | chat pane shows join line + room name | PASS | status=200 |
| sunsetstrip-chat | room page uses its own background | PASS |  |
| sunsetstrip-chat | post a message (303 back to room) | PASS | status=200 |
| sunsetstrip-chat | poll API returns posted message | PASS | found=1 |
| sunsetstrip-chat | presence lists the chatter | PASS |  |
| sunsetstrip-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| sunsetstrip-chat | jump to /area51-chat keeps session, redirects | PASS | status=200 |
| sunsetstrip-chat | jump posts join line in area51-chat | PASS |  |
| sunsetstrip-chat | leave area51-chat redirects to chat directory | PASS | status=200 |
| area51-chat | entry page /neighborhoods/chat/area51.html 200 | PASS | status=200 |
| area51-chat | GET /area51-chat w/o session redirects to entry page | PASS | status=303 loc=/neighborhoods/chat/area51.html |
| area51-chat | guest entry POST redirects to /area51-chat | PASS | status=200 |
| area51-chat | chat pane shows join line + room name | PASS | status=200 |
| area51-chat | room page uses its own background | PASS |  |
| area51-chat | Area51 room page is black with white text, red links | PASS |  |
| area51-chat | post a message (303 back to room) | PASS | status=200 |
| area51-chat | poll API returns posted message | PASS | found=1 |
| area51-chat | presence lists the chatter | PASS |  |
| area51-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| area51-chat | jump to /westhollywood-chat keeps session, redirects | PASS | status=200 |
| area51-chat | jump posts join line in westhollywood-chat | PASS |  |
| area51-chat | leave westhollywood-chat redirects to chat directory | PASS | status=200 |
| westhollywood-chat | entry page /neighborhoods/chat/westhollywood.html 200 | PASS | status=200 |
| westhollywood-chat | GET /westhollywood-chat w/o session redirects to entry page | PASS | status=303 loc=/neighborhoods/chat/westhollywood.html |
| westhollywood-chat | guest entry POST redirects to /westhollywood-chat | PASS | status=200 |
| westhollywood-chat | chat pane shows join line + room name | PASS | status=200 |
| westhollywood-chat | room page uses its own background | PASS |  |
| westhollywood-chat | post a message (303 back to room) | PASS | status=200 |
| westhollywood-chat | poll API returns posted message | PASS | found=1 |
| westhollywood-chat | presence lists the chatter | PASS |  |
| westhollywood-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| westhollywood-chat | jump to /aol keeps session, redirects | PASS | status=200 |
| westhollywood-chat | jump posts join line in aol | PASS |  |
| westhollywood-chat | leave aol redirects to chat directory | PASS | status=200 |
| aol | entry page /aol.html 200 | PASS | status=200 |
| aol | GET /aol w/o session redirects to entry page | PASS | status=303 loc=/aol.html |
| aol | guest entry POST redirects to /aol | PASS | status=200 |
| aol | chat pane shows join line + room name | PASS | status=200 |
| aol | post a message (303 back to room) | PASS | status=200 |
| aol | poll API returns posted message | PASS | found=1 |
| aol | presence lists the chatter | PASS |  |
| aol | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| aol | jump to /msn-chat keeps session, redirects | PASS | status=200 |
| aol | jump posts join line in msn-chat | PASS |  |
| aol | leave msn-chat redirects to chat directory | PASS | status=200 |
| msn-chat | entry page /msn.html 200 | PASS | status=200 |
| msn-chat | GET /msn-chat w/o session redirects to entry page | PASS | status=303 loc=/msn.html |
| msn-chat | guest entry POST redirects to /msn-chat | PASS | status=200 |
| msn-chat | chat pane shows join line + room name | PASS | status=200 |
| msn-chat | post a message (303 back to room) | PASS | status=200 |
| msn-chat | poll API returns posted message | PASS | found=1 |
| msn-chat | presence lists the chatter | PASS |  |
| msn-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| msn-chat | jump to /yahoo-chat keeps session, redirects | PASS | status=200 |
| msn-chat | jump posts join line in yahoo-chat | PASS |  |
| msn-chat | leave yahoo-chat redirects to chat directory | PASS | status=200 |
| yahoo-chat | entry page /yahoo.html 200 | PASS | status=200 |
| yahoo-chat | GET /yahoo-chat w/o session redirects to entry page | PASS | status=303 loc=/yahoo.html |
| yahoo-chat | guest entry POST redirects to /yahoo-chat | PASS | status=200 |
| yahoo-chat | chat pane shows join line + room name | PASS | status=200 |
| yahoo-chat | post a message (303 back to room) | PASS | status=200 |
| yahoo-chat | poll API returns posted message | PASS | found=1 |
| yahoo-chat | presence lists the chatter | PASS |  |
| yahoo-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| yahoo-chat | jump to /icq-chat keeps session, redirects | PASS | status=200 |
| yahoo-chat | jump posts join line in icq-chat | PASS |  |
| yahoo-chat | leave icq-chat redirects to chat directory | PASS | status=200 |
| icq-chat | entry page /icq.html 200 | PASS | status=200 |
| icq-chat | GET /icq-chat w/o session redirects to entry page | PASS | status=303 loc=/icq.html |
| icq-chat | guest entry POST redirects to /icq-chat | PASS | status=200 |
| icq-chat | chat pane shows join line + room name | PASS | status=200 |
| icq-chat | post a message (303 back to room) | PASS | status=200 |
| icq-chat | poll API returns posted message | PASS | found=1 |
| icq-chat | presence lists the chatter | PASS |  |
| icq-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| icq-chat | jump to /mirc-chat keeps session, redirects | PASS | status=200 |
| icq-chat | jump posts join line in mirc-chat | PASS |  |
| icq-chat | leave mirc-chat redirects to chat directory | PASS | status=200 |
| mirc-chat | entry page /mirc.html 200 | PASS | status=200 |
| mirc-chat | GET /mirc-chat w/o session redirects to entry page | PASS | status=303 loc=/mirc.html |
| mirc-chat | guest entry POST redirects to /mirc-chat | PASS | status=200 |
| mirc-chat | chat pane shows join line + room name | PASS | status=200 |
| mirc-chat | post a message (303 back to room) | PASS | status=200 |
| mirc-chat | poll API returns posted message | PASS | found=1 |
| mirc-chat | presence lists the chatter | PASS |  |
| mirc-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| mirc-chat | jump to /excite-chat keeps session, redirects | PASS | status=200 |
| mirc-chat | jump posts join line in excite-chat | PASS |  |
| mirc-chat | leave excite-chat redirects to chat directory | PASS | status=200 |
| excite-chat | entry page /excite.html 200 | PASS | status=200 |
| excite-chat | GET /excite-chat w/o session redirects to entry page | PASS | status=303 loc=/excite.html |
| excite-chat | guest entry POST redirects to /excite-chat | PASS | status=200 |
| excite-chat | chat pane shows join line + room name | PASS | status=200 |
| excite-chat | post a message (303 back to room) | PASS | status=200 |
| excite-chat | poll API returns posted message | PASS | found=1 |
| excite-chat | presence lists the chatter | PASS |  |
| excite-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| excite-chat | jump to /paltalk-chat keeps session, redirects | PASS | status=200 |
| excite-chat | jump posts join line in paltalk-chat | PASS |  |
| excite-chat | leave paltalk-chat redirects to chat directory | PASS | status=200 |
| paltalk-chat | entry page /paltalk.html 200 | PASS | status=200 |
| paltalk-chat | GET /paltalk-chat w/o session redirects to entry page | PASS | status=303 loc=/paltalk.html |
| paltalk-chat | guest entry POST redirects to /paltalk-chat | PASS | status=200 |
| paltalk-chat | chat pane shows join line + room name | PASS | status=200 |
| paltalk-chat | post a message (303 back to room) | PASS | status=200 |
| paltalk-chat | poll API returns posted message | PASS | found=1 |
| paltalk-chat | presence lists the chatter | PASS |  |
| paltalk-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| paltalk-chat | jump to /lycos-chat keeps session, redirects | PASS | status=200 |
| paltalk-chat | jump posts join line in lycos-chat | PASS |  |
| paltalk-chat | leave lycos-chat redirects to chat directory | PASS | status=200 |
| lycos-chat | entry page /lycos.html 200 | PASS | status=200 |
| lycos-chat | GET /lycos-chat w/o session redirects to entry page | PASS | status=303 loc=/lycos.html |
| lycos-chat | guest entry POST redirects to /lycos-chat | PASS | status=200 |
| lycos-chat | chat pane shows join line + room name | PASS | status=200 |
| lycos-chat | post a message (303 back to room) | PASS | status=200 |
| lycos-chat | poll API returns posted message | PASS | found=1 |
| lycos-chat | presence lists the chatter | PASS |  |
| lycos-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| lycos-chat | jump to /palace-chat keeps session, redirects | PASS | status=200 |
| lycos-chat | jump posts join line in palace-chat | PASS |  |
| lycos-chat | leave palace-chat redirects to chat directory | PASS | status=200 |
| palace-chat | entry page /palace.html 200 | PASS | status=200 |
| palace-chat | GET /palace-chat w/o session redirects to entry page | PASS | status=303 loc=/palace.html |
| palace-chat | guest entry POST redirects to /palace-chat | PASS | status=200 |
| palace-chat | chat pane shows join line + room name | PASS | status=200 |
| palace-chat | post a message (303 back to room) | PASS | status=200 |
| palace-chat | poll API returns posted message | PASS | found=1 |
| palace-chat | presence lists the chatter | PASS |  |
| palace-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| palace-chat | jump to /habbo-chat keeps session, redirects | PASS | status=200 |
| palace-chat | jump posts join line in habbo-chat | PASS |  |
| palace-chat | leave habbo-chat redirects to chat directory | PASS | status=200 |
| habbo-chat | entry page /habbo.html 200 | PASS | status=200 |
| habbo-chat | GET /habbo-chat w/o session redirects to entry page | PASS | status=303 loc=/habbo.html |
| habbo-chat | guest entry POST redirects to /habbo-chat | PASS | status=200 |
| habbo-chat | chat pane shows join line + room name | PASS | status=200 |
| habbo-chat | post a message (303 back to room) | PASS | status=200 |
| habbo-chat | poll API returns posted message | PASS | found=1 |
| habbo-chat | presence lists the chatter | PASS |  |
| habbo-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| habbo-chat | jump to /powwow-chat keeps session, redirects | PASS | status=200 |
| habbo-chat | jump posts join line in powwow-chat | PASS |  |
| habbo-chat | leave powwow-chat redirects to chat directory | PASS | status=200 |
| powwow-chat | entry page /powwow.html 200 | PASS | status=200 |
| powwow-chat | GET /powwow-chat w/o session redirects to entry page | PASS | status=303 loc=/powwow.html |
| powwow-chat | guest entry POST redirects to /powwow-chat | PASS | status=200 |
| powwow-chat | chat pane shows join line + room name | PASS | status=200 |
| powwow-chat | post a message (303 back to room) | PASS | status=200 |
| powwow-chat | poll API returns posted message | PASS | found=1 |
| powwow-chat | presence lists the chatter | PASS |  |
| powwow-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| powwow-chat | jump to /compuserve-chat keeps session, redirects | PASS | status=200 |
| powwow-chat | jump posts join line in compuserve-chat | PASS |  |
| powwow-chat | leave compuserve-chat redirects to chat directory | PASS | status=200 |
| compuserve-chat | entry page /compuserve.html 200 | PASS | status=200 |
| compuserve-chat | GET /compuserve-chat w/o session redirects to entry page | PASS | status=303 loc=/compuserve.html |
| compuserve-chat | guest entry POST redirects to /compuserve-chat | PASS | status=200 |
| compuserve-chat | chat pane shows join line + room name | PASS | status=200 |
| compuserve-chat | post a message (303 back to room) | PASS | status=200 |
| compuserve-chat | poll API returns posted message | PASS | found=1 |
| compuserve-chat | presence lists the chatter | PASS |  |
| compuserve-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| compuserve-chat | jump to /prodigy-chat keeps session, redirects | PASS | status=200 |
| compuserve-chat | jump posts join line in prodigy-chat | PASS |  |
| compuserve-chat | leave prodigy-chat redirects to chat directory | PASS | status=200 |
| prodigy-chat | entry page /prodigy.html 200 | PASS | status=200 |
| prodigy-chat | GET /prodigy-chat w/o session redirects to entry page | PASS | status=303 loc=/prodigy.html |
| prodigy-chat | guest entry POST redirects to /prodigy-chat | PASS | status=200 |
| prodigy-chat | chat pane shows join line + room name | PASS | status=200 |
| prodigy-chat | post a message (303 back to room) | PASS | status=200 |
| prodigy-chat | poll API returns posted message | PASS | found=1 |
| prodigy-chat | presence lists the chatter | PASS |  |
| prodigy-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| prodigy-chat | jump to /xfire-chat keeps session, redirects | PASS | status=200 |
| prodigy-chat | jump posts join line in xfire-chat | PASS |  |
| prodigy-chat | leave xfire-chat redirects to chat directory | PASS | status=200 |
| xfire-chat | entry page /xfire.html 200 | PASS | status=200 |
| xfire-chat | GET /xfire-chat w/o session redirects to entry page | PASS | status=303 loc=/xfire.html |
| xfire-chat | guest entry POST redirects to /xfire-chat | PASS | status=200 |
| xfire-chat | chat pane shows join line + room name | PASS | status=200 |
| xfire-chat | post a message (303 back to room) | PASS | status=200 |
| xfire-chat | poll API returns posted message | PASS | found=1 |
| xfire-chat | presence lists the chatter | PASS |  |
| xfire-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| xfire-chat | jump to /myspace-chat keeps session, redirects | PASS | status=200 |
| xfire-chat | jump posts join line in myspace-chat | PASS |  |
| xfire-chat | leave myspace-chat redirects to chat directory | PASS | status=200 |
| myspace-chat | entry page /myspace.html 200 | PASS | status=200 |
| myspace-chat | GET /myspace-chat w/o session redirects to entry page | PASS | status=303 loc=/myspace.html |
| myspace-chat | guest entry POST redirects to /myspace-chat | PASS | status=200 |
| myspace-chat | chat pane shows join line + room name | PASS | status=200 |
| myspace-chat | post a message (303 back to room) | PASS | status=200 |
| myspace-chat | poll API returns posted message | PASS | found=1 |
| myspace-chat | presence lists the chatter | PASS |  |
| myspace-chat | HISTORY=8 caps initial pane at 8 | PASS | n=4 |
| myspace-chat | jump to /lobby keeps session, redirects | PASS | status=200 |
| myspace-chat | jump posts join line in lobby | PASS |  |
| myspace-chat | leave lobby redirects to chat directory | PASS | status=200 |
| lobby | guest form (archived Guest1251) redirects to /lobby | PASS | status=200 |
| lobby | guest gets fresh auto-name GuestNNNN (not literal 1251) | PASS | names=['Tlobby', 'Tlobby', 'Tmyspacec', 'Tmyspacec', 'Guest6206'] |
| lobby | member entry flagged (member) in presence | PASS | presence=['Guest6206', 'TestMember (member)'] |
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
| filter | innocent phrase across a word boundary passes | PASS | status=200 |
| filter | innocent phrase is stored/shown | PASS |  |
| filter | three blocked posts all return 403 | PASS | statuses=[403, 403, 403] |
| filter | 3 strikes -> banned: clean message rejected (403) | PASS | status=403 |
| filter | banned user's clean message never stored | PASS |  |
| filter | ban is per-user: another user posts fine | PASS | status=200 |
| filter | whisper with banned word passes unfiltered | PASS | status=200 |
| filter | whisper with banned word is delivered to recipient | PASS |  |
| board | board page has post form + 1997 archive | PASS | status=200 |
| board | clean board post accepted | PASS | status=200 |
| board | new post shows above the 1997 archive | PASS |  |
| board | GET /api/board/posts returns the new post as JSON | PASS | status=200 |
| board | GET /api/board/posts?board=clubgabbay filters to the main board | PASS | status=200 |
| board | GET /api/board/posts?board=hollywood is empty (no posts yet) | PASS | status=200 |
| board | GET /api/board/posts?board=nope is 404 | PASS | status=404 |
| visits | GET /api/visits returns unique + total | PASS | status=200 body=b'{"unique": 55, "total": 33}' |
| visits | landing page loads (200) and carries the counter | PASS | status=200 |
| visits | first landing visit counts one unique person | PASS | unique=56 total=35 |
| visits | same person reloading does NOT count again (unique stays) | PASS | unique=56 total=36 |
| visits | a different visitor IP counts as a new person | PASS | unique=57 |
| visits | landing page has the donations / Ko-fi tip link | PASS |  |
| board | markup post accepted (stored, escaped at render) | PASS | status=200 |
| board | markup in a post is escaped, never rendered | PASS |  |
| board | banned word in board post is blocked (403) | PASS | status=403 |
| board | blocked board post never stored/shown | PASS |  |
| board | three blocked board posts all return 403 | PASS | statuses=[403, 403, 403] |
| board | 3 strikes -> banned from board: clean post rejected | PASS | status=403 |
| board | post with no From name is not stored | PASS |  |
| board | restore seeds an empty board from the backup file | PASS | restored=1 |
| board | restore is idempotent (second run restores 0) | PASS | restored=0 |
| board | restore skips a non-empty board (live posts kept) | PASS | restored=0 |
| board | restore with an unreachable URL returns 0, no crash | PASS |  |
| board | restore with no URL configured is a no-op | PASS |  |
| board | neighborhood board page serves with its own form | PASS | status=200 |
| board | unknown neighborhood board is 404 | PASS | status=404 |
| board | neighborhood board post accepted | PASS | status=200 |
| board | neighborhood post shows on its own board | PASS |  |
| board | neighborhood post does NOT leak onto the main board | PASS |  |
| board | API ?board=hollywood returns the neighborhood post | PASS |  |
| board | API ?board=siliconvalley does not return it | PASS |  |
| board | banned word in neighborhood post is blocked (403) | PASS | status=403 |
| board | post to an unknown neighborhood board is 404 | PASS | status=404 |
| aol | AOL entry page serves with its handle form | PASS | status=200 |
| aol | GET /aol w/o session redirects to entry page | PASS | status=303 loc=/aol.html |
| aol | room page is the AOL skin with click-to-PM | PASS | status=200 |
| aol | message sound: AIM ding + Sound toggle, plays only for others | PASS | status=200 |
| aol | PM visible to sender + recipient only, not others | PASS | {'sender': True, 'recipient': True, 'other': False} |
| aol | chat directory lists AOL Chat | PASS | status=200 |
| aol | handles board page serves with its own form | PASS | status=200 |
| aol | handles board post accepted | PASS | status=200 |
| aol | handles post shows on its own board | PASS |  |
| aol | handles post does NOT leak onto the main board | PASS |  |
| aol | API ?board=aol-handles returns the handles post | PASS |  |
| aol | banned word in handles post is blocked (403) | PASS | status=403 |
| action | lobby room page has the action form | PASS | status=200 |
| action | valid action accepted | PASS | status=200 |
| action | action shows in the poll as kind=action | PASS |  |
| action | action renders as '* user winks at target *' | PASS |  |
| action | verb outside the whitelist is rejected | PASS | status=200 |
| action | target not in the room is rejected | PASS | status=200 |
| action | acting on yourself is rejected | PASS | status=200 |
| action | rejected actions are never stored | PASS | [] |
| action | second valid action accepted after the wait | PASS | status=200 |
| action | rate limit: 2nd action within 2s is 429 | PASS | status=429 |
| action | AOL room page has the action form | PASS | status=200 |
| aol-style | AOL room page has color + font pickers | PASS | status=200 |
| aol-style | colored post accepted | PASS | status=200 |
| aol-style | API carries the color + font | PASS | [{'id': 168, 'user': 'AolSty', 'kind': 'say', 'text': 'aol-style-test-12345', 'to': None, 'ts': 1794296905.6912494, 'color': 'red', 'font': 'Courier New', 'time': '07:48'}] |
| aol-style | colored message renders in its color + font | PASS |  |
| aol-style | the color choice sticks in the session | PASS |  |
| aol-style | injected color/font falls back to default | PASS | status=200 |
| aol-style | bad color/font stored as default (None) | PASS | [{'id': 169, 'user': 'AolSty', 'kind': 'say', 'text': 'aol-style-bad-12345', 'to': None, 'ts': 1794296907.856088, 'color': None, 'font': None, 'time': '07:48'}] |
| aol-style | injected markup never renders | PASS |  |
| aol-style | lobby posts never carry a color/font | PASS | [{'id': 171, 'user': 'LobbySty', 'kind': 'say', 'text': 'lobby-style-test-12345', 'to': None, 'ts': 1794296910.0994148, 'color': None, 'font': None, 'time': '07:48'}] |
| 21plus | lobby room page says 21 and over | PASS | status=200 |
| 21plus | hollywood-chat room page says 21 and over | PASS | status=200 |
| 21plus | aol room page says 21 and over | PASS | status=200 |
| 21plus | /chat.htm says 21 and over | PASS | status=200 |
| 21plus | /chat2.htm says 21 and over | PASS | status=200 |
| 21plus | /lobby.cfm says 21 and over | PASS | status=200 |
| 21plus | /lobby2.cfm says 21 and over | PASS | status=200 |
| 21plus | /anything_goes.cfm says 21 and over | PASS | status=200 |
| 21plus | /jokeland.cfm says 21 and over | PASS | status=200 |
| 21plus | /aol.html says 21 and over | PASS | status=200 |
| 21plus | /neighborhoods/chat/hollywood.html says 21 and over | PASS | status=200 |
| 21plus | /neighborhoods/chat/area51.html says 21 and over | PASS | status=200 |
| 21plus | Anything Goes no longer says 18 anywhere | PASS |  |
| landing | homepage is the new landing page: ADULTS ONLY gate | PASS | status=200 |
| landing | homepage says 21, never 18; no fake counts, no Netscape | PASS |  |
| landing | homepage links all fourteen service pages | PASS |  |
| landing | homepage has a Have Discord? link (Paul, 2026-11-09) | PASS |  |
| landing | homepage carries the TheOldNet webring widget (Paul, 2026-11-09) | PASS |  |
| landing | under-21 stop page serves | PASS | status=200 |
| landing | fine print carries the 21+ note + terms of entry | PASS | status=200 |
| landing | age gate without confirm bounces to / | PASS | status=303 loc=/ |
| landing | no flag: directory bounces home (landing page) | PASS | status=200 |
| landing | age gate with confirm goes to /chat.htm | PASS | status=303 loc=/chat.htm |
| landing | flag set: directory 200 | PASS | status=200 |
| landing | /chat.htm without the flag bounces to / | PASS | status=303 loc=/ |
| landing | /chat2.htm without the flag bounces to / | PASS | status=303 loc=/ |
| landing | room entry without confirm bounces home | PASS |  |
| landing | room entry with confirm reaches the room | PASS | status=200 |
| landing | entry set the flag: directory 200 after | PASS | status=200 |
| services | msn landing page serves with gate + handle form | PASS | status=200 |
| services | msn page links all fourteen services | PASS |  |
| services | msn entry without confirm bounces home | PASS |  |
| services | msn room wears its own skin: title bar #0078D7, member list + IM box, no AOL pickers | PASS | status=200 |
| services | msn v2+v3 chrome: Chat Rooms panel, MSN Chat tab, styled Send Send, chat white/Tahoma, colored joins, Nudge, gradient title, display pictures | PASS | status=200 |
| services | msn message sound: ding-msn + toggle, plays only for others | PASS | status=200 |
| services | msn permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | yahoo landing page serves with gate + handle form | PASS | status=200 |
| services | yahoo page links all fourteen services | PASS |  |
| services | yahoo entry without confirm bounces home | PASS |  |
| services | yahoo room wears its own skin: title bar #6001D2, member list + IM box, no AOL pickers | PASS | status=200 |
| services | yahoo v2+v3 chrome: Chat Rooms panel, Yahoo! Chat tab, styled Send Send, chat white/Tahoma, colored joins, BUZZ!, smiley | PASS | status=200 |
| services | yahoo message sound: ding-yahoo + toggle, plays only for others | PASS | status=200 |
| services | yahoo permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | icq landing page serves with gate + handle form | PASS | status=200 |
| services | icq page links all fourteen services | PASS |  |
| services | icq entry without confirm bounces home | PASS |  |
| services | icq room wears its own skin: title bar #00A000, member list + IM box, no AOL pickers | PASS | status=200 |
| services | icq v2+v3 chrome: Chat Rooms panel, #icq_usa tab, styled Send Send, chat white/Tahoma, colored joins, flower mark, flower petals | PASS | status=200 |
| services | icq message sound: uhoh + toggle, plays only for others | PASS | status=200 |
| services | icq permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | mirc landing page serves with gate + handle form | PASS | status=200 |
| services | mirc page links all fourteen services | PASS |  |
| services | mirc entry without confirm bounces home | PASS |  |
| services | mirc room wears its own skin: title bar #000080, member list + IM box, no AOL pickers | PASS | status=200 |
| services | mirc v2+v3 chrome: Chat Rooms panel, #Canada tab, styled Send Send, chat white/Courier New, colored joins, monospace, topic line, status bar | PASS | status=200 |
| services | mirc message sound: beep + toggle, plays only for others | PASS | status=200 |
| services | mirc permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | excite landing page serves with gate + handle form | PASS | status=200 |
| services | excite page links all fourteen services | PASS |  |
| services | excite entry without confirm bounces home | PASS |  |
| services | excite room wears its own skin: title bar #CC0000, member list + IM box, no AOL pickers | PASS | status=200 |
| services | excite v2+v3 chrome: Chat Rooms panel, Excite Chat tab, styled Send Send, chat white/Tahoma, colored joins, portal masthead | PASS | status=200 |
| services | excite message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | excite permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | paltalk landing page serves with gate + handle form | PASS | status=200 |
| services | paltalk page links all fourteen services | PASS |  |
| services | paltalk entry without confirm bounces home | PASS |  |
| services | paltalk room wears its own skin: title bar #0099CC, member list + IM box, no AOL pickers | PASS | status=200 |
| services | paltalk v2+v3 chrome: Chat Rooms panel, Paltalk Chat tab, styled Send Send, chat white/Tahoma, colored joins, video strip | PASS | status=200 |
| services | paltalk message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | paltalk permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | lycos landing page serves with gate + handle form | PASS | status=200 |
| services | lycos page links all fourteen services | PASS |  |
| services | lycos entry without confirm bounces home | PASS |  |
| services | lycos room wears its own skin: title bar #FF6600, member list + IM box, no AOL pickers | PASS | status=200 |
| services | lycos v2+v3 chrome: Chat Rooms panel, Lycos Chat tab, styled Send Send, chat white/Tahoma, colored joins, black/yellow masthead | PASS | status=200 |
| services | lycos message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | lycos permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | palace landing page serves with gate + handle form | PASS | status=200 |
| services | palace page links all fourteen services | PASS |  |
| services | palace entry without confirm bounces home | PASS |  |
| services | palace room wears its own skin: title bar #993399, member list + IM box, no AOL pickers | PASS | status=200 |
| services | palace v2+v3 chrome: Chat Rooms panel, The Palace Chat tab, styled Send Send, chat #87CEEB/Comic Sans MS, colored joins, playful font, smiley avatars + bubbles, backdrop | PASS | status=200 |
| services | palace message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | palace permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | habbo landing page serves with gate + handle form | PASS | status=200 |
| services | habbo page links all fourteen services | PASS |  |
| services | habbo entry without confirm bounces home | PASS |  |
| services | habbo room wears its own skin: title bar #E6B800, member list + IM box, no AOL pickers | PASS | status=200 |
| services | habbo v2+v3 chrome: Chat Rooms panel, Habbo Hotel Chat tab, styled Send Send, chat #003399/Verdana, colored joins, dark chat log, pixel floor, HC sofa | PASS | status=200 |
| services | habbo message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | habbo permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | powwow landing page serves with gate + handle form | PASS | status=200 |
| services | powwow page links all fourteen services | PASS |  |
| services | powwow entry without confirm bounces home | PASS |  |
| services | powwow room wears its own skin: title bar #006666, member list + IM box, no AOL pickers | PASS | status=200 |
| services | powwow v2+v3 chrome: Chat Rooms panel, PowWow Chat tab, styled Send Send, chat white/Tahoma, colored joins, voice dot | PASS | status=200 |
| services | powwow message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | powwow permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | compuserve landing page serves with gate + handle form | PASS | status=200 |
| services | compuserve page links all fourteen services | PASS |  |
| services | compuserve entry without confirm bounces home | PASS |  |
| services | compuserve room wears its own skin: title bar #003366, member list + IM box, no AOL pickers | PASS | status=200 |
| services | compuserve v2+v3 chrome: Chat Rooms panel, CB Channel 1 tab, styled GO Send, chat #000000/Courier New, colored joins, GO button | PASS | status=200 |
| services | compuserve message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | compuserve permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | prodigy landing page serves with gate + handle form | PASS | status=200 |
| services | prodigy page links all fourteen services | PASS |  |
| services | prodigy entry without confirm bounces home | PASS |  |
| services | prodigy room wears its own skin: title bar #800000, member list + IM box, no AOL pickers | PASS | status=200 |
| services | prodigy v2+v3 chrome: Chat Rooms panel, Prodigy Chat tab, styled Send Send, chat white/Tahoma, colored joins, welcome strip, blue sidebar links | PASS | status=200 |
| services | prodigy message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | prodigy permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | xfire landing page serves with gate + handle form | PASS | status=200 |
| services | xfire page links all fourteen services | PASS |  |
| services | xfire entry without confirm bounces home | PASS |  |
| services | xfire room wears its own skin: title bar #000000, member list + IM box, no AOL pickers | PASS | status=200 |
| services | xfire v2+v3 chrome: Chat Rooms panel, Xfire Chat tab, styled Send Send, chat #1A1A1A/Tahoma, colored joins, dark chat | PASS | status=200 |
| services | xfire message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | xfire permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| services | myspace landing page serves with gate + handle form | PASS | status=200 |
| services | myspace page links all fourteen services | PASS |  |
| services | myspace entry without confirm bounces home | PASS |  |
| services | myspace room wears its own skin: title bar #003399, member list + IM box, no AOL pickers | PASS | status=200 |
| services | myspace v2+v3 chrome: Chat Rooms panel, MySpace Chat tab, styled Send Send, chat white/Tahoma, colored joins, Top 8 strip | PASS | status=200 |
| services | myspace message sound: silent + toggle, plays only for others | PASS | status=200 |
| services | myspace permanent join lines: Mira + 1990calling at the top | PASS | status=200 |
| board | db_init adds the board column to an old board DB | PASS | cols=['id', 'name', 'to_name', 'subject', 'message', 'ts', 'board'] |
| board | old post reads back on the main board | PASS |  |
| board | new post lands on its neighborhood board | PASS |  |
| board | neighborhood post is not on the main board | PASS |  |
| board | restore seeds a neighborhood post onto its board | PASS | restored=1 |
| board | restored neighborhood post is not on the main board | PASS |  |
| neighborhoods | neighborhoods index serves | PASS | status=200 |
| neighborhoods | home page links the neighborhoods | PASS |  |
| neighborhoods | chat directory lists all five neighborhood rooms | PASS | status=200 |
| neighborhoods | button hollywood.gif serves as a GIF | PASS | status=200 |
| neighborhoods | button siliconvalley.gif serves as a GIF | PASS | status=200 |
| neighborhoods | button sunsetstrip.gif serves as a GIF | PASS | status=200 |
| neighborhoods | button area51.gif serves as a GIF | PASS | status=200 |
| neighborhoods | button westhollywood.gif serves as a GIF | PASS | status=200 |
| neighborhoods | our own 8-bit pixel G serves (not the trademarked logo) | PASS | status=200 |
| neighborhoods | original background background.gif serves as a GIF | PASS | status=200 |
| neighborhoods | original background area_glow.gif serves as a GIF | PASS | status=200 |
| neighborhoods | /neighborhoods/hollywood.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/chat/hollywood.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/siliconvalley.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/chat/siliconvalley.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/sunsetstrip.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/chat/sunsetstrip.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/area51.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/chat/area51.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/area51.html is black with white text, red links | PASS |  |
| neighborhoods | /neighborhoods/chat/area51.html is black with white text, red links | PASS |  |
| neighborhoods | /neighborhoods/westhollywood.html uses its own background | PASS | status=200 |
| neighborhoods | /neighborhoods/chat/westhollywood.html uses its own background | PASS | status=200 |
| neighborhoods | portal hollywood serves with its directory | PASS | status=200 |
| neighborhoods | board page for hollywood serves | PASS | status=200 |
| neighborhoods | portal siliconvalley serves with its directory | PASS | status=200 |
| neighborhoods | board page for siliconvalley serves | PASS | status=200 |
| neighborhoods | portal sunsetstrip serves with its directory | PASS | status=200 |
| neighborhoods | board page for sunsetstrip serves | PASS | status=200 |
| neighborhoods | portal area51 serves with its directory | PASS | status=200 |
| neighborhoods | board page for area51 serves | PASS | status=200 |
| neighborhoods | portal westhollywood serves with its directory | PASS | status=200 |
| neighborhoods | board page for westhollywood serves | PASS | status=200 |
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
| link check / (36 links): server matches archive | PASS | pre-existing archive gaps (404, expected): ['//webring.theoldnet.com/widget/4426ccce3a3ac890584bf223872b964d/navigate', '//webring.theoldnet.com/widget/4426ccce3a3ac890584bf223872b964d/image', '//webring.theoldnet.com/member/4426ccce3a3ac890584bf223872b964d/previous/navigate', '//webring.theoldnet.com/member/4426ccce3a3ac890584bf223872b964d/random/navigate', '//webring.theoldnet.com/member/4426ccce3a3ac890584bf223872b964d/next/navigate', '//webring.theoldnet.com/widget/widget.js'] |
| link check /chat.htm (26 links): server matches archive | PASS | all resolve |
| link check /chat2.htm (34 links): server matches archive | PASS | all resolve |
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
- jokeland — jump to /hollywood-chat keeps session, redirects
- jokeland — jump posts join line in hollywood-chat
- jokeland — leave hollywood-chat redirects to chat directory
- hollywood-chat — entry page /neighborhoods/chat/hollywood.html 200
- hollywood-chat — GET /hollywood-chat w/o session redirects to entry page
- hollywood-chat — guest entry POST redirects to /hollywood-chat
- hollywood-chat — chat pane shows join line + room name
- hollywood-chat — room page uses its own background
- hollywood-chat — post a message (303 back to room)
- hollywood-chat — poll API returns posted message
- hollywood-chat — presence lists the chatter
- hollywood-chat — HISTORY=8 caps initial pane at 8
- hollywood-chat — jump to /siliconvalley-chat keeps session, redirects
- hollywood-chat — jump posts join line in siliconvalley-chat
- hollywood-chat — leave siliconvalley-chat redirects to chat directory
- siliconvalley-chat — entry page /neighborhoods/chat/siliconvalley.html 200
- siliconvalley-chat — GET /siliconvalley-chat w/o session redirects to entry page
- siliconvalley-chat — guest entry POST redirects to /siliconvalley-chat
- siliconvalley-chat — chat pane shows join line + room name
- siliconvalley-chat — room page uses its own background
- siliconvalley-chat — post a message (303 back to room)
- siliconvalley-chat — poll API returns posted message
- siliconvalley-chat — presence lists the chatter
- siliconvalley-chat — HISTORY=8 caps initial pane at 8
- siliconvalley-chat — jump to /sunsetstrip-chat keeps session, redirects
- siliconvalley-chat — jump posts join line in sunsetstrip-chat
- siliconvalley-chat — leave sunsetstrip-chat redirects to chat directory
- sunsetstrip-chat — entry page /neighborhoods/chat/sunsetstrip.html 200
- sunsetstrip-chat — GET /sunsetstrip-chat w/o session redirects to entry page
- sunsetstrip-chat — guest entry POST redirects to /sunsetstrip-chat
- sunsetstrip-chat — chat pane shows join line + room name
- sunsetstrip-chat — room page uses its own background
- sunsetstrip-chat — post a message (303 back to room)
- sunsetstrip-chat — poll API returns posted message
- sunsetstrip-chat — presence lists the chatter
- sunsetstrip-chat — HISTORY=8 caps initial pane at 8
- sunsetstrip-chat — jump to /area51-chat keeps session, redirects
- sunsetstrip-chat — jump posts join line in area51-chat
- sunsetstrip-chat — leave area51-chat redirects to chat directory
- area51-chat — entry page /neighborhoods/chat/area51.html 200
- area51-chat — GET /area51-chat w/o session redirects to entry page
- area51-chat — guest entry POST redirects to /area51-chat
- area51-chat — chat pane shows join line + room name
- area51-chat — room page uses its own background
- area51-chat — Area51 room page is black with white text, red links
- area51-chat — post a message (303 back to room)
- area51-chat — poll API returns posted message
- area51-chat — presence lists the chatter
- area51-chat — HISTORY=8 caps initial pane at 8
- area51-chat — jump to /westhollywood-chat keeps session, redirects
- area51-chat — jump posts join line in westhollywood-chat
- area51-chat — leave westhollywood-chat redirects to chat directory
- westhollywood-chat — entry page /neighborhoods/chat/westhollywood.html 200
- westhollywood-chat — GET /westhollywood-chat w/o session redirects to entry page
- westhollywood-chat — guest entry POST redirects to /westhollywood-chat
- westhollywood-chat — chat pane shows join line + room name
- westhollywood-chat — room page uses its own background
- westhollywood-chat — post a message (303 back to room)
- westhollywood-chat — poll API returns posted message
- westhollywood-chat — presence lists the chatter
- westhollywood-chat — HISTORY=8 caps initial pane at 8
- westhollywood-chat — jump to /aol keeps session, redirects
- westhollywood-chat — jump posts join line in aol
- westhollywood-chat — leave aol redirects to chat directory
- aol — entry page /aol.html 200
- aol — GET /aol w/o session redirects to entry page
- aol — guest entry POST redirects to /aol
- aol — chat pane shows join line + room name
- aol — post a message (303 back to room)
- aol — poll API returns posted message
- aol — presence lists the chatter
- aol — HISTORY=8 caps initial pane at 8
- aol — jump to /msn-chat keeps session, redirects
- aol — jump posts join line in msn-chat
- aol — leave msn-chat redirects to chat directory
- msn-chat — entry page /msn.html 200
- msn-chat — GET /msn-chat w/o session redirects to entry page
- msn-chat — guest entry POST redirects to /msn-chat
- msn-chat — chat pane shows join line + room name
- msn-chat — post a message (303 back to room)
- msn-chat — poll API returns posted message
- msn-chat — presence lists the chatter
- msn-chat — HISTORY=8 caps initial pane at 8
- msn-chat — jump to /yahoo-chat keeps session, redirects
- msn-chat — jump posts join line in yahoo-chat
- msn-chat — leave yahoo-chat redirects to chat directory
- yahoo-chat — entry page /yahoo.html 200
- yahoo-chat — GET /yahoo-chat w/o session redirects to entry page
- yahoo-chat — guest entry POST redirects to /yahoo-chat
- yahoo-chat — chat pane shows join line + room name
- yahoo-chat — post a message (303 back to room)
- yahoo-chat — poll API returns posted message
- yahoo-chat — presence lists the chatter
- yahoo-chat — HISTORY=8 caps initial pane at 8
- yahoo-chat — jump to /icq-chat keeps session, redirects
- yahoo-chat — jump posts join line in icq-chat
- yahoo-chat — leave icq-chat redirects to chat directory
- icq-chat — entry page /icq.html 200
- icq-chat — GET /icq-chat w/o session redirects to entry page
- icq-chat — guest entry POST redirects to /icq-chat
- icq-chat — chat pane shows join line + room name
- icq-chat — post a message (303 back to room)
- icq-chat — poll API returns posted message
- icq-chat — presence lists the chatter
- icq-chat — HISTORY=8 caps initial pane at 8
- icq-chat — jump to /mirc-chat keeps session, redirects
- icq-chat — jump posts join line in mirc-chat
- icq-chat — leave mirc-chat redirects to chat directory
- mirc-chat — entry page /mirc.html 200
- mirc-chat — GET /mirc-chat w/o session redirects to entry page
- mirc-chat — guest entry POST redirects to /mirc-chat
- mirc-chat — chat pane shows join line + room name
- mirc-chat — post a message (303 back to room)
- mirc-chat — poll API returns posted message
- mirc-chat — presence lists the chatter
- mirc-chat — HISTORY=8 caps initial pane at 8
- mirc-chat — jump to /excite-chat keeps session, redirects
- mirc-chat — jump posts join line in excite-chat
- mirc-chat — leave excite-chat redirects to chat directory
- excite-chat — entry page /excite.html 200
- excite-chat — GET /excite-chat w/o session redirects to entry page
- excite-chat — guest entry POST redirects to /excite-chat
- excite-chat — chat pane shows join line + room name
- excite-chat — post a message (303 back to room)
- excite-chat — poll API returns posted message
- excite-chat — presence lists the chatter
- excite-chat — HISTORY=8 caps initial pane at 8
- excite-chat — jump to /paltalk-chat keeps session, redirects
- excite-chat — jump posts join line in paltalk-chat
- excite-chat — leave paltalk-chat redirects to chat directory
- paltalk-chat — entry page /paltalk.html 200
- paltalk-chat — GET /paltalk-chat w/o session redirects to entry page
- paltalk-chat — guest entry POST redirects to /paltalk-chat
- paltalk-chat — chat pane shows join line + room name
- paltalk-chat — post a message (303 back to room)
- paltalk-chat — poll API returns posted message
- paltalk-chat — presence lists the chatter
- paltalk-chat — HISTORY=8 caps initial pane at 8
- paltalk-chat — jump to /lycos-chat keeps session, redirects
- paltalk-chat — jump posts join line in lycos-chat
- paltalk-chat — leave lycos-chat redirects to chat directory
- lycos-chat — entry page /lycos.html 200
- lycos-chat — GET /lycos-chat w/o session redirects to entry page
- lycos-chat — guest entry POST redirects to /lycos-chat
- lycos-chat — chat pane shows join line + room name
- lycos-chat — post a message (303 back to room)
- lycos-chat — poll API returns posted message
- lycos-chat — presence lists the chatter
- lycos-chat — HISTORY=8 caps initial pane at 8
- lycos-chat — jump to /palace-chat keeps session, redirects
- lycos-chat — jump posts join line in palace-chat
- lycos-chat — leave palace-chat redirects to chat directory
- palace-chat — entry page /palace.html 200
- palace-chat — GET /palace-chat w/o session redirects to entry page
- palace-chat — guest entry POST redirects to /palace-chat
- palace-chat — chat pane shows join line + room name
- palace-chat — post a message (303 back to room)
- palace-chat — poll API returns posted message
- palace-chat — presence lists the chatter
- palace-chat — HISTORY=8 caps initial pane at 8
- palace-chat — jump to /habbo-chat keeps session, redirects
- palace-chat — jump posts join line in habbo-chat
- palace-chat — leave habbo-chat redirects to chat directory
- habbo-chat — entry page /habbo.html 200
- habbo-chat — GET /habbo-chat w/o session redirects to entry page
- habbo-chat — guest entry POST redirects to /habbo-chat
- habbo-chat — chat pane shows join line + room name
- habbo-chat — post a message (303 back to room)
- habbo-chat — poll API returns posted message
- habbo-chat — presence lists the chatter
- habbo-chat — HISTORY=8 caps initial pane at 8
- habbo-chat — jump to /powwow-chat keeps session, redirects
- habbo-chat — jump posts join line in powwow-chat
- habbo-chat — leave powwow-chat redirects to chat directory
- powwow-chat — entry page /powwow.html 200
- powwow-chat — GET /powwow-chat w/o session redirects to entry page
- powwow-chat — guest entry POST redirects to /powwow-chat
- powwow-chat — chat pane shows join line + room name
- powwow-chat — post a message (303 back to room)
- powwow-chat — poll API returns posted message
- powwow-chat — presence lists the chatter
- powwow-chat — HISTORY=8 caps initial pane at 8
- powwow-chat — jump to /compuserve-chat keeps session, redirects
- powwow-chat — jump posts join line in compuserve-chat
- powwow-chat — leave compuserve-chat redirects to chat directory
- compuserve-chat — entry page /compuserve.html 200
- compuserve-chat — GET /compuserve-chat w/o session redirects to entry page
- compuserve-chat — guest entry POST redirects to /compuserve-chat
- compuserve-chat — chat pane shows join line + room name
- compuserve-chat — post a message (303 back to room)
- compuserve-chat — poll API returns posted message
- compuserve-chat — presence lists the chatter
- compuserve-chat — HISTORY=8 caps initial pane at 8
- compuserve-chat — jump to /prodigy-chat keeps session, redirects
- compuserve-chat — jump posts join line in prodigy-chat
- compuserve-chat — leave prodigy-chat redirects to chat directory
- prodigy-chat — entry page /prodigy.html 200
- prodigy-chat — GET /prodigy-chat w/o session redirects to entry page
- prodigy-chat — guest entry POST redirects to /prodigy-chat
- prodigy-chat — chat pane shows join line + room name
- prodigy-chat — post a message (303 back to room)
- prodigy-chat — poll API returns posted message
- prodigy-chat — presence lists the chatter
- prodigy-chat — HISTORY=8 caps initial pane at 8
- prodigy-chat — jump to /xfire-chat keeps session, redirects
- prodigy-chat — jump posts join line in xfire-chat
- prodigy-chat — leave xfire-chat redirects to chat directory
- xfire-chat — entry page /xfire.html 200
- xfire-chat — GET /xfire-chat w/o session redirects to entry page
- xfire-chat — guest entry POST redirects to /xfire-chat
- xfire-chat — chat pane shows join line + room name
- xfire-chat — post a message (303 back to room)
- xfire-chat — poll API returns posted message
- xfire-chat — presence lists the chatter
- xfire-chat — HISTORY=8 caps initial pane at 8
- xfire-chat — jump to /myspace-chat keeps session, redirects
- xfire-chat — jump posts join line in myspace-chat
- xfire-chat — leave myspace-chat redirects to chat directory
- myspace-chat — entry page /myspace.html 200
- myspace-chat — GET /myspace-chat w/o session redirects to entry page
- myspace-chat — guest entry POST redirects to /myspace-chat
- myspace-chat — chat pane shows join line + room name
- myspace-chat — post a message (303 back to room)
- myspace-chat — poll API returns posted message
- myspace-chat — presence lists the chatter
- myspace-chat — HISTORY=8 caps initial pane at 8
- myspace-chat — jump to /lobby keeps session, redirects
- myspace-chat — jump posts join line in lobby
- myspace-chat — leave lobby redirects to chat directory
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
- filter — innocent phrase across a word boundary passes
- filter — innocent phrase is stored/shown
- filter — three blocked posts all return 403
- filter — 3 strikes -> banned: clean message rejected (403)
- filter — banned user's clean message never stored
- filter — ban is per-user: another user posts fine
- filter — whisper with banned word passes unfiltered
- filter — whisper with banned word is delivered to recipient
- board — board page has post form + 1997 archive
- board — clean board post accepted
- board — new post shows above the 1997 archive
- board — GET /api/board/posts returns the new post as JSON
- board — GET /api/board/posts?board=clubgabbay filters to the main board
- board — GET /api/board/posts?board=hollywood is empty (no posts yet)
- board — GET /api/board/posts?board=nope is 404
- visits — GET /api/visits returns unique + total
- visits — landing page loads (200) and carries the counter
- visits — first landing visit counts one unique person
- visits — same person reloading does NOT count again (unique stays)
- visits — a different visitor IP counts as a new person
- visits — landing page has the donations / Ko-fi tip link
- board — markup post accepted (stored, escaped at render)
- board — markup in a post is escaped, never rendered
- board — banned word in board post is blocked (403)
- board — blocked board post never stored/shown
- board — three blocked board posts all return 403
- board — 3 strikes -> banned from board: clean post rejected
- board — post with no From name is not stored
- board — restore seeds an empty board from the backup file
- board — restore is idempotent (second run restores 0)
- board — restore skips a non-empty board (live posts kept)
- board — restore with an unreachable URL returns 0, no crash
- board — restore with no URL configured is a no-op
- board — neighborhood board page serves with its own form
- board — unknown neighborhood board is 404
- board — neighborhood board post accepted
- board — neighborhood post shows on its own board
- board — neighborhood post does NOT leak onto the main board
- board — API ?board=hollywood returns the neighborhood post
- board — API ?board=siliconvalley does not return it
- board — banned word in neighborhood post is blocked (403)
- board — post to an unknown neighborhood board is 404
- aol — AOL entry page serves with its handle form
- aol — GET /aol w/o session redirects to entry page
- aol — room page is the AOL skin with click-to-PM
- aol — message sound: AIM ding + Sound toggle, plays only for others
- aol — PM visible to sender + recipient only, not others
- aol — chat directory lists AOL Chat
- aol — handles board page serves with its own form
- aol — handles board post accepted
- aol — handles post shows on its own board
- aol — handles post does NOT leak onto the main board
- aol — API ?board=aol-handles returns the handles post
- aol — banned word in handles post is blocked (403)
- action — lobby room page has the action form
- action — valid action accepted
- action — action shows in the poll as kind=action
- action — action renders as '* user winks at target *'
- action — verb outside the whitelist is rejected
- action — target not in the room is rejected
- action — acting on yourself is rejected
- action — rejected actions are never stored
- action — second valid action accepted after the wait
- action — rate limit: 2nd action within 2s is 429
- action — AOL room page has the action form
- aol-style — AOL room page has color + font pickers
- aol-style — colored post accepted
- aol-style — API carries the color + font
- aol-style — colored message renders in its color + font
- aol-style — the color choice sticks in the session
- aol-style — injected color/font falls back to default
- aol-style — bad color/font stored as default (None)
- aol-style — injected markup never renders
- aol-style — lobby posts never carry a color/font
- 21plus — lobby room page says 21 and over
- 21plus — hollywood-chat room page says 21 and over
- 21plus — aol room page says 21 and over
- 21plus — /chat.htm says 21 and over
- 21plus — /chat2.htm says 21 and over
- 21plus — /lobby.cfm says 21 and over
- 21plus — /lobby2.cfm says 21 and over
- 21plus — /anything_goes.cfm says 21 and over
- 21plus — /jokeland.cfm says 21 and over
- 21plus — /aol.html says 21 and over
- 21plus — /neighborhoods/chat/hollywood.html says 21 and over
- 21plus — /neighborhoods/chat/area51.html says 21 and over
- 21plus — Anything Goes no longer says 18 anywhere
- landing — homepage is the new landing page: ADULTS ONLY gate
- landing — homepage says 21, never 18; no fake counts, no Netscape
- landing — homepage links all fourteen service pages
- landing — homepage has a Have Discord? link (Paul, 2026-11-09)
- landing — homepage carries the TheOldNet webring widget (Paul, 2026-11-09)
- landing — under-21 stop page serves
- landing — fine print carries the 21+ note + terms of entry
- landing — age gate without confirm bounces to /
- landing — no flag: directory bounces home (landing page)
- landing — age gate with confirm goes to /chat.htm
- landing — flag set: directory 200
- landing — /chat.htm without the flag bounces to /
- landing — /chat2.htm without the flag bounces to /
- landing — room entry without confirm bounces home
- landing — room entry with confirm reaches the room
- landing — entry set the flag: directory 200 after
- services — msn landing page serves with gate + handle form
- services — msn page links all fourteen services
- services — msn entry without confirm bounces home
- services — msn room wears its own skin: title bar #0078D7, member list + IM box, no AOL pickers
- services — msn v2+v3 chrome: Chat Rooms panel, MSN Chat tab, styled Send Send, chat white/Tahoma, colored joins, Nudge, gradient title, display pictures
- services — msn message sound: ding-msn + toggle, plays only for others
- services — msn permanent join lines: Mira + 1990calling at the top
- services — yahoo landing page serves with gate + handle form
- services — yahoo page links all fourteen services
- services — yahoo entry without confirm bounces home
- services — yahoo room wears its own skin: title bar #6001D2, member list + IM box, no AOL pickers
- services — yahoo v2+v3 chrome: Chat Rooms panel, Yahoo! Chat tab, styled Send Send, chat white/Tahoma, colored joins, BUZZ!, smiley
- services — yahoo message sound: ding-yahoo + toggle, plays only for others
- services — yahoo permanent join lines: Mira + 1990calling at the top
- services — icq landing page serves with gate + handle form
- services — icq page links all fourteen services
- services — icq entry without confirm bounces home
- services — icq room wears its own skin: title bar #00A000, member list + IM box, no AOL pickers
- services — icq v2+v3 chrome: Chat Rooms panel, #icq_usa tab, styled Send Send, chat white/Tahoma, colored joins, flower mark, flower petals
- services — icq message sound: uhoh + toggle, plays only for others
- services — icq permanent join lines: Mira + 1990calling at the top
- services — mirc landing page serves with gate + handle form
- services — mirc page links all fourteen services
- services — mirc entry without confirm bounces home
- services — mirc room wears its own skin: title bar #000080, member list + IM box, no AOL pickers
- services — mirc v2+v3 chrome: Chat Rooms panel, #Canada tab, styled Send Send, chat white/Courier New, colored joins, monospace, topic line, status bar
- services — mirc message sound: beep + toggle, plays only for others
- services — mirc permanent join lines: Mira + 1990calling at the top
- services — excite landing page serves with gate + handle form
- services — excite page links all fourteen services
- services — excite entry without confirm bounces home
- services — excite room wears its own skin: title bar #CC0000, member list + IM box, no AOL pickers
- services — excite v2+v3 chrome: Chat Rooms panel, Excite Chat tab, styled Send Send, chat white/Tahoma, colored joins, portal masthead
- services — excite message sound: silent + toggle, plays only for others
- services — excite permanent join lines: Mira + 1990calling at the top
- services — paltalk landing page serves with gate + handle form
- services — paltalk page links all fourteen services
- services — paltalk entry without confirm bounces home
- services — paltalk room wears its own skin: title bar #0099CC, member list + IM box, no AOL pickers
- services — paltalk v2+v3 chrome: Chat Rooms panel, Paltalk Chat tab, styled Send Send, chat white/Tahoma, colored joins, video strip
- services — paltalk message sound: silent + toggle, plays only for others
- services — paltalk permanent join lines: Mira + 1990calling at the top
- services — lycos landing page serves with gate + handle form
- services — lycos page links all fourteen services
- services — lycos entry without confirm bounces home
- services — lycos room wears its own skin: title bar #FF6600, member list + IM box, no AOL pickers
- services — lycos v2+v3 chrome: Chat Rooms panel, Lycos Chat tab, styled Send Send, chat white/Tahoma, colored joins, black/yellow masthead
- services — lycos message sound: silent + toggle, plays only for others
- services — lycos permanent join lines: Mira + 1990calling at the top
- services — palace landing page serves with gate + handle form
- services — palace page links all fourteen services
- services — palace entry without confirm bounces home
- services — palace room wears its own skin: title bar #993399, member list + IM box, no AOL pickers
- services — palace v2+v3 chrome: Chat Rooms panel, The Palace Chat tab, styled Send Send, chat #87CEEB/Comic Sans MS, colored joins, playful font, smiley avatars + bubbles, backdrop
- services — palace message sound: silent + toggle, plays only for others
- services — palace permanent join lines: Mira + 1990calling at the top
- services — habbo landing page serves with gate + handle form
- services — habbo page links all fourteen services
- services — habbo entry without confirm bounces home
- services — habbo room wears its own skin: title bar #E6B800, member list + IM box, no AOL pickers
- services — habbo v2+v3 chrome: Chat Rooms panel, Habbo Hotel Chat tab, styled Send Send, chat #003399/Verdana, colored joins, dark chat log, pixel floor, HC sofa
- services — habbo message sound: silent + toggle, plays only for others
- services — habbo permanent join lines: Mira + 1990calling at the top
- services — powwow landing page serves with gate + handle form
- services — powwow page links all fourteen services
- services — powwow entry without confirm bounces home
- services — powwow room wears its own skin: title bar #006666, member list + IM box, no AOL pickers
- services — powwow v2+v3 chrome: Chat Rooms panel, PowWow Chat tab, styled Send Send, chat white/Tahoma, colored joins, voice dot
- services — powwow message sound: silent + toggle, plays only for others
- services — powwow permanent join lines: Mira + 1990calling at the top
- services — compuserve landing page serves with gate + handle form
- services — compuserve page links all fourteen services
- services — compuserve entry without confirm bounces home
- services — compuserve room wears its own skin: title bar #003366, member list + IM box, no AOL pickers
- services — compuserve v2+v3 chrome: Chat Rooms panel, CB Channel 1 tab, styled GO Send, chat #000000/Courier New, colored joins, GO button
- services — compuserve message sound: silent + toggle, plays only for others
- services — compuserve permanent join lines: Mira + 1990calling at the top
- services — prodigy landing page serves with gate + handle form
- services — prodigy page links all fourteen services
- services — prodigy entry without confirm bounces home
- services — prodigy room wears its own skin: title bar #800000, member list + IM box, no AOL pickers
- services — prodigy v2+v3 chrome: Chat Rooms panel, Prodigy Chat tab, styled Send Send, chat white/Tahoma, colored joins, welcome strip, blue sidebar links
- services — prodigy message sound: silent + toggle, plays only for others
- services — prodigy permanent join lines: Mira + 1990calling at the top
- services — xfire landing page serves with gate + handle form
- services — xfire page links all fourteen services
- services — xfire entry without confirm bounces home
- services — xfire room wears its own skin: title bar #000000, member list + IM box, no AOL pickers
- services — xfire v2+v3 chrome: Chat Rooms panel, Xfire Chat tab, styled Send Send, chat #1A1A1A/Tahoma, colored joins, dark chat
- services — xfire message sound: silent + toggle, plays only for others
- services — xfire permanent join lines: Mira + 1990calling at the top
- services — myspace landing page serves with gate + handle form
- services — myspace page links all fourteen services
- services — myspace entry without confirm bounces home
- services — myspace room wears its own skin: title bar #003399, member list + IM box, no AOL pickers
- services — myspace v2+v3 chrome: Chat Rooms panel, MySpace Chat tab, styled Send Send, chat white/Tahoma, colored joins, Top 8 strip
- services — myspace message sound: silent + toggle, plays only for others
- services — myspace permanent join lines: Mira + 1990calling at the top
- board — db_init adds the board column to an old board DB
- board — old post reads back on the main board
- board — new post lands on its neighborhood board
- board — neighborhood post is not on the main board
- board — restore seeds a neighborhood post onto its board
- board — restored neighborhood post is not on the main board
- neighborhoods — neighborhoods index serves
- neighborhoods — home page links the neighborhoods
- neighborhoods — chat directory lists all five neighborhood rooms
- neighborhoods — button hollywood.gif serves as a GIF
- neighborhoods — button siliconvalley.gif serves as a GIF
- neighborhoods — button sunsetstrip.gif serves as a GIF
- neighborhoods — button area51.gif serves as a GIF
- neighborhoods — button westhollywood.gif serves as a GIF
- neighborhoods — our own 8-bit pixel G serves (not the trademarked logo)
- neighborhoods — original background background.gif serves as a GIF
- neighborhoods — original background area_glow.gif serves as a GIF
- neighborhoods — /neighborhoods/hollywood.html uses its own background
- neighborhoods — /neighborhoods/chat/hollywood.html uses its own background
- neighborhoods — /neighborhoods/siliconvalley.html uses its own background
- neighborhoods — /neighborhoods/chat/siliconvalley.html uses its own background
- neighborhoods — /neighborhoods/sunsetstrip.html uses its own background
- neighborhoods — /neighborhoods/chat/sunsetstrip.html uses its own background
- neighborhoods — /neighborhoods/area51.html uses its own background
- neighborhoods — /neighborhoods/chat/area51.html uses its own background
- neighborhoods — /neighborhoods/area51.html is black with white text, red links
- neighborhoods — /neighborhoods/chat/area51.html is black with white text, red links
- neighborhoods — /neighborhoods/westhollywood.html uses its own background
- neighborhoods — /neighborhoods/chat/westhollywood.html uses its own background
- neighborhoods — portal hollywood serves with its directory
- neighborhoods — board page for hollywood serves
- neighborhoods — portal siliconvalley serves with its directory
- neighborhoods — board page for siliconvalley serves
- neighborhoods — portal sunsetstrip serves with its directory
- neighborhoods — board page for sunsetstrip serves
- neighborhoods — portal area51 serves with its directory
- neighborhoods — board page for area51 serves
- neighborhoods — portal westhollywood serves with its directory
- neighborhoods — board page for westhollywood serves
- site — homepage carries the approved blurb
- site — homepage notes monitoring / 18+ / private whispers
- filter — blocklist is not served over HTTP (/blocklist.txt 404)
- filter — blocklist is not served (/backend/blocklist.txt 404)
- site — link check / (36 links): server matches archive
- site — link check /chat.htm (26 links): server matches archive
- site — link check /chat2.htm (34 links): server matches archive
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
