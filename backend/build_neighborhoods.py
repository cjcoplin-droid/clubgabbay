#!/usr/bin/env python3
"""Build the five GeoCities neighborhood portal pages + the neighborhoods
index, from one template (Paul, 2026-11-09: same setup for all).

Suburb lists and facts come from neighborhoods-research.md (Blade's Place
cross-checked against the Restorativland gallery and the 1996 Wikipedia
table). Outbound links are the ones verified live with curl on 2026-11-09:
Oocities neighborhood browse, Wayback wildcard, Blade's Place, GifCities,
Cameron's World. No Restorativland links (down, 522, on 2026-11-09) and
never geocities.ws. Run from the repo root: python3 backend/build_neighborhoods.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "www2.clubgabbay.com", "neighborhoods")

HOODS = [
    {
        "slug": "hollywood",
        "name": "Hollywood",
        "tag": "Films and TV -- the very first GeoCities neighborhood, July 1995",
        "chat_desc": ("Lights, camera, chat!!! Talk movies, TV and stars with "
                      "your fellow Hollywood homesteaders!!!"),
        "chat_join": "Joins The Hollywood Chat...",
        "intro": ("Hollywood was the very first GeoCities neighborhood, opened "
                  "July 1995 -- films and TV, actors and actresses. If you loved "
                  "movies, this was your block. Its suburbs had names like Hills, "
                  "Star, Studio and Cinema, and every homesteader picked a "
                  "four-digit block to call home."),
        "suburbs": ["Academy", "Agency", "Backdrop", "Boulevard", "Bungalow",
                    "Camera", "Chateau", "Cinema", "Club", "Derby", "Diva",
                    "Film", "Guild", "Heights", "Highrise", "Hills",
                    "Interview", "Land", "Location", "Lot", "Makeup",
                    "Mansion", "Movie", "Palace", "Park", "Pavillion",
                    "Picture", "Prop", "Screen", "Set", "Star", "Studio",
                    "Theater", "Trailer", "Video"],
    },
    {
        "slug": "siliconvalley",
        "name": "SiliconValley",
        "tag": "Computers, hardware, software and programming -- August 1995",
        "chat_desc": ("Log on and talk tech!!! Hardware, software, programming "
                      "-- the SiliconValley homesteaders are online!!!"),
        "chat_join": "Joins The SiliconValley Chat...",
        "intro": ("SiliconValley opened August 1995 for computers, hardware, "
                  "software and programming -- the techies' neighborhood. Its "
                  "suburbs were named for the trade: Heights, Park, Pines, Chip, "
                  "Code, Modem, Server."),
        "suburbs": ["Bay", "Bit", "Board", "Bridge", "Byte", "Cable", "Campus",
                    "Chip", "Circuit", "Code", "Disk", "Drive", "File",
                    "Foothills", "Garage", "Grid", "Hardware", "Haven",
                    "Heights", "Hills", "Horizon", "Hub", "Lab", "Lakes",
                    "Modem", "Monitor", "Mouse", "Network", "Node", "Office",
                    "Orchard", "Park", "Peaks", "Pines", "Platform", "Port",
                    "Program", "Ridge", "Screen", "Sector", "Server",
                    "Software", "Station", "Storage", "Vista", "Way"],
    },
    {
        "slug": "sunsetstrip",
        "name": "SunsetStrip",
        "tag": "Rock, grunge, punk, blues and the club scene -- July 1995",
        "chat_desc": ("Turn it up!!! Talk rock, grunge, punk and the club scene "
                      "with your SunsetStrip neighbors!!!"),
        "chat_join": "Joins The SunsetStrip Chat...",
        "intro": ("SunsetStrip opened July 1995 for music -- rock, grunge, punk, "
                  "blues and the club scene. Its suburbs read like a night out: "
                  "Vine, Alley, Palms, Studio, Towers, Backstage, Frontrow."),
        "suburbs": ["Alley", "Amphitheater", "Arena", "Auditorium",
                    "Backstage", "Balcony", "Bar", "Basement", "Bass", "Beat",
                    "Birdland", "Bistro", "Booth", "Cabaret", "Club",
                    "Concert", "Derby", "Diner", "Disco", "Event", "Exhibit",
                    "Festival", "Floor", "Frontrow", "Gala", "Garage",
                    "Hall", "Hotel", "Limo", "Lobby", "Loft", "Loge",
                    "Lounge", "Mezzanine", "Palace", "Palladium", "Palms",
                    "Pavilion", "Performance", "Pit", "Plaza", "Scene",
                    "Set", "Show", "Stadium", "Stage", "Street", "Studio",
                    "Tempo", "Theater", "Towers", "Underground", "Venue",
                    "Villa", "Vine"],
    },
    {
        "slug": "area51",
        "name": "Area51",
        "tag": "Science fiction and fantasy -- April 1996",
        "chat_desc": ("The truth is in here!!! Talk sci-fi, fantasy and "
                      "conspiracy theories with your fellow Area51 "
                      "homesteaders!!!"),
        "chat_join": "Joins The Area51 Chat...",
        "intro": ("Area51 opened April 1996 for science fiction and fantasy -- "
                  "and conspiracy theories. Its suburbs were pure imagination: "
                  "Vault, Stargate, Starship, Nebula, Dimension, Dreamworld."),
        "suburbs": ["Alien", "Atlantis", "Aurora", "Capsule", "Cavern",
                    "Chamber", "Comet", "Corridor", "Crater", "Dimension",
                    "Dreamworld", "Dunes", "Dungeon", "Hole", "Hollow",
                    "Jupiter", "Keep", "Labyrinth", "Lair", "Matrix",
                    "Meteor", "Nebula", "Neptune", "Nova", "Omega", "Orion",
                    "Planet", "Portal", "Quadrant", "Quark", "Quasar",
                    "Rampart", "Realm", "Saturn", "Shadowlands", "Shire",
                    "Shuttle", "Stargate", "Starship", "Station",
                    "Underworld", "Vault", "Zone"],
    },
    {
        "slug": "westhollywood",
        "name": "WestHollywood",
        "tag": "Gay, lesbian, bisexual and transgender topics -- July 1995",
        "chat_desc": ("Come as you are!!! Talk life, love and community with "
                      "your WestHollywood neighbors!!!"),
        "chat_join": "Joins The WestHollywood Chat...",
        "intro": ("WestHollywood opened July 1995 for gay, lesbian, bisexual and "
                  "transgender topics -- one of the six original neighborhoods, "
                  "and a community that mattered. Its suburbs: Cafe, Castro, "
                  "Chelsea, Stonewall, Village."),
        "suburbs": ["Cafe", "Castro", "Chateau", "Chelsea", "Club", "Heights",
                    "Parade", "Park", "Salon", "Stonewall", "Villa",
                    "Village"],
    },
]

FOOTER = ('<font color=gray size=2>Club Gabbay -- a fan-run homage to the '
          '1996-1999 original. <a href="/fine-print.html">Fine print</a>'
          '</font><br>\n'
          '<font color=gray size=1>Neighborhood buttons by Chaz Boston '
          'Baden, via <a href="https://www.bladesplace.id.au/geocities-'
          'neighborhoods-suburbs.html">Blade\'s Place</a>.</font>')


def chat_entry(h):
    """The chat room's entry page, mirroring the Gabbay room entries:
    a handle + history picker posting USER/SAYS/HISTORY to the room."""
    heading = ('<center><img src="/images/neighborhoods/%s.gif"></center>\n'
               '<center><font size="+3"><strong>%s Chat</strong></font>'
               '</center>\n'
               '<center><font size="+1">%s</font></center>'
               % (h["slug"], h["name"], h["chat_desc"]))
    body = ('<center>\n'
            '<form action="/%s-chat" method="post">\n'
            'Your handle: <input type="text" name="USER" size="12" '
            'maxlength="12"><br>\n'
            'Show last <select name="HISTORY">'
            '<option value="8" selected>8</option>'
            '<option value="16">16</option>'
            '<option value="32">32</option></select> messages<br>\n'
            '<input type="hidden" name="SAYS" value="%s">\n'
            '<input type="submit" value="Enter the chat">\n'
            '</form>\n</center>\n'
            '<hr noshade>\n'
            '<center><font size="-1"><a href="/neighborhoods/%s.html">Back '
            'to %s</a> | <a href="/neighborhoods/">All neighborhoods</a> | '
            '<a href="/">Club Gabbay Home</a> | '
            '<a href="/fine-print.html">Fine print</a></font></center>\n'
            '<hr noshade>\n<center>%s</center>\n'
            % (h["slug"], h["chat_join"], h["slug"], h["name"], FOOTER))
    return page("%s Chat -- GeoCities neighborhood" % h["name"],
                heading, body)


def webring(current=None):
    parts = ['<a href="/">Club Gabbay</a>']
    for h in HOODS:
        if h["slug"] == current:
            parts.append("<b>%s</b>" % h["name"])
        else:
            parts.append('<a href="/neighborhoods/%s.html">%s</a>'
                         % (h["slug"], h["name"]))
    return ("<center><font size=2>The GeoCities neighborhoods ring:<br>\n"
            + " | ".join(parts) + "</font></center>\n")


def page(title, heading, body):
    return ('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n<html>\n<head>\n'
            '<meta http-equiv="Content-Type" content="text/html; '
            'charset=iso-8859-1">\n'
            '<title>%s</title>\n</head>\n'
            '<body background="/clubgabbay.com/images/bg/home_bg.jpg">\n'
            '%s\n'
            '<hr noshade>\n%s\n'
            '</body></html>\n' % (title, heading, body))


def portal(h):
    heading = ('<center><img src="/images/neighborhoods/%s.gif"></center>\n'
               '<center><font size="+3"><strong>%s</strong></font></center>\n'
               '<center><font size="+1">%s</font></center>'
               % (h["slug"], h["name"], h["tag"]))
    body = ('<p><font size="+1">%s</font></p>\n'
            '<p>This is a fan-made portal, not the original GeoCities page. '
            'The original is gone; the homesteads live on in the archives '
            'linked below. Were you a homesteader here? '
            '<a href="/%s-chat">Enter the %s chat</a> or '
            '<a href="/neighborhoods/%s/board/">leave a message on the %s '
            'board</a> -- say what your address was, who you remember, and '
            'where life took you.</p>\n'
            '<hr noshade>\n'
            '<center><b>The suburbs of %s</b></center>\n'
            '<p>When a neighborhood filled up, the volunteer Community Leaders '
            'opened suburbs -- each with its own blocks. %s\'s suburbs were: '
            '%s.</p>\n'
            '<hr noshade>\n'
            '<center><b>Browse the old pages</b></center>\n'
            '<ul>\n'
            '<li><a href="http://www.oocities.org/%s/">%s on Oocities</a> -- '
            'the live mirror: browse the archived homesteads at their old '
            'addresses.</li>\n'
            '<li><a href="https://web.archive.org/web/*/geocities.com/%s/">'
            '%s on the Wayback Machine</a> -- every capture of the '
            'neighborhood.</li>\n'
            '<li><a href="https://www.bladesplace.id.au/geocities-'
            'neighborhoods-suburbs.html">Every GeoCities neighborhood and '
            'suburb, at Blade\'s Place</a></li>\n'
            '<li><a href="https://gifcities.org/">GifCities</a> -- the '
            'Internet Archive\'s GeoCities GIF search. '
            '<a href="https://www.cameronsworld.net/">Cameron\'s World</a> '
            '-- a collage of the old web.</li>\n'
            '</ul>\n'
            '<hr noshade>\n%s'
            '<hr noshade>\n<center>%s</center>\n'
            % (h["intro"], h["slug"], h["name"], h["slug"], h["name"],
               h["name"], h["name"], ", ".join(h["suburbs"]), h["name"],
               h["name"], h["name"], h["name"], webring(h["slug"]), FOOTER))
    return page("%s -- GeoCities neighborhood, back home" % h["name"],
                heading, body)


def index():
    heading = ('<center><img src="/images/neighborhoods/geocities-logo.jpg">'
               '</center>\n'
               '<center><font size="+3"><strong>The old GeoCities '
               'neighborhoods</strong></font></center>\n'
               '<center><font size="+1">Five neighborhoods, the way they '
               'were -- fan-made portals, each with its own board and chat '
               'room</font>'
               '</center>')
    rows = []
    for h in HOODS:
        rows.append('<li><img src="/images/neighborhoods/%s.gif"> '
                    '<a href="/neighborhoods/%s.html"><b>%s</b></a> -- %s '
                    '<a href="/%s-chat">(chat)</a> '
                    '<a href="/neighborhoods/%s/board/">(board)</a></li>'
                    % (h["slug"], h["slug"], h["name"], h["tag"],
                       h["slug"], h["slug"]))
    body = ('<p><font size="+1">GeoCities sorted its free home pages into '
            'themed neighborhoods, each with its own directory, chat rooms, '
            'bulletin boards and volunteer Community Leaders. Yahoo shut it '
            'down in October 2009, but the neighborhoods live on in the '
            'archives -- and now here, as fan-made portals. Pick one, browse '
            'the old pages, chat with your neighbors, and leave a message on '
            'its board if you were there.</font></p>\n'
            '<ul>\n' + "\n".join(rows) + '\n</ul>\n'
            '<hr noshade>\n'
            '<center><b>Browse all of GeoCities</b></center>\n'
            '<ul>\n'
            '<li><a href="http://www.oocities.org/">Oocities</a> -- the live '
            'mirror of the old GeoCities addresses.</li>\n'
            '<li><a href="https://web.archive.org/web/*/geocities.com/">'
            'GeoCities on the Wayback Machine</a></li>\n'
            '<li><a href="https://www.bladesplace.id.au/geocities-'
            'neighborhoods-suburbs.html">Every GeoCities neighborhood and '
            'suburb, at Blade\'s Place</a></li>\n'
            '<li><a href="https://gifcities.org/">GifCities</a> -- the '
            'Internet Archive\'s GeoCities GIF search. '
            '<a href="https://www.cameronsworld.net/">Cameron\'s World</a> '
            '-- a collage of the old web.</li>\n'
            '</ul>\n'
            '<hr noshade>\n%s'
            '<hr noshade>\n<center>%s</center>\n'
            % (webring(), FOOTER))
    return page("The old GeoCities neighborhoods -- back home", heading, body)


def main():
    os.makedirs(OUT, exist_ok=True)
    chat_dir = os.path.join(OUT, "chat")
    os.makedirs(chat_dir, exist_ok=True)
    for h in HOODS:
        path = os.path.join(OUT, h["slug"] + ".html")
        with open(path, "w", encoding="ascii") as fh:
            fh.write(portal(h))
        print("wrote", path)
        path = os.path.join(chat_dir, h["slug"] + ".html")
        with open(path, "w", encoding="ascii") as fh:
            fh.write(chat_entry(h))
        print("wrote", path)
    path = os.path.join(OUT, "index.html")
    with open(path, "w", encoding="ascii") as fh:
        fh.write(index())
    print("wrote", path)


if __name__ == "__main__":
    main()
