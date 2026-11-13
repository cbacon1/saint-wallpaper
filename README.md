# Saint Wallpaper

This repository is the online home of **Saint Wallpaper**, a Mac menu-bar app that sets the desktop to the saint or feast of the day.

- `index.html` – the download page: https://cbacon1.github.io/saint-wallpaper/
- `download/Saint-Wallpaper.zip` – the app people download
- `content/` – what every copy of the app reads:
  - `calendar.json` – the liturgical calendar (U.S. and General Roman), 2026–2045
  - `images.json` – which picture goes with each saint, feast or Gospel, with artist and license
  - `bios.json` – the text about each saint, feast or day's Gospel
  - `art.json` – the note about each picture
  - `sources.tsv` – Wikipedia articles for the "Read About Today's Feast" menu item
  - `img/` – the pictures (each file name ends in a fingerprint, so a changed picture gets a new name and every app downloads it)

When anything in `content/` changes here, the website updates within a minute or two and every copy of the app picks it up within a few hours (or right away with **Refresh Wallpaper Now** in the ✝ menu).

The app's source code and the tools that prepare the pictures live in the project folder on the owner's Mac.
