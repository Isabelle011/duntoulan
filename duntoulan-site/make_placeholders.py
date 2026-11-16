# -*- coding: utf-8 -*-
"""生成扎染风格占位图。正式照片到位后，直接用同名 jpg 覆盖 images/ 里的文件即可。"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)

def shibori(w, h, seed, base, ring, label=""):
    """蓝底 + 放射状团花纹（模拟扎染防染留白）"""
    random.seed(seed)
    img = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(img)
    cx, cy = w * random.uniform(0.42, 0.58), h * random.uniform(0.42, 0.58)
    maxr = max(w, h) * 0.75
    petals = random.choice([8, 10, 12])
    # 底层柔和光斑
    glow = Image.new("RGB", (w, h), base)
    gd = ImageDraw.Draw(glow)
    for i in range(6):
        r = maxr * (0.9 - i * 0.13)
        c = tuple(min(255, int(v + (255 - v) * 0.10)) for v in base)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)
    # 花瓣环
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
    # 中心晕圈
    for i in range(4):
        r = maxr * (0.05 + i * 0.035)
        col = tuple(min(255, int(v + (255 - v) * (0.75 - i * 0.15))) for v in base)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=max(2, int(min(w, h) * 0.008)))
    # 满天星小圆点（散花）
    for _ in range(60):
        x, y = random.uniform(0, w), random.uniform(0, h)
        if math.hypot(x - cx, y - cy) < maxr * 0.18:
            continue
        r = random.uniform(1.5, 4.5)
        col = tuple(min(255, int(v + (255 - v) * 0.55)) for v in base)
        d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    # 角标提示（ASCII，避免字体问题）
    if label:
        d2 = ImageDraw.Draw(img)
        d2.rectangle([12, h - 40, 12 + len(label) * 8 + 20, h - 14], fill=(20, 40, 62))
        d2.text((22, h - 34), label, fill=(235, 240, 246))
    return img

BASE_DARK = (24, 52, 84)
BASE_MID = (36, 74, 112)
BASE_SOFT = (58, 106, 148)

jobs = [
    ("hero-banner.jpg", 1600, 700, 1, BASE_DARK),
    ("culture-intro.jpg", 900, 720, 2, BASE_MID),
    ("work-01.jpg", 600, 510, 3, BASE_MID),
    ("work-02.jpg", 600, 510, 4, BASE_DARK),
    ("work-03.jpg", 600, 510, 5, BASE_SOFT),
    ("work-04.jpg", 600, 510, 6, BASE_DARK),
    ("work-05.jpg", 600, 510, 7, BASE_MID),
    ("news-01.jpg", 800, 500, 8, BASE_MID),
    ("news-02.jpg", 800, 500, 9, BASE_SOFT),
    ("news-03.jpg", 800, 500, 10, BASE_DARK),
]
for name, w, h, seed, base in jobs:
    im = shibori(w, h, seed, base, None, label="PLACEHOLDER: " + name)
    im.save(os.path.join(OUT, name), quality=88)
    print("OK", name)
