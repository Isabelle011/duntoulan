# -*- coding: utf-8 -*-
"""内页占位图。正式照片到位后，用同名 jpg 覆盖 images/ 里的文件即可。"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)

def shibori(w, h, seed, base, label=""):
    random.seed(seed)
    img = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(img)
    cx, cy = w * random.uniform(0.42, 0.58), h * random.uniform(0.42, 0.58)
    maxr = max(w, h) * 0.75
    glow = Image.new("RGB", (w, h), base)
    gd = ImageDraw.Draw(glow)
    for i in range(6):
        r = maxr * (0.9 - i * 0.13)
        c = tuple(min(255, int(v + (255 - v) * 0.10)) for v in base)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)
    petals = random.choice([8, 10, 12])
    for layer in range(5):
        r = maxr * (0.16 + layer * 0.13)
        lw = max(2, int(min(w, h) * 0.012 * (5 - layer) * 0.5))
        col = tuple(min(255, int(v + (255 - v) * (0.62 - layer * 0.11))) for v in base)
        for p in range(petals):
            a0 = 2 * math.pi * p / petals
            pts = []
            for t in range(0, 36):
                tt = t / 35.0
                ang = a0 + tt * (2 * math.pi / petals)
                rr = r * (1 + 0.18 * math.sin(tt * math.pi))
                pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
            d.line(pts, fill=col, width=lw, joint="curve")
    for i in range(4):
        r = maxr * (0.05 + i * 0.035)
        col = tuple(min(255, int(v + (255 - v) * (0.75 - i * 0.15))) for v in base)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=max(2, int(min(w, h) * 0.008)))
    for _ in range(60):
        x, y = random.uniform(0, w), random.uniform(0, h)
        if math.hypot(x - cx, y - cy) < maxr * 0.18:
            continue
        r = random.uniform(1.5, 4.5)
        col = tuple(min(255, int(v + (255 - v) * 0.55)) for v in base)
        d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    if label:
        d2 = ImageDraw.Draw(img)
        d2.rectangle([12, h - 40, 12 + len(label) * 8 + 20, h - 14], fill=(20, 40, 62))
        d2.text((22, h - 34), label, fill=(235, 240, 246))
    return img

BASE_DARK = (24, 52, 84)
BASE_MID = (36, 74, 112)
BASE_SOFT = (58, 106, 148)

jobs = []
def add(name, w, h, base):
    jobs.append((name, w, h, base))

# 文化页
add("origin.jpg", 900, 720, BASE_MID)
add("genre-01.jpg", 600, 450, BASE_MID)
add("genre-02.jpg", 600, 450, BASE_DARK)
add("genre-03.jpg", 600, 450, BASE_SOFT)
add("pattern-big.jpg", 700, 700, BASE_DARK)
# 工艺页
add("journey.jpg", 800, 600, BASE_MID)
add("process-01.jpg", 720, 480, BASE_DARK)
add("process-02.jpg", 720, 480, BASE_SOFT)
add("process-03.jpg", 720, 480, BASE_MID)
add("process-04.jpg", 720, 480, BASE_DARK)
add("process-05.jpg", 720, 480, BASE_SOFT)
add("tool-01.jpg", 500, 380, BASE_MID)
add("tool-02.jpg", 500, 380, BASE_DARK)
add("tool-03.jpg", 500, 380, BASE_SOFT)
add("tool-04.jpg", 500, 380, BASE_MID)
# 作品页
add("featured-works.jpg", 900, 680, BASE_DARK)
for i in range(1, 9):
    add(f"series-0{i}.jpg", 600, 450, (BASE_MID, BASE_DARK, BASE_SOFT)[i % 3])
# 商城页
add("shop-intro.jpg", 800, 620, BASE_DARK)
for i in range(1, 9):
    add(f"product-0{i}.jpg", 600, 600, (BASE_MID, BASE_DARK, BASE_SOFT, BASE_MID)[i % 4])
# 课程页
add("course-hero.jpg", 900, 720, BASE_MID)
add("course-01.jpg", 600, 450, BASE_MID)
add("course-02.jpg", 600, 450, BASE_DARK)
add("course-03.jpg", 600, 450, BASE_SOFT)
add("scene-01.jpg", 500, 380, BASE_DARK)
add("scene-02.jpg", 500, 380, BASE_SOFT)
add("scene-03.jpg", 500, 380, BASE_MID)
add("scene-04.jpg", 500, 380, BASE_DARK)
# 新闻页
add("headline.jpg", 860, 590, BASE_DARK)
for i in range(1, 7):
    add(f"article-0{i}.jpg", 640, 400, (BASE_MID, BASE_DARK, BASE_SOFT)[i % 3])
# 联系页
add("contact-hero.jpg", 900, 640, BASE_MID)
add("visit.jpg", 800, 620, BASE_DARK)

seed = 100
for name, w, h, base in jobs:
    seed += 1
    im = shibori(w, h, seed, base, label="PLACEHOLDER: " + name)
    im.save(os.path.join(OUT, name), quality=88)
print("OK", len(jobs), "images")
