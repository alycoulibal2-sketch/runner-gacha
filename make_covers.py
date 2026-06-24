#!/usr/bin/env python3
"""CrazyGames-compliant cover art for Runner Gacha — NO text/logo (their policy).
Hero composition of the game's real elements:
  cyan square character (with a friendly face) mid-jump,
  red rectangle obstacles, gold coins, space/nebula background.
Sizes: 1920x1080, 800x1200, 800x800.
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# palette from game source
NAVY_TOP = (10, 20, 50)
NAVY_BOT = (4, 7, 16)
CYAN     = (56, 189, 248)
CYAN_DK  = (20, 120, 210)
RED_OBST = (244, 63, 94)
GOLD     = (250, 204, 21)
PURPLE   = (124, 77, 255)
PINK     = (255, 107, 148)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgradient(w, h, top, bot):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        c = lerp(top, bot, (y / (h - 1)) ** 0.9)
        for x in range(w):
            px[x, y] = c
    return img


def radial_glow(radius, color, max_alpha=160):
    s = max(2, radius * 2)
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    steps = 50
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(max_alpha * (1 - i / steps) ** 1.7)
        d.ellipse([radius - r, radius - r, radius + r, radius + r], fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(radius * 0.05))


def nebula(img, blobs):
    for (x, y, r, col, a) in blobs:
        g = radial_glow(int(r), col, a)
        img.alpha_composite(g, (int(x - r), int(y - r)))


def add_stars(img, n, seed=1):
    random.seed(seed)
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for _ in range(n):
        x, y = random.randint(0, w), random.randint(0, h)
        r = random.choice([1, 1, 1, 2, 2, 3])
        a = random.randint(40, 210)
        col = random.choice([(255, 255, 255), CYAN, (200, 210, 255)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))
        # occasional sparkle cross
        if r == 3 and random.random() < 0.4:
            d.line([x - r * 2, y, x + r * 2, y], fill=(255, 255, 255, a // 2))
            d.line([x, y - r * 2, x, y + r * 2], fill=(255, 255, 255, a // 2))


def draw_ground(img, gy):
    w, h = img.size
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, gy, w, h], fill=(8, 12, 28, 220))
    d.line([0, gy, w, gy], fill=CYAN + (90,), width=max(2, h // 360))
    # faint reflected glow under the line
    g = Image.new("RGBA", (w, 60), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for i in range(60):
        gd.line([0, i, w, i], fill=CYAN + (int(28 * (1 - i / 60)),))
    img.alpha_composite(g, (0, gy))


def draw_obstacle(img, x, y, w, h):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # soft red glow
    g = radial_glow(int(max(w, h) * 0.9), RED_OBST, 70)
    img.alpha_composite(g, (int(x + w / 2 - max(w, h) * 0.9), int(y + h / 2 - max(w, h) * 0.9)))
    d.rectangle([x, y, x + w, y + h], fill=RED_OBST)
    d.rectangle([x, y, x + w, y + int(h * 0.16)], fill=lerp(RED_OBST, (255, 255, 255), 0.25))
    d.rectangle([x, y, x + max(2, int(w * 0.12)), y + h], fill=lerp(RED_OBST, (255, 255, 255), 0.12))
    img.alpha_composite(layer)


def draw_coin(img, cx, cy, r):
    g = radial_glow(int(r * 2.4), (250, 190, 0), 120)
    img.alpha_composite(g, (int(cx - r * 2.4), int(cy - r * 2.4)))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=lerp(GOLD, (255, 255, 255), 0.6),
              width=max(1, int(r * 0.14)))
    d.ellipse([cx - r * 0.5, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
              fill=lerp(GOLD, (255, 255, 255), 0.85))
    img.alpha_composite(layer)


def draw_hero(img, cx, cy, size, look=0.0):
    """Cyan square character (the player) with a friendly face + glow + speed trail.
    cx, cy = CENTER of the square. look = horizontal pupil bias (-1..1)."""
    # big soft glow
    gr = int(size * 1.7)
    img.alpha_composite(radial_glow(gr, CYAN, 150), (int(cx - gr), int(cy - gr)))

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = size
    x0, y0 = cx - s / 2, cy - s / 2

    # speed trail behind (left), receding squares
    for i, a in enumerate([70, 40, 20]):
        off = s * (0.45 + i * 0.5)
        sq = s * (1 - i * 0.12)
        d.rounded_rectangle([cx - off - sq / 2, cy - sq / 2, cx - off + sq / 2, cy + sq / 2],
                            radius=int(sq * 0.18), fill=CYAN + (a,))

    # body with vertical gradient + rounded corners
    body = Image.new("RGBA", (int(s), int(s)), (0, 0, 0, 0))
    bpx = body.load()
    for yy in range(int(s)):
        c = lerp(lerp(CYAN, (255, 255, 255), 0.18), CYAN_DK, yy / s)
        for xx in range(int(s)):
            bpx[xx, yy] = c + (255,)
    mask = Image.new("L", (int(s), int(s)), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.18), fill=255)
    layer.paste(body, (int(x0), int(y0)), mask)
    dd = ImageDraw.Draw(layer)
    # rim light
    dd.rounded_rectangle([x0, y0, x0 + s, y0 + s], radius=int(s * 0.18),
                         outline=(180, 240, 255, 180), width=max(2, int(s * 0.025)))
    # top-left gloss
    dd.rounded_rectangle([x0 + s * 0.10, y0 + s * 0.10, x0 + s * 0.42, y0 + s * 0.30],
                         radius=int(s * 0.08), fill=(255, 255, 255, 70))

    # face — two eyes + smile
    er = s * 0.135
    ey = y0 + s * 0.42
    pupil = er * 0.45
    for ex in (x0 + s * 0.34, x0 + s * 0.66):
        dd.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(255, 255, 255, 255))
        px = ex + look * er * 0.5
        dd.ellipse([px - pupil, ey - pupil * 0.7, px + pupil, ey + pupil * 1.1],
                   fill=(12, 22, 44, 255))
        dd.ellipse([px - pupil * 0.5, ey - pupil * 0.7, px - pupil * 0.05, ey - pupil * 0.2],
                   fill=(255, 255, 255, 230))
    # determined smile
    dd.arc([x0 + s * 0.36, y0 + s * 0.56, x0 + s * 0.64, y0 + s * 0.80],
           start=8, end=172, fill=(12, 22, 44, 230), width=max(2, int(s * 0.05)))

    img.alpha_composite(layer)


# ─── compositions ─────────────────────────────────────────────────────────────

def compose_landscape(w, h):
    bg = vgradient(w, h, NAVY_TOP, NAVY_BOT).convert("RGBA")
    nebula(bg, [(w * 0.30, h * 0.30, 560, PURPLE, 95),
                (w * 0.78, h * 0.35, 480, PINK, 80),
                (w * 0.55, h * 0.78, 420, CYAN, 55)])
    add_stars(bg, 220, seed=11)
    gy = int(h * 0.80)
    draw_ground(bg, gy)

    # background obstacles (depth)
    draw_obstacle(bg, int(w * 0.80), gy - int(h * 0.18), int(w * 0.030), int(h * 0.18))
    draw_obstacle(bg, int(w * 0.20), gy - int(h * 0.11), int(w * 0.024), int(h * 0.11))
    # hero obstacle being jumped
    oh = int(h * 0.28)
    draw_obstacle(bg, int(w * 0.58), gy - oh, int(w * 0.035), oh)

    # coin arc over the jump
    for cf, ya in [(0.40, 0.55), (0.46, 0.45), (0.52, 0.40), (0.58, 0.43), (0.64, 0.52)]:
        draw_coin(bg, int(w * cf), int(h * ya), int(min(w, h) * 0.026))

    # hero character mid-jump, large, clearing the obstacle
    hs = int(min(w, h) * 0.20)
    draw_hero(bg, int(w * 0.46), int(gy - oh - hs * 0.30), hs, look=0.6)
    return bg.convert("RGB")


def compose_portrait(w, h):
    bg = vgradient(w, h, NAVY_TOP, NAVY_BOT).convert("RGBA")
    nebula(bg, [(w * 0.50, h * 0.28, 380, PURPLE, 100),
                (w * 0.20, h * 0.55, 300, PINK, 80),
                (w * 0.80, h * 0.62, 300, CYAN, 60)])
    add_stars(bg, 150, seed=23)
    gy = int(h * 0.84)
    draw_ground(bg, gy)

    draw_obstacle(bg, int(w * 0.66), gy - int(h * 0.16), int(w * 0.08), int(h * 0.16))
    oh = int(h * 0.13)
    draw_obstacle(bg, int(w * 0.18), gy - oh, int(w * 0.07), oh)

    # coins rising column
    for cf, ya in [(0.40, 0.70), (0.46, 0.60), (0.50, 0.50), (0.52, 0.40), (0.51, 0.30)]:
        draw_coin(bg, int(w * cf), int(h * ya), int(min(w, h) * 0.034))

    hs = int(min(w, h) * 0.34)
    draw_hero(bg, int(w * 0.44), int(h * 0.55), hs, look=0.3)
    return bg.convert("RGB")


def compose_square(w, h):
    bg = vgradient(w, h, NAVY_TOP, NAVY_BOT).convert("RGBA")
    nebula(bg, [(w * 0.50, h * 0.40, 360, PURPLE, 105),
                (w * 0.22, h * 0.30, 250, CYAN, 70),
                (w * 0.80, h * 0.66, 260, PINK, 80)])
    add_stars(bg, 120, seed=31)
    gy = int(h * 0.84)
    draw_ground(bg, gy)

    draw_obstacle(bg, int(w * 0.74), gy - int(h * 0.18), int(w * 0.085), int(h * 0.18))
    oh = int(h * 0.12)
    draw_obstacle(bg, int(w * 0.14), gy - oh, int(w * 0.075), oh)

    # coin arc around hero
    for cf, ya in [(0.28, 0.50), (0.40, 0.40), (0.55, 0.36), (0.70, 0.42), (0.78, 0.55)]:
        draw_coin(bg, int(w * cf), int(h * ya), int(min(w, h) * 0.036))

    hs = int(min(w, h) * 0.36)
    draw_hero(bg, int(w * 0.48), int(h * 0.52), hs, look=0.0)
    return bg.convert("RGB")


jobs = [
    ("cover_landscape_1920x1080.png", 1920, 1080, compose_landscape),
    ("cover_portrait_800x1200.png",    800, 1200, compose_portrait),
    ("cover_square_800x800.png",       800,  800, compose_square),
]
for name, w, h, fn in jobs:
    img = fn(w, h)
    img.save(f"/home/user/runner-gacha/{name}", "PNG")
    # also JPG (smaller, universally accepted)
    img.save(f"/home/user/runner-gacha/{name.replace('.png', '.jpg')}", "JPEG", quality=92)
    print("wrote", name, img.size)
print("done")
