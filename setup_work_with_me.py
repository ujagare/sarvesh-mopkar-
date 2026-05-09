#!/usr/bin/env python3
"""
=======================================================
  Sarvesh Mopkar — Work With Me Page Complete Setup
  
  Ye script ek saath karta hai:
  1. Images → WebP convert + optimize
  2. SEO-friendly rename
  3. HTML references update
  4. Alt tags add (icon images)
  5. Semantic tags improve
  6. Meta tags + Canonical
  7. Open Graph + Twitter Card
  8. Schema markup (Service + WebPage)
  9. Sitemap.xml update
=======================================================
"""

import os, re, json, shutil
from pathlib import Path
from datetime import date

try:
    from PIL import Image, ImageOps
except ImportError:
    print("❌ Pillow install karein: pip install Pillow")
    exit(1)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BASE_URL    = "https://ujagare.github.io/sarvesh-mopkar-"
HTML_FILE   = "work-with-me.html"
IMG_FOLDER  = "images/Work with me"
ICON_FOLDER = "images/Work with me/icons"
QUALITY     = 82
MAX_SIZE    = 1920
TODAY       = date.today().strftime("%Y-%m-%d")
# ──────────────────────────────────────────────────────────────────────────────

# ─── IMAGE RENAME MAP ─────────────────────────────────────────────────────────
# Original PNG naam → New SEO naam (without extension)
IMAGE_RENAME_MAP = {
    # Main card images
    "ChatGPT Image May 9, 2026, 02_33_36 PM.png":
        "sarvesh-mopkar-kuber-consciousness-abundance",
    "ChatGPT Image May 9, 2026, 02_34_28 PM.png":
        "sarvesh-mopkar-millionaire-trader-mentorship",
    "ChatGPT Image May 9, 2026, 02_35_11 PM.png":
        "sarvesh-mopkar-one-on-one-deep-work-transformation",
    "ChatGPT Image May 9, 2026, 02_36_14 PM.png":
        "sarvesh-mopkar-energy-work-sound-healing-sessions",

    # Icon images
    "icons/ChatGPT Image May 9, 2026, 02_38_38 PM.png":
        "icon-inner-abundance-kuber-consciousness",
    "icons/ChatGPT Image May 9, 2026, 02_40_26 PM.png":
        "icon-wealth-alignment-abundance",
    "icons/ChatGPT Image May 9, 2026, 02_44_11 PM.png":
        "icon-expansion-flow-consciousness",
    "icons/ChatGPT Image May 9, 2026, 02_43_54 PM.png":
        "icon-trading-psychology-mindset",
    "icons/ChatGPT Image May 9, 2026, 02_44_45 PM.png":
        "icon-risk-discipline-trader",
    "icons/ChatGPT Image May 9, 2026, 02_45_39 PM.png":
        "icon-emotional-neutrality-trading",
    "icons/ChatGPT Image May 9, 2026, 02_46_11 PM.png":
        "icon-structured-decisions-trader",
    "icons/ChatGPT Image May 9, 2026, 02_47_01 PM.png":
        "icon-identity-shift-deep-work",
    "icons/ChatGPT Image May 9, 2026, 02_47_40 PM.png":
        "icon-emotional-patterns-healing",
    "icons/ChatGPT Image May 9, 2026, 02_48_30 PM.png":
        "icon-wealth-ceiling-breakthrough",
    "icons/ChatGPT Image May 9, 2026, 02_49_06 PM.png":
        "icon-sound-healing-energy-session",
}

# Alt text for icon images (li text se match karta hai)
ICON_ALT_MAP = {
    "icon-inner-abundance-kuber-consciousness.webp":   "Inner abundance icon",
    "icon-wealth-alignment-abundance.webp":             "Wealth alignment icon",
    "icon-expansion-flow-consciousness.webp":           "Expansion and flow icon",
    "icon-trading-psychology-mindset.webp":             "Trading psychology icon",
    "icon-risk-discipline-trader.webp":                 "Risk discipline icon",
    "icon-emotional-neutrality-trading.webp":           "Emotional neutrality icon",
    "icon-structured-decisions-trader.webp":            "Structured decisions icon",
    "icon-identity-shift-deep-work.webp":               "Identity shift icon",
    "icon-emotional-patterns-healing.webp":             "Emotional patterns icon",
    "icon-wealth-ceiling-breakthrough.webp":            "Wealth ceiling breakthrough icon",
    "icon-sound-healing-energy-session.webp":           "Sound healing icon",
    # Already renamed icons
    "sarvesh-mopkar-philosophy-08.webp":   "Kuber consciousness icon",
    "sarvesh-mopkar-philosophy-09.webp":   "Spiritual alignment icon",
    "sarvesh-mopkar-philosophy-10.webp":   "Subconscious reprogramming icon",
    "icon-trading-strategy-discipline.webp": "Trading strategy discipline icon",
    "icon-transformation-abundance.webp":    "Transformation and abundance icon",
    "icon-energy-alignment-coach.webp":      "Energy alignment coach icon",
}


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: IMAGES — Convert PNG → WebP, Optimize, Rename
# ═══════════════════════════════════════════════════════════════════════════════
def convert_and_rename_images():
    print("\n" + "="*55)
    print("  📸 STEP 1: Images Convert + Optimize + Rename")
    print("="*55)

    if not os.path.isdir(IMG_FOLDER):
        print(f"  ⚠️  Folder nahi mila: '{IMG_FOLDER}'")
        print("      Script ko website root folder se run karein.")
        return {}

    # Backup
    backup = IMG_FOLDER + "_backup"
    if not os.path.exists(backup):
        shutil.copytree(IMG_FOLDER, backup)
        print(f"  💾 Backup banaya: {backup}\n")

    src_to_new = {}   # old src path → new src path (for HTML update)
    converted = 0
    total_saved = 0

    for rel_path, new_stem in IMAGE_RENAME_MAP.items():
        old_path = Path(IMG_FOLDER) / rel_path
        sub      = "icons/" if rel_path.startswith("icons/") else ""
        new_path = Path(IMG_FOLDER) / sub / (new_stem + ".webp")

        if not old_path.exists():
            print(f"  ⚠️  Nahi mili (skip): {old_path}")
            continue

        # Already converted & renamed?
        if new_path.exists() and old_path.suffix.lower() == ".webp":
            print(f"  ✔  Already done: {new_path.name}")
            src_to_new[f"images/Work with me/{rel_path}"] = \
                f"images/Work with me/{sub}{new_stem}.webp"
            continue

        try:
            img = Image.open(old_path)
            try:
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            # Resize if too large
            w, h = img.size
            if max(w, h) > MAX_SIZE:
                ratio = MAX_SIZE / max(w, h)
                img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)

            # Save as WebP (keep transparency if RGBA)
            if img.mode not in ("RGB", "RGBA", "L"):
                img = img.convert("RGB")

            new_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(new_path), "WEBP", quality=QUALITY,
                     method=6, optimize=True)

            orig_kb = old_path.stat().st_size / 1024
            new_kb  = new_path.stat().st_size / 1024
            saved   = orig_kb - new_kb
            total_saved += saved

            print(f"  ✅ {old_path.name}")
            print(f"     → {new_path.name}")
            print(f"     {orig_kb:.0f} KB → {new_kb:.0f} KB  "
                  f"({saved/orig_kb*100:.0f}% chota)\n")

            # Map old HTML src → new src
            src_to_new[f"images/Work with me/{rel_path}"] = \
                f"images/Work with me/{sub}{new_stem}.webp"
            converted += 1

        except Exception as e:
            print(f"  ❌ Error ({old_path.name}): {e}")

    print(f"  Converted: {converted}  |  "
          f"Total saved: {total_saved:.0f} KB\n")
    return src_to_new


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: HTML — Update src references + alt tags + semantic + meta + schema + OG
# ═══════════════════════════════════════════════════════════════════════════════
def update_html(src_to_new: dict):
    print("="*55)
    print("  📝 STEP 2: HTML Update")
    print("="*55)

    if not os.path.exists(HTML_FILE):
        print(f"  ❌ '{HTML_FILE}' nahi mila. Root folder se run karein.")
        return

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # ── 2a. Image src update (PNG → WebP renamed paths) ──────────────────────
    changes = 0
    for old_src, new_src in src_to_new.items():
        # Handle both forward and back slash + quote variants
        pattern = re.compile(
            r'(src=["\'])' + re.escape(old_src) + r'(["\'])',
            re.IGNORECASE
        )
        new_html, n = pattern.subn(rf'\g<1>{new_src}\g<2>', html)
        if n:
            html = new_html
            changes += n
            print(f"  🔄 src updated: {Path(old_src).name} → {Path(new_src).name}")

    print(f"  → {changes} image src updated\n")

    # ── 2b. Add alt tags to icon <img> that have empty alt="" ────────────────
    def fix_icon_alt(m):
        tag = m.group(0)
        # Find src
        src_m = re.search(r'src=["\']([^"\']+)["\']', tag)
        if not src_m:
            return tag
        filename = Path(src_m.group(1)).name
        alt_text = ICON_ALT_MAP.get(filename, "")
        if alt_text:
            # Replace empty alt
            tag = re.sub(r'alt=["\']["\']', f'alt="{alt_text}"', tag)
        return tag

    html = re.sub(r'<img\s[^>]*>', fix_icon_alt, html, flags=re.IGNORECASE)
    print("  ✅ Alt tags icon images pe add kiye\n")

    # ── 2c. Improve <html> lang attribute ────────────────────────────────────
    html = re.sub(r'<html\s+lang="en">', '<html lang="en-IN">', html)

    # ── 2d. Meta tags block (title, description, canonical, keywords) ─────────
    improved_head = """\
    <title>Work With Me | Kuber Consciousness &amp; Coaching — Sarvesh Mopkar</title>
    <meta name="description" content="Work with Sarvesh Mopkar — explore Kuber Consciousness (flagship), Millionaire Trader Mentorship, 1:1 Deep Work, and Energy Sessions for wealth expansion and inner transformation." />
    <meta name="keywords" content="Kuber Consciousness, Millionaire Trader Mentorship, Spiritual Finance Coaching, Sarvesh Mopkar, 1:1 Deep Work, Abundance Coach India, Energy Work Sessions, Wealth Consciousness" />
    <meta name="author" content="Sarvesh Mopkar" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="{base}/work-with-me.html" />""".format(base=BASE_URL)

    # Replace existing <title> + <meta description>
    html = re.sub(
        r'<title>.*?</title>\s*<meta\s+name="description"[^>]+>',
        improved_head,
        html,
        flags=re.DOTALL
    )
    print("  ✅ Meta title + description + canonical + keywords add kiye\n")

    # ── 2e. Open Graph + Twitter Card ─────────────────────────────────────────
    og_tags = """
    <!-- Open Graph -->
    <meta property="og:type"        content="website" />
    <meta property="og:url"         content="{base}/work-with-me.html" />
    <meta property="og:title"       content="Work With Me — Sarvesh Mopkar | Kuber Consciousness &amp; Coaching" />
    <meta property="og:description" content="Kuber Consciousness, Millionaire Trader Mentorship, 1:1 Deep Work &amp; Energy Sessions for wealth expansion and inner transformation." />
    <meta property="og:image"       content="images/home/sarvesh-mopkar-logo.webp" />
    <meta property="og:site_name"   content="Sarvesh Mopkar" />
    <meta property="og:locale"      content="en_IN" />
    <!-- Twitter Card -->
    <meta name="twitter:card"        content="summary_large_image" />
    <meta name="twitter:title"       content="Work With Me — Sarvesh Mopkar" />
    <meta name="twitter:description" content="Kuber Consciousness, Millionaire Trader Mentorship, 1:1 Deep Work &amp; Energy Sessions." />
    <meta name="twitter:image"       content="images/home/sarvesh-mopkar-logo.webp" />""".format(base=BASE_URL)

    if 'property="og:title"' in html:
        html = re.sub(
            r'<!-- Open Graph -->.*?<meta name="twitter:image"[^>]+/>',
            og_tags.strip(),
            html, flags=re.DOTALL
        )
        print("  🔄 OG + Twitter tags update kiye\n")
    else:
        html = html.replace("</head>", og_tags + "\n  </head>")
        print("  ✅ OG + Twitter Card tags add kiye\n")

    # ── 2f. Schema Markup ──────────────────────────────────────────────────────
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Work With Me — Sarvesh Mopkar",
            "description": "Explore offerings by Sarvesh Mopkar: Kuber Consciousness, Millionaire Trader Mentorship, 1:1 Deep Work, and Energy Sessions.",
            "url": BASE_URL + "/work-with-me.html",
            "author": {"@type": "Person", "name": "Sarvesh Mopkar"},
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1,
                     "name": "Home", "item": BASE_URL + "/index.html"},
                    {"@type": "ListItem", "position": 2,
                     "name": "Work With Me",
                     "item": BASE_URL + "/work-with-me.html"}
                ]
            }
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": "Kuber Consciousness Program",
            "description": "A deep immersion into abundance as a state of being. Subconscious reprogramming, wealth alignment, and energetic expansion with Sarvesh Mopkar.",
            "provider": {"@type": "Person", "name": "Sarvesh Mopkar",
                         "url": BASE_URL + "/about.html"},
            "url": BASE_URL + "/work-with-me.html#work-with-me",
            "serviceType": "Abundance & Wealth Consciousness Coaching",
            "areaServed": "IN",
            "offers": {"@type": "Offer", "availability": "https://schema.org/InStock",
                       "url": BASE_URL + "/contact.html"}
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": "Millionaire Trader Mentorship",
            "description": "For traders focused on psychology, risk discipline, emotional neutrality, and structured decision-making.",
            "provider": {"@type": "Person", "name": "Sarvesh Mopkar"},
            "url": BASE_URL + "/work-with-me.html",
            "serviceType": "Trading Psychology Mentorship",
            "areaServed": "IN"
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": "1:1 Deep Work Sessions",
            "description": "Private, high-level coaching for identity shifts, emotional patterns, wealth ceilings, and personal strategy alignment.",
            "provider": {"@type": "Person", "name": "Sarvesh Mopkar"},
            "url": BASE_URL + "/work-with-me.html",
            "serviceType": "Private Coaching",
            "areaServed": "IN"
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": "Energy Work, Experiences & Sessions",
            "description": "Sound-based healing, energy alignment processes, and consciousness work. Subtle, precise, transformative.",
            "provider": {"@type": "Person", "name": "Sarvesh Mopkar"},
            "url": BASE_URL + "/work-with-me.html",
            "serviceType": "Energy Healing & Consciousness Work",
            "areaServed": "IN"
        }
    ]

    schema_tag = ('<script type="application/ld+json">\n'
                  + json.dumps(schema, indent=2, ensure_ascii=False)
                  + '\n</script>')

    if "application/ld+json" in html:
        html = re.sub(
            r'<script type="application/ld\+json">.*?</script>',
            schema_tag, html, flags=re.DOTALL
        )
        print("  🔄 Schema markup update kiya\n")
    else:
        html = html.replace("</head>", schema_tag + "\n  </head>")
        print("  ✅ Schema markup add kiya (5 schemas)\n")

    # ── 2g. Semantic improvements ─────────────────────────────────────────────
    # Add role="main" to <main>
    html = re.sub(r'<main>', '<main id="main-content" role="main">', html)

    # Add aria-label to wwm-hero section
    html = re.sub(
        r'<section class="wwm-hero"',
        '<section class="wwm-hero" aria-labelledby="wwm-hero-heading"',
        html
    )
    html = re.sub(r'<h1>', '<h1 id="wwm-hero-heading">', html)

    # Add aria-label to closing section
    html = re.sub(
        r'<section class="wwm-closing">',
        '<section class="wwm-closing" aria-label="Transformation invitation">', html
    )

    # Skip-to-content link (accessibility)
    skip_link = '<a class="skip-link" href="#main-content">Skip to main content</a>\n    '
    if 'skip-link' not in html:
        html = html.replace('<div class="page-shell">', skip_link + '<div class="page-shell">')

    print("  ✅ Semantic tags improve kiye (aria-label, role, skip-link)\n")

    # ── Save ──────────────────────────────────────────────────────────────────
    # Backup original HTML
    if not os.path.exists(HTML_FILE + ".bak"):
        shutil.copy2(HTML_FILE, HTML_FILE + ".bak")
        print(f"  💾 Original HTML backup: {HTML_FILE}.bak\n")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✅ '{HTML_FILE}' save ho gaya!\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: Update sitemap.xml
# ═══════════════════════════════════════════════════════════════════════════════
def update_sitemap():
    print("="*55)
    print("  🗺️  STEP 3: Sitemap Update")
    print("="*55)

    new_entry = f"""  <url>
    <loc>{BASE_URL}/work-with-me.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>"""

    if not os.path.exists("sitemap.xml"):
        print("  ⚠️  sitemap.xml nahi mili — naya bana raha hoon...")
        sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                   + new_entry + "\n</urlset>")
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap)
        print("  ✅ sitemap.xml banaya\n")
        return

    with open("sitemap.xml", "r", encoding="utf-8") as f:
        sitemap = f.read()

    if "work-with-me.html" in sitemap:
        # Update lastmod
        sitemap = re.sub(
            r'(<loc>[^<]*work-with-me\.html</loc>\s*<lastmod>)[^<]*(</lastmod>)',
            rf'\g<1>{TODAY}\g<2>', sitemap
        )
        print("  🔄 work-with-me.html ka lastmod update kiya\n")
    else:
        sitemap = sitemap.replace("</urlset>", new_entry + "\n</urlset>")
        print("  ✅ work-with-me.html sitemap mein add kiya\n")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  Sarvesh Mopkar — Work With Me Complete Setup")
    print("="*55)
    print(f"  📅 Date: {TODAY}")
    print(f"  📄 Page: {HTML_FILE}")
    print(f"  📁 Folder: {IMG_FOLDER}")
    print("="*55)

    src_map = convert_and_rename_images()
    update_html(src_map)
    update_sitemap()

    print("="*55)
    print("  🎉 SABA KAM COMPLETE!")
    print()
    print("  ✅ Images → WebP convert + optimize + rename")
    print("  ✅ HTML src references update")
    print("  ✅ Alt tags add")
    print("  ✅ Semantic tags improve")
    print("  ✅ Meta title + description + canonical")
    print("  ✅ Open Graph + Twitter Card")
    print("  ✅ Schema markup (5 schemas)")
    print("  ✅ Sitemap update")
    print()
    print("  Ab GitHub pe push karo:")
    print('  git add .')
    print('  git commit -m "feat: work-with-me page full SEO setup"')
    print('  git push')
    print("="*55 + "\n")
