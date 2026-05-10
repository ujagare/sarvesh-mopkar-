#!/usr/bin/env python3
"""
=======================================================
  Sarvesh Mopkar — Lighthouse Image Fix Script
  
  Ye images fix karta hai jo Lighthouse ne flag ki hain:
  1. Logo — 1843x1593 → 260x260 (display: 100x86, 2x retina)
  2. Mountain peak — 1402x651 → 776x380 (display: 388x310, 2x)
  3. Kuber tree — 1041x484 → 776x562 (display: 388x562, 2x)
  4. Icons — 300px+ → 108x108 (display: ~54x54, 2x)
  
  Expected savings: ~596 KB
=======================================================
  Run: python fix_lighthouse_images.py
=======================================================
"""

import os, shutil
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    print("❌ pip install Pillow")
    exit(1)

QUALITY = 80

# Format: (filepath, max_width, max_height, quality)
IMAGES = [
    # Logo — bahut bada hai (1843x1593) display sirf 100x86
    ("images/home/sarvesh-mopkar-logo.webp",           260, 260,  85),

    # Main pillar images
    ("images/home/trading-strategy-mountain-peak-sunrise.webp", 776, 380, 78),
    ("images/home/kuber-consciousness-abundance-golden-tree.webp", 776, 580, 78),
    ("images/home/nervous-system-balance-stacked-stones.webp",    776, 580, 78),
    ("images/home/wealth-abundance-kuber-golden-pot.webp",        776, 580, 78),
    ("images/home/spiritual-finance-coaching-sanctuary.webp",     776, 580, 78),

    # Icons — display ~54x54, 2x = 108x108
    ("images/home/icon/icon-transformation-abundance.webp",       108, 108, 80),
    ("images/home/icon/icon-clarity-spiritual-finance.webp",      108, 108, 80),
    ("images/home/icon/icon-awareness-wealth-consciousness.webp", 108, 108, 80),
    ("images/home/icon/icon-consciousness-kuber.webp",            80,  80,  80),
    ("images/home/icon/icon-trading-strategy-discipline.webp",    60,  60,  80),
    ("images/home/icon/icon-identity-wealth-expansion.webp",      108, 108, 80),
    ("images/home/icon/icon-nervous-system-income.webp",          108, 108, 80),
    ("images/home/icon/icon-energy-alignment-coach.webp",         108, 108, 80),
    ("images/home/icon/icon-millionaire-trader-mentorship.webp",  108, 108, 80),
]

def resize_image(filepath, max_w, max_h, quality):
    path = Path(filepath)
    if not path.exists():
        print(f"  ⚠️  Nahi mila: {filepath}")
        return

    # Backup (ek baar)
    bak = Path(str(path) + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)

    img = Image.open(path)
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    orig_w, orig_h = img.size
    orig_kb = path.stat().st_size / 1024

    # Resize only if larger than target
    if orig_w > max_w or orig_h > max_h:
        img.thumbnail((max_w, max_h), Image.LANCZOS)

    new_w, new_h = img.size

    # Keep RGBA for transparency
    if img.mode not in ("RGB", "RGBA", "L"):
        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")

    img.save(str(path), "WEBP", quality=quality, method=6, optimize=True)

    new_kb = path.stat().st_size / 1024
    saved  = orig_kb - new_kb
    pct    = (saved / orig_kb * 100) if orig_kb else 0

    print(f"  ✅ {path.name}")
    print(f"     {orig_w}x{orig_h} → {new_w}x{new_h}  |  "
          f"{orig_kb:.0f} KB → {new_kb:.0f} KB  ({pct:.0f}% saved)\n")
    return saved


print("\n" + "="*52)
print("  Lighthouse Image Fix — Sarvesh Mopkar")
print("="*52 + "\n")

total_saved = 0
for item in IMAGES:
    saved = resize_image(*item)
    if saved:
        total_saved += saved

print("="*52)
print(f"  🎉 Total size saved: ~{total_saved:.0f} KB")
print(f"  Expected Performance: 95 → 98-100")
print()
print("  Ab push karo:")
print('  git add .')
print('  git commit -m "perf: resize oversized images per Lighthouse"')
print('  git push')
print("="*52 + "\n")
