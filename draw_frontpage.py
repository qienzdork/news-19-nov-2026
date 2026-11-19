#!/usr/bin/env python3
"""Draw 'Thursday 19 November 2026' as a one-page newspaper front page.

Original vector-style artwork, drawn from scratch with Pillow. Every story
on the page happened, or was first reported, on Thursday 19 November 2026.
Output: entry.png, 1024x1024, deterministic (no randomness, no network).
Run: python3 draw_frontpage.py   -> writes entry.png beside this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (163, 18, 31)
NAVY = (18, 40, 75)
TEAL = (14, 90, 86)
GOLD = (176, 124, 22)
GREY = (90, 86, 76)
LIGHT = (232, 226, 208)
BLUE = (28, 78, 140)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, size, max_w, leading=None, fill=INK):
    fnt = font(SERIF_B, size)
    leading = leading or int(size * 1.08)
    return para(draw, x, y, text, fnt, max_w, leading, fill=fill)


def kicker(draw, x, y, num, label, color=RED):
    """Numbered story kicker: '1  ASIA - APEC SUMMIT'."""
    fnt = font(SANS_B, 11)
    draw.text((x, y), str(num), font=font(SANS_B, 13), fill=color)
    draw.text((x + 20, y + 1), label, font=fnt, fill=color)
    return y + 16


def rule(draw, x, y, w, fill=INK, width=1):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# (n, region, kicker, headline, deck) for the 13 pictured stories.
TOP = [
    (1, "ASIA", "ASIA - APEC SUMMIT",
     "Trump, Xi and Putin hold first three-way summit",
     "The three nuclear powers meet at APEC in Shenzhen; arms control, "
     "Ukraine and the Iran war top the agenda."),
    (2, "EUROPE", "EUROPE - WORLD COURT",
     "World Court rules on Myanmar's Rohingya case",
     "The ICJ reads its judgment in The Gambia's case over the 2017 "
     "campaign that drove 730,000 Rohingya to flee."),
    (3, "AMERICAS", "AMERICAS - MARKETS",
     "Anthropic debuts in the biggest IPO on record",
     "Priced at $83, above its range, the Claude maker raised $81.3bn; "
     "Thursday's first trades set the real price."),
    (4, "EUROPE", "EUROPE - UKRAINE WAR",
     "Ukraine strikes Crimean Bridge a third time",
     "Traffic is halted after the week's third attack."),
    (5, "EUROPE", "EUROPE - CLIMATE",
     "COP31 enters its final 48 hours",
     "Ministers take over the text in Antalya."),
    (6, "ASIA", "ASIA - WEATHER",
     "Akvan bears down as 200,000 flee the coast",
     "Red alerts in 11 districts; landfall due Friday."),
    (7, "ASIA", "ASIA - UNREST",
     "Yunus's home torched as 28 districts burn",
     "Bangladesh sinks deeper into turmoil."),
    (8, "MIDDLE EAST", "MIDDLE EAST - IRAN WAR",
     "Iran hits back across the Gulf",
     "A tanker is struck in the Strait of Hormuz."),
    (9, "MIDDLE EAST", "MIDDLE EAST - ISRAEL",
     "Knesset picks Kahana as speaker",
     "66 votes for the Yashar party's candidate."),
    (10, "AMERICAS", "AMERICAS - VENEZUELA",
     "US and Venezuela sign military deal",
     "Hegseth signs a cooperation pact in Caracas."),
    (11, "ASIA", "ASIA - NUCLEAR",
     "IAEA: North Korea grew uranium enrichment",
     "Yongbyon expanded, inspectors report."),
    (12, "GLOBAL", "GLOBAL - GAMES",
     "GTA VI arrives after a 13-year wait",
     "Midnight launch starts in New Zealand."),
    (13, "OCEANIA", "OCEANIA - DISASTER",
     "Fiji declares disaster over El Ni\u00f1o drought",
     "A national emergency as water runs short."),
]

# Briefs 14-40: short, one-line, in "Also on Thursday 19 November".
BRIEFS = [
    "Tokyo: India and Japan review defence ties at 2+2 talks",
    "Jakarta: Indonesia's parliament approves asset-forfeiture bill",
    "New Delhi: Modi meets the Prince and Princess of Wales",
    "Canberra: Australia sanctions West Bank settlers",
    "Washington: Supreme Court asked to rule on Venezuelan TPS",
    "Horn: Ethiopia and Eritrea mass troops at the border",
    "Wellington: India vs New Zealand First Test begins",
    "Cape Canaveral: NASA sets coverage for NG CRS-25 launch",
    "Geneva: 589m children lived in conflict zones in 2025",
    "Kuala Lumpur: UNHCR stops registering new asylum cases",
    "Panama City: second arrest over attack on journalist's home",
    "Sana'a: coalition reports missile threat towards Riyadh",
    "Manila: US pursues a $2bn+ loan package for the Philippines",
    "Nadi: Cyclone Xavier winds hit 100 knots near Cook Islands",
    "Riyadh: Civil Defence says danger has passed after warning",
    "New Delhi: schools reopen as Delhi lifts GRAP Stage-III curbs",
    "New Delhi: India puts 162.5% duty on bulk Scotch imports",
    "Mumbai: Goldman Sachs upgrades India to overweight",
    "Shenzhen: APEC leaders adopt the Shenzhen Declaration",
    "Nairobi: Kenya floods kill six as Ruto gives address",
    "Sacramento: California braces for an atmospheric river",
    "La Paz: Bolivia declares an El Ni\u00f1o emergency",
    "Baghdad: six French ISIL members jailed for life in Iraq",
    "Auckland: New Zealand plays first as GTA VI unlocks at midnight",
    "Mogadishu: Somalia accuses UAE of secret military bases",
    "Ottawa: Canada rethinks China ties, seeking the right deal",
    "Riyadh: Gulf leaders urge Trump not to strike Iran",
]

# Big-number strip under the masthead: the day in six figures.
STATS = [
    ("$81.3bn", "raised by Anthropic, the largest IPO on record"),
    ("200,000", "evacuated ahead of Cyclone Akvan"),
    ("15.9m", "GTA VI pre-orders banked before release day"),
    ("$120bn", "a year of adaptation finance unresolved at COP31"),
    ("730,000", "Rohingya who fled in 2017, the ICJ case"),
    ("66", "votes that made Kahana Knesset speaker"),
]

REGIONS = [
    ("ASIA", 13, (122, 62, 140)),
    ("EUROPE", 3, (28, 78, 140)),
    ("AMERICAS", 8, (176, 32, 32)),
    ("MIDDLE EAST", 6, (176, 124, 22)),
    ("AFRICA", 3, (14, 90, 86)),
    ("OCEANIA", 5, (60, 110, 70)),
    ("GLOBAL", 2, (90, 86, 76)),
]


# ------------------------------------------------------------- illustrations
def draw_skyline(draw, x, y, w, h):
    """Shenzhen tarmac: dusk sky, skyline, runway, plane, three flags."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 196, 138))
    draw.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(214, 120, 40))
    # skyline blocks
    for i, (bx, bw, bh) in enumerate([(0, 26, 52), (30, 18, 70), (52, 30, 44),
                                      (86, 16, 62), (106, 24, 38), (134, 20, 58)]):
        draw.rectangle([x + bx, y + h - 34 - bh, x + bx + bw, y + h - 34],
                       fill=(120, 88, 70) if i % 2 else (96, 70, 58))
    draw.rectangle([x, y + h - 34, x + w, y + h - 22], fill=(90, 90, 92))
    draw.line([(x, y + h - 28), (x + w, y + h - 28)], fill=(250, 250, 250), width=2)
    # plane: fuselage, wing, tail
    px, py = x + 14, y + h - 52
    draw.polygon([(px, py), (px + 62, py), (px + 72, py + 7), (px + 62, py + 11),
                  (px, py + 11)], fill=(240, 244, 248))
    draw.polygon([(px + 34, py + 2), (px + 52, py + 2), (px + 46, py + 16),
                  (px + 38, py + 16)], fill=(190, 200, 210))
    draw.polygon([(px + 58, py - 8), (px + 64, py - 8), (px + 64, py + 2),
                  (px + 58, py + 2)], fill=(163, 18, 31))
    # three small flags on poles
    for i, col in enumerate([(178, 32, 32), (214, 120, 40), (28, 78, 140)]):
        fx = x + 128 + i * 26
        draw.line([(fx, y + h - 34), (fx, y + h - 14)], fill=INK, width=2)
        draw.rectangle([fx, y + h - 34, fx + 18, y + h - 24], fill=col)
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(163, 18, 31))
    draw.text((x + 8, y + h - 19), "SHENZHEN  •  APEC LEADERS' WEEK",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def draw_gulf(draw, x, y, w, h):
    """Simplified Gulf map: sea, Iran / Kuwait / Bahrain, drone tracks."""
    draw.rectangle([x, y, x + w, y + h], fill=(168, 196, 214))
    # land masses
    draw.polygon([(x + 8, y + 6), (x + w - 8, y + 6), (x + w - 8, y + 34),
                  (x + 130, y + 34), (x + 120, y + 62), (x + 8, y + 62)],
                 fill=(222, 200, 150))
    draw.polygon([(x + 8, y + 66), (x + 150, y + 66), (x + 150, y + h - 8),
                  (x + 8, y + h - 8)], fill=(222, 200, 150))
    draw.text((x + 130, y + 10), "IRAN", font=font(SANS_B, 13), fill=INK)
    draw.text((x + 14, y + 44), "KUWAIT", font=font(SANS_B, 11), fill=INK)
    draw.text((x + 96, y + 78), "BAHRAIN", font=font(SANS_B, 10), fill=INK)
    draw.text((x + 150, y + 78), "THE GULF", font=font(SANS_B, 10), fill=NAVY)
    # drone tracks: dashed red arcs Kuwait -> Gulf
    for k in range(6):
        t = k / 5.0
        dx = x + 40 + t * 110
        dy = y + 46 + int(14 * math.sin(t * math.pi)) - 8
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
    draw.polygon([(x + 150, y + 44), (x + 162, y + 50), (x + 150, y + 56)],
                 fill=RED)
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=NAVY)
    draw.text((x + 8, y + h - 19), "KUWAIT  •  BAHRAIN  •  IRAN WAR",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def draw_court(draw, x, y, w, h):
    """The Hague: courthouse columns, scales of justice, UN blue."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 40, 75))
    # pediment + columns
    draw.polygon([(x + 60, y + 10), (x + w - 60, y + 10), (x + w - 20, y + 34),
                  (x + 20, y + 34)], fill=(240, 240, 230))
    for i in range(5):
        cx = x + 34 + i * 56
        draw.rectangle([cx, y + 38, cx + 16, y + h - 30], fill=(240, 240, 230))
    draw.rectangle([x, y + h - 30, x + w, y + h - 22], fill=(240, 240, 230))
    # scales: beam + two pans, centred between columns
    sx, sy = x + w // 2, y + 46
    draw.line([(sx - 26, sy), (sx + 26, sy)], fill=(255, 200, 60), width=3)
    draw.line([(sx, sy - 8), (sx, sy + 8)], fill=(255, 200, 60), width=3)
    draw.polygon([(sx - 30, sy + 12), (sx - 16, sy + 12), (sx - 23, sy + 2)],
                 fill=(255, 200, 60))
    draw.polygon([(sx + 16, sy + 12), (sx + 30, sy + 12), (sx + 23, sy + 2)],
                 fill=(255, 200, 60))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(163, 18, 31))
    draw.text((x + 8, y + h - 19), "THE HAGUE  •  ICJ  •  GAMBIA v MYANMAR",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def draw_ipo(draw, x, y, w, h):
    """Nasdaq debut: rising candlesticks on a dark green board, $83 tag."""
    draw.rectangle([x, y, x + w, y + h], fill=(8, 48, 32))
    bars = [(20, 52, 30), (70, 44, 44), (120, 52, 34), (170, 34, 58),
            (220, 26, 66), (268, 16, 74)]
    for bx, bt, bh in bars:
        draw.rectangle([x + bx, y + bt, x + bx + 26, y + bt + bh],
                       fill=(60, 200, 120))
        draw.line([(x + bx + 13, y + bt - 8), (x + bx + 13, y + bt + bh + 8)],
                  fill=(255, 255, 255), width=2)
    draw.line([(x + 14, y + 66), (x + w - 14, y + 14)], fill=(255, 200, 60),
              width=3)
    draw.polygon([(x + w - 34, y + 8), (x + w - 14, y + 14), (x + w - 32, y + 26)],
                 fill=(255, 200, 60))
    draw.text((x + 16, y + 8), "ANT  •  NASDAQ", font=font(SANS_B, 13),
              fill=(255, 255, 255))
    draw.rectangle([x + w - 92, y + 30, x + w - 12, y + 58], fill=(255, 200, 60))
    draw.text((x + w - 84, y + 34), "$83", font=font(SANS_B, 20), fill=NAVY)
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(163, 18, 31))
    draw.text((x + 8, y + h - 19), "FIRST TRADES TODAY  •  $81.3bn RAISED",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def draw_small_icon(draw, x, y, w, h, kind):
    """One small flat illustration per second-row story."""
    if kind == "bridge":
        draw.rectangle([x, y, x + w, y + h], fill=(28, 78, 140))
        draw.rectangle([x + 10, y + 34, x + w - 10, y + 42], fill=(240, 240, 230))
        for i in range(4):
            px = x + 26 + i * 44
            draw.line([(px, y + 34), (px, y + 8)], fill=(255, 255, 255), width=2)
            draw.line([(px, y + 8), (px + 22, y + 34)], fill=(255, 255, 255), width=1)
            draw.line([(px, y + 8), (px - 22, y + 34)], fill=(255, 255, 255), width=1)
        draw.ellipse([x + w // 2 - 14, y + 46, x + w // 2 + 14, y + 60],
                     fill=(255, 120, 40))
    elif kind == "cop":
        draw.rectangle([x, y, x + w, y + h], fill=(176, 124, 22))
        draw.ellipse([x + 60, y + 6, x + 150, y + 58], fill=(120, 180, 120))
        draw.arc([x + 70, y + 12, x + 140, y + 52], 0, 360,
                 fill=(255, 255, 255), width=3)
    elif kind == "cyclone":
        draw.rectangle([x, y, x + w, y + h], fill=(14, 90, 86))
        cx, cy = x + w // 2, y + h // 2 - 4
        for r in (34, 26, 18, 10):
            draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                     fill=(255, 255, 255), width=4)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 200, 60))
    elif kind == "fire":
        draw.rectangle([x, y, x + w, y + h], fill=(40, 30, 30))
        draw.rectangle([x + 20, y + 44, x + w - 20, y + 56], fill=(120, 90, 70))
        for i, (fx, fh) in enumerate([(34, 34), (62, 46), (96, 38), (130, 44)]):
            draw.polygon([(x + fx, y + 52), (x + fx + 12, y + 52 - fh),
                          (x + fx + 24, y + 52)], fill=(255, 120, 40) if i % 2
                         else (255, 200, 60))
    elif kind == "tanker":
        draw.rectangle([x, y, x + w, y + h], fill=(18, 40, 75))
        draw.rectangle([x, y + 40, x + w, y + h], fill=(28, 78, 140))
        draw.rectangle([x + 40, y + 30, x + 150, y + 46], fill=(200, 60, 40))
        draw.rectangle([x + 120, y + 14, x + 140, y + 30], fill=(240, 240, 230))
        draw.polygon([(x + 60, y + 8), (x + 70, y + 26), (x + 50, y + 26)],
                     fill=(255, 200, 60))
    elif kind == "speaker":
        draw.rectangle([x, y, x + w, y + h], fill=(18, 40, 75))
        draw.polygon([(x + 50, y + 8), (x + 140, y + 8), (x + 156, y + 28),
                      (x + 34, y + 28)], fill=(240, 240, 230))
        draw.rectangle([x + 44, y + 28, x + 146, y + 50], fill=(240, 240, 230))
        for i in range(4):
            draw.rectangle([x + 52 + i * 24, y + 32, x + 62 + i * 24, y + 50],
                           fill=NAVY)
    elif kind == "deal":
        draw.rectangle([x, y, x + w, y + h], fill=(246, 241, 227))
        draw.rectangle([x + 50, y + 12, x + 140, y + 52], fill=(255, 255, 255),
                       outline=INK, width=2)
        draw.line([(x + 60, y + 24), (x + 130, y + 24)], fill=INK, width=2)
        draw.line([(x + 60, y + 34), (x + 130, y + 34)], fill=INK, width=2)
        draw.line([(x + 60, y + 44), (x + 100, y + 44)], fill=INK, width=2)
        draw.polygon([(x + 118, y + 40), (x + 132, y + 48), (x + 118, y + 54)],
                     fill=RED)
    elif kind == "atom":
        draw.rectangle([x, y, x + w, y + h], fill=(10, 16, 38))
        cx, cy = x + w // 2, y + h // 2 - 4
        for ang in (0, 60, 120):
            draw.ellipse([cx - 40, cy - 16, cx + 40, cy + 16],
                         outline=(255, 200, 60), width=2)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    elif kind == "gta":
        draw.rectangle([x, y, x + w, y + h], fill=(90, 30, 110))
        draw.rounded_rectangle([x + 50, y + 10, x + 160, y + 46], radius=12,
                               fill=(30, 30, 40))
        draw.ellipse([x + 62, y + 22, x + 74, y + 34], fill=(255, 255, 255))
        draw.ellipse([x + 136, y + 22, x + 148, y + 34], fill=(255, 200, 60))
    elif kind == "drought":
        draw.rectangle([x, y, x + w, y + h], fill=(233, 196, 138))
        draw.ellipse([x + w - 52, y + 6, x + w - 14, y + 44], fill=(255, 160, 40))
        draw.line([(x + 12, y + 58), (x + 60, y + 46), (x + 100, y + 58),
                   (x + 150, y + 44), (x + w - 12, y + 56)], fill=(150, 100, 60),
                  width=3)
        draw.line([(x + 60, y + 46), (x + 70, y + 62)], fill=(150, 100, 60), width=2)
    # Caption bar at the foot of every small icon: one solid strip, so the
    # label never collides with the drawing above it.
    labels = {
        "bridge": "3RD STRIKE THIS WEEK",
        "cop": "FINAL 48 HOURS",
        "cyclone": "LANDFALL FRI 20 NOV",
        "fire": "28 DISTRICTS HIT",
        "tanker": "STRAIT OF HORMUZ",
        "speaker": "66 VOTES  •  KNESSET",
        "deal": "CARACAS  •  HEGSETH SIGNS",
        "atom": "YONGBYON EXPANDED",
        "gta": "00:00  •  NEW ZEALAND FIRST",
        "drought": "NATIONAL EMERGENCY",
    }
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(17, 17, 17))
    draw.text((x + 8, y + h - 18), labels[kind], font=font(SANS_B, 10),
              fill=(255, 255, 255))


def draw_map(draw, x, y, w, h):
    """Stylised world map with numbered pins for stories 1-11."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 232))
    # rough continent blobs (stylised, not to scale)
    blobs = [
        [(14, 26), (70, 14), (96, 30), (78, 62), (30, 66), (10, 46)],   # N America
        [(86, 78), (118, 70), (128, 92), (104, 108), (88, 94)],          # S America
        [(150, 18), (196, 10), (214, 26), (196, 44), (162, 40)],         # Europe
        [(152, 52), (196, 48), (210, 76), (188, 104), (160, 88)],        # Africa
        [(220, 12), (286, 8), (300, 34), (272, 66), (238, 52)],          # Asia
        [(268, 92), (300, 86), (308, 106), (282, 112)],                  # Oceania
    ]
    for b in blobs:
        draw.polygon([(x + bx, y + by) for bx, by in b], fill=(222, 200, 150),
                     outline=(150, 130, 100))
    # Approximate locations: 1 Shenzhen, 2 The Hague, 3 New York, 4 Crimea,
    # 5 Antalya, 6 Odisha, 7 Dhaka, 8 the Gulf, 9 Jerusalem, 10 Caracas,
    # 11 Pyongyang, 12 New Zealand, 13 Fiji.
    pins = [(282, 48), (176, 18), (38, 32), (206, 26), (200, 42),
            (260, 60), (272, 50), (230, 50), (214, 52), (58, 80),
            (288, 38), (305, 105), (298, 90)]
    pin_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    for i, (px, py) in zip(pin_nums, pins):
        draw.ellipse([x + px - 7, y + py - 7, x + px + 7, y + py + 7],
                     fill=RED, outline=(255, 255, 255), width=1)
        draw.text((x + px - 3, y + py - 6), str(i), font=font(SANS_B, 9),
                  fill=(255, 255, 255))
    draw.text((x + 8, y + h - 18),
              "Numbered pins: stories 1-13",
              font=font(SANS, 10), fill=GREY)


# ------------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 18
    # --- top strip
    d.text((mx, 10), "THE WORLD IN ONE DAY  —  ONE PAGE, ONE DATE",
           font=font(SANS_B, 11), fill=RED)
    d.text((W - mx - 300, 10), "40 STORIES  •  7 REGIONS  •  13 DRAWN",
           font=font(SANS_B, 11), fill=NAVY)
    rule(d, mx, 28, W - 2 * mx, width=2)
    # --- masthead: date box + title
    d.rectangle([mx, 36, mx + 84, 106], fill=RED)
    d.text((mx + 10, 40), "NOV", font=font(SANS_B, 15), fill=(255, 255, 255))
    d.text((mx + 8, 58), "19", font=font(SERIF_B, 30), fill=(255, 255, 255))
    d.text((mx + 10, 90), "THU 2026", font=font(SANS_B, 10), fill=(255, 255, 255))
    d.text((mx + 96, 38), "Thursday 19 November 2026",
           font=font(SERIF_B, 44), fill=INK)
    d.text((mx + 98, 88),
           "Everything on this page happened, or was first reported, on "
           "Thursday 19 November 2026.",
           font=font(SERIF, 13), fill=GREY)
    rule(d, mx, 112, W - 2 * mx, width=3)
    # --- region bar
    x = mx
    total_w = W - 2 * mx
    for name, count, col in REGIONS:
        seg = int(total_w * count / 40)
        d.rectangle([x, 118, x + seg - 2, 138], fill=col)
        label = f"{name} {count}" if seg >= 70 else str(count)
        d.text((x + 6, 122), label, font=font(SANS_B, 11),
               fill=(255, 255, 255))
        x += seg
    # --- big-number stat strip
    y = 144
    col_w = (W - 2 * mx) // 6
    for i, (num, what) in enumerate(STATS):
        tx = mx + i * col_w
        d.rectangle([tx, y, tx + col_w - 4, y + 46], fill=LIGHT,
                    outline=(180, 170, 145))
        d.text((tx + 6, y + 3), num, font=font(SANS_B, 17), fill=RED)
        para(d, tx + 6, y + 24, what, font(SANS, 9), col_w - 12, 10,
             max_lines=2)
    # --- top 3 stories
    y = 196
    col_w = (W - 2 * mx - 16) // 3
    illus = [draw_skyline, draw_court, draw_ipo]
    for i, story in enumerate(TOP[:3]):
        sx = mx + i * (col_w + 8)
        n, region, kick, head, deck = story
        illus[i](d, sx, y, col_w, 96)
        kicker(d, sx, y + 100, n, kick)
        yy = headline(d, sx, y + 116, head, 22, col_w)
        para(d, sx, yy + 2, deck, font(SERIF, 11), col_w, 14, max_lines=2)
    # --- second row: stories 4-13, five per row, two rows
    kinds = ["bridge", "cop", "cyclone", "fire", "tanker",
             "speaker", "deal", "atom", "gta", "drought"]
    col_w2 = (W - 2 * mx - 32) // 5
    for row in range(2):
        ry = 392 + row * 104
        for c in range(5):
            idx = 3 + row * 5 + c
            story = TOP[idx]
            sx = mx + c * (col_w2 + 8)
            n, region, kick, head, deck = story
            draw_small_icon(d, sx, ry, col_w2, 52, kinds[idx - 3])
            kicker(d, sx, ry + 56, n, kick)
            headline(d, sx, ry + 72, head, 13, col_w2, leading=15)
            # No deck in this row: headline + kicker alone keep the
            # grid clean at thumbnail size; the deck lives in the top row.
    # --- bottom: map + briefs
    y = 606
    rule(d, mx, y, W - 2 * mx, width=2)
    d.text((mx, y + 6), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    d.text((mx + 330, y + 6), "ALSO ON THURSDAY 19 NOVEMBER",
           font=font(SANS_B, 12), fill=RED)
    draw_map(d, mx, y + 24, 312, 222)
    # briefs in 3 columns, 9 each
    bx0 = mx + 330
    bcol_w = (W - mx - bx0 - 6) // 3
    per_col = 9
    for ci in range(3):
        bx = bx0 + ci * (bcol_w + 4)
        by = y + 24
        for j in range(per_col):
            k = ci * per_col + j
            if k >= len(BRIEFS):
                break
            num = 14 + k
            d.text((bx, by), str(num), font=font(SANS_B, 9), fill=RED)
            by = para(d, bx + 22, by, BRIEFS[k], font(SANS, 9), bcol_w - 24,
                      11, max_lines=2)
            by += 1
    # --- footer: date check + sources
    fy = 936
    d.rectangle([mx, fy, W - mx, fy + 44], outline=RED, width=2)
    d.text((mx + 8, fy + 4), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    para(d, mx + 92, fy + 4,
         "Left out, first reported Wed 18 Nov: the Iranian drone "
         "interceptions; the EU's proposed \u20ac45bn loan for Ukraine; the "
         "Democrats' 251-11 Jeffries vote; Voyager 1 at one light-day; the "
         "Van Gogh sale at $190.4m; UK inflation at 3.6%. Not yet news Thu: "
         "Cyclone Akvan's landfall; the COP31 final text (both due Fri 20 Nov).",
         font(SANS, 10), W - mx - 100, 12, max_lines=3)
    d.text((mx, fy + 50),
           "All 40 stories happened, or were first reported, on Thu 19 Nov 2026; "
           "each has two or more sources. Claims are attributed. Original drawings.",
           font=font(SANS, 9), fill=GREY)
    d.text((mx, fy + 63),
           "Sources: Reuters  •  AP  •  AFP  •  BBC  •  CBS  •  The Hindu  •  "
           "IMD  •  NASA  •  ICJ  •  IAEA  •  WHO",
           font=font(SANS, 9), fill=GREY)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
