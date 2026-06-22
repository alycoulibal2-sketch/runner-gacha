#!/usr/bin/env python3
"""Generate CrazyGames cover images for Runner Gacha.
Sizes: Landscape 1920x1080, Portrait 800x1200, Square 800x800.
Matches the in-game art: deep-space navy bg, multicolor wordmark,
cyan jumping runner, gold coins, dark obstacles, gacha capsule.
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
TITLE_FONT = f"{FONT_DIR}/BigShoulders-Bold.ttf"
SUB_FONT   = f"{FONT_DIR}/Outfit-Bold.ttf"

# palette (from index.html)
NAVY_TOP   = (7, 16, 41)      # #071029
NAVY_MID   = (12, 20, 48)     # #0c1430
NAVY_BOT   = (18, 12, 46)     # purple-ish floor
ORANGE     = (255, 122, 89)   # #ff7a59
AMBER      = (255, 184, 107)  # #ffb86b
PURPLE     = (124, 77, 255)   # #7c4dff
PINK       = (255, 107, 148)  # #ff6b94
BLUE       = (56, 189, 248)   # #38bdf8
CYAN       = (56, 189, 248)
GOLD       = (250, 204, 21)   # #facc15
GOLD_HI    = (255, 240, 170)
OBST       = (55, 65, 81)     # #374151
OBST_HI    = (80, 92, 112)

WORDMARK_STOPS = [ORANGE, AMBER, PURPLE, PINK, BLUE]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgradient(w, h, top, mid, bot):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        if t < 0.5:
            c = lerp(top, mid, t / 0.5)
        else:
            c = lerp(mid, bot, (t - 0.5) / 0.5)
        for x in range(w):
            px[x, y] = c
    return img


def hgrad_strip(w, h, stops):
    """horizontal multi-stop gradient strip as RGBA."""
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


def radial_glow(radius, color, max_alpha=180):
    """soft radial glow RGBA, transparent edge."""
    s = radius * 2
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    steps = 60
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(max_alpha * (1 - i / steps) ** 1.6)
        d.ellipse([radius - r, radius - r, radius + r, radius + r],
                  fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(radius * 0.06))


def gradient_text(text, font, stops, kerning=0):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = int(th * 0.5)
    W, H = tw + pad * 2, th + pad * 2
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.text((pad - bbox[0], pad - bbox[1]), text, font=font, fill=255)
    grad = hgrad_strip(W, H, stops).convert("RGBA")
    grad.putalpha(mask)
    return grad


def add_stars(img, n, seed=1):
    random.seed(seed)
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for _ in range(n):
        x, y = random.randint(0, w), random.randint(0, int(h * 0.8))
        r = random.choice([1, 1, 1, 2, 2, 3])
        a = random.randint(40, 170)
        col = random.choice([(255, 255, 255), BLUE, (200, 210, 255)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))


def draw_coin(img, cx, cy, r):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    glow = radial_glow(int(r * 2.2), GOLD, 110)
    img.alpha_composite(glow, (int(cx - r * 2.2), int(cy - r * 2.2)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD_HI, width=max(1, int(r * 0.12)))
    # inner shine
    d.ellipse([cx - r * 0.45, cy - r * 0.55, cx + r * 0.15, cy + r * 0.05], fill=GOLD_HI)
    # star spark
    sk = r * 0.5
    d.line([cx - sk, cy, cx + sk, cy], fill=(255, 255, 255, 200), width=max(1, int(r * 0.10)))
    d.line([cx, cy - sk, cx, cy + sk], fill=(255, 255, 255, 200), width=max(1, int(r * 0.10)))
    img.alpha_composite(layer)


def draw_obstacle(d, x, y, w, h):
    rad = int(min(w, h) * 0.18)
    d.rounded_rectangle([x, y, x + w, y + h], radius=rad, fill=OBST)
    d.rounded_rectangle([x, y, x + w, y + h * 0.25], radius=rad, fill=OBST_HI)


def draw_runner(img, cx, cy, s, tilt=-12):
    """cyan rounded runner mid-jump, with glow + trail."""
    # glow
    glow = radial_glow(int(s * 1.6), CYAN, 150)
    img.alpha_composite(glow, (int(cx - s * 1.6), int(cy - s * 1.6)))
    char = Image.new("RGBA", (int(s * 2.4), int(s * 2.8)), (0, 0, 0, 0))
    d = ImageDraw.Draw(char)
    w, h = char.size
    bw, bh = s * 1.15, s * 1.5
    bx, by = (w - bw) / 2, (h - bh) / 2
    # body gradient (cyan -> deeper blue)
    body = Image.new("RGBA", (int(bw), int(bh)), (0, 0, 0, 0))
    bpx = body.load()
    for yy in range(int(bh)):
        c = lerp(BLUE, (24, 110, 200), yy / bh)
        for xx in range(int(bw)):
            bpx[xx, yy] = c + (255,)
    bmask = Image.new("L", (int(bw), int(bh)), 0)
    ImageDraw.Draw(bmask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=int(bw * 0.42), fill=255)
    char.paste(body, (int(bx), int(by)), bmask)
    # eyes
    er = s * 0.13
    ey = by + bh * 0.34
    for ex in (bx + bw * 0.34, bx + bw * 0.64):
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(255, 255, 255, 255))
        d.ellipse([ex - er * 0.45, ey - er * 0.2, ex + er * 0.55, ey + er * 0.7], fill=(10, 20, 40, 255))
    # little smile
    d.arc([bx + bw * 0.36, by + bh * 0.46, bx + bw * 0.64, by + bh * 0.66],
          start=10, end=170, fill=(10, 20, 40, 220), width=max(2, int(s * 0.05)))
    # legs (running)
    legc = (24, 110, 200, 255)
    lw = max(3, int(s * 0.16))
    d.line([bx + bw * 0.35, by + bh, bx + bw * 0.2, by + bh + s * 0.5], fill=legc, width=lw)
    d.line([bx + bw * 0.65, by + bh, bx + bw * 0.82, by + bh + s * 0.32], fill=legc, width=lw)
    char = char.rotate(tilt, resample=Image.BICUBIC, expand=True)
    # motion trail BEHIND the runner (down-left, opposite travel direction), faint
    for i, a in enumerate([22, 42]):
        idx = 1 - i  # draw fainter/farther first
        amt = [22, 42][idx]
        t = char.copy()
        alpha = t.split()[3].point(lambda p: int(p * amt / 255))
        t.putalpha(alpha)
        off = s * (0.55 + idx * 0.45)
        img.alpha_composite(t, (int(cx - t.width / 2 - off), int(cy - t.height / 2 + off * 0.55)))
    img.alpha_composite(char, (int(cx - char.width / 2), int(cy - char.height / 2)))


def draw_capsule(img, cx, cy, r, angle=-20):
    """gacha capsule: top pink, bottom white, with star."""
    cap = Image.new("RGBA", (int(r * 2.4), int(r * 2.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(cap)
    w = cap.width
    cc = w / 2
    glow = radial_glow(int(r * 1.5), PINK, 120)
    img.alpha_composite(glow, (int(cx - r * 1.5), int(cy - r * 1.5)))
    box = [cc - r, cc - r, cc + r, cc + r]
    d.pieslice(box, 180, 360, fill=PINK)            # top half
    d.pieslice(box, 0, 180, fill=(238, 240, 248))   # bottom half
    d.line([cc - r, cc, cc + r, cc], fill=(255, 255, 255), width=max(2, int(r * 0.10)))
    d.ellipse(box, outline=(255, 255, 255, 120), width=max(1, int(r * 0.06)))
    # star
    sr = r * 0.42
    pts = []
    for k in range(10):
        ang = math.pi / 2 + k * math.pi / 5
        rr = sr if k % 2 == 0 else sr * 0.42
        pts.append((cc + rr * math.cos(ang), cc - r * 0.42 - rr * math.sin(ang)))
    d.polygon(pts, fill=GOLD)
    cap = cap.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(cap, (int(cx - cap.width / 2), int(cy - cap.height / 2)))


def nebula(img, blobs):
    for (x, y, r, col, a) in blobs:
        g = radial_glow(r, col, a)
        img.alpha_composite(g, (int(x - r), int(y - r)))


def compose(w, h, layout):
    bg = vgradient(w, h, NAVY_TOP, NAVY_MID, NAVY_BOT).convert("RGBA")
    nebula(bg, layout["nebula"])
    add_stars(bg, layout["stars"], seed=layout["seed"])

    # ground glow line
    gy = int(h * layout["ground"])
    gd = ImageDraw.Draw(bg, "RGBA")
    gd.line([0, gy, w, gy], fill=(120, 140, 200, 50), width=max(1, int(h * 0.004)))

    # obstacles on the ground
    for (ox, ow, oh) in layout["obstacles"]:
        x = int(ox * w)
        ww = int(ow * w)
        hh = int(oh * h)
        draw_obstacle(gd, x, gy - hh, ww, hh)

    # coins arc
    for (cxf, cyf, rf) in layout["coins"]:
        draw_coin(bg, cxf * w, cyf * h, rf * min(w, h))

    # capsule
    if layout.get("capsule"):
        cx, cy, rf = layout["capsule"]
        draw_capsule(bg, cx * w, cy * h, rf * min(w, h))

    # runner
    rx, ry, rs = layout["runner"]
    draw_runner(bg, rx * w, ry * h, rs * min(w, h))

    # title wordmark
    fsize = layout["title_size"]
    tf = ImageFont.truetype(TITLE_FONT, fsize)
    if layout.get("stacked"):
        l1 = gradient_text("RUNNER", tf, WORDMARK_STOPS)
        l2 = gradient_text("GACHA", tf, WORDMARK_STOPS)
        scale = (w * layout["title_w"]) / max(l1.width, l2.width)
        l1 = l1.resize((int(l1.width * scale), int(l1.height * scale)), Image.LANCZOS)
        l2 = l2.resize((int(l2.width * scale), int(l2.height * scale)), Image.LANCZOS)
        ty = int(h * layout["title_y"])
        for ln in (l1, l2):
            sh = ln.filter(ImageFilter.GaussianBlur(6))
            bg.alpha_composite(sh, ((w - ln.width) // 2 + 3, ty + 5))
            bg.alpha_composite(ln, ((w - ln.width) // 2, ty))
            ty += int(ln.height * 0.92)
        last_y = ty
    else:
        wm = gradient_text("RUNNER GACHA", tf, WORDMARK_STOPS)
        scale = (w * layout["title_w"]) / wm.width
        wm = wm.resize((int(wm.width * scale), int(wm.height * scale)), Image.LANCZOS)
        tx = (w - wm.width) // 2
        ty = int(h * layout["title_y"])
        sh = wm.filter(ImageFilter.GaussianBlur(8))
        bg.alpha_composite(sh, (tx + 4, ty + 6))
        bg.alpha_composite(wm, (tx, ty))
        last_y = ty + wm.height

    # subtitle
    if layout.get("subtitle"):
        sf = ImageFont.truetype(SUB_FONT, layout["sub_size"])
        sub = "JUMP  ·  COLLECT COINS  ·  UNLOCK RARE SKINS"
        sd = ImageDraw.Draw(bg)
        bb = sd.textbbox((0, 0), sub, font=sf)
        sw = bb[2] - bb[0]
        sd.text(((w - sw) // 2, last_y + layout["sub_gap"]), sub, font=sf,
                fill=(180, 195, 230, 235))

    return bg.convert("RGB")


# ---- layouts per format ----
landscape = dict(
    seed=7, stars=140, ground=0.86, title_w=0.62, title_y=0.10, title_size=300,
    stacked=False, subtitle=True, sub_size=34, sub_gap=18,
    nebula=[(1500, 250, 520, PURPLE, 90), (350, 750, 480, ORANGE, 70),
            (1700, 850, 420, PINK, 70)],
    obstacles=[(0.12, 0.035, 0.10), (0.72, 0.045, 0.16), (0.88, 0.03, 0.07)],
    coins=[(0.40, 0.50, 0.022), (0.47, 0.42, 0.022), (0.54, 0.38, 0.022),
           (0.61, 0.42, 0.022), (0.68, 0.50, 0.022)],
    capsule=(0.80, 0.42, 0.072),
    runner=(0.33, 0.62, 0.12),
)

portrait = dict(
    seed=3, stars=110, ground=0.88, title_w=0.80, title_y=0.06, title_size=300,
    stacked=True, subtitle=True, sub_size=26, sub_gap=16,
    nebula=[(620, 300, 360, PURPLE, 95), (180, 650, 340, ORANGE, 75),
            (650, 950, 320, PINK, 75)],
    obstacles=[(0.10, 0.07, 0.07), (0.74, 0.10, 0.10)],
    coins=[(0.30, 0.66, 0.030), (0.42, 0.60, 0.030), (0.54, 0.58, 0.030),
           (0.66, 0.62, 0.030)],
    capsule=(0.80, 0.64, 0.078),
    runner=(0.34, 0.76, 0.14),
)

square = dict(
    seed=5, stars=90, ground=0.87, title_w=0.78, title_y=0.07, title_size=300,
    stacked=True, subtitle=False, sub_size=22, sub_gap=12,
    nebula=[(560, 230, 320, PURPLE, 95), (180, 560, 300, ORANGE, 75),
            (620, 640, 280, PINK, 70)],
    obstacles=[(0.12, 0.07, 0.09), (0.76, 0.09, 0.13)],
    coins=[(0.34, 0.62, 0.034), (0.46, 0.56, 0.034), (0.58, 0.58, 0.034)],
    capsule=(0.72, 0.46, 0.090),
    runner=(0.34, 0.70, 0.155),
)

jobs = [("cover_landscape_1920x1080.png", 1920, 1080, landscape),
        ("cover_portrait_800x1200.png", 800, 1200, portrait),
        ("cover_square_800x800.png", 800, 800, square)]

for name, w, h, layout in jobs:
    out = compose(w, h, layout)
    out.save(f"/home/user/runner-gacha/{name}", "PNG")
    print("wrote", name, out.size)
print("done")
