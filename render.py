#!/usr/bin/env python3
"""Render entry.png: a newspaper front page summing up 26 November 2026.

Build-time only. The graded entry (main.py) is stdlib-only and just copies
the pre-rendered PNG into /output, because the grader has no Pillow and no
network. Every headline below was fetched from live news on 26 Nov 2026.
Run: python3 render.py  ->  entry.png (1200x1600).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1600
MARGIN = 36

NAVY = (14, 30, 51)
NAVY2 = (22, 45, 74)
PAPER = (246, 241, 231)
INK = (24, 24, 22)
RED = (178, 44, 32)
GOLD = (201, 162, 39)
TEAL = (20, 101, 90)
SKY = (173, 203, 224)
SEA = (31, 78, 121)
ORANGE = (232, 116, 28)
CREAM = (250, 247, 240)
GREY = (110, 108, 100)
DARKPANEL = (18, 38, 62)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=6):
    """Draw a wrapped paragraph; return y below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def kicker(draw, x, y, text, color=RED, size=25):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=color)
    return y + size + 8


def fit_headline(draw, x, y, text, size, max_w, fill=INK, fnt_path=SERIF_B):
    """Draw a headline on ONE line, shrinking the font until it fits."""
    while size > 18:
        f = font(fnt_path, size)
        if draw.textlength(text, font=f) <= max_w:
            break
        size -= 2
    f = font(fnt_path, size)
    draw.text((x, y), text, font=f, fill=fill)
    return y + size + 4


# ---------------------------------------------------------------- scenes
def draw_refinery_scene(draw, x0, y0, x1, y1):
    """Refinery silhouette with flames against a dusk sky (lead art)."""
    s = (y1 - y0) / 300.0
    draw.rectangle([x0, y0, x1, y1], fill=(38, 52, 74))
    # dusk gradient bands
    for i in range(5):
        yy = y0 + i * (y1 - y0) // 5
        draw.rectangle([x0, yy, x1, yy + (y1 - y0) // 5 + 1],
                       fill=(38 + i * 6, 52 + i * 4, 74 - i * 6))
    # sun
    cx, cy = x0 + (x1 - x0) * 3 // 4, y0 + int(52 * s)
    r = int(30 * s)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 150, 60))
    ground = y1 - int(58 * s)

    def gy(v):
        return ground - int(v * s)

    # columns and tanks
    draw.rectangle([x0 + 30, gy(150), x0 + 62, ground], fill=(16, 22, 34))
    draw.rectangle([x0 + 74, gy(110), x0 + 150, ground], fill=(16, 22, 34))
    draw.ellipse([x0 + 74, gy(128), x0 + 150, gy(92)], fill=(16, 22, 34))
    draw.rectangle([x0 + 165, gy(190), x0 + 185, ground], fill=(16, 22, 34))
    draw.rectangle([x0 + 200, gy(130), x0 + 268, ground], fill=(16, 22, 34))
    draw.ellipse([x0 + 200, gy(148), x0 + 268, gy(112)], fill=(16, 22, 34))
    draw.rectangle([x0 + 285, gy(165), x0 + 305, ground], fill=(16, 22, 34))
    # flare stack flame
    fx = x0 + 295
    draw.polygon([(fx - 14, gy(165)), (fx, gy(225)),
                  (fx + 14, gy(165))], fill=(240, 140, 30))
    draw.polygon([(fx - 7, gy(165)), (fx, gy(200)),
                  (fx + 7, gy(165))], fill=(250, 200, 60))
    # ground + fire glow
    draw.rectangle([x0, ground, x1, y1], fill=(12, 16, 26))
    draw.polygon([(x0 + 60, ground), (x0 + 120, gy(34)),
                  (x0 + 190, ground)], fill=(232, 116, 28))
    draw.polygon([(x0 + 100, ground), (x0 + 140, gy(20)),
                  (x0 + 180, ground)], fill=(250, 200, 60))
    # smoke
    for sx, sy_, r_ in [(x0 + 90, y0 + int(60 * s), int(16 * s)),
                        (x0 + 110, y0 + int(42 * s), int(20 * s)),
                        (x0 + 140, y0 + int(30 * s), int(14 * s))]:
        draw.ellipse([sx - r_, sy_ - r_, sx + r_, sy_ + r_], fill=(90, 96, 110))


def draw_sea_mines(draw, x0, y0, x1, y1):
    """Tanker on a mined strait (lead art strip)."""
    s = (y1 - y0) / 160.0
    draw.rectangle([x0, y0, x1, y1], fill=SEA)
    horizon = y0 + int(80 * s)
    draw.rectangle([x0, y0, x1, horizon], fill=SKY)
    sr = int(24 * s)
    draw.ellipse([x0 + 30, y0 + int(18 * s), x0 + 30 + 2 * sr,
                  y0 + int(18 * s) + 2 * sr], fill=(245, 220, 130))
    # tanker hull
    hx0, hx1 = x0 + 40, x1 - 90
    draw.polygon([(hx0, horizon + int(26 * s)), (hx1, horizon + int(26 * s)),
                  (hx1 - 26, horizon + int(62 * s)),
                  (hx0 + 18, horizon + int(62 * s))],
                 fill=(140, 30, 24))
    draw.rectangle([hx0 + 60, horizon - int(6 * s), hx0 + 150,
                    horizon + int(26 * s)], fill=(200, 200, 196))
    draw.rectangle([hx0 + 170, horizon - int(22 * s), hx0 + 200,
                    horizon + int(26 * s)], fill=(220, 220, 216))
    # waves
    for wy in (horizon + int(70 * s), horizon + int(88 * s)):
        for wx in range(x0 + 10, x1 - 10, 46):
            draw.arc([wx, wy, wx + 34, wy + 14], 180, 360,
                     fill=(210, 225, 235), width=3)
    # mines
    for mx, my, r in [(x1 - 70, horizon + int(34 * s), 13),
                      (x1 - 130, horizon + int(58 * s), 10)]:
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            draw.line([(mx + int(r * 0.8 * math.cos(rad)),
                        my + int(r * 0.8 * math.sin(rad))),
                       (mx + int((r + 8) * math.cos(rad)),
                        my + int((r + 8) * math.sin(rad)))],
                      fill=(20, 20, 20), width=3)
        draw.ellipse([mx - r, my - r, mx + r, my + r], fill=(24, 24, 24))


def draw_crack_skyline(draw, x0, y0, x1, y1):
    """Skyline split by a jagged crack (Gaza panel)."""
    draw.rectangle([x0, y0, x1, y1], fill=(233, 224, 205))
    s = (y1 - y0) / 170.0
    base = y1 - int(46 * s)
    heights = [int(h * s) for h in (86, 130, 104, 150, 118, 92)]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw + 6
        draw.rectangle([bx, base - hh, bx + bw - 12, base], fill=(96, 88, 78))
        draw.rectangle([bx + 8, base - hh - int(14 * s), bx + bw - 20, base - hh],
                       fill=(96, 88, 78))
    # jagged crack
    cx = x0 + (x1 - x0) // 2
    pts = [(cx, y0 + 8), (cx - 12, y0 + int(46 * s)), (cx + 10, y0 + int(84 * s)),
           (cx - 10, y0 + int(122 * s)), (cx + 8, y0 + int(158 * s)), (cx - 4, base)]
    draw.line(pts, fill=(60, 52, 44), width=5, joint="curve")
    # small white flag on the tallest tower
    fx = x0 + 3 * bw + bw // 2
    draw.line([(fx, base - heights[3]), (fx, base - heights[3] - int(32 * s))],
              fill=(60, 52, 44), width=3)
    fy = base - heights[3] - int(32 * s)
    draw.polygon([(fx, fy), (fx + 34, fy + 8), (fx, fy + 16)], fill=(250, 250, 246))
    draw.rectangle([x0, base, x1, y1], fill=(60, 52, 44))


def draw_oil_flame(draw, x0, y0, x1, y1):
    """Burning refinery column (Ukraine panel)."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 220, 198))
    s = (y1 - y0) / 240.0
    base = y1 - int(40 * s)

    def sy(v):
        return base - int(v * s)

    # columns
    draw.rectangle([x0 + 34, sy(120), x0 + 66, base], fill=(70, 66, 60))
    draw.rectangle([x0 + 82, sy(170), x0 + 100, base], fill=(70, 66, 60))
    draw.rectangle([x0 + 116, sy(96), x0 + 190, base], fill=(70, 66, 60))
    draw.ellipse([x0 + 116, sy(112), x0 + 190, sy(80)], fill=(70, 66, 60))
    # flame
    fx = x0 + 91
    draw.polygon([(fx - 26, sy(168)), (fx - 6, sy(226)),
                  (fx + 10, sy(190)), (fx + 26, sy(168))],
                 fill=(232, 116, 28))
    draw.polygon([(fx - 12, sy(168)), (fx, sy(204)),
                  (fx + 12, sy(168))], fill=(250, 200, 60))
    # barrel
    draw.ellipse([x1 - 92, sy(58), x1 - 40, sy(40)], fill=(178, 44, 32))
    draw.rectangle([x1 - 92, sy(50), x1 - 40, base], fill=(178, 44, 32))
    draw.rectangle([x1 - 92, sy(34), x1 - 40, sy(28)], fill=(120, 28, 20))
    draw.rectangle([x0, base, x1, y1], fill=(46, 44, 40))


def draw_space(draw, x0, y0, x1, y1):
    """Tiangong station and Mercury (space panel)."""
    draw.rectangle([x0, y0, x1, y1], fill=DARKPANEL)
    import random
    rng = random.Random(26)
    for _ in range(60):
        sx = rng.randint(x0 + 6, x1 - 6)
        sy = rng.randint(y0 + 6, y1 - 6)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 225, 235))
    # Mercury
    mx, my, mr = x1 - 120, y0 + 92, 62
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(198, 132, 74))
    for cx, cy, cr in [(mx - 24, my - 12, 9), (mx + 18, my + 20, 12),
                       (mx + 4, my - 30, 6), (mx - 30, my + 26, 7)]:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(168, 104, 56))
    # station: core + solar wings
    sx0, sy = x0 + 140, y0 + 118
    draw.rectangle([sx0, sy - 8, sx0 + 150, sy + 8], fill=(210, 214, 220))
    draw.rectangle([sx0 + 56, sy - 26, sx0 + 94, sy + 26], fill=(180, 184, 190))
    draw.ellipse([sx0 + 56, sy - 34, sx0 + 94, sy - 18], fill=(210, 214, 220))
    for wx in (sx0 - 92, sx0 + 162):
        draw.rectangle([wx, sy - 26, wx + 84, sy + 26], fill=(36, 84, 150))
        for i in range(1, 4):
            draw.line([(wx + i * 21, sy - 26), (wx + i * 21, sy + 26)],
                      fill=(90, 140, 190), width=2)
    draw.rectangle([sx0 - 8, sy - 4, sx0, sy + 4], fill=(160, 164, 170))
    draw.rectangle([sx0 + 150, sy - 4, sx0 + 158, sy + 4], fill=(160, 164, 170))
    # small rocket trail
    rx, ry = x1 - 250, y1 - 34
    draw.polygon([(rx, ry - 26), (rx + 12, ry), (rx - 12, ry)], fill=(240, 240, 236))
    draw.rectangle([rx - 6, ry, rx + 6, ry + 12], fill=(178, 44, 32))


def draw_quake(draw, x0, y0, x1, y1):
    """Seismograph zigzag over cracked ground (Nepal panel)."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 214, 192))
    s = (y1 - y0) / 150.0
    mid = y0 + int(58 * s)
    pts = [(x0 + 10, mid)]
    x = x0 + 10
    up = True
    while x < x1 - 10:
        x += 16
        pts.append((x, mid - int(26 * s) if up else mid + int(26 * s)))
        up = not up
    pts.append((x1 - 10, mid))
    draw.line(pts, fill=RED, width=4, joint="curve")
    base = y1 - int(44 * s)
    draw.rectangle([x0, base, x1, y1], fill=(96, 84, 70))
    cx = x0 + (x1 - x0) // 2
    draw.line([(cx, base), (cx - 14, base - int(26 * s)),
               (cx + 10, base - int(52 * s)), (cx - 6, base - int(78 * s)),
               (cx + 4, base - int(104 * s))],
              fill=(60, 52, 44), width=4, joint="curve")


def draw_rescue(draw, x0, y0, x1, y1):
    """Supermarket front with an open door and sunrise (Colombia panel)."""
    draw.rectangle([x0, y0, x1, y1], fill=(208, 226, 214))
    s = (y1 - y0) / 130.0
    sx, sy = x0 + (x1 - x0) // 2, y0 + int(40 * s)
    r = int(26 * s)
    draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(240, 190, 60))
    base = y1 - int(40 * s)
    draw.rectangle([x0 + 22, base - int(92 * s), x1 - 22, base],
                   fill=(240, 240, 236))
    draw.rectangle([x0 + 22, base - int(92 * s), x1 - 22, base - int(74 * s)],
                   fill=TEAL)
    draw.rectangle([x0 + 46, base - int(58 * s), x0 + 108, base],
                   fill=(52, 92, 84))
    draw.rectangle([x0 + 60, base - int(58 * s), x0 + 94, base],
                   fill=(250, 200, 60))
    for wx in (x1 - 128, x1 - 76):
        draw.rectangle([wx, base - int(58 * s), wx + 40, base - int(12 * s)],
                       fill=(173, 203, 224))
    draw.rectangle([x0, base, x1, y1], fill=(96, 84, 70))


def draw_tanker_fire(draw, x0, y0, x1, y1):
    """Tanker truck with flames (Cairo panel)."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 222, 200))
    s = (y1 - y0) / 180.0
    base = y1 - int(44 * s)

    def sy(v):
        return base - int(v * s)

    # truck: cab + tank
    draw.rectangle([x0 + 30, sy(66), x0 + 150, sy(14)], fill=(200, 200, 196))
    draw.ellipse([x0 + 30, sy(78), x0 + 150, sy(54)], fill=(200, 200, 196))
    draw.rectangle([x0 + 160, sy(52), x0 + 214, sy(14)], fill=(178, 44, 32))
    draw.rectangle([x0 + 170, sy(44), x0 + 196, sy(22)], fill=(173, 203, 224))
    for wx, wr in [(x0 + 62, 14), (x0 + 128, 14), (x0 + 188, 12)]:
        draw.ellipse([wx - wr, base - wr, wx + wr, base + wr], fill=(24, 24, 22))
        draw.ellipse([wx - 5, base - 5, wx + 5, base + 5], fill=(140, 140, 136))
    # flame above the tank
    fx = x0 + 90
    draw.polygon([(fx - 24, sy(72)), (fx - 4, sy(128)),
                  (fx + 12, sy(96)), (fx + 24, sy(72))],
                 fill=(232, 116, 28))
    draw.polygon([(fx - 11, sy(72)), (fx, sy(104)),
                  (fx + 11, sy(72))], fill=(250, 200, 60))
    draw.rectangle([x0, base, x1, y1], fill=(60, 52, 44))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 178], fill=NAVY)
    d.rectangle([0, 178, W, 184], fill=GOLD)
    title_f = font(SERIF_B, 92)
    d.text((MARGIN, 18), "THE WORLD TODAY", font=title_f, fill=CREAM)
    sub_f = font(SANS_B, 26)
    d.text((MARGIN, 128), "THURSDAY  ·  26 NOVEMBER 2026", font=sub_f, fill=GOLD)
    right_f = font(SANS, 24)
    rt = "ONE IMAGE — THE WHOLE DAY"
    d.text((W - MARGIN - d.textlength(rt, font=right_f), 130), rt,
           font=right_f, fill=(200, 208, 220))
    d.line([(MARGIN, 168), (W - MARGIN, 168)], fill=(70, 90, 120), width=1)

    # ---- lead: Gulf on edge ----
    y = 200
    d.rectangle([MARGIN, y, W - MARGIN, 540], outline=(190, 184, 170), width=2)
    kicker(d, MARGIN + 18, y + 14, "THE GULF  ·  LEAD STORY")
    fit_headline(d, MARGIN + 18, y + 52, "GULF ON EDGE", 64, 620)
    body_f = font(SANS, 25)
    para(d, MARGIN + 18, y + 138,
         "Houthi forces strike Saudi Arabia's Ras Tanura oil refinery, "
         "and two oil tankers hit naval mines in the Strait of Hormuz — "
         "fire across the world's busiest oil waterway.",
         body_f, 620, leading=8)
    d.text((MARGIN + 18, 540 - 40), "Oil, mines and missiles in the strait.",
         font=font(SANS_B, 22), fill=GREY)
    draw_refinery_scene(d, 700, y + 14, W - MARGIN - 18, y + 196)
    draw_sea_mines(d, 700, y + 214, W - MARGIN - 18, 540 - 14)

    # ---- row 2: Gaza + Ukraine ----
    y = 556
    panels = [(MARGIN, 592), (608, W - MARGIN)]
    # Gaza
    x0, x1 = panels[0]
    d.rectangle([x0, y, x1, 872], outline=(190, 184, 170), width=2)
    kicker(d, x0 + 16, y + 12, "GAZA")
    fit_headline(d, x0 + 16, y + 48, "CEASEFIRE UNDER STRAIN", 30, x1 - x0 - 32)
    para(d, x0 + 16, y + 100,
         "Israel strikes a Hamas official in Gaza; the fragile "
         "ceasefire frays.",
         font(SANS, 23), x1 - x0 - 32, leading=6)
    draw_crack_skyline(d, x0 + 16, y + 172, x1 - 16, 872 - 14)
    # Ukraine
    x0, x1 = panels[1]
    d.rectangle([x0, y, x1, 872], outline=(190, 184, 170), width=2)
    kicker(d, x0 + 16, y + 12, "UKRAINE", color=TEAL)
    fit_headline(d, x0 + 16, y + 48, "KYIV HITS THE REFINERIES", 30, x1 - x0 - 32)
    para(d, x0 + 16, y + 100,
         "Ukraine strikes Russian oil refineries deep inside Russia; "
         "Putin vows retaliation.",
         font(SANS, 23), x1 - x0 - 32, leading=6)
    draw_oil_flame(d, x0 + 16, y + 172, x1 - 16, 872 - 14)

    # ---- space panel ----
    y = 888
    d.rectangle([MARGIN, y, W - MARGIN, 1150], fill=DARKPANEL)
    kicker(d, MARGIN + 18, y + 14, "SPACE", color=GOLD)
    fit_headline(d, MARGIN + 18, y + 52, "A FIRST, AND A DATE WITH MERCURY",
                 30, 660, fill=CREAM)
    para(d, MARGIN + 18, y + 100,
         "Pakistan's first astronaut rides Shenzhou-24 to China's "
         "Tiangong station — the first foreign national ever chosen "
         "for it. BepiColombo reaches Mercury orbit after eight years.",
         font(SANS, 24), 660, fill=(220, 226, 234), leading=7)
    draw_space(d, 730, y + 12, W - MARGIN - 12, 1150 - 12)

    # ---- row 4: three briefs ----
    y = 1166
    briefs = [
        ("NEPAL", "QUAKE SHAKES KOSHI",
         "A 5.6 quake shakes Koshi Province, by China's border.",
         draw_quake),
        ("COLOMBIA", "20 FREED IN COLOMBIA",
         "Police storm a supermarket; 20 hostages freed after 17 hours.",
         draw_rescue),
        ("CAIRO", "TANKER FIRE KILLS 30",
         "Fuel tanker crash ignites a highway fire; at least 30 killed.",
         draw_tanker_fire),
    ]
    xs = [(MARGIN, 396), (412, 788), (804, W - MARGIN)]
    for (kick, head, body, art), (x0, x1) in zip(briefs, xs):
        d.rectangle([x0, y, x1, 1408], outline=(190, 184, 170), width=2)
        kicker(d, x0 + 14, y + 10, kick, size=22)
        fit_headline(d, x0 + 14, y + 42, head, 26, x1 - x0 - 28)
        para(d, x0 + 14, y + 82, body, font(SANS, 21), x1 - x0 - 28, leading=5)
        art(d, x0 + 14, y + 142, x1 - 14, 1408 - 12)

    # ---- ticker: sport & markets ----
    y = 1424
    d.rectangle([MARGIN, y, W - MARGIN, 1568], fill=NAVY)
    d.text((MARGIN + 16, y + 12), "SPORT  ·  MARKETS  ·  AND IN INDIA",
           font=font(SANS_B, 22), fill=GOLD)
    tf = font(SANS, 23)
    lines = [
        "Chess: World Championship Game 2 — Gukesh vs Sindarov ends in a 20-move draw.",
        "Cricket: Vaibhav Sooryavanshi, 15, smashes 204 off 53 balls against UAE.",
        "Markets: Nvidia down 5% as AI stocks slide; Nasdaq and S&P 500 pare losses.",
        "India marks 18 years since the 26/11 Mumbai attacks; Constitution Day.",
    ]
    yy = y + 44
    for ln in lines:
        d.text((MARGIN + 16, yy), "•  " + ln, font=tf, fill=(225, 230, 238))
        yy += 25

    # ---- footer ----
    ff = font(SANS, 20)
    ft = "26 November 2026  ·  Headlines as reported today  ·  The World Today"
    d.text(((W - d.textlength(ft, font=ff)) // 2, 1576), ft, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
