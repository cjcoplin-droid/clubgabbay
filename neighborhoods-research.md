# GeoCities top-5 neighborhoods — research brief
Researched 2026-11-09 by Mira (directly; the research helper refused its
attempt without doing any work — no file was written, so the digging was
done here instead). All links below were verified live with curl on
2026-11-09 unless marked otherwise. Nothing is invented: suburb lists
come from Blade's Place (bladesplace.id.au) cross-checked against the
Restorativland gallery listing and the 1996 Wikipedia neighborhood table.

## Sources (all live 2026-11-09)
- Blade's Place, GeoHoods: https://www.bladesplace.id.au/geocities-neighborhoods-suburbs.html (200) — every neighborhood + suburb, with Community Center links.
- The Geocities Gallery (Restorativland): https://geocities.restorativland.org/ — DOWN on 2026-11-09 (522 from Cloudflare, origin unreachable; crawled 1 day earlier). DO NOT link it until it recovers and re-checks 200.
- Oocities: http://www.oocities.org/ (200) — the live mirror; old GeoCities URLs work under oocities.org/<Neighborhood>/<lot>/.
- Wayback wildcard per neighborhood: https://web.archive.org/web/*/geocities.com/<Neighborhood>/ (200, all five).
- GifCities: https://gifcities.org/ (200). Cameron's World: https://www.cameronsworld.net/ (200).
- NEVER link geocities.ws (flagged scam site). reocities / geocitiesarchive.org are dead.

## General facts (already established)
- GeoCities: 38M pages, 3rd most visited site in the world (early 1999), Yahoo bought it for $3.57B (Jan 1999), shut down Oct 26 2009. 29 neighborhoods in 1996, 41 by 1997.
- Homesteaders picked a neighborhood + a 4-digit block (1000-9999): geocities.com/<Neighborhood>/<XXXX>. When a neighborhood filled, Community Leaders created suburbs, also with blocks: geocities.com/<Neighborhood>/<Suburb>/<XXXX>.
- Yahoo dismantled the neighborhoods + Community Leaders program in July 1999 (vanity URLs tied to Yahoo IDs); homestead addresses kept working.

## Hollywood — Film and TV. Added July 1995, the FIRST neighborhood.
Suburbs (35): Academy, Agency, Backdrop, Boulevard, Bungalow, Camera, Chateau, Cinema, Club, Derby, Diva, Film, Guild, Heights, Highrise, Hills, Interview, Land, Location, Lot, Makeup, Mansion, Movie, Palace, Park, Pavillion, Picture, Prop, Screen, Set, Star, Studio, Theater, Trailer, Video.
1996 core (Wikipedia): Hollywood and Hills.
Verified links: Oocities http://www.oocities.org/Hollywood/ (200); Wayback https://web.archive.org/web/*/geocities.com/Hollywood/ (200).

## SiliconValley — Computers, hardware, software, programming. Added August 1995.
Suburbs (45): Bay, Bit, Board, Bridge, Byte, Cable, Campus, Chip, Circuit, Code, Disk, Drive, File, Foothills, Garage, Grid, Hardware, Haven, Heights, Hills, Horizon, Hub, Lab, Lakes, Modem, Monitor, Mouse, Network, Node, Office, Orchard, Park, Peaks, Pines, Platform, Port, Program, Ridge, Screen, Sector, Server, Software, Station, Storage, Vista, Way.
1996 core (Wikipedia): Heights, Park, Pines.
Verified links: Oocities http://www.oocities.org/SiliconValley/ (200); Wayback https://web.archive.org/web/*/geocities.com/SiliconValley/ (200).
Note: CDX returned real captures incl. the 1996 neighborhood root and lot 1000 (ham-radio page).

## SunsetStrip — Rock, grunge, punk, blues, the club scene. Added July 1995.
Suburbs (55): Alley, Amphitheater, Arena, Auditorium, Backstage, Balcony, Bar, Basement, Bass, Beat, Birdland, Bistro, Booth, Cabaret, Club, Concert, Derby, Diner, Disco, Event, Exhibit, Festival, Floor, Frontrow, Gala, Garage, Hall, Hotel, Limo, Lobby, Loft, Loge, Lounge, Mezzanine, Palace, Palladium, Palms, Pavilion, Performance, Pit, Plaza, Scene, Set, Show, Stadium, Stage, Street, Studio, Tempo, Theater, Towers, Underground, Venue, Villa, Vine.
1996 core (Wikipedia): Vine, Alley, Palms, Studio, Towers.
Verified links: Oocities http://www.oocities.org/SunsetStrip/ (200); Wayback https://web.archive.org/web/*/geocities.com/SunsetStrip/ (200).
Note: CDX returned real captures incl. the 1996 neighborhood root and lot 1000 (Community Leaders contest pages).

## Area51 — Science Fiction, Fantasy. Added April 1996.
Suburbs (43): Alien, Atlantis, Aurora, Capsule, Cavern, Chamber, Comet, Corridor, Crater, Dimension, Dreamworld, Dunes, Dungeon, Hole, Hollow, Jupiter, Keep, Labyrinth, Lair, Matrix, Meteor, Nebula, Neptune, Nova, Omega, Orion, Planet, Portal, Quadrant, Quark, Quasar, Rampart, Realm, Saturn, Shadowlands, Shire, Shuttle, Stargate, Starship, Station, Underworld, Vault, Zone.
1996 core (Wikipedia): Vault.
Verified links: Oocities http://www.oocities.org/Area51/ (200); Wayback https://web.archive.org/web/*/geocities.com/Area51/ (200).
Note: the Wayback CDX query for Area51 failed twice (slow/rate-limited); no individual member pages listed — see the decision below.

## WestHollywood — Gay, lesbian, bisexual and transgender topics. Added July 1995.
Suburbs (12): Cafe, Castro, Chateau, Chelsea, Club, Heights, Parade, Park, Salon, Stonewall, Villa, Village.
(Blade's list; the gallery lists the same minus Chateau and Villa.)
Verified links: Oocities http://www.oocities.org/WestHollywood/ (200); Wayback https://web.archive.org/web/*/geocities.com/WestHollywood/ (200).
Note: CDX returned real captures incl. the 1996 neighborhood root and lot 1000.

## Decisions for the portal build (Paul's rules)
- Each portal links OUT to its neighborhood's archive browse (Oocities root + Wayback wildcard) and to Blade's Place — all verified 200. No Restorativland links until it recovers and re-checks 200. No geocities.ws ever.
- NO individual member pages are listed on the portals. The Wayback CDX results were noisy (mostly image files and subpages; Hollywood + Area51 queries failed outright), and listing arbitrary lot numbers would be noise, not a directory. The archive-browse links ARE the path into the member pages — the way a directory pointed you into the neighborhood. If a real, identifiable famous page surfaces later, it can be added once verified.
- Portal copy is our own words (homage), not copied pages. Same template for all five, webring bar linking all five + Club Gabbay, each with its own board (already built in server.py).
