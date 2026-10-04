#!/usr/bin/env python3
"""learn-avalanche için özgün piksel-art görselleri üretir.

Çıktılar (docs/img/):
  banner.svg / banner.png            README başlığı        (1280x320)
  social-preview.png                 GitHub "Social preview" (1280x640)

Tasarım bu repoya özgüdür: gece dağları, ay, çığ (kar bulutu), zincir bloklarının
yan yana dizilişi. Avalanche'ın ya da herhangi bir markanın logosu çizilmez ve
taklit edilmez.

Kullanım:   python3 tools/make-art.py            (Pillow gerekir: pip install pillow)
Deterministik: aynı kod aynı görseli üretir (sabit tohum).
"""
import os
import random
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow gerekli: pip install pillow")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "img")

# ------------------------------------------------------------------ renkler
SKY = ["#060A1C", "#0A1130", "#0F1A47", "#16275F", "#213A7C", "#3A5E98", "#6C97BF", "#A9CFE0"]
STAR = ["#FFFFFF", "#BFD8FF", "#7FA6E0"]
TITLE_GRAD = ["#FFFFFF", "#FFFFFF", "#E4F1FF", "#C8E3FF", "#A5CFF7", "#86BDEE", "#6AAEE6"]
TITLE_SHADOW = "#12306E"
TAG = "#9CC4EE"
TAG_SHADOW = "#0B1A44"
MOON, MOON_SHADE, MOON_CRATER, MOON_GLOW = "#EEF4FF", "#C7D6F0", "#B0C2E4", "#2C4A8C"
BLOCK_FILL, BLOCK_HI, BLOCK_LINE, BLOCK_DARK = "#7CF3E0", "#D5FFF7", "#0E3B4A", "#3FB8A8"

# far, mid, near: (taban, tepe[(x_oran, yükseklik)], eğim, gövde, gölge, kar, kar gölgesi)
LAYERS = [
    dict(base=-20, slope=0.62, jit=1, snow=9,
         peaks=[(0.05, 17), (0.30, 19), (0.55, 20), (0.85, 22)],
         body="#1B2A55", shade="#141F44", snow_c="#5B74A8", snow_s="#46608F"),
    dict(base=-12, slope=0.80, jit=1, snow=11,
         peaks=[(0.20, 17), (0.45, 22), (0.68, 24), (0.92, 21)],
         body="#243767", shade="#192853", snow_c="#A9C2E6", snow_s="#7F9CCB"),
    dict(base=-8, slope=1.05, jit=2, snow=10,
         peaks=[(0.10, 15), (0.38, 13), (0.58, 21), (0.78, 29), (0.95, 17)],
         body="#2E4580", shade="#1B2A55", snow_c="#F2F8FF", snow_s="#BCD2F0"),
]

BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

# ------------------------------------------------------------------ 5x7 font
FONT_SRC = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#",
    "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".####|#....|#....|#....|#....|#....|.####",
    "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####",
    "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".####|#....|#....|#.###|#...#|#...#|.####",
    "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": "#####|..#..|..#..|..#..|..#..|..#..|#####",
    "J": "..###|...#.|...#.|...#.|...#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
    "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
    "N": "#...#|##..#|#.#.#|#..##|#...#|#...#|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
    "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.",
    "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
    "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#",
    "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
    "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "-": ".....|.....|.....|#####|.....|.....|.....",
    "+": ".....|..#..|..#..|#####|..#..|..#..|.....",
    "/": "....#|....#|...#.|..#..|.#...|#....|#....",
    ".": ".....|.....|.....|.....|.....|..##.|..##.",
    " ": ".....|.....|.....|.....|.....|.....|.....",
}
FONT = {k: [row for row in v.split("|")] for k, v in FONT_SRC.items()}


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[None] * w for _ in range(h)]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def text(self, x, y, s, scale=1, colors=None, shadow=None, spacing=1, shadow_off=None):
        """5x7 piksel yazı. colors: satır başına renk listesi (7) ya da tek renk."""
        if isinstance(colors, str):
            colors = [colors] * 7
        off = shadow_off if shadow_off is not None else scale
        for pass_shadow in ([True, False] if shadow else [False]):
            cx = x
            for ch in s.upper():
                glyph = FONT.get(ch, FONT[" "])
                for ry, row in enumerate(glyph):
                    for rx, v in enumerate(row):
                        if v != "#":
                            continue
                        col = shadow if pass_shadow else colors[ry]
                        ox = off if pass_shadow else 0
                        oy = off if pass_shadow else 0
                        self.rect(cx + rx * scale + ox, y + ry * scale + oy, scale, scale, col)
                cx += (5 + spacing) * scale
        return cx - spacing * scale  # bitiş x


def text_width(s, scale=1, spacing=1):
    return len(s) * (5 + spacing) * scale - spacing * scale


# ------------------------------------------------------------------ sahne
def sky(cv):
    n = len(SKY)
    span = cv.h * 0.88
    for y in range(cv.h):
        t = min(y / span, 1.0) * (n - 1)
        i = min(int(t), n - 2)
        frac = t - i
        for x in range(cv.w):
            thr = (BAYER4[y % 4][x % 4] + 0.5) / 16.0
            cv.px[y][x] = SKY[i + 1] if frac > thr else SKY[i]


def stars(cv, rng, count, ymax):
    for _ in range(count):
        x, y = rng.randrange(cv.w), rng.randrange(ymax)
        cv.set(x, y, rng.choice(STAR))
    for _ in range(max(4, count // 12)):  # parlak, artı biçimli yıldızlar
        x, y = rng.randrange(4, cv.w - 4), rng.randrange(3, int(ymax * 0.8))
        cv.set(x, y, "#FFFFFF")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            cv.set(x + dx, y + dy, "#8FB4EA")


def moon(cv, cx, cy, r):
    for y in range(cy - r - 6, cy + r + 7):
        for x in range(cx - r - 6, cx + r + 7):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if d2 <= r * r:
                sd = (x - (cx - r // 3)) ** 2 + (y - (cy + r // 3)) ** 2
                cv.set(x, y, MOON_SHADE if sd > r * r * 1.15 else MOON)
            elif d2 <= (r + 5) ** 2 and BAYER4[y % 4][x % 4] > 9 + (d2 ** 0.5 - r) * 2:
                cv.set(x, y, MOON_GLOW)
    for dx, dy in ((-2, -2), (2, 1), (-1, 3), (3, -3)):
        if r >= 8:
            cv.set(cx + dx, cy + dy, MOON_CRATER)
            cv.set(cx + dx + 1, cy + dy, MOON_CRATER)


def heights(W, s, peaks, slope, jit, rng):
    h = []
    noise = 0
    for x in range(W):
        best = 0.0
        for fx, ph in peaks:
            best = max(best, ph * s - abs(x - fx * W) * slope * s)
        noise = max(-2, min(2, noise + rng.choice([-1, 0, 0, 1])))
        h.append(max(0, int(best + noise * jit * 0.5)))
    return h


def mountains(cv, rng, s):
    tops = []
    for L in LAYERS:
        y0 = cv.h + int(L["base"] * s) if L["base"] < 0 else L["base"]
        h = heights(cv.w, s, L["peaks"], L["slope"], L["jit"], rng)
        top = [y0 - hv for hv in h]
        tops.append((top, y0))
        snow_line = int(L["snow"] * s)
        for x in range(cv.w):
            lit = x + 1 < cv.w and h[x] > h[x + 1]  # ay sağda: sağa bakan yüz aydınlık
            for y in range(top[x], cv.h):
                height_here = y0 - y
                depth = y - top[x]
                thr = (BAYER4[y % 4][x % 4] - 7.5) * 0.35
                in_snow = height_here + thr > snow_line - 1 and depth < max(4, int(10 * s))
                if in_snow:
                    col = L["snow_c"] if lit else L["snow_s"]
                else:
                    col = L["body"] if lit else L["shade"]
                    if (x * 5 + y * 3) % 13 == 0 and depth > 3:
                        col = L["shade"]
                cv.set(x, y, col)
    return tops


def avalanche(cv, rng, tops, s):
    """En yüksek ön tepenin sağ yüzünde aşağı akan kar bulutu."""
    top, y0 = tops[-1]
    px = max(range(cv.w), key=lambda x: y0 - top[x])
    length = int(30 * (0.8 + 0.2 * s))
    end_x = px
    for t in range(2, length):
        x = px + 2 + t
        if x >= cv.w - 2:
            break
        end_x = x
        surf = top[x]
        spread = 1 + t // 3
        for _ in range(3 + t // 4):
            dx = rng.randint(-1, 1)
            dy = rng.randint(0, spread)
            c = rng.choice(["#FFFFFF", "#FFFFFF", "#E4F1FF", "#C8DDF5"])
            cv.set(x + dx, surf - dy, c)
            if t > 10 and rng.random() < 0.5:
                cv.set(x + dx + 1, surf - dy, c)
        if t > 6 and rng.random() < 0.6:  # ince toz bulutu
            cv.set(x + rng.randint(-2, 2), surf - spread - rng.randint(1, 4), "#8FB4EA")
    # dibe yığılan kar
    for dx in range(-7, 8):
        x = end_x + dx
        hgt = max(0, 4 - abs(dx) // 2)
        for k in range(hgt):
            cv.set(x, top[min(max(x, 0), cv.w - 1)] - k - 1, "#FFFFFF" if k >= hgt - 1 or dx % 2 else "#DCEBFA")


def ground(cv, s):
    g = max(6, int(7 * s * 0.8))
    for y in range(cv.h - g, cv.h):
        for x in range(cv.w):
            cv.px[y][x] = "#0B1433" if y > cv.h - g else "#DCEBFA"
    return cv.h - g


def chain(cv, ground_y, n=5, x0=18, size=7, gap=9):
    y = ground_y - size - 1
    for i in range(n):
        x = x0 + i * (size + gap)
        last = i == n - 1
        if i < n - 1:  # bağlantı
            cv.rect(x + size, y + size // 2, gap, 1, BLOCK_LINE)
            cv.rect(x + size + 2, y + size // 2 - 1, gap - 4, 1, BLOCK_FILL)
        cv.rect(x, y, size, size, BLOCK_LINE)
        cv.rect(x + 1, y + 1, size - 2, size - 2, BLOCK_FILL)
        cv.rect(x + 1, y + 1, size - 2, 1, BLOCK_HI)
        cv.rect(x + 1, y + 1, 1, size - 2, BLOCK_HI)
        cv.rect(x + size - 2, y + 2, 1, size - 3, BLOCK_DARK)
        cv.rect(x + 2, y + size - 2, size - 3, 1, BLOCK_DARK)
        if last:  # son blok "parlıyor" (senin deploy'un)
            for dx, dy in ((-2, 3), (size + 1, 3), (3, -2), (3, size + 1)):
                cv.set(x + dx, y + dy, "#FFFFFF")


def scene(W, H, seed, layout):
    rng = random.Random(seed)
    s = H / 80.0
    cv = Canvas(W, H)
    sky(cv)
    stars(cv, rng, 70 if H < 100 else 150, int(H * 0.45))
    moon(cv, layout["moon_x"], layout["moon_y"], layout["moon_r"])
    tops = mountains(cv, rng, s)
    avalanche(cv, rng, tops, s)
    gy = ground(cv, s)
    chain(cv, gy)
    # başlık
    tx = layout["x"]
    cv.text(tx, layout["title_y"], "LEARN-AVALANCHE", scale=3, colors=TITLE_GRAD,
            shadow=TITLE_SHADOW, shadow_off=2)
    for i, line in enumerate(layout["tags"]):
        cv.text(tx, layout["tag_y"] + i * 11, line, scale=1, colors=TAG,
                shadow=TAG_SHADOW, shadow_off=1)
    return cv


# ------------------------------------------------------------------ çıktı
def save_png(cv, path, scale):
    img = Image.new("RGB", (cv.w, cv.h))
    img.putdata([hexc(c) for row in cv.px for c in row])
    img.resize((cv.w * scale, cv.h * scale), Image.NEAREST).save(path, optimize=True)


def save_svg(cv, path, scale):
    by_color = {}
    for y, row in enumerate(cv.px):
        x = 0
        while x < cv.w:
            c = row[x]
            x2 = x
            while x2 < cv.w and row[x2] == c:
                x2 += 1
            by_color.setdefault(c, []).append((x, y, x2 - x))
            x = x2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cv.w} {cv.h}" '
        f'width="{cv.w * scale}" height="{cv.h * scale}" shape-rendering="crispEdges" '
        f'role="img" aria-label="learn-avalanche: pixel-art mountains, moon, avalanche and chain blocks">'
    ]
    for c, runs in by_color.items():
        d = "".join(f"M{x} {y}h{w}v1h-{w}z" for x, y, w in runs)
        parts.append(f'<path fill="{c}" d="{d}"/>')
    parts.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(parts))


def main():
    os.makedirs(OUT, exist_ok=True)
    banner = scene(320, 80, seed=7, layout=dict(
        x=18, title_y=10, tag_y=37, moon_x=302, moon_y=15, moon_r=8,
        tags=["SOLIDITY / AVALANCHE / YOU WRITE THE CODE"]))
    save_svg(banner, os.path.join(OUT, "banner.svg"), 4)
    save_png(banner, os.path.join(OUT, "banner.png"), 4)

    social = scene(320, 160, seed=11, layout=dict(
        x=18, title_y=34, tag_y=66, moon_x=300, moon_y=34, moon_r=10,
        tags=["SOLIDITY / AVALANCHE / YOU WRITE THE CODE",
              "REMIX + CORE WALLET  /  TESTNET ONLY"]))
    save_png(social, os.path.join(OUT, "social-preview.png"), 4)
    print("yazıldı:", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
