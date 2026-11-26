"""Render one newspaper front page summing up world news of Thursday
26 November 2026 -- the FULL day, morning through evening. Pure Pillow,
no network, fully deterministic: same input, same bytes, every run.

Run:  python3 render_news.py [output.png]
Default output is entry.png next to this file.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (22, 22, 22)
RED = (178, 34, 28)
NAVY = (28, 52, 92)
TEAL = (14, 112, 104)
GOLD = (198, 158, 38)
GREY = (96, 92, 82)
BODY = (43, 41, 35)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(SANS, size)
        except Exception:
            return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=BODY, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.24)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon_burst(draw, x, y, s):
    """Explosion: layered starbursts, red-orange-yellow."""
    cx, cy = x + s // 2, y + s // 2
    draw.polygon(star(cx, cy, s // 2, s // 5, 12), fill=(196, 50, 28))
    draw.polygon(star(cx, cy, s // 3, s // 7, 12, rot=-76), fill=(232, 126, 32))
    draw.polygon(star(cx, cy, s // 5, s // 11, 8), fill=(246, 198, 66))


def icon_chart_down(draw, x, y, s):
    """Falling market chart: axes, descending line, bars, arrowhead."""
    draw.line([(x + 8, y + 8), (x + 8, y + s - 8)], fill=INK, width=3)
    draw.line([(x + 8, y + s - 8), (x + s - 8, y + s - 8)], fill=INK, width=3)
    pts = [(x + 14, y + 14), (x + 32, y + 24), (x + 48, y + 20),
           (x + 64, y + 42), (x + 78, y + 56), (x + s - 14, y + s - 22)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(x + s - 14, y + s - 22), (x + s - 28, y + s - 26),
                  (x + s - 24, y + s - 36)], fill=RED)
    for bx, bh in [(18, 16), (36, 24), (54, 18), (72, 10)]:
        draw.rectangle([x + bx, y + s - 14 - bh, x + bx + 10, y + s - 14],
                       fill=(178, 178, 168))


def icon_rocket(draw, x, y, s):
    """Missile climbing: body, fins, nose, flame, motion lines."""
    cx = x + s // 2
    draw.polygon([(cx - 12, y + s - 26), (cx - 12, y + 26),
                  (cx, y + 8), (cx + 12, y + 26),
                  (cx + 12, y + s - 26)], fill=(60, 60, 60))
    draw.polygon([(cx - 22, y + s - 26), (cx - 12, y + s - 44),
                  (cx - 12, y + s - 26)], fill=RED)
    draw.polygon([(cx + 22, y + s - 26), (cx + 12, y + s - 44),
                  (cx + 12, y + s - 26)], fill=RED)
    draw.polygon(star(cx, y + s - 8, 14, 6, 5), fill=(232, 126, 32))
    for dy in (18, 34):
        draw.line([(x + 8, y + dy), (x + 26, y + dy)], fill=GREY, width=3)
        draw.line([(x + s - 26, y + dy + 12), (x + s - 8, y + dy + 12)],
                  fill=GREY, width=3)


def icon_scales(draw, x, y, s, color=NAVY):
    """Scales of justice."""
    cx = x + s // 2
    draw.line([(cx, y + 8), (cx, y + s - 24)], fill=color, width=4)
    draw.line([(x + 8, y + 22), (x + s - 8, y + 22)], fill=color, width=4)
    draw.line([(cx, y + 22), (x + 16, y + 52)], fill=color, width=3)
    draw.line([(cx, y + 22), (x + s - 16, y + 52)], fill=color, width=3)
    draw.pieslice([x + 4, y + 48, x + 28, y + 66], 0, 180, fill=color)
    draw.pieslice([x + s - 28, y + 48, x + s - 4, y + 66], 0, 180, fill=color)
    draw.line([(x + 14, y + s - 12), (x + s - 14, y + s - 12)],
              fill=color, width=5)
    draw.ellipse([cx - 6, y + 4, cx + 6, y + 16], fill=color)


def icon_shield(draw, x, y, s, color=NAVY):
    """Shield with a star: defence / NATO air cover."""
    cx = x + s // 2
    draw.polygon([(cx, y + 4), (x + s - 6, y + 18), (x + s - 6, y + s // 2),
                  (cx, y + s - 6), (x + 6, y + s // 2), (x + 6, y + 18)],
                 outline=color, width=5)
    draw.polygon(star(cx, y + s // 2 - 4, 20, 8), fill=color)
    draw.arc([x - 4, y - 6, x + s + 4, y + s + 6], 300, 60, fill=GREY, width=3)


def icon_flame(draw, x, y, s):
    """Fire: outer flame, inner flame, sparks."""
    cx = x + s // 2
    draw.pieslice([cx - 26, y + 14, cx + 26, y + s - 6], 180, 360, fill=(232, 90, 20))
    draw.polygon([(cx - 26, y + s // 2), (cx, y + 6), (cx + 26, y + s // 2),
                  (cx + 14, y + s - 8), (cx - 14, y + s - 8)], fill=(232, 90, 20))
    draw.pieslice([cx - 14, y + 34, cx + 14, y + s - 10], 180, 360, fill=(246, 198, 66))
    draw.polygon([(cx - 14, y + s // 2 + 6), (cx, y + 30),
                  (cx + 14, y + s // 2 + 6), (cx + 7, y + s - 12),
                  (cx - 7, y + s - 12)], fill=(246, 198, 66))
    for dx, dy in [(-30, 10), (28, 4), (34, 30)]:
        draw.ellipse([cx + dx, y + dy, cx + dx + 5, y + dy + 5], fill=RED)


def icon_balloon(draw, x, y, s):
    """Parade balloon: big round balloon, ropes, basket, wind lines."""
    cx, cy = x + s // 2, y + s // 2 - 8
    draw.ellipse([cx - 20, cy - 18, cx + 20, cy + 18], fill=(178, 34, 28))
    draw.ellipse([cx - 20, cy - 18, cx - 6, cy + 18], fill=(214, 74, 62))
    draw.arc([cx - 20, cy - 18, cx + 20, cy + 18], 90, 270, fill=INK, width=2)
    draw.line([(cx - 12, cy + 16), (cx - 6, cy + 26)], fill=INK, width=3)
    draw.line([(cx + 12, cy + 16), (cx + 6, cy + 26)], fill=INK, width=3)
    draw.rectangle([cx - 7, cy + 26, cx + 7, cy + 34], outline=INK, width=3)
    for dy in (2, 14, 26):
        draw.line([(x + s - 12, y + dy), (x + s - 2, y + dy)],
                  fill=GREY, width=3)


def kicker(draw, text, x, y, color, size=16):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=color)
    return y + size + 8


def story_panel(draw, x, y, w, h, kick, kick_color, headline, deck,
                icon=None, head_size=26, deck_size=17):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 6], fill=kick_color)
    pad = 14
    tx, ty = x + pad, y + 14
    text_w = w - 2 * pad - (104 if icon else 0)
    ty = kicker(draw, kick, tx, ty, kick_color)
    ty = draw_wrapped(draw, headline, font(SERIF_B, head_size),
                      tx, ty, text_w, leading=head_size + 5)
    deck_fnt = font(SANS, deck_size)
    deck_leading = deck_size + 6
    room = (y + h - pad) - (ty + 4)
    max_lines = max(1, room // deck_leading)
    lines = wrap(draw, deck, deck_fnt, text_w)[:max_lines]
    yy = ty + 4
    for line in lines:
        draw.text((tx, yy), line, font=deck_fnt, fill=BODY)
        yy += deck_leading
    if icon:
        icon(draw, x + w - 100, y + 14, 86)


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin

    # ---- masthead ----
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 64)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 18), title, font=tf, fill=INK)
    d.line([(m, 102), (W - m, 102)], fill=INK, width=3)
    d.line([(m, 108), (W - m, 108)], fill=INK, width=1)
    date_f = font(SANS_B, 25)
    d.text((m, 120), "THURSDAY, 26 NOVEMBER 2026", font=date_f, fill=RED)
    tag_f = font(SANS, 19)
    tag = "THE FULL DAY IN ONE PAGE"
    d.text((W - m - d.textlength(tag, font=tag_f), 122), tag,
           font=tag_f, fill=GREY)
    d.line([(m, 154), (W - m, 154)], fill=RED, width=3)

    # ---- lead story: Trump's new tariffs ----
    lx, ly, lw, lh = m, 166, W - 2 * m, 234
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
    d.rectangle([lx + 2, ly + 2, lx + lw - 2, ly + 8], fill=RED)
    ty = kicker(d, "WASHINGTON  •  TRADE  •  LEAD STORY", lx + 18, ly + 16,
                RED, 17)
    ty = draw_wrapped(d, "TRUMP HITS 14 PARTNERS WITH NEW TARIFFS",
                      font(SERIF_B, 40), lx + 18, ty, 640, leading=46)
    draw_wrapped(d,
                 "Washington proposes duties of 15% on the EU, Japan and "
                 "South Korea, 20% on China, 25% on India and 35% on "
                 "Vietnam, blaming factory overcapacity. Partners protest.",
                 font(SANS, 18), lx + 18, ty + 8, 640,
                 fill=BODY, leading=24)
    icon_chart_down(d, lx + lw - 152, ly + 96, 120)

    # ---- row 2: Kyiv strikes back + North Korea ----
    y2, h2 = 412, 206
    story_panel(d, m, y2, 472, h2,
                "KYIV  •  WAR IN UKRAINE", RED,
                "RUSSIA HITS KYIV, UKRAINE HITS BACK",
                "Russian missiles hit a Kyiv shopping centre, wounding "
                "seven. Kyiv's drones hit a Russian air base and "
                "refineries; Russian refining falls to a 20-year low.",
                icon=icon_burst, head_size=24, deck_size=17)
    story_panel(d, W - m - 472, y2, 472, h2,
                "PYONGYANG  •  NUCLEAR", NAVY,
                "KIM: MORE NUKES, LESS AID FOR RUSSIA",
                "Kim Jong Un orders tactical nuclear weapons deployed "
                "more widely. North Korea is reported to have suspended "
                "military support to Russia.",
                icon=icon_rocket, head_size=24, deck_size=17)

    # ---- row 3: Gaza / Netanyahu + Poland / NATO ----
    y3, h3 = 630, 206
    story_panel(d, m, y3, 472, h3,
                "GAZA  •  ISRAEL", TEAL,
                "NINE KILLED IN GAZA STRIKES",
                "Israeli strikes kill nine in Gaza, including a "
                "Hamas-appointed deputy minister. Judges urge dropping "
                "the Case 4000 charge against Netanyahu.",
                icon=icon_scales, head_size=24, deck_size=17)
    story_panel(d, W - m - 472, y3, 472, h3,
                "WARSAW  •  NATO", NAVY,
                "POLAND PLANS NO-FLY ZONE",
                "Warsaw prepares flight curbs on its eastern border and "
                "asks NATO to weigh downing Russian missiles over "
                "Ukraine. NATO sends early-warning jets.",
                icon=icon_shield, head_size=24, deck_size=17)

    # ---- row 4: Cairo fire + Macy's parade ----
    y4, h4 = 848, 72
    d.rectangle([m, y4, W - m, y4 + h4], outline=INK, width=2)
    d.rectangle([m + 2, y4 + 2, m + 6, y4 + h4 - 2], fill=GOLD)
    icon_flame(d, m + 8, y4 + 8, 56)
    d.text((m + 78, y4 + 8), "CAIRO TANKER FIRE KILLS 31",
           font=font(SERIF_B, 22), fill=INK)
    d.text((m + 78, y4 + 38),
           "Fuel truck overturns; 21 hurt.",
           font=font(SANS, 15), fill=BODY)
    icon_balloon(d, m + 494, y4 + 8, 56)
    d.text((m + 566, y4 + 8), "MACY'S PARADE POSTPONED",
           font=font(SERIF_B, 22), fill=INK)
    d.text((m + 566, y4 + 38),
           "First weather delay in a century; winds to 60 mph.",
           font=font(SANS, 15), fill=BODY)

    # ---- footer ticker: the rest of the day ----
    fy = 936
    draw_wrapped(d,
                 "ALSO TODAY: SpaceX cleared to launch a million "
                 "satellites  •  US economy grew 4.3%, fastest in three "
                 "years  •  Russia approves a record $606bn military "
                 "budget  •  Houthi missiles aimed at Riyadh intercepted  "
                 "•  Solomon Islands signs a security treaty with "
                 "Australia  •  First Pakistani astronaut boards China's "
                 "Tiangong station  •  DR Congo Ebola passes 12,000 cases "
                 "•  World tops 2°C for a sixth straight day",
                 font(SANS, 15), m, fy, W - 2 * m, fill=GREY, leading=20)

    img.save(path, "PNG", optimize=True)
    return path


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
