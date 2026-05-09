"""
Image → WebP Converter & Optimizer — Sarvesh Mopkar Website
=============================================================
Yeh script:
1. images/ folder ki saari PNG/JPG files dhundega
2. Unhe WebP format mein convert + optimize karega
3. index.html aur baaki HTML files mein .png/.jpg → .webp update karega
4. Original files backup folder mein safe rakh dega

INSTALL (pehle ek baar chalao):
  pip install Pillow

CHALAO (website root folder se):
  python convert_to_webp.py
"""

import os
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("\n❌ Pillow library install nahi hai!")
    print("   Yeh command chalao pehle:\n")
    print("   pip install Pillow\n")
    exit()

# ─── SETTINGS ───────────────────────────────────────────────────────────────
IMAGES_FOLDER   = "images"          # Jahan saari images hain
BACKUP_FOLDER   = "images_backup"   # Original files yahan save hongi
WEBP_QUALITY    = 85                # 80-90 recommended (smaller + good quality)
LOGO_QUALITY    = 95                # Logo ke liye high quality
MAX_WIDTH       = 1920              # Is se badi images resize ho jaayengi
HTML_FILES      = [
    "index.html",
    "about.html",
    "philosophy.html",
    "work.html",
    "contact.html",
]

# ─── STEP 1: BACKUP ─────────────────────────────────────────────────────────
def backup_originals():
    if os.path.exists(BACKUP_FOLDER):
        print(f"  ℹ️  Backup folder already hai ({BACKUP_FOLDER}/) — skip\n")
        return
    shutil.copytree(IMAGES_FOLDER, BACKUP_FOLDER)
    print(f"  ✅ Backup bana diya: {BACKUP_FOLDER}/\n")

# ─── STEP 2: CONVERT TO WEBP ────────────────────────────────────────────────
def convert_images():
    exts = {".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"}
    converted = 0
    skipped   = 0
    saved_kb  = 0

    image_files = [
        p for p in Path(IMAGES_FOLDER).rglob("*")
        if p.suffix in exts
    ]

    if not image_files:
        print("  ⚠️  Koi image nahi mili images/ folder mein.\n")
        return 0

    for img_path in image_files:
        webp_path = img_path.with_suffix(".webp")

        try:
            with Image.open(img_path) as img:
                # RGBA → RGB convert (WebP supports both but safe hai)
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                # Logo ke liye high quality
                quality = LOGO_QUALITY if "logo" in img_path.name.lower() else WEBP_QUALITY

                # Bahut badi images resize karo
                w, h = img.size
                if w > MAX_WIDTH:
                    ratio    = MAX_WIDTH / w
                    new_size = (MAX_WIDTH, int(h * ratio))
                    img      = img.resize(new_size, Image.LANCZOS)
                    print(f"  ↕️  Resized: {img_path.name} ({w}px → {MAX_WIDTH}px)")

                img.save(webp_path, "WEBP", quality=quality, method=6)

            # Size comparison
            old_size = img_path.stat().st_size
            new_size = webp_path.stat().st_size
            saved    = (old_size - new_size) // 1024
            saved_kb += max(saved, 0)
            pct      = int((1 - new_size / old_size) * 100) if old_size > 0 else 0

            print(f"  ✅ {img_path.name}")
            print(f"      {old_size//1024} KB → {new_size//1024} KB  ({pct}% chhota)\n")
            converted += 1

            # Original delete karo (backup already hai)
            img_path.unlink()

        except Exception as e:
            print(f"  ❌ Error ({img_path.name}): {e}\n")
            skipped += 1

    print(f"  Converted: {converted}  |  Skipped: {skipped}")
    print(f"  💾 Total space bachaya: ~{saved_kb} KB\n")
    return converted

# ─── STEP 3: HTML UPDATE ────────────────────────────────────────────────────
def update_html_files():
    print("📝 Step 3: HTML files update ho rahi hain (.png/.jpg → .webp)...\n")

    for html_file in HTML_FILES:
        if not os.path.exists(html_file):
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        # Replace all image extensions with .webp
        import re
        content = re.sub(r'(src=["\'][^"\']+?)\.(png|jpg|jpeg)(["\'])',
                         r'\1.webp\3', content, flags=re.IGNORECASE)
        content = re.sub(r'(srcset=["\'][^"\']+?)\.(png|jpg|jpeg)(["\'])',
                         r'\1.webp\3', content, flags=re.IGNORECASE)

        if content != original:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ {html_file} — updated")
        else:
            print(f"  — {html_file} — koi image reference nahi tha")

    print()

# ─── MAIN ───────────────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 55)
    print("  Sarvesh Mopkar — Image WebP Converter & Optimizer")
    print("=" * 55 + "\n")

    if not os.path.exists("index.html"):
        print("❌ ERROR: index.html nahi mili!")
        print("   Script ko website ke ROOT folder se chalao\n")
        return

    if not os.path.exists(IMAGES_FOLDER):
        print(f"❌ ERROR: '{IMAGES_FOLDER}' folder nahi mila!\n")
        return

    print("📦 Step 1: Original images ka backup ban raha hai...\n")
    backup_originals()

    print("🖼️  Step 2: Images WebP mein convert ho rahi hain...\n")
    count = convert_images()

    if count > 0:
        update_html_files()

    print("=" * 55)
    if count > 0:
        print("  ✅ Sab images WebP mein convert ho gayi!")
        print()
        print("  Ab kya karein:")
        print("  1. rename_images_sarvesh.py chalao (renaming ke liye)")
        print("  2. Phir GitHub pe push karo:")
        print("     git add .")
        print('     git commit -m "Perf: convert images to WebP"')
        print("     git push")
        print()
        print(f"  Original files safe hain: {BACKUP_FOLDER}/")
    print("=" * 55 + "\n")

if __name__ == "__main__":
    main()
