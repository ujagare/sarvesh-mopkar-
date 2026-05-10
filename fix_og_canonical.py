#!/usr/bin/env python3
"""
=======================================================
  Sarvesh Mopkar — OG + Canonical + Copyright Fix
  
  Ye script sare pages mein fix karta hai:
  1. og:url  → https://www.sarveshmopkar.co/page.html
  2. og:image → full URL (https://www.sarveshmopkar.co/...)
  3. twitter:image → full URL
  4. <link rel="canonical"> → correct URL add/fix
  5. © 2024 → © 2026 (footer)
=======================================================
  Run karo:
    python fix_og_canonical.py
=======================================================
"""

import os, re, shutil

BASE = "https://www.sarveshmopkar.co"
OG_IMAGE = f"{BASE}/images/home/sarvesh-mopkar-logo.webp"

PAGES = {
    "index.html":        f"{BASE}/index.html",
    "about.html":        f"{BASE}/about.html",
    "philosophy.html":   f"{BASE}/philosophy.html",
    "work.html":         f"{BASE}/work.html",
    "work-with-me.html": f"{BASE}/work-with-me.html",
    "contact.html":      f"{BASE}/contact.html",
    "blog.html":         f"{BASE}/blog.html",
}

def fix_page(filename, page_url):
    if not os.path.exists(filename):
        print(f"  ⏭  Skip (nahi mila): {filename}")
        return

    # Backup
    bak = filename + ".bak2"
    if not os.path.exists(bak):
        shutil.copy2(filename, bak)

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    original = html
    changes = []

    # ── 1. og:url fix ────────────────────────────────────────────────────────
    # Match any og:url value (GitHub ya koi bhi purana URL)
    new_og_url = f'<meta property="og:url" content="{page_url}"'
    html, n = re.subn(
        r'<meta\s+property=["\']og:url["\'][^>]*>',
        new_og_url + " />",
        html, flags=re.IGNORECASE
    )
    if n: changes.append(f"og:url → {page_url}")

    # ── 2. og:image fix → full URL ───────────────────────────────────────────
    new_og_img = f'<meta property="og:image" content="{OG_IMAGE}"'
    html, n = re.subn(
        r'<meta\s+property=["\']og:image["\'][^>]*>',
        new_og_img + " />",
        html, flags=re.IGNORECASE
    )
    if n: changes.append(f"og:image → full URL")

    # ── 3. twitter:image fix → full URL ──────────────────────────────────────
    new_tw_img = f'<meta name="twitter:image" content="{OG_IMAGE}"'
    html, n = re.subn(
        r'<meta\s+name=["\']twitter:image["\'][^>]*>',
        new_tw_img + " />",
        html, flags=re.IGNORECASE
    )
    if n: changes.append("twitter:image → full URL")

    # ── 4. canonical fix/add ─────────────────────────────────────────────────
    canonical_tag = f'<link rel="canonical" href="{page_url}" />'

    if re.search(r'<link\s+rel=["\']canonical["\']', html, re.IGNORECASE):
        # Update existing canonical
        html, n = re.subn(
            r'<link\s+rel=["\']canonical["\'][^>]*>',
            canonical_tag,
            html, flags=re.IGNORECASE
        )
        if n: changes.append(f"canonical updated → {page_url}")
    else:
        # Add before </head>
        html = html.replace("</head>", f"  {canonical_tag}\n  </head>")
        changes.append(f"canonical added → {page_url}")

    # ── 5. Copyright year fix ─────────────────────────────────────────────────
    html, n = re.subn(
        r'© 2024 Sarvesh Mopkar',
        '© 2026 Sarvesh Mopkar',
        html
    )
    if n: changes.append("© 2024 → © 2026")

    # ── 6. og:type fix (work-with-me ke liye) ────────────────────────────────
    # Ensure og:type is correct per page
    if "about" in filename:
        html = re.sub(
            r'(<meta property="og:type" content=")[^"]*(")',
            r'\1profile\2', html
        )
    elif "blog" in filename:
        html = re.sub(
            r'(<meta property="og:type" content=")[^"]*(")',
            r'\1blog\2', html
        )

    # ── Save ─────────────────────────────────────────────────────────────────
    if html != original:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n  ✅ {filename}")
        for c in changes:
            print(f"     • {c}")
    else:
        print(f"\n  — {filename} (koi change nahi)")


# ═══════════════════════════════════════════════════════
print("\n" + "="*52)
print("  Sarvesh Mopkar — OG + Canonical + Copyright Fix")
print("="*52)

for filename, url in PAGES.items():
    fix_page(filename, url)

print("\n" + "="*52)
print("  ✅ Sab fix ho gaya!")
print()
print("  Ab ye karo:")
print("  1. Browser mein test karo:")
print("     https://developers.facebook.com/tools/debug/")
print("     (apna URL paste karo — OG preview check karo)")
print()
print("  2. Google Search Console mein:")
print("     sitemap.xml submit karo (agar nahi kiya)")
print()
print("  3. GitHub pe push karo:")
print("     git add .")
print('     git commit -m "fix: og urls, canonical, copyright year"')
print("     git push")
print("="*52 + "\n")
