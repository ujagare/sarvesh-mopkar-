"""
Smart Image Renamer — Sarvesh Mopkar Website (All 6 Folders)
=============================================================
Yeh script saare folders scan karke images rename karega:
  About, Blog, Contact, home, Philosophy, The Work

CHALAO (website root folder se):
  python smart_rename.py
"""

import os
import re
from pathlib import Path

# ─── FOLDER → SEO PREFIX MAPPING ────────────────────────────────────────────
FOLDER_PREFIX = {
    "about":      "sarvesh-mopkar-about",
    "blog":       "sarvesh-mopkar-blog",
    "contact":    "sarvesh-mopkar-contact",
    "home":       "sarvesh-mopkar-home",
    "philosophy": "sarvesh-mopkar-philosophy",
    "the work":   "sarvesh-mopkar-the-work",
    "icon":       "sarvesh-mopkar-icon",
    "favicon":    "sarvesh-mopkar-favicon",
}

# ─── SPECIFIC KNOWN FILES (home folder — from website content) ──────────────
KNOWN_FILES = {
    # home/
    "images/home/ChatGPT Image Apr 24, 2026, 09_51_23 PM.webp":
        "images/home/kuber-consciousness-abundance-golden-tree.webp",
    "images/home/ChatGPT Image Apr 24, 2026, 09_55_50 PM.webp":
        "images/home/trading-strategy-mountain-peak-sunrise.webp",
    "images/home/ChatGPT Image Apr 24, 2026, 09_57_09 PM.webp":
        "images/home/nervous-system-balance-stacked-stones.webp",
    "images/home/ChatGPT Image Apr 24, 2026, 09_59_07 PM.webp":
        "images/home/wealth-abundance-kuber-golden-pot.webp",
    "images/home/ChatGPT Image Apr 25, 2026, 01_22_10 AM.webp":
        "images/home/spiritual-finance-coaching-sanctuary.webp",
    "images/home/ChatGPT Image Apr 24, 2026, 10_01_18 PM.webp":
        "images/home/sarvesh-mopkar-spiritual-decorative-1.webp",
    "images/home/ChatGPT Image Apr 24, 2026, 10_03_38 PM.webp":
        "images/home/sarvesh-mopkar-spiritual-decorative-2.webp",
    "images/home/Sarvesh M Logo_PNG.webp":
        "images/home/sarvesh-mopkar-logo.webp",
    "images/home/Sarvesh M Logo_PNG1.webp":
        "images/home/sarvesh-mopkar-logo-alt.webp",
    "images/home/contact_sheet.webp":
        "images/home/sarvesh-mopkar-contact-sheet.webp",

    # home/icon/
    "images/home/icon/ChatGPT Image Apr 24, 2026, 08_03_24 PM.webp":
        "images/home/icon/icon-clarity-spiritual-finance.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 08_04_09 PM.webp":
        "images/home/icon/icon-awareness-wealth-consciousness.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 08_06_56 PM.webp":
        "images/home/icon/icon-consciousness-kuber.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 08_07_38 PM.webp":
        "images/home/icon/icon-transformation-abundance.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 08_12_37 PM.webp":
        "images/home/icon/icon-trading-strategy-discipline.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 08_16_57 PM.webp":
        "images/home/icon/icon-identity-wealth-expansion.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 09_30_51 PM.webp":
        "images/home/icon/icon-nervous-system-income.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 09_41_32 PM.webp":
        "images/home/icon/icon-energy-alignment-coach.webp",
    "images/home/icon/ChatGPT Image Apr 24, 2026, 09_47_53 PM.webp":
        "images/home/icon/icon-millionaire-trader-mentorship.webp",
}

# ─── FILES TO SKIP (already good names) ─────────────────────────────────────
SKIP_PATTERNS = [
    "sarvesh-mopkar",   # already renamed
    "kuber-",
    "trading-",
    "nervous-",
    "wealth-",
    "spiritual-",
    "icon-",
    "contact-sheet",
]

# ─── HTML FILES TO UPDATE ────────────────────────────────────────────────────
HTML_FILES = [
    "index.html",
    "about.html",
    "philosophy.html",
    "work.html",
    "contact.html",
    "blog.html",
]

def needs_rename(filename):
    name_lower = filename.lower()
    for pat in SKIP_PATTERNS:
        if pat in name_lower:
            return False
    return True

def get_folder_prefix(file_path):
    parts = Path(file_path).parts
    for part in reversed(parts[:-1]):
        key = part.lower()
        if key in FOLDER_PREFIX:
            return FOLDER_PREFIX[key]
    return "sarvesh-mopkar"

def build_auto_rename_map():
    """Known files ke baad, baaki sab auto-number se rename"""
    auto_map = {}
    counters = {}

    for root, dirs, files in os.walk("images"):
        # Sort for consistent numbering
        for fname in sorted(files):
            if not fname.lower().endswith(".webp"):
                continue
            if not needs_rename(fname):
                continue

            full_path = os.path.join(root, fname).replace("\\", "/")

            # Skip if already in KNOWN_FILES
            if full_path in KNOWN_FILES:
                continue

            prefix = get_folder_prefix(full_path)
            counters[prefix] = counters.get(prefix, 0) + 1
            n = counters[prefix]

            new_name = f"{prefix}-{n:02d}.webp"
            new_path = os.path.join(root, new_name).replace("\\", "/")
            auto_map[full_path] = new_path

    return auto_map

def rename_files(rename_map):
    renamed = 0
    skipped = 0
    for old, new in rename_map.items():
        if os.path.exists(old):
            # Avoid overwriting existing file
            if os.path.exists(new) and old != new:
                print(f"  ⚠️  Skip (target exists): {os.path.basename(new)}")
                skipped += 1
                continue
            os.rename(old, new)
            old_kb = os.path.getsize(new) // 1024
            print(f"  ✅ {os.path.basename(old)}")
            print(f"      → {os.path.basename(new)}  ({old_kb} KB)\n")
            renamed += 1
        else:
            print(f"  ⚠️  File nahi mili: {old}\n")
            skipped += 1
    return renamed, skipped

def update_html(rename_map):
    print("\n📝 HTML files update ho rahi hain...\n")
    for html_file in HTML_FILES:
        if not os.path.exists(html_file):
            continue
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        original = content
        for old, new in rename_map.items():
            old_name = os.path.basename(old)
            new_name = os.path.basename(new)
            # Match filename anywhere in src/href
            old_esc = re.escape(old_name)
            content = re.sub(old_esc, new_name, content)
            # Also match URL-encoded version
            old_enc = re.escape(old_name.replace(" ", "%20"))
            content = re.sub(old_enc, new_name, content)
            # Full path match
            content = content.replace(old, new)
        if content != original:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ {html_file} updated")
        else:
            print(f"  —  {html_file} (koi change nahi)")

def main():
    print("\n" + "="*56)
    print("  Sarvesh Mopkar — Smart Image Renamer (All Folders)")
    print("="*56 + "\n")

    if not os.path.exists("index.html"):
        print("❌ index.html nahi mili! Root folder se chalao.\n")
        return

    if not os.path.exists("images"):
        print("❌ images/ folder nahi mila!\n")
        return

    # Combine known + auto maps
    full_map = {}
    full_map.update(KNOWN_FILES)
    full_map.update(build_auto_rename_map())

    total = len(full_map)
    print(f"  {total} images rename hongi\n")
    print("─"*56)

    print("\n🖼️  Renaming...\n")
    renamed, skipped = rename_files(full_map)

    update_html(full_map)

    print("\n" + "="*56)
    print(f"  ✅ Renamed: {renamed}  |  Skipped: {skipped}")
    print()
    print("  Ab GitHub pe push karo:")
    print("  git add .")
    print('  git commit -m "SEO: rename all images descriptively"')
    print("  git push")
    print("="*56 + "\n")

if __name__ == "__main__":
    main()
