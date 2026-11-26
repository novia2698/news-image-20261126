#!/usr/bin/env python3
"""Draw entry.png for news-image-20261126: one image summing up the world
news of Thursday 26 November 2026.

Build-time provenance only: main.py (the entrypoint the grader runs) is
stdlib-only and just copies the entry.png committed beside it. This script
runs on the builder's machine with Pillow and renders the picture from the
headlines reported on the morning of 26 November 2026.

Stories (all reported 25-26 Nov 2026, cross-checked across several outlets):
  1. Houthis attack Saudi Arabia's Ras Tanura oil refinery; two tankers hit
     naval mines in the Strait of Hormuz.
  2. Israel kills senior Hamas official Mohammad Abuelouf in Gaza; the
     ceasefire is under strain.
  3. Ukraine strikes Russian oil refineries; Russia's own figures show
     nearly 500,000 dead in the war.
  4. The US prepares new tariffs on global trading partners; markets slide
     as Nvidia leads an AI sell-off.
  5. Pakistan's first astronaut, Muhammad Zeeshan Ali, joins China's
     Shenzhou-24 mission to the Tiangong station.
  6. Also today: Bangladesh raises garment wages 36%; North Korea orders
     Switzerland to shut its Pyongyang office; asteroid-defence test
     images reveal a new crater; 15-year-old Vaibhav Sooryavanshi hits a
     record 204 off 53 balls.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
NAVY_LIGHT = (38, 58, 94)
GOLD = (201, 162, 39)
RED = (180, 35, 24)
INK = (28, 28, 28)
MUTED = (90, 86, 76)
PANEL = (255, 255, 255)
BORDER = (216, 210, 196)
TEAL = (14, 116, 110)
ORANGE = (214, 106, 24)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` pixels."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, width, leading=None):
    """Draw wrapped text; return y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, box, fill=PANEL, outline=BORDER, width=2):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def tag(draw, x, y, text, bg, fg=(255, 255, 255)):
    """Small coloured kicker tag; returns its right edge."""
    fnt = SANS_B(17)
    w = int(draw.textlength(text, font=fnt)) + 18
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=5, fill=bg)
    draw.text((x + 9, y + 3), text, font=fnt, fill=fg)
    return x + w

# --- flat pictogram icons, drawn with plain shapes -------------------------

def icon_pumpjack(draw, x, y, s, color):
    """Oil pumpjack silhouette inside a square of side s."""
    u = s / 100.0
    draw.line([(x + 12 * u, y + 88 * u), (x + 55 * u, y + 20 * u),
               (x + 88 * u, y + 30 * u)], fill=color, width=int(5 * u))
    draw.line([(x + 55 * u, y + 20 * u), (x + 55 * u, y + 88 * u)],
              fill=color, width=int(5 * u))
    draw.line([(x + 30 * u, y + 88 * u), (x + 82 * u, y + 88 * u)],
              fill=color, width=int(5 * u))
    draw.rectangle([x + 82 * u, y + 24 * u, x + 96 * u, y + 44 * u], fill=color)
    draw.line([(x + 88 * u, y + 44 * u), (x + 88 * u, y + 62 * u)],
              fill=color, width=int(4 * u))
    draw.ellipse([x + 50 * u, y + 15 * u, x + 60 * u, y + 25 * u], fill=color)


def icon_flame(draw, x, y, s, color):
    u = s / 100.0
    draw.polygon([(x + 50 * u, y + 4 * u), (x + 78 * u, y + 48 * u),
                  (x + 66 * u, y + 48 * u), (x + 84 * u, y + 74 * u),
                  (x + 50 * u, y + 98 * u), (x + 16 * u, y + 74 * u),
                  (x + 34 * u, y + 48 * u), (x + 22 * u, y + 48 * u)],
                 fill=color)


def icon_flag(draw, x, y, s, color):
    u = s / 100.0
    draw.line([(x + 20 * u, y + 6 * u), (x + 20 * u, y + 96 * u)],
              fill=color, width=int(6 * u))
    draw.polygon([(x + 22 * u, y + 8 * u), (x + 92 * u, y + 22 * u),
                  (x + 22 * u, y + 46 * u)], fill=color)
    draw.line([(x + 30 * u, y + 56 * u), (x + 62 * u, y + 86 * u)],
              fill=(180, 35, 24), width=int(6 * u))


def icon_shield(draw, x, y, s, color):
    u = s / 100.0
    draw.polygon([(x + 50 * u, y + 4 * u), (x + 92 * u, y + 20 * u),
                  (x + 92 * u, y + 56 * u), (x + 50 * u, y + 96 * u),
                  (x + 8 * u, y + 56 * u), (x + 8 * u, y + 20 * u)],
                 outline=color, width=int(6 * u))
    draw.text((x + 34 * u, y + 30 * u), "*", font=SANS_B(int(44 * u)), fill=color)


def icon_chart(draw, x, y, s, color):
    u = s / 100.0
    draw.line([(x + 12 * u, y + 90 * u), (x + 92 * u, y + 90 * u)],
              fill=color, width=int(5 * u))
    for i, h in enumerate((34, 52, 70)):
        bx = x + (20 + i * 24) * u
        draw.rectangle([bx, y + (88 - h) * u, bx + 14 * u, y + 88 * u], fill=color)
    draw.line([(x + 14 * u, y + 30 * u), (x + 52 * u, y + 52 * u),
               (x + 90 * u, y + 16 * u)], fill=(180, 35, 24), width=int(6 * u))
    draw.polygon([(x + 90 * u, y + 8 * u), (x + 96 * u, y + 24 * u),
                  (x + 78 * u, y + 22 * u)], fill=(180, 35, 24))


def icon_rocket(draw, x, y, s, color):
    u = s / 100.0
    draw.polygon([(x + 50 * u, y + 4 * u), (x + 68 * u, y + 44 * u),
                  (x + 32 * u, y + 44 * u)], fill=color)
    draw.rectangle([x + 34 * u, y + 40 * u, x + 66 * u, y + 72 * u], fill=color)
    draw.polygon([(x + 34 * u, y + 60 * u), (x + 18 * u, y + 84 * u),
                  (x + 34 * u, y + 78 * u)], fill=color)
    draw.polygon([(x + 66 * u, y + 60 * u), (x + 82 * u, y + 84 * u),
                  (x + 66 * u, y + 78 * u)], fill=color)
    draw.ellipse([x + 42 * u, y + 22 * u, x + 58 * u, y + 38 * u], fill=PAPER)
    draw.polygon([(x + 50 * u, y + 74 * u), (x + 62 * u, y + 96 * u),
                  (x + 38 * u, y + 96 * u)], fill=(214, 106, 24))


# --- page -------------------------------------------------------------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    d.text((32, 14), "THE WORLD IN ONE DAY", font=SERIF_B(52), fill=(255, 255, 255))
    d.text((32, 76), "THURSDAY, 26 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
           font=SANS_B(21), fill=GOLD)

    # Lead story: Gulf energy under attack
    panel(d, [24, 138, 1000, 396])
    tag(d, 44, 156, "LEAD  •  MIDDLE EAST", RED)
    icon_pumpjack(d, 830, 170, 130, NAVY)
    icon_flame(d, 908, 158, 56, ORANGE)
    y = 196
    y = draw_text_block(d, 44, y, "Gulf oil under fire", SERIF_B(40), INK, 770)
    y = draw_text_block(d, 44, y + 6,
                        "Houthis hit Saudi Arabia's Ras Tanura refinery, "
                        "setting it ablaze — and two oil tankers strike naval "
                        "mines in the Strait of Hormuz.",
                        SANS(23), INK, 770)

    # Four stories, 2 x 2 grid
    grid = [
        (24, 412, 488, 676, "GAZA", TEAL, icon_flag,
         "Ceasefire under strain",
         "Israel kills senior Hamas official Mohammad Abuelouf in Gaza, "
         "along with his family, as the truce frays."),
        (512, 412, 1000, 676, "UKRAINE", NAVY_LIGHT, icon_shield,
         "Kyiv hits Russia's refineries",
         "Ukraine strikes Russian oil plants; Moscow's own figures put its "
         "war dead near 500,000."),
        (24, 692, 488, 956, "TRADE", ORANGE, icon_chart,
         "New US tariffs loom",
         "Washington prepares tariffs on global partners; markets slide as "
         "Nvidia leads an AI sell-off."),
        (512, 692, 1000, 956, "SPACE", TEAL, icon_rocket,
         "Pakistan reaches for orbit",
         "Muhammad Zeeshan Ali becomes the first Pakistani astronaut bound "
         "for China's Tiangong station."),
    ]
    for x0, y0, x1, y1, kicker, kc, icon, head, body in grid:
        panel(d, [x0, y0, x1, y1])
        tag(d, x0 + 18, y0 + 14, kicker, kc)
        icon(d, x1 - 92, y0 + 16, 66, kc)
        yy = draw_text_block(d, x0 + 18, y0 + 52, head, SERIF_B(27), INK,
                             x1 - x0 - 36 - 80)
        draw_text_block(d, x0 + 18, yy + 4, body, SANS(19), MUTED,
                        x1 - x0 - 36)

    # Footer strip: the rest of the day in one line each
    d.rectangle([0, 972, W, H], fill=NAVY)
    d.text((32, 980), "ALSO TODAY:  Bangladesh wages up 36%  •  North Korea expels "
           "Swiss office  •  Asteroid test reveals new crater",
           font=SANS_B(15), fill=GOLD)
    d.text((32, 1001), "SPORT:  Sooryavanshi, 15, smashes a record 204 off 53 balls  •  "
           "Gukesh draws game 2 of the World Chess Championship.",
           font=SANS(15), fill=(255, 255, 255))
    return img


if __name__ == "__main__":
    out = build()
    out.save("entry.png", optimize=True)
    import os
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes",
          out.size)
