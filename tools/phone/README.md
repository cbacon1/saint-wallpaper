# iPhone wallpapers

`render_all.py [YYYY-MM-DD]` draws the iPhone lock-screen wallpaper for every day in
`content/days.json` (from the given date on) into `content/phone/YYYY-MM-DD.jpg`.
The iPhone Shortcut downloads `content/phone/<today>.jpg` each morning.

Needs Python 3 with Pillow. Fonts: Inter Display (SIL Open Font License).
