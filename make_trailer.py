#!/usr/bin/env python3
"""Render a REAL gameplay trailer for Runner Gacha (no AI, pixel-accurate).
Simulates the actual mechanic: cyan square runs, auto-jumps red walls,
collects gold coins, score counts up. Outputs MP4 via ffmpeg.
Formats: landscape 1920x1080 and portrait 1080x1920.
"""
import os, math, random, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
SCORE_FONT = f"{FONT_DIR}/Outfit-Bold.ttf"
BIG_FONT   = f"{FONT_DIR}/BigShoulders-Bold.ttf"

NAVY_TOP = (10, 20, 50)
NAVY_BOT = (4, 7, 16)
CYAN     = (56, 189, 248)
CYAN_DK  = (20, 120, 210)
RED_OBST = (244, 63, 94)
GOLD     = (250, 204, 21)
PURPLE   = (124, 77, 255)
PINK     = (255, 107, 148)
FPS      = 30


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
    s = max(2, int(radius) * 2)
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    steps = 46
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(max_alpha * (1 - i / steps) ** 1.7)
        d.ellipse([radius - r, radius - r, radius + r, radius + r], fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(radius * 0.05))


def make_coin_sprite(r):
    pad = int(r * 2.6)
    img = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
    glow = radial_glow(int(r * 2.4), (250, 190, 0), 130)
    img.alpha_composite(glow, (pad - int(r * 2.4), pad - int(r * 2.4)))
    d = ImageDraw.Draw(img)
    cx = cy = pad
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=lerp(GOLD, (255, 255, 255), 0.6),
              width=max(1, int(r * 0.14)))
    d.ellipse([cx - r * 0.5, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
              fill=lerp(GOLD, (255, 255, 255), 0.85))
    return img, pad


def make_player_sprite(size):
    """Cyan rounded square with friendly face + glow. Returns (img, pad) centered."""
    s = size
    gr = int(s * 1.6)
    pad = gr
    img = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
    img.alpha_composite(radial_glow(gr, CYAN, 150), (pad - gr, pad - gr))
    cx = cy = pad
    x0, y0 = cx - s / 2, cy - s / 2
    body = Image.new("RGBA", (int(s), int(s)), (0, 0, 0, 0))
    bpx = body.load()
    for yy in range(int(s)):
        c = lerp(lerp(CYAN, (255, 255, 255), 0.18), CYAN_DK, yy / s)
        for xx in range(int(s)):
            bpx[xx, yy] = c + (255,)
    mask = Image.new("L", (int(s), int(s)), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.18), fill=255)
    img.paste(body, (int(x0), int(y0)), mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + s, y0 + s], radius=int(s * 0.18),
                        outline=(180, 240, 255, 180), width=max(2, int(s * 0.025)))
    d.rounded_rectangle([x0 + s * 0.10, y0 + s * 0.10, x0 + s * 0.42, y0 + s * 0.30],
                        radius=int(s * 0.08), fill=(255, 255, 255, 70))
    er = s * 0.135; ey = y0 + s * 0.42; pupil = er * 0.45
    for ex in (x0 + s * 0.34, x0 + s * 0.66):
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(255, 255, 255, 255))
        d.ellipse([ex - pupil, ey - pupil * 0.7, ex + pupil, ey + pupil * 1.1], fill=(12, 22, 44, 255))
        d.ellipse([ex - pupil * 0.5, ey - pupil * 0.7, ex - pupil * 0.05, ey - pupil * 0.2],
                  fill=(255, 255, 255, 230))
    d.arc([x0 + s * 0.36, y0 + s * 0.56, x0 + s * 0.64, y0 + s * 0.80],
          start=8, end=172, fill=(12, 22, 44, 230), width=max(2, int(s * 0.05)))
    return img, pad


def build_background(w, h, gy, seed=11):
    bg = vgradient(w, h, NAVY_TOP, NAVY_BOT).convert("RGBA")
    for (xf, yf, r, col, a) in [(0.30, 0.30, w*0.32, PURPLE, 95),
                                 (0.78, 0.32, w*0.26, PINK, 80),
                                 (0.55, 0.72, w*0.24, CYAN, 50)]:
        g = radial_glow(int(r), col, a)
        bg.alpha_composite(g, (int(w*xf - r), int(h*yf - r)))
    random.seed(seed)
    d = ImageDraw.Draw(bg, "RGBA")
    stars = []
    for _ in range(int(w*h/9000)):
        x, y = random.randint(0, w), random.randint(0, gy)
        r = random.choice([1, 1, 1, 2, 2, 3]); a = random.randint(40, 210)
        col = random.choice([(255,255,255), CYAN, (200,210,255)])
        d.ellipse([x-r, y-r, x+r, y+r], fill=col+(a,))
        stars.append((x, y, r))
    # ground
    d.rectangle([0, gy, w, h], fill=(8, 12, 28, 230))
    d.line([0, gy, w, gy], fill=CYAN + (110,), width=max(2, h // 360))
    gl = Image.new("RGBA", (w, 70), (0, 0, 0, 0))
    gld = ImageDraw.Draw(gl)
    for i in range(70):
        gld.line([0, i, w, i], fill=CYAN + (int(30 * (1 - i / 70)),))
    bg.alpha_composite(gl, (0, gy))
    return bg


def render(w, h, out_path, seconds=12, seed=11):
    gy = int(h * 0.82)
    bg = build_background(w, h, gy, seed)

    # sprites
    P_SIZE = int(min(w, h) * (0.16 if w > h else 0.20))
    p_sprite, p_pad = make_player_sprite(P_SIZE)
    coin_r = int(min(w, h) * 0.024)
    coin_sprite, coin_pad = make_coin_sprite(coin_r)
    score_font = ImageFont.truetype(SCORE_FONT, int(min(w, h) * 0.055))
    label_font = ImageFont.truetype(SCORE_FONT, int(min(w, h) * 0.026))

    # physics (px/frame @30fps)
    player_x = int(w * (0.20 if w > h else 0.26))   # left side, fixed
    speed = w * 0.0090                               # world scroll
    gravity = h * 0.0016
    jump_v = -math.sqrt(2 * gravity * (h * 0.26))    # clears ~26%-tall walls
    ground_top = gy - P_SIZE
    py = ground_top
    vy = 0.0
    on_ground = True

    obstacles = []   # dict x, w, h
    coins = []       # dict x, y, taken, pop
    score = 0
    next_obstacle_x = w + w * 0.15
    rng = random.Random(seed + 5)

    n_frames = seconds * FPS
    tmp = f"/tmp/claude-0/-home-user-runner-gacha/_trailer_{('L' if w>h else 'P')}"
    if os.path.isdir(tmp): shutil.rmtree(tmp)
    os.makedirs(tmp, exist_ok=True)

    score_pop = 0  # frames remaining of score punch

    for fi in range(n_frames):
        # ---- spawn ----
        if not obstacles or obstacles[-1]["x"] < w - w * (0.42 + rng.random() * 0.18):
            oh = int(h * (0.10 + rng.random() * 0.16))
            ow = int(w * (0.024 + rng.random() * 0.014))
            ox = w + ow
            obstacles.append({"x": ox, "w": ow, "h": oh})
            # coin arc in the gap before this obstacle
            n = rng.choice([3, 4, 5])
            gap_start = ox - w * 0.30
            arc_h = h * (0.12 + rng.random() * 0.10)
            for k in range(n):
                t = k / max(1, n - 1)
                cx = gap_start + t * (w * 0.18)
                cy = gy - P_SIZE * 0.5 - math.sin(t * math.pi) * arc_h - h * 0.04
                coins.append({"x": cx, "y": cy, "taken": False, "pop": 0})

        # ---- move ----
        for o in obstacles: o["x"] -= speed
        for c in coins: c["x"] -= speed
        obstacles = [o for o in obstacles if o["x"] + o["w"] > -50]
        coins = [c for c in coins if c["x"] > -50 and c["pop"] < 8]

        # ---- auto jump ----
        if on_ground:
            for o in obstacles:
                d_left = o["x"] - (player_x + P_SIZE)
                if 0 < d_left < P_SIZE * 1.7:
                    vy = jump_v; on_ground = False; break

        # ---- gravity ----
        if not on_ground:
            vy += gravity; py += vy
            if py >= ground_top:
                py = ground_top; vy = 0; on_ground = True

        # ---- coin collect ----
        pcx, pcy = player_x + P_SIZE / 2, py + P_SIZE / 2
        for c in coins:
            if not c["taken"]:
                if abs(c["x"] - pcx) < P_SIZE * 0.6 and abs(c["y"] - pcy) < P_SIZE * 0.7:
                    c["taken"] = True; c["pop"] = 1; score += 1; score_pop = 6
            elif c["pop"] > 0:
                c["pop"] += 1

        # ---- draw frame ----
        fr = bg.copy()
        # obstacles
        od = ImageDraw.Draw(fr, "RGBA")
        for o in obstacles:
            x, oy, ow, oh = o["x"], gy - o["h"], o["w"], o["h"]
            g = radial_glow(int(max(ow, oh) * 0.8), RED_OBST, 60)
            fr.alpha_composite(g, (int(x + ow/2 - max(ow,oh)*0.8), int(oy + oh/2 - max(ow,oh)*0.8)))
            od.rectangle([x, oy, x + ow, oy + oh], fill=RED_OBST)
            od.rectangle([x, oy, x + ow, oy + oh * 0.16], fill=lerp(RED_OBST, (255,255,255), 0.25))
        # coins
        for c in coins:
            if c["taken"]:
                if c["pop"] > 0:  # expanding fade ring
                    pr = coin_r * (1 + c["pop"] * 0.4)
                    a = max(0, 200 - c["pop"] * 28)
                    od.ellipse([c["x"]-pr, c["y"]-pr, c["x"]+pr, c["y"]+pr],
                               outline=GOLD + (a,), width=max(2, int(coin_r*0.25)))
            else:
                bob = math.sin((fi + c["x"]) * 0.15) * coin_r * 0.18
                fr.alpha_composite(coin_sprite, (int(c["x"]-coin_pad), int(c["y"]+bob-coin_pad)))
        # player trail
        for i, a in enumerate([60, 30]):
            t = p_sprite.copy()
            t.putalpha(t.split()[3].point(lambda p: int(p*a/255)))
            fr.alpha_composite(t, (int(player_x + P_SIZE/2 - p_pad - speed*(i+1)*2.2),
                                   int(py + P_SIZE/2 - p_pad)))
        # player
        fr.alpha_composite(p_sprite, (int(player_x + P_SIZE/2 - p_pad), int(py + P_SIZE/2 - p_pad)))

        # ---- score HUD ----
        hud = ImageDraw.Draw(fr)
        cy_lbl = int(h * 0.05)
        hud.text((int(w*0.5), cy_lbl), "SCORE", font=label_font, anchor="mm",
                 fill=(170, 190, 230, 220))
        sc_size = 1.0 + (0.18 if score_pop > 0 else 0.0)
        sf = ImageFont.truetype(SCORE_FONT, int(min(w, h) * 0.055 * sc_size))
        hud.text((int(w*0.5), int(h*0.095)), str(score), font=sf, anchor="mm",
                 fill=(255, 255, 255))
        if score_pop > 0: score_pop -= 1

        fr.convert("RGB").save(f"{tmp}/f{fi:04d}.png")

    # ---- encode (use imageio's bundled ffmpeg; system ffmpeg is broken) ----
    import imageio_ffmpeg
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([
        ffmpeg_bin, "-y", "-framerate", str(FPS), "-i", f"{tmp}/f%04d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
        "-movflags", "+faststart", out_path
    ], check=True, capture_output=True)
    shutil.rmtree(tmp)
    print("wrote", out_path)


if __name__ == "__main__":
    render(1920, 1080, "/home/user/runner-gacha/trailer_landscape_1080p.mp4", seconds=12, seed=11)
    render(1080, 1920, "/home/user/runner-gacha/trailer_portrait_1080x1920.mp4", seconds=12, seed=7)
    print("done")
