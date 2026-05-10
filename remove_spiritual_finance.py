"""
remove_spiritual_finance.py
----------------------------
Ye script aapki website ke sabhi HTML files se
"Spiritual Finance", "Spiritual-Finance" words ko
replace karti hai.

USAGE:
  python remove_spiritual_finance.py --folder /path/to/your/website

EXAMPLE:
  python remove_spiritual_finance.py --folder C:/Users/YourName/website
  python remove_spiritual_finance.py --folder /home/user/website

Replacements jo honge:
  - "Spiritual Finance & Abundance Coach"  →  "Abundance & Wealth Coach"
  - "Spiritual Finance coach"              →  "Abundance & Wealth coach"
  - "Spiritual-Finance coach"             →  "Abundance & Wealth coach"
  - "Spiritual Finance"                    →  "Abundance Coaching"
  - "Spiritual-Finance"                    →  "Abundance Coaching"

Backup: script automatically ek backup folder banati hai
        taki koi galti ho to original restore kar sako.
"""

import os
import re
import shutil
import argparse
from datetime import datetime


# ─── Replacement Rules (order matters — specific pehle, generic baad mein) ───
REPLACEMENTS = [
    # Titles / OG / Twitter mein
    ("Spiritual Finance & Abundance Coach",  "Abundance & Wealth Coach"),
    ("Spiritual-Finance & Abundance Coach",  "Abundance & Wealth Coach"),
    ("Spiritual Finance &amp; Abundance Coach", "Abundance &amp; Wealth Coach"),

    # Meta description / body text
    ("Spiritual Finance coach",              "Abundance & Wealth coach"),
    ("Spiritual-Finance coach",             "Abundance & Wealth coach"),
    ("Premium Spiritual-Finance coach",     "Premium Abundance & Wealth coach"),
    ("Premium Spiritual Finance coach",     "Premium Abundance & Wealth coach"),

    # jobTitle in schema
    ("Spiritual Finance &amp; Abundance",   "Abundance &amp; Wealth"),

    # Generic fallback (case-insensitive handled below)
    ("Spiritual Finance",                    "Abundance Coaching"),
    ("Spiritual-Finance",                   "Abundance Coaching"),
]


def backup_folder(folder):
    """Original files ka backup banao."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = folder.rstrip("/\\") + f"_backup_{timestamp}"
    shutil.copytree(folder, backup_path)
    print(f"✅ Backup bana diya: {backup_path}\n")
    return backup_path


def process_file(filepath):
    """Ek HTML file mein replacements karo."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content
    changes = []

    for old, new in REPLACEMENTS:
        # Case-insensitive match karo
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        count = len(pattern.findall(content))
        if count:
            content = pattern.sub(new, content)
            changes.append(f"    '{old}' → '{new}'  ({count} jagah)")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return changes
    return []


def main():
    parser = argparse.ArgumentParser(
        description="Website HTML files se 'Spiritual Finance' word remove karo"
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Aapki website ka root folder path"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Backup skip karo (recommended nahi)"
    )
    args = parser.parse_args()

    folder = os.path.abspath(args.folder)

    if not os.path.isdir(folder):
        print(f"❌ ERROR: Folder nahi mila: {folder}")
        return

    print(f"📁 Folder: {folder}")
    print("=" * 55)

    # Backup
    if not args.no_backup:
        backup_folder(folder)

    # Sabhi HTML files dhundho
    html_files = []
    for root, dirs, files in os.walk(folder):
        # Backup folders skip karo
        dirs[:] = [d for d in dirs if "_backup_" not in d]
        for file in files:
            if file.endswith((".html", ".htm")):
                html_files.append(os.path.join(root, file))

    if not html_files:
        print("⚠️  Koi HTML file nahi mili!")
        return

    print(f"🔍 {len(html_files)} HTML files mili\n")

    total_changed = 0

    for filepath in html_files:
        rel_path = os.path.relpath(filepath, folder)
        changes = process_file(filepath)
        if changes:
            total_changed += 1
            print(f"✏️  {rel_path}")
            for c in changes:
                print(c)
            print()

    print("=" * 55)
    if total_changed:
        print(f"✅ {total_changed} files update ho gayi!")
        print("\n📌 Ab karo:")
        print("   1. Updated files apni hosting (Vercel) par upload karo")
        print("   2. Google Search Console mein Request Indexing karo")
    else:
        print("ℹ️  Koi 'Spiritual Finance' word nahi mila kisi file mein.")


if __name__ == "__main__":
    main()
