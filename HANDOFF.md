# Saint Wallpaper: notes for picking up the work

Owner: Charles Bacon (GitHub: cbacon1). Not a programmer: explain things in plain
English, say where things are stored, and show pictures of changes before/after.

## What it is
A daily wallpaper of the Catholic saint, feast or Gospel scene of the day, on the
official U.S. liturgical calendar (worldwide calendar is a setting).
- **Mac app** (menu-bar ✝): draws and sets the desktop wallpaper every day.
- **iPhone**: a Shortcut downloads that day's pre-made Lock Screen picture.
- **Website**: https://cbacon1.github.io/saint-wallpaper/ (GitHub Pages, repo
  cbacon1/saint-wallpaper, branch main). It is also where every Mac and phone
  gets its content, so content edits reach everyone within hours.

## Where things live
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
- Installed app: `/Applications/Saint Wallpaper.app`; its downloaded content:
  `~/Library/Application Support/Saint Wallpaper/Content`
- Website repo: `content/` (img/ full pictures named `<id>-<sha8>.jpg`, thumb/,
  phone/YYYY-MM-DD.jpg, days.json, bios/art/images/calendar json),
  `download/` (Saint-Wallpaper.zip, latest.json, Saint-Wallpaper.shortcut),
  `tools/phone/` (phone.py renderer, render_all.py), `index.html`.

## How changes reach people
- **Content** (pictures, quotes, texts): edit data, copy changed files into the
  repo `content/`, regenerate `content/days.json` with the installed app:
  `SaintWallpaper --days 2026-11-12 2027-12-31 out.json` (after the app has synced
  the new content), re-render affected iPhone pictures with tools/phone, push.
- **App code**: raise CFBundleVersion, `./build.sh --install --share`, copy
  build/Saint Wallpaper.zip → download/Saint-Wallpaper.zip and build/latest.json →
  download/latest.json, push. Installed Macs (build ≥ 2) update themselves.
- The iPhone Shortcut fetches `content/phone/<today>.jpg` daily at 12:01 AM.

## Rules decided so far
- Show paintings whole, never cropped; no picture used twice in the year;
  no white/grey borders; most famous public-domain depiction of each saint.
- Gospel days: an RSV-2CE quote (credit line in ✝ Credits and site footer, not on
  the wallpaper). About 300 verses used of the 500 allowed without permission.
- Church ranking: Lent weekdays, Dec 17–24 and the Christmas octave outrank
  memorials; the saint gets "Commemoration of …" under the title.
- Mac text: saint days = rank on top, title · lifetime in italics; other days =
  date on top (season name when the title is a date). No Gospel reference shown.
- iPhone text: name, italic title or commemoration, dot + rank, quote/story.

## Open items
1. iPhone pictures and days.json end 2027-12-31: render 2028 before then.
2. GitHub Pages ~833 MB of 1 GB: shrink phone JPEGs or move pictures elsewhere.
3. Mac app is unsigned ("Open Anyway"); App Store/notarizing needs the $99 program.
4. iPhone widget app waits on macOS update + Xcode; free signing expires weekly.
5. Three Lent days use small Tissot watercolors (lower resolution).
