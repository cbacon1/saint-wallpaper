# Ordo: notes for picking up the work

Owner: Charles Bacon (GitHub: cbacon1). Not a programmer: explain things in plain
English, say where things are stored, and show pictures of changes before/after.

## What it is
**Ordo** (renamed from "Saint Wallpaper" on 2026-11-15) is a daily check-in with the
liturgical day: whatever the Church celebrates that day (a solemnity or feast, a
Sunday or season weekday with its Gospel, or a saint's memorial) shown with a great
painting, on the official U.S. liturgical calendar (worldwide calendar is a setting).
- **The name, and what didn't change:** people see "Ordo" (menu, Settings, website,
  Shortcut). Behind the scenes the old name stays on purpose: the web address
  `cbacon1.github.io/saint-wallpaper`, both repo names, the app ID
  `com.charlesbacon.SaintWallpaper`, the program name `SaintWallpaper`, the folder
  `~/Library/Application Support/Saint Wallpaper`, the Desktop project folder, and
  for now the app's file name `Saint Wallpaper.app` (see Open items).
- **Mac app** (menu-bar ✝): draws and sets the desktop wallpaper every day.
- **iPhone**: a Shortcut downloads that day's pre-made Lock Screen picture.
- **Website**: https://cbacon1.github.io/saint-wallpaper/ (GitHub Pages, repo
  cbacon1/saint-wallpaper, branch main). It is also where every Mac and phone
  gets its content, so content edits reach everyone within hours.

## Where things live
- **Two GitHub repos:** `cbacon1/saint-wallpaper` (PUBLIC: the website and all
  daily content; never rename it, every installed app downloads from its address)
  and `cbacon1/saint-wallpaper-code` (PRIVATE: the code, data and tools; a backup of
  the Mac project folder minus the pictures).
- Mac project folder ("the workshop"): `~/Desktop/Saint Wallpaper/`
  - `Sources/*.swift` app code · `App/Info.plist` (CFBundleVersion = build number)
  - `data/` calendar.json (2026–2045), paintings.tsv (which picture per day),
    bios.json (story, or Gospel quote + reference in "years"), art.json (picture
    notes), images.json (credits, licenses)
  - `images/` prepared pictures · `images_src/` originals · `previews/` checks
  - `tools/fetch_paintings.py` (download pictures in paintings.tsv),
    `tools/render_previews.sh` (re-make previews/)
  - `iPhone App/` demo iPhone app + widget (needs Xcode 27 + macOS 26.6+; not built yet)
  - `build.sh [--install] [--share] [--with-images]`
- Installed app: `/Applications/Saint Wallpaper.app` (shows as Ordo); its downloaded content:
  `~/Library/Application Support/Saint Wallpaper/Content`
- Website repo: `content/` (img/ full pictures named `<id>-<sha8>.jpg`, thumb/,
  phone/YYYY-MM-DD.jpg, days.json, bios/art/images/calendar json),
  `download/` (Saint-Wallpaper.zip, latest.json, Ordo.shortcut; the old
  Saint-Wallpaper.shortcut is an identical copy kept for old links),
  `tools/phone/` (phone.py renderer, render_all.py), `index.html`.

## How changes reach people
- **Content** (pictures, quotes, texts): edit data, copy changed files into the
  repo `content/`, regenerate `content/days.json` with the installed app:
  `SaintWallpaper --days 2026-11-12 2027-12-31 out.json` (after the app has synced
  the new content), re-render affected iPhone pictures with tools/phone, push.
- **App code**: raise CFBundleVersion in `mac-app/App/Info.plist` and push to the
  code repo. GitHub builds it on its own Mac (`.github/workflows/build-mac.yml`,
  about 1 minute) and puts Saint-Wallpaper.zip, latest.json, days-check.json (should
  match content/days.json) and two sample wallpapers on the code repo's `builds`
  branch. Check those, copy the zip and latest.json into the website's `download/`,
  push. Installed Macs (build ≥ 2) update themselves within hours. Building on the
  Mac with `./build.sh --install --share` still works the same way.
- The iPhone Shortcut fetches `content/phone/<today>.jpg` daily at 12:01 AM.

## Rules decided so far
- **The day comes first, not the saint.** Each day shows the celebration that wins
  under the Church's Table of Liturgical Days (the ranking in calendar.json), from
  the top: the Easter Triduum; Christmas, Epiphany, Ascension, Pentecost; Sundays
  of Advent, Lent and Easter, Ash Wednesday, Holy Week and the Easter octave;
  solemnities; feasts of the Lord; other Sundays; feasts; Advent weekdays Dec 17–24,
  the Christmas octave and Lent weekdays; obligatory memorials; optional memorials;
  ordinary weekdays (which show that day's Gospel).
- When a privileged weekday (Lent, Dec 17–24, Christmas octave) falls on a
  memorial, the weekday is shown and the saint gets "Commemoration of …" under it.
- Show paintings whole, never cropped; no picture used twice in the year;
  no white/grey borders; most famous public-domain depiction of each saint.
- Gospel days: an RSV-2CE quote (credit line in ✝ Credits and site footer, not on
  the wallpaper). About 300 verses used of the 500 allowed without permission.
- Mac text: saint days = rank on top, title · lifetime in italics; other days =
  date on top (season name when the title is a date). No Gospel reference shown.
- iPhone text: name, italic title or commemoration, dot + rank, quote/story.

## Open items
1. iPhone pictures and days.json end 2027-12-31: render 2028 before then.
2. GitHub Pages ~833 MB of 1 GB: shrink phone JPEGs or move pictures elsewhere.
3. Mac app is unsigned ("Open Anyway"); App Store/notarizing needs the $99 program.
4. iPhone widget app waits on macOS update + Xcode; free signing expires weekly.
5. Three Lent days use small Tissot watercolors (lower resolution).
6. App file name: still `Saint Wallpaper.app` because Macs on build 5 or older only
   accept an update with that name. Build 6 (published 2026-11-15) accepts
   `Ordo.app` too. Once installed copies are on 6+, change `APPNAME` in build.sh to
   "Ordo" and add a one-time step in the app that renames itself in Applications
   (and re-registers the login item); test that on the Mac before publishing.
7. The text note inside the signed iPhone Shortcut still says "Saint Wallpaper"
   (only visible when editing it). Fixing it means editing and re-signing it on a
   Mac (`shortcuts sign`) as Ordo.shortcut.
