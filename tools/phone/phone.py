"""Draws the iPhone lock-screen wallpaper for a day.

usage: phone.py STYLE DATE OUT.jpg [--mock]
STYLE is gallery | season | blur. --mock draws a fake lock-screen clock on top (for previews only).
"""
import json, os, re, sys, textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("SITE", os.path.join(HERE, "..", ".."))
W, H = 1290, 2796                      # iPhone Pro Max size; iOS scales it for other iPhones
F = lambda name, size: ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

INK, QUIET = (238, 232, 220), (190, 182, 168)
GALLERY = (59, 64, 56)
SEASON = {"green": (31, 52, 37), "violet": (44, 33, 62), "purple": (44, 33, 62), "red": (64, 22, 19),
          "rose": (78, 42, 52), "white": (58, 48, 33), "gold": (58, 48, 33), "black": (24, 24, 24)}
DOT = {"green": (86, 150, 86), "violet": (138, 104, 186), "purple": (138, 104, 186), "red": (200, 64, 52),
       "rose": (222, 150, 170), "white": (214, 178, 92), "gold": (214, 178, 92), "black": (120, 120, 120)}

# Where things go (lock-screen safe areas)
PAINT_TOP, PAINT_BOTTOM, SIDE = 800, 2030, 110
TEXT_TOP, TEXT_BOTTOM = 2110, 2440


def shadow(canvas, box, radius=40, offset=24, alpha=150):
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle((x0 + 6, y0 + offset, x1 - 6, y1 + offset), fill=(0, 0, 0, alpha))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(radius)))


def font(kind, size, weight=None, italic=False):
    if kind == "fell":
        return F("IMFeENit28P.ttf" if italic else "IMFeENrm28P.ttf", size)
    if kind == "source":
        f = F("SourceSerif4-Italic.ttf" if italic else "SourceSerif4.ttf", size)
        f.set_variation_by_axes([weight or 600, min(60, max(8, size / 3))])
        return f
    if kind == "cinzel":
        f = F("Cinzel.ttf", size); f.set_variation_by_axes([weight or 400]); return f
    if kind == "inter":
        name = {400: "Regular", 500: "Medium", 600: "SemiBold"}.get(weight or 500, "Medium")
        fn = f"InterDisplay-{name}{'Italic' if italic else ''}.otf".replace("RegularItalic", "Italic")
        return F(fn, size)
    return F("AlegreyaSans-Regular.ttf", size)


def centered(d, y, text, f, fill, width=None, leading=1.15, dry=False):
    lines = wrap_px(d, text, f, width) if width else [text]
    for line in lines:
        if not dry: d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=fill)
        y += int(f.size * leading)
    return y


def wrap_px(d, text, f, width_chars):
    """Wrap by measured width (W - 2*SIDE - 40 px), not by character count."""
    maxw = W - 2 * SIDE - 40
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= maxw or not cur: cur = trial
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


ABBR = ("St.", "Sts.", "Ss.", "Bl.", "Mt.", "Lk.", "Jn.", "Mk.", "Fr.", "c.", "ca.", "U.S.", "A.D.", "B.C.", "e.g.", "i.e.")
def short_text(b, limit=220):
    """The whole text if it is short; otherwise as many whole sentences as fit."""
    if len(b) <= limit: return b
    out, cur = [], ""
    for tok in re.split(r"(\s+)", b):
        cur += tok
        if re.search(r"[.!?]['’\"”)]*$", tok) and not tok.endswith(ABBR) and not re.match(r"^[A-Z]\.$", tok):
            out.append(cur.strip()); cur = ""
    if cur.strip(): out.append(cur.strip())
    r = out[0]
    for x in out[1:]:
        if len(r) + 1 + len(x) <= limit: r += " " + x
        else: break
    return r


def draw_final(d, day, y, color, dry):
    """Chosen design: iPhone-style type; name, title, kind of day, and a short text about the day."""
    y0 = y
    head, sub = split_title(day["t"])
    y = centered(d, y, head, font("inter", 70, 600), INK, 1, 1.12, dry)
    if sub:
        y = centered(d, y + 2, sub, font("inter", 46, 400, italic=True), (232, 226, 214), 1, 1.2, dry)
    rank = day.get("r", "")
    ref = day.get("y", "")
    if re.match(r"^(Matthew|Mark|Luke|John) \d", ref):
        rank = f"{rank}, {ref}" if rank else ref
    f = font("inter", 38, 400)
    if dry: y += int(f.size * 1.4) + 14
    else: y = rank_line(d, y + 14, rank, color, f)
    b = day.get("b", "")
    if not b.startswith("“"): b = short_text(b)   # Gospel quotes are shown whole
    if b:
        y = centered(d, y + 18, b, font("inter", 40, 400), (214, 207, 194), 1, 1.38, dry)
    return y - y0


def rank_line(d, y, rank, color, f):
    dot = int(f.size * 0.5)
    rw = d.textlength(rank, font=f)
    rx = (W - rw - dot - 16) / 2
    d.ellipse((rx, y + f.size * 0.42, rx + dot, y + f.size * 0.42 + dot), fill=DOT.get(color, DOT["white"]))
    d.text((rx + dot + 16, y), rank, font=f, fill=QUIET)
    return y + int(f.size * 1.4)


def split_title(t):
    """'Saint Frances Xavier Cabrini, Virgin' -> ('Saint Frances Xavier Cabrini', 'Virgin')"""
    if ", " in t and not t.startswith("The "):
        a, b = t.split(", ", 1)
        return a, b
    return t, ""


def first_sentence(text, limit=150):
    if not text: return ""
    s = text.split(". ")[0].rstrip(".") + "."
    return s if len(s) <= limit else ""


def draw_text(d, day, style, y, color, dry=False):
    t, r = day["t"], day.get("r", "")
    if style == "final":
        return draw_final(d, day, y, color, dry)
    if style == "none":
        return
    if style == "fell":
        y = centered(d, y, t, font("fell", 78), INK, 26)
        rank_line(d, y + 6, r, color, font("alegreya", 44))
    elif style == "inter":
        y = centered(d, y, t, font("inter", 66, 600), INK, 28, 1.2)
        rank_line(d, y + 8, r, color, font("inter", 40, 400))
    elif style == "cinzel":
        y = centered(d, y, t.upper() if False else t, font("cinzel", 64, 400), INK, 28, 1.25)
        rank_line(d, y + 8, r, color, font("source", 42, 400, italic=True))
    elif style == "mac":            # like the Mac wallpaper: name, then the title in italics
        head, sub = split_title(t)
        y = centered(d, y, head, font("source", 80, 600), INK, 24, 1.1)
        if sub:
            y = centered(d, y + 4, sub, font("source", 52, 400, italic=True), (230, 224, 212), 36)
        rank_line(d, y + 18, r, color, font("inter", 38, 400))
    elif style == "credit":          # name plus who painted the picture
        head, sub = split_title(t)
        y = centered(d, y, head, font("source", 76, 600), INK, 26, 1.1)
        if sub:
            y = centered(d, y + 4, sub, font("source", 50, 400, italic=True), (230, 224, 212), 36)
        cred = first_sentence(day.get("a", ""), 110)
        if cred:
            centered(d, y + 26, cred, font("source", 38, 400, italic=True), QUIET, 46, 1.3)
    elif style == "bio":             # name plus one line about the saint
        head, sub = split_title(t)
        y = centered(d, y, head, font("source", 76, 600), INK, 26, 1.1)
        if sub:
            y = centered(d, y + 4, sub, font("source", 50, 400, italic=True), (230, 224, 212), 36)
        line = first_sentence(day.get("b", ""), 140)
        if line:
            centered(d, y + 26, line, font("source", 40, 400), QUIET, 44, 1.32)


def render(style, day, painting_path, out, mock=False, text_style="fell"):
    pic = ImageOps.exif_transpose(Image.open(painting_path)).convert("RGB")
    color = day.get("c", "white")

    if style == "blur":
        bg = ImageOps.fit(pic, (W // 4, H // 4)).filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.LANCZOS)
        bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.58)
    elif style == "season":
        bg = Image.new("RGB", (W, H), SEASON.get(color, SEASON["white"]))
    else:
        bg = Image.new("RGB", (W, H), GALLERY)
    canvas = bg.convert("RGBA")

    # A soft darkening toward the edges, like light falling on a wall
    if style != "blur":
        v = Image.new("L", (W, H), 0)
        ImageDraw.Draw(v).ellipse((-W * 0.35, -H * 0.05, W * 1.35, H * 1.05), fill=255)
        v = v.filter(ImageFilter.GaussianBlur(260))
        dark = Image.new("RGBA", (W, H), (0, 0, 0, 120))
        canvas.alpha_composite(Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), dark, v))

    # The text block decides how much room the painting gets
    measure = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    text_h = draw_text(measure, day, text_style, 0, color, dry=True) or 0
    paint_bottom = min(PAINT_BOTTOM, TEXT_BOTTOM - text_h - 78)

    # The painting, whole
    box_w, box_h = W - 2 * SIDE, paint_bottom - PAINT_TOP
    scale = min(box_w / pic.width, box_h / pic.height)
    pw, ph = int(pic.width * scale), int(pic.height * scale)
    slack = (TEXT_BOTTOM - PAINT_TOP) - (ph + 78 + text_h)
    px, py = (W - pw) // 2, PAINT_TOP + max(0, int(slack * 0.45))
    shadow(canvas, (px, py, px + pw, py + ph))
    canvas.paste(pic.resize((pw, ph), Image.LANCZOS), (px, py))

    # The name and the kind of day
    d = ImageDraw.Draw(canvas)
    draw_text(d, day, text_style, py + ph + 78, color)

    if mock:   # a stand-in for the iPhone's own clock, only for previews
        clock = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf", 300)
        small = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf", 58)
        date = day.get("mockdate", "Friday, November 13")
        d.text(((W - d.textlength(date, font=small)) / 2, 250), date, font=small, fill=(255, 255, 255, 230))
        d.text(((W - d.textlength("9:41", font=clock)) / 2, 300), "9:41", font=clock, fill=(255, 255, 255, 235))
        d.rounded_rectangle((W / 2 - 200, H - 40, W / 2 + 200, H - 28), 6, fill=(255, 255, 255, 200))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for cx in (190, W - 190):
            od.ellipse((cx - 75, H - 290, cx + 75, H - 140), fill=(255, 255, 255, 45))
        canvas.alpha_composite(ov)

    canvas.convert("RGB").save(out, quality=84, optimize=True, progressive=True)


if __name__ == "__main__":
    style, date, out = sys.argv[1:4]
    days = json.load(open(os.path.join(SITE, "content/days.json")))
    day = dict(days[date])
    import datetime
    day["mockdate"] = datetime.date.fromisoformat(date).strftime("%A, %B %-d")
    ts = next((a[7:] for a in sys.argv if a.startswith("--text=")), "fell")
    render(style, day, os.path.join(SITE, "content/img", day["img"]), out, mock="--mock" in sys.argv, text_style=ts)
