#!/usr/bin/env python3
"""Generate CrazyGames cover images for Runner Gacha.
Faithful to the actual game:
  - Player: cyan square (#38bdf8)
  - Obstacles: red/pink rectangles (#f43f5e) sitting on the ground
  - Coins: gold circles (#facc15)
  - Background: dark navy with twinkling stars
  - Ground: thin white line at ~87% height
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
TITLE_FONT = f"{FONT_DIR}/BigShoulders-Bold.ttf"
SUB_FONT   = f"{FONT_DIR}/Outfit-Bold.ttf"

# colours from game source
NAVY_TOP  = (7,  16, 41)     # #071029
NAVY_MID  = (12, 20, 48)     # #0c1430
NAVY_BOT  = (5,  9,  19)     # #050913
CYAN      = (56, 189, 248)   # #38bdf8  ← player default
RED_OBST  = (244, 63,  94)   # #f43f5e  ← obstacle default
GOLD      = (250, 204, 21)   # #facc15  ← coins
ORANGE    = (255, 122, 89)   # #ff7a59
AMBER     = (255, 184, 107)  # #ffb86b
PURPLE    = (124, 77, 255)   # #7c4dff
PINK      = (255, 107, 148)  # #ff6b94
BLUE      = (56,  189, 248)  # #38bdf8
WORDMARK  = [ORANGE, AMBER, PURPLE, PINK, BLUE, ORANGE]


# ─── helpers ──────────────────────────────────────────────────────────────────

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgradient(w, h, top, bot):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        c = lerp(top, bot, y / (h - 1))
        for x in range(w):
            px[x, y] = c
    return img


def hgrad_strip(w, h, stops):
    img = Image.new("RGB", (w, h))
    px = img.load()
    n = len(stops) - 1
    for x in range(w):
        t = x / (w - 1) * n
        i = min(int(t), n - 1)
        c = lerp(stops[i], stops[i + 1], t - i)
        for y in range(h):
            px[x, y] = c
    return img


def radial_glow(radius, color, max_alpha=160):
    s = radius * 2
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    steps = 48
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(max_alpha * (1 - i / steps) ** 1.8)
        d.ellipse([radius - r, radius - r, radius + r, radius + r],
                  fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(radius * 0.05))


def gradient_text(text, font, stops):
    bb = font.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = int(th * 0.45)
    W, H = tw + pad * 2, th + pad * 2
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).text((pad - bb[0], pad - bb[1]), text, font=font, fill=255)
    grad = hgrad_strip(W, H, stops).convert("RGBA")
    grad.putalpha(mask)
    return grad


def add_stars(img, n, seed=1):
    random.seed(seed)
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for _ in range(n):
        x, y = random.randint(0, w), random.randint(0, int(h * 0.75))
        r = random.choice([1, 1, 1, 2, 2, 3])
        a = random.randint(50, 200)
        col = random.choice([(255, 255, 255), BLUE, (200, 210, 255)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))


# ─── game element drawers ─────────────────────────────────────────────────────

def draw_player_square(img, x, y, size, glow_r=None):
    """Cyan square, mid-jump with motion lines behind it."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # glow
    gr = glow_r or int(size * 1.4)
    g = radial_glow(gr, CYAN, 140)
    img.alpha_composite(g, (int(x + size // 2 - gr), int(y + size // 2 - gr)))
    # subtle trailing streak lines (horizontal, left of player)
    streak_col = CYAN + (40,)
    for k, (llen, ly_off, thick) in enumerate([(size * 2.8, 0.28, max(1, size // 10)),
                                                (size * 1.8, 0.60, max(1, size // 12)),
                                                (size * 1.2, 0.80, max(1, size // 14))]):
        lx = int(x - llen)
        ly = int(y + size * ly_off)
        d.line([lx, ly, int(x) - 2, ly], fill=streak_col, width=thick)
    # the square itself
    d.rectangle([x, y, x + size, y + size], fill=CYAN)
    # bright top-left highlight
    hi = lerp(CYAN, (255, 255, 255), 0.55)
    d.rectangle([x, y, x + size * 0.38, y + size * 0.38], fill=hi)
    img.alpha_composite(layer)


def draw_obstacle(img, x, y, w, h):
    """Red rectangle obstacle with a brighter top edge."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([x, y, x + w, y + h], fill=RED_OBST)
    top_hi = lerp(RED_OBST, (255, 255, 255), 0.22)
    d.rectangle([x, y, x + w, y + int(h * 0.18)], fill=top_hi)
    img.alpha_composite(layer)


def draw_coin(img, cx, cy, r):
    """Gold circle coin with glow."""
    g = radial_glow(int(r * 2.6), (250, 180, 0), 110)
    img.alpha_composite(g, (int(cx - r * 2.6), int(cy - r * 2.6)))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    # shine
    hi = lerp(GOLD, (255, 255, 255), 0.7)
    d.ellipse([cx - r * 0.48, cy - r * 0.52, cx - r * 0.05, cy + r * 0.08], fill=hi)
    img.alpha_composite(layer)


# ─── nebula / atmosphere ─────────────────────────────────────────────────────

def nebula(img, blobs):
    for (x, y, r, col, a) in blobs:
        g = radial_glow(r, col, a)
        img.alpha_composite(g, (int(x - r), int(y - r)))


# ─── title wordmark ───────────────────────────────────────────────────────────

def place_title(bg, text_lines, fsize, title_w_frac, title_y_frac):
    """Draw wordmark (one or two lines). Returns bottom y of last line."""
    w, h = bg.size
    tf = ImageFont.truetype(TITLE_FONT, fsize)
    imgs = [gradient_text(ln, tf, WORDMARK) for ln in text_lines]
    # scale so widest line fits title_w_frac of canvas
    max_w = max(im.width for im in imgs)
    scale = (w * title_w_frac) / max_w
    imgs = [im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
            for im in imgs]
    y = int(h * title_y_frac)
    for im in imgs:
        sx = (w - im.width) // 2
        sh = im.filter(ImageFilter.GaussianBlur(8))
        bg.alpha_composite(sh, (sx + 4, y + 6))
        bg.alpha_composite(im, (sx, y))
        y += int(im.height * 0.90)
    return y


def place_subtitle(bg, text, fsize, y):
    w = bg.size[0]
    sf = ImageFont.truetype(SUB_FONT, fsize)
    d = ImageDraw.Draw(bg)
    bb = d.textbbox((0, 0), text, font=sf)
    sw = bb[2] - bb[0]
    d.text(((w - sw) // 2, y), text, font=sf, fill=(170, 185, 225, 220))


# ─── compose ─────────────────────────────────────────────────────────────────

def compose_landscape(w, h):
    """1920×1080 landscape banner."""
    bg = vgradient(w, h, NAVY_TOP, NAVY_BOT).convert("RGBA")
    nebula(bg, [
        (w * 0.72, h * 0.25, 480, PURPLE, 80),
        (w * 0.18, h * 0.65, 420, (255, 80, 60), 65),
        (w * 0.88, h * 0.70, 360, PINK, 60),
    ])
    add_stars(bg, 180, seed=7)

    gy = int(h * 0.82)  # ground y
    d = ImageDraw.Draw(bg, "RGBA")
    # ground line
    d.line([0, gy, w, gy], fill=(200, 220, 255, 55), width=3)
    d.rectangle([0, gy + 1, w, h], fill=(8, 12, 30, 200))

    # ── title (left third) ──
    title_bottom = place_title(bg, ["RUNNER GACHA"], fsize=200,
                               title_w_frac=0.43, title_y_frac=0.09)
    place_subtitle(bg, "JUMP  ·  COLLECT COINS  ·  UNLOCK RARE SKINS",
                   fsize=30, y=title_bottom + 14)

    # ── scene (right 55%) ──
    # obstacle 1 - tall, right side
    ox1 = int(w * 0.68); oh1 = int(h * 0.30)
    draw_obstacle(bg, ox1, gy - oh1, int(w * 0.032), oh1)
    # obstacle 2 - medium, far right
    ox2 = int(w * 0.83); oh2 = int(h * 0.18)
    draw_obstacle(bg, ox2, gy - oh2, int(w * 0.028), oh2)
    # obstacle 3 - small stump left of scene
    ox3 = int(w * 0.56); oh3 = int(h * 0.10)
    draw_obstacle(bg, ox3, gy - oh3, int(w * 0.022), oh3)

    # coins arc over the tall obstacle
    for k, (cf, ya) in enumerate([
        (0.58, 0.60), (0.62, 0.52), (0.66, 0.47), (0.70, 0.52), (0.74, 0.60)
    ]):
        draw_coin(bg, int(w * cf), int(h * ya), int(min(w, h) * 0.022))

    # player square mid-jump clearing the tall obstacle
    ps = int(min(w, h) * 0.095)  # player size
    px = int(w * 0.60); py = int(gy - oh1 - ps * 1.1)
    draw_player_square(bg, px, py, ps)

    return bg.convert("RGB")


def compose_portrait(w, h):
    """800×1200 portrait."""
    bg = vgradient(w, h, NAVY_TOP, NAVY_BOT).convert("RGBA")
    nebula(bg, [
        (w * 0.65, h * 0.18, 320, PURPLE, 85),
        (w * 0.20, h * 0.45, 280, (255, 80, 60), 70),
        (w * 0.75, h * 0.60, 260, PINK, 65),
    ])
    add_stars(bg, 130, seed=3)

    gy = int(h * 0.80)
    d = ImageDraw.Draw(bg, "RGBA")
    d.line([0, gy, w, gy], fill=(200, 220, 255, 50), width=2)
    d.rectangle([0, gy + 1, w, h], fill=(8, 12, 30, 200))

    # title — stacked, top
    title_bottom = place_title(bg, ["RUNNER", "GACHA"], fsize=240,
                               title_w_frac=0.82, title_y_frac=0.04)
    place_subtitle(bg, "JUMP · COLLECT · UNLOCK",
                   fsize=26, y=title_bottom + 10)

    # scene centred below title
    # tall obstacle
    oh1 = int(h * 0.24)
    ox1 = int(w * 0.60)
    draw_obstacle(bg, ox1, gy - oh1, int(w * 0.09), oh1)
    # small stump left
    oh2 = int(h * 0.10)
    draw_obstacle(bg, int(w * 0.15), gy - oh2, int(w * 0.07), oh2)

    # coins arc
    for cf, ya in [(0.30, 0.66), (0.42, 0.60), (0.54, 0.57), (0.66, 0.60)]:
        draw_coin(bg, int(w * cf), int(h * ya), int(min(w, h) * 0.030))

    # player mid-jump
    ps = int(min(w, h) * 0.11)
    px = int(w * 0.40); py = int(gy - oh1 - ps * 1.25)
    draw_player_square(bg, px, py, ps)

    return bg.convert("RGB")


def compose_square(w, h):
    """800×800 square."""
    bg = vgradient(w, h, NAVY_TOP, NAVY_BOT).convert("RGBA")
    nebula(bg, [
        (w * 0.70, h * 0.22, 300, PURPLE, 88),
        (w * 0.18, h * 0.55, 260, (255, 80, 60), 70),
        (w * 0.80, h * 0.68, 240, PINK, 65),
    ])
    add_stars(bg, 100, seed=5)

    gy = int(h * 0.87)
    d = ImageDraw.Draw(bg, "RGBA")
    d.line([0, gy, w, gy], fill=(200, 220, 255, 50), width=2)
    d.rectangle([0, gy + 1, w, h], fill=(8, 12, 30, 200))

    # title stacked — compact so it ends well above the ground scene
    title_bottom = place_title(bg, ["RUNNER", "GACHA"], fsize=190,
                               title_w_frac=0.76, title_y_frac=0.04)

    # tall obstacle — shorter so player clears text
    oh1 = int(h * 0.22)
    ox1 = int(w * 0.62)
    draw_obstacle(bg, ox1, gy - oh1, int(w * 0.09), oh1)
    # small stump
    oh2 = int(h * 0.09)
    draw_obstacle(bg, int(w * 0.16), gy - oh2, int(w * 0.08), oh2)

    # coins below the title wordmark
    for cf, ya in [(0.32, 0.73), (0.44, 0.67), (0.56, 0.64), (0.68, 0.68)]:
        draw_coin(bg, int(w * cf), int(h * ya), int(min(w, h) * 0.033))

    # player mid-jump — well below the title
    ps = int(min(w, h) * 0.105)
    px = int(w * 0.40); py = int(gy - oh1 - ps * 1.15)
    draw_player_square(bg, px, py, ps)

    return bg.convert("RGB")


# ─── render ──────────────────────────────────────────────────────────────────

jobs = [
    ("cover_landscape_1920x1080.png", 1920, 1080, compose_landscape),
    ("cover_portrait_800x1200.png",    800, 1200, compose_portrait),
    ("cover_square_800x800.png",       800,  800, compose_square),
]

for name, w, h, fn in jobs:
    img = fn(w, h)
    img.save(f"/home/user/runner-gacha/{name}", "PNG")
    print("wrote", name, img.size)

print("done")
