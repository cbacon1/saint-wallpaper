# Ordo

This repository is the online home of **Ordo** (formerly Saint Wallpaper), a Mac menu-bar app and iPhone Lock Screen picture showing what the Church celebrates each day: the feast, the Sunday or season with its Gospel, or the saint. Its address keeps the old name, because every installed copy downloads from it.

- `index.html` – the download page: https://cbacon1.github.io/saint-wallpaper/
- `download/Ordo.zip` – the Mac app people download from the page
- `download/Saint-Wallpaper.zip` – the same app under its old file name, used only by automatic updates (`latest.json` points to it)
- `download/Ordo.shortcut` – the iPhone Shortcut (`Saint-Wallpaper.shortcut` is the same file under its old name)
- `content/` – what every copy of the app reads (`phone/` holds each day's ready-made iPhone Lock Screen picture; `thumb/` small pictures for the widget; `days.json` the whole calendar day by day):
  - `calendar.json` – the liturgical calendar (U.S. and General Roman), 2026–2045
  - `images.json` – which picture goes with each saint, feast or Gospel, with artist and license
  - `bios.json` – the text about each saint, feast or day's Gospel
  - `art.json` – the note about each picture
  - `sources.tsv` – Wikipedia articles for the "Read About Today's Celebration" menu item
  - `img/` – the pictures (each file name ends in a fingerprint, so a changed picture gets a new name and every app downloads it)

When anything in `content/` changes here, the website updates within a minute or two and every copy of the app picks it up within a few hours (or right away with **Refresh Wallpaper Now** in the ✝ menu).

The app's source code, the notes, and the tools that prepare the pictures (including the one that draws `content/phone/`) live in the private repository cbacon1/saint-wallpaper-code and the project folder on the owner's Mac.
