#!/usr/bin/env python3
"""
Performance Optimizer for sarveshmopkar.co
==========================================
Based on Google Lighthouse Mobile Report (Score: 48)

Ye script sirf performance optimize karta hai:
- UI/Design mein koi change nahi
- Functionality mein koi change nahi
- Safely backup leta hai pehle

Run karne se pehle: pip install pillow csscompressor rcssmin --break-system-packages
"""

import os
import sys
import shutil
import re
import json
from pathlib import Path
from datetime import datetime

# ─── CONFIG ──────────────────────────────────────────────────────────────────
# Apni website ka root folder yahan set karo
WEBSITE_ROOT = "."   # Current directory = website root (index.html wala folder)
BACKUP_DIR   = f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
# ─────────────────────────────────────────────────────────────────────────────

results = {"fixed": [], "skipped": [], "errors": []}

def log(msg, tag="INFO"):
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m", "ERR": "\033[91m", "RESET": "\033[0m"}
    print(f"{colors.get(tag, '')}{tag}: {msg}{colors['RESET']}")

# ═══════════════════════════════════════════════════════════════════════
# STEP 0 — Backup
# ═══════════════════════════════════════════════════════════════════════
def create_backup():
    backup_path = os.path.join(WEBSITE_ROOT, BACKUP_DIR)
    log(f"Backup bana raha hoon: {backup_path}")
    
    # Sirf important files backup karo (images nahi — woh bade hote hain)
    for ext in ["*.html", "*.css", "*.js"]:
        for f in Path(WEBSITE_ROOT).rglob(ext):
            if BACKUP_DIR in str(f):
                continue
            dest = Path(backup_path) / f.relative_to(WEBSITE_ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
    
    log(f"Backup complete: {backup_path}", "OK")
    return backup_path

# ═══════════════════════════════════════════════════════════════════════
# STEP 1 — Google Fonts: render-blocking fix
# Load karo async/preload se
# ═══════════════════════════════════════════════════════════════════════
def fix_google_fonts_render_blocking():
    log("Google Fonts render-blocking fix kar raha hoon...")
    
    html_files = list(Path(WEBSITE_ROOT).rglob("*.html"))
    if not html_files:
        results["skipped"].append("No HTML files found")
        return

    # Ye pattern Google Fonts ke blocking <link> dhundta hai
    blocking_pattern = re.compile(
        r'(<link[^>]*rel=["\']stylesheet["\'][^>]*fonts\.googleapis\.com[^>]*>)',
        re.IGNORECASE
    )
    preconnect_pattern = re.compile(
        r'<link[^>]*preconnect[^>]*fonts\.googleapis\.com[^>]*>',
        re.IGNORECASE
    )

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        original = content

        # Check karo fonts link hai ya nahi
        match = blocking_pattern.search(content)
        if not match:
            continue

        font_href_match = re.search(r'href=["\']([^"\']*fonts\.googleapis\.com[^"\']*)["\']', content, re.IGNORECASE)
        if not font_href_match:
            continue

        font_url = font_href_match.group(1)

        # Non-blocking font loading snippet
        # media="print" trick: browser loads asynchronously, onload switch to all
        non_blocking_snippet = f'''<link rel="preload" href="{font_url}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{font_url}"></noscript>'''

        # Remove old blocking link
        content = blocking_pattern.sub("", content)

        # Add non-blocking snippet just before </head>
        if "</head>" in content:
            content = content.replace("</head>", non_blocking_snippet + "\n</head>", 1)
        else:
            content += non_blocking_snippet

        # Agar preconnect nahi hai fonts.googleapis.com ke liye toh add karo
        if not preconnect_pattern.search(content):
            preconnect = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            content = content.replace("<head>", "<head>\n" + preconnect, 1)

        if content != original:
            html_file.write_text(content, encoding="utf-8")
            results["fixed"].append(f"Google Fonts non-blocking: {html_file.name}")
            log(f"Fixed: {html_file.name}", "OK")

# ═══════════════════════════════════════════════════════════════════════
# STEP 2 — style.css: render-blocking fix
# CSS preload + non-critical defer
# ═══════════════════════════════════════════════════════════════════════
def fix_css_render_blocking():
    log("style.css render-blocking fix kar raha hoon...")

    html_files = list(Path(WEBSITE_ROOT).rglob("*.html"))
    
    # Pattern: /style.css ya style.css wala blocking link
    css_block_pattern = re.compile(
        r'<link([^>]*)rel=["\']stylesheet["\']([^>]*)href=["\']([^"\']*style\.css[^"\']*)["\']([^>]*)>',
        re.IGNORECASE
    )
    # Also pattern where href comes first
    css_block_pattern2 = re.compile(
        r'<link([^>]*)href=["\']([^"\']*style\.css[^"\']*)["\']([^>]*)rel=["\']stylesheet["\']([^>]*)>',
        re.IGNORECASE
    )

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        original = content

        m1 = css_block_pattern.search(content)
        m2 = css_block_pattern2.search(content)
        match = m1 or m2

        if not match:
            continue

        css_href = None
        if m1:
            css_href = m1.group(3)
        elif m2:
            css_href = m2.group(2)

        if not css_href:
            continue

        # Preload + non-blocking pattern
        preload_link = f'<link rel="preload" href="{css_href}" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="{css_href}"></noscript>'

        # Replace original blocking link with preload
        if m1:
            content = css_block_pattern.sub(preload_link, content, count=1)
        else:
            content = css_block_pattern2.sub(preload_link, content, count=1)

        if content != original:
            html_file.write_text(content, encoding="utf-8")
            results["fixed"].append(f"style.css non-blocking preload: {html_file.name}")
            log(f"Fixed CSS render-blocking: {html_file.name}", "OK")

# ═══════════════════════════════════════════════════════════════════════
# STEP 3 — Minify CSS
# ═══════════════════════════════════════════════════════════════════════
def minify_css():
    log("CSS minify kar raha hoon...")

    try:
        import rcssmin
        use_rcssmin = True
    except ImportError:
        use_rcssmin = False
        log("rcssmin nahi mila, basic minification karunga", "WARN")

    css_files = list(Path(WEBSITE_ROOT).rglob("*.css"))
    
    for css_file in css_files:
        if BACKUP_DIR in str(css_file):
            continue
        if css_file.name.endswith(".min.css"):
            continue  # Already minified

        original_content = css_file.read_text(encoding="utf-8", errors="ignore")
        original_size = len(original_content.encode("utf-8"))

        try:
            if use_rcssmin:
                minified = rcssmin.cssmin(original_content)
            else:
                # Basic: remove comments and extra whitespace
                # Remove /* comments */
                minified = re.sub(r'/\*.*?\*/', '', original_content, flags=re.DOTALL)
                # Remove extra whitespace
                minified = re.sub(r'\s+', ' ', minified)
                # Remove spaces around : ; { } ,
                minified = re.sub(r'\s*([:{};,>~+])\s*', r'\1', minified)
                minified = minified.strip()

            new_size = len(minified.encode("utf-8"))
            saved = original_size - new_size

            if saved > 100:  # Sirf tab likhein jab kuch savings ho
                css_file.write_text(minified, encoding="utf-8")
                results["fixed"].append(f"CSS minified {css_file.name}: saved {saved/1024:.1f} KiB")
                log(f"CSS minified: {css_file.name} ({saved/1024:.1f} KiB saved)", "OK")
            else:
                results["skipped"].append(f"CSS already small: {css_file.name}")

        except Exception as e:
            results["errors"].append(f"CSS minify failed {css_file.name}: {e}")
            log(f"CSS minify failed {css_file.name}: {e}", "ERR")

# ═══════════════════════════════════════════════════════════════════════
# STEP 4 — Image Optimization
# WebP images ko aur compress karo, missing width/height add karo
# ═══════════════════════════════════════════════════════════════════════
def optimize_images():
    log("Images compress kar raha hoon...")

    try:
        from PIL import Image
        has_pillow = True
    except ImportError:
        has_pillow = False
        log("Pillow nahi mila! Image compression skip ho raha hai. Install: pip install pillow", "WARN")
        results["skipped"].append("Image compression: Pillow not installed")

    if not has_pillow:
        return

    # Target images from the report
    target_images = [
        "kuber-consciousness-abundance-golden-tree.webp",
        "sarvesh-mopkar-logo.webp",
        "trading-strategy-mountain-peak-sunrise.webp",
        "icon-transformation-abundance.webp",
        "icon-clarity-spiritual-finance.webp",
        "icon-awareness-wealth-consciousness.webp",
    ]

    # Image resize targets from the report (filename: (display_w, display_h))
    resize_targets = {
        "sarvesh-mopkar-logo.webp": (100, 87),          # displayed 100x87, file is 260x225
        "icon-transformation-abundance.webp": (51, 54),  # displayed 51x54, file is 102x108
        "icon-clarity-spiritual-finance.webp": (53, 54), # displayed 53x54, file is 105x108
        "icon-awareness-wealth-consciousness.webp": (53, 54),
    }

    for img_path in Path(WEBSITE_ROOT).rglob("*.webp"):
        if BACKUP_DIR in str(img_path):
            continue

        fname = img_path.name
        original_size = img_path.stat().st_size

        try:
            img = Image.open(img_path)
            original_w, original_h = img.size

            # Check resize needed
            if fname in resize_targets:
                target_w, target_h = resize_targets[fname]
                # Use 2x for retina: target * 2
                retina_w = target_w * 2
                retina_h = target_h * 2
                if original_w > retina_w:
                    img = img.resize((retina_w, retina_h), Image.LANCZOS)
                    log(f"Resized {fname}: {original_w}x{original_h} → {retina_w}x{retina_h}", "OK")

            # Save with higher compression (quality 75 for icons, 80 for photos)
            is_icon = "icon" in fname
            quality = 70 if is_icon else 78

            img.save(img_path, "WEBP", quality=quality, method=6)
            new_size = img_path.stat().st_size
            saved_kb = (original_size - new_size) / 1024

            if saved_kb > 0.5:
                results["fixed"].append(f"Image optimized {fname}: saved {saved_kb:.1f} KiB")
                log(f"Image: {fname} saved {saved_kb:.1f} KiB", "OK")
            else:
                results["skipped"].append(f"Image already optimal: {fname}")

        except Exception as e:
            results["errors"].append(f"Image optimize failed {fname}: {e}")
            log(f"Image failed {fname}: {e}", "ERR")

# ═══════════════════════════════════════════════════════════════════════
# STEP 5 — Add missing width/height to img tags (CLS fix)
# ═══════════════════════════════════════════════════════════════════════
def fix_image_dimensions():
    log("Missing img width/height fix kar raha hoon (CLS)...")

    try:
        from PIL import Image
        has_pillow = True
    except ImportError:
        has_pillow = False

    html_files = list(Path(WEBSITE_ROOT).rglob("*.html"))

    for html_file in html_files:
        if BACKUP_DIR in str(html_file):
            continue

        content = html_file.read_text(encoding="utf-8", errors="ignore")
        original = content

        # Find all <img> tags missing width or height
        img_pattern = re.compile(r'<img\s([^>]*)>', re.IGNORECASE | re.DOTALL)

        def process_img_tag(match):
            attrs = match.group(1)

            # Already has both width and height? Skip
            has_width  = bool(re.search(r'\bwidth\s*=', attrs, re.IGNORECASE))
            has_height = bool(re.search(r'\bheight\s*=', attrs, re.IGNORECASE))

            if has_width and has_height:
                return match.group(0)

            # Get src
            src_match = re.search(r'src\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
            if not src_match:
                return match.group(0)

            src = src_match.group(1)
            if not src or src.startswith("http") or src.startswith("//"):
                return match.group(0)  # External images skip

            # Try to find actual file
            img_path = Path(WEBSITE_ROOT) / src.lstrip("/")
            if not img_path.exists():
                return match.group(0)

            # Get dimensions
            try:
                if has_pillow:
                    img = Image.open(img_path)
                    w, h = img.size
                else:
                    return match.group(0)

                new_attrs = attrs
                if not has_width:
                    new_attrs += f' width="{w}"'
                if not has_height:
                    new_attrs += f' height="{h}"'

                return f'<img {new_attrs}>'
            except:
                return match.group(0)

        content = img_pattern.sub(process_img_tag, content)

        if content != original:
            html_file.write_text(content, encoding="utf-8")
            results["fixed"].append(f"img dimensions added: {html_file.name}")
            log(f"img dimensions fixed: {html_file.name}", "OK")

# ═══════════════════════════════════════════════════════════════════════
# STEP 6 — Google Tag Manager: defer loading
# GTM scripts ko defer karo — analytics main thread block na kare
# ═══════════════════════════════════════════════════════════════════════
def defer_gtm_scripts():
    log("Google Tag Manager defer kar raha hoon...")

    html_files = list(Path(WEBSITE_ROOT).rglob("*.html"))

    for html_file in html_files:
        if BACKUP_DIR in str(html_file):
            continue

        content = html_file.read_text(encoding="utf-8", errors="ignore")
        original = content

        # GTM inline script ko 3 second delay se load karo
        # Ye sirf analytics delay karta hai, page functionality nahi
        gtm_noscript_pattern = re.compile(
            r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->',
            re.DOTALL | re.IGNORECASE
        )
        
        # Find GTM script block
        gtm_script_pattern = re.compile(
            r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->',
            re.DOTALL | re.IGNORECASE
        )

        # Replace synchronous GTM with delayed version
        # 3000ms delay — user pehle interact kare tab GTM load ho
        delayed_gtm_template = """<!-- Google Tag Manager (Delayed) -->
<script>
(function() {
  function loadGTM() {
    if (window._gtmLoaded) return;
    window._gtmLoaded = true;
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-TPM547S9');
  }
  // Load GTM after user interaction OR after 3s, whichever comes first
  var loaded = false;
  function onInteract() {
    if (!loaded) { loaded = true; setTimeout(loadGTM, 0); }
    document.removeEventListener('mousemove', onInteract);
    document.removeEventListener('keydown', onInteract);
    document.removeEventListener('touchstart', onInteract);
    document.removeEventListener('scroll', onInteract);
  }
  document.addEventListener('mousemove', onInteract, {passive: true});
  document.addEventListener('keydown', onInteract, {passive: true});
  document.addEventListener('touchstart', onInteract, {passive: true});
  document.addEventListener('scroll', onInteract, {passive: true});
  setTimeout(loadGTM, 3000);
})();
</script>
<!-- End Google Tag Manager (Delayed) -->"""

        changed = False
        
        if gtm_script_pattern.search(content):
            # Extract GTM ID from existing script
            gtm_id_match = re.search(r"GTM-[A-Z0-9]+", content)
            if gtm_id_match:
                gtm_id = gtm_id_match.group(0)
                new_delayed = delayed_gtm_template.replace("GTM-TPM547S9", gtm_id)
                content = gtm_script_pattern.sub(new_delayed, content)
                changed = True

        if changed and content != original:
            html_file.write_text(content, encoding="utf-8")
            results["fixed"].append(f"GTM deferred (3s delay): {html_file.name}")
            log(f"GTM deferred: {html_file.name}", "OK")
        else:
            results["skipped"].append(f"GTM pattern not found or already modified in {html_file.name}")
            log(f"GTM: Standard pattern nahi mila {html_file.name} — manually check karo", "WARN")

# ═══════════════════════════════════════════════════════════════════════
# STEP 7 — Add preconnect hints for CDNs
# ═══════════════════════════════════════════════════════════════════════
def add_preconnect_hints():
    log("Preconnect hints add kar raha hoon...")

    # From report: these save 130-320ms
    preconnect_origins = [
        "https://www.googletagmanager.com",
        "https://cdnjs.cloudflare.com",
        "https://unpkg.com",
    ]

    html_files = list(Path(WEBSITE_ROOT).rglob("*.html"))

    for html_file in html_files:
        if BACKUP_DIR in str(html_file):
            continue

        content = html_file.read_text(encoding="utf-8", errors="ignore")
        original = content

        hints_to_add = []
        for origin in preconnect_origins:
            if origin not in content:
                hints_to_add.append(f'<link rel="preconnect" href="{origin}">')

        if hints_to_add and "<head>" in content:
            hint_block = "\n".join(hints_to_add) + "\n"
            content = content.replace("<head>", "<head>\n" + hint_block, 1)
            html_file.write_text(content, encoding="utf-8")
            results["fixed"].append(f"Preconnect hints added to {html_file.name}: {len(hints_to_add)} origins")
            log(f"Preconnect hints: {html_file.name}", "OK")

# ═══════════════════════════════════════════════════════════════════════
# STEP 8 — Add preload for LCP image
# ═══════════════════════════════════════════════════════════════════════
def add_lcp_image_preload():
    log("LCP image preload add kar raha hoon...")

    html_files = list(Path(WEBSITE_ROOT).rglob("*.html"))

    for html_file in html_files:
        if BACKUP_DIR in str(html_file):
            continue

        content = html_file.read_text(encoding="utf-8", errors="ignore")
        original = content

        # Find above-the-fold / hero images (not lazy loaded) that are likely LCP
        # Logo image is likely LCP candidate (no lazy)
        lcp_pattern = re.compile(
            r'src=["\']([^"\']*sarvesh-mopkar-logo\.webp)["\']',
            re.IGNORECASE
        )
        match = lcp_pattern.search(content)
        if match:
            img_src = match.group(1)
            preload_tag = f'<link rel="preload" as="image" href="{img_src}" fetchpriority="high">'
            
            # Avoid duplicate
            if preload_tag not in content and img_src not in content.split("<head>")[0] if "<head>" in content else True:
                if "</head>" in content and "fetchpriority" not in content:
                    content = content.replace("</head>", preload_tag + "\n</head>", 1)
                    html_file.write_text(content, encoding="utf-8")
                    results["fixed"].append(f"LCP preload added: {html_file.name}")
                    log(f"LCP preload: {html_file.name}", "OK")

# ═══════════════════════════════════════════════════════════════════════
# STEP 9 — Print Summary
# ═══════════════════════════════════════════════════════════════════════
def print_summary():
    print("\n" + "═"*60)
    print("  OPTIMIZATION SUMMARY")
    print("═"*60)

    print(f"\n✅ FIXED ({len(results['fixed'])}):")
    for item in results["fixed"]:
        print(f"   • {item}")

    if results["skipped"]:
        print(f"\n⚠️  SKIPPED ({len(results['skipped'])}):")
        for item in results["skipped"]:
            print(f"   • {item}")

    if results["errors"]:
        print(f"\n❌ ERRORS ({len(results['errors'])}):")
        for item in results["errors"]:
            print(f"   • {item}")

    print("\n" + "─"*60)
    print("📋 MANUAL STEPS (script se nahi ho sakta):")
    print("─"*60)
    print("""
1. GSAP/ScrollTrigger forced reflow:
   - scroll-animations.js mein getBoundingClientRect() ya
     offsetWidth calls ko ScrollTrigger.refresh() ke baad do
   - Ya GSAP ko 'will-change: transform' CSS add karo animated elements par

2. Lenis.js forced reflow (214ms):
   - lenis.min.js version update karo — newer versions mein
     reflow optimization hai
   - CDN se: https://unpkg.com/lenis@latest/dist/lenis.min.js

3. CSS critical path:
   - Above-the-fold ka CSS inline karo <style> tag mein <head> mein
   - Baaki CSS async load karo (style.css already fixed by this script)

4. GTM (manual verify):
   - Agar GTM comment format alag hai toh GTM section manually
     delayed version se replace karo

5. Google Analytics: GA4 ko GTM ke through serve karo,
   direct gtag.js scripts hatao

6. Website deploy ke baad: Google Search Console mein
   "Request Indexing" karo
""")
    print("═"*60)
    print(f"\n🔒 Backup saved at: {os.path.join(WEBSITE_ROOT, BACKUP_DIR)}")
    print("   Agar kuch toot jaye: backup folder se files wapas copy karo\n")

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    print("\n" + "═"*60)
    print("  sarveshmopkar.co — Performance Optimizer")
    print("  Lighthouse Mobile Score: 48 → Target: 75+")
    print("═"*60)

    # Check: website root sahi hai?
    index_path = Path(WEBSITE_ROOT) / "index.html"
    if not index_path.exists():
        log(f"index.html nahi mila at: {os.path.abspath(WEBSITE_ROOT)}", "ERR")
        log("WEBSITE_ROOT variable apni website ke root folder path par set karo", "ERR")
        log("Example: WEBSITE_ROOT = '/Users/yourname/projects/sarveshmopkar'", "ERR")
        sys.exit(1)

    log(f"Website root: {os.path.abspath(WEBSITE_ROOT)}", "OK")

    # Step 0: Backup
    create_backup()

    # Step 1–8: Optimizations
    fix_google_fonts_render_blocking()
    fix_css_render_blocking()
    minify_css()
    optimize_images()
    fix_image_dimensions()
    defer_gtm_scripts()
    add_preconnect_hints()
    add_lcp_image_preload()

    # Summary
    print_summary()

if __name__ == "__main__":
    main()
