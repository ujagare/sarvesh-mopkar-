"""
fix_website.py
--------------
Ye script aapki puri website ke sabhi issues fix karti hai:

1. "Spiritual Finance" word remove/replace
2. Galat GitHub URLs fix (ujagare.github.io → sarveshmopkar.co)
3. Copyright 2024 → 2026
4. OG image relative path → full URL
5. Contact form mein Supabase integration add

USAGE:
  python fix_website.py --folder . --supabase-url YOUR_URL --supabase-key YOUR_KEY

EXAMPLE:
  python fix_website.py --folder . --supabase-url https://yhspeotjjjkeryodqxtn.supabase.co --supabase-key eyJhbGci...

Agar Supabase keys baad mein dalni hain:
  python fix_website.py --folder .
"""

import os
import re
import shutil
import argparse
from datetime import datetime

# ─── Configuration ────────────────────────────────────────────────────────────

SITE_URL = "https://www.sarveshmopkar.co"
OLD_GITHUB_URL = "https://ujagare.github.io/sarvesh-mopkar-"

# Spiritual Finance replacements (specific pehle, generic baad mein)
SPIRITUAL_REPLACEMENTS = [
    ("Spiritual Finance &amp; Abundance Coach",     "Abundance &amp; Wealth Coach"),
    ("Spiritual Finance & Abundance Coach",         "Abundance & Wealth Coach"),
    ("Spiritual-Finance &amp; Abundance Coach",     "Abundance &amp; Wealth Coach"),
    ("Spiritual-Finance & Abundance Coach",         "Abundance & Wealth Coach"),
    ("Spiritual Finance coach",                     "Abundance & Wealth coach"),
    ("Spiritual-Finance coach",                     "Abundance & Wealth coach"),
    ("Premium Spiritual-Finance coach",             "Premium Abundance & Wealth coach"),
    ("Premium Spiritual Finance coach",             "Premium Abundance & Wealth coach"),
    ("Spiritual Finance Coach",                     "Abundance & Wealth Coach"),
    ("Spiritual-Finance Coach",                     "Abundance & Wealth Coach"),
    ("Spiritual Finance",                           "Abundance Coaching"),
    ("Spiritual-Finance",                           "Abundance Coaching"),
]

# Supabase script jo contact form mein add hoga
SUPABASE_SCRIPT = """
    <!-- Supabase Contact Form Integration -->
    <script type="module">
      const SUPABASE_URL = '{supabase_url}';
      const SUPABASE_ANON_KEY = '{supabase_key}';

      const form = document.querySelector('[data-contact-form]');
      const status = document.querySelector('[data-contact-status]');

      if (form) {{
        form.addEventListener('submit', async (e) => {{
          e.preventDefault();

          // Honeypot spam protection
          if (form.company && form.company.value) return;

          const name    = form.name.value.trim();
          const email   = form.email.value.trim();
          const subject = form.subject?.value.trim() || '';
          const message = form.message.value.trim();

          const btn = form.querySelector('button[type="submit"]');
          btn.disabled = true;
          status.textContent = 'Sending...';
          status.style.color = '';

          try {{
            const res = await fetch(`${{SUPABASE_URL}}/rest/v1/contacts`, {{
              method: 'POST',
              headers: {{
                'Content-Type': 'application/json',
                'apikey': SUPABASE_ANON_KEY,
                'Authorization': `Bearer ${{SUPABASE_ANON_KEY}}`,
                'Prefer': 'return=minimal'
              }},
              body: JSON.stringify({{ name, email, subject, message }})
            }});

            if (res.ok) {{
              status.textContent = '✅ Message sent! I will get back to you soon.';
              status.style.color = 'green';
              form.reset();
            }} else {{
              const err = await res.json();
              throw new Error(err.message || 'Something went wrong');
            }}
          }} catch (err) {{
            console.error(err);
            status.textContent = '❌ Something went wrong. Please try again or email directly.';
            status.style.color = 'red';
          }} finally {{
            btn.disabled = false;
          }}
        }});
      }}
    </script>
"""


# ─── Helper Functions ─────────────────────────────────────────────────────────

def backup_folder(folder):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = folder.rstrip("/\\") + f"_backup_{timestamp}"
    shutil.copytree(folder, backup_path)
    print(f"✅ Backup bana diya: {backup_path}\n")
    return backup_path


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def fix_spiritual_finance(content):
    """Spiritual Finance words replace karo."""
    changes = []
    for old, new in SPIRITUAL_REPLACEMENTS:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        count = len(pattern.findall(content))
        if count:
            content = pattern.sub(new, content)
            changes.append(f"    🔤 '{old}' → '{new}'  ({count}x)")
    return content, changes


def fix_github_urls(content):
    """Galat GitHub URLs ko sahi domain se replace karo."""
    changes = []
    pattern = re.compile(re.escape(OLD_GITHUB_URL), re.IGNORECASE)
    count = len(pattern.findall(content))
    if count:
        content = pattern.sub(SITE_URL, content)
        changes.append(f"    🔗 GitHub URL → sarveshmopkar.co  ({count}x)")
    return content, changes


def fix_copyright(content):
    """Copyright year 2024 → 2026."""
    changes = []
    patterns = [
        (r'© 2024 Sarvesh', '© 2026 Sarvesh'),
        (r'&copy; 2024 Sarvesh', '&copy; 2026 Sarvesh'),
        (r'Â© 2024 Sarvesh', '© 2026 Sarvesh'),
        (r'Â© 2026 Sarvesh', '© 2026 Sarvesh'),  # Fix encoding issue
    ]
    for old, new in patterns:
        if re.search(old, content):
            content = re.sub(old, new, content)
            changes.append(f"    📅 Copyright year fixed → 2026")
            break
    return content, changes


def fix_og_image(content, filename):
    """Relative OG image paths ko full URL se replace karo."""
    changes = []
    # Relative path patterns
    patterns = [
        (r'content="images/home/sarvesh-mopkar-logo\.webp"',
         f'content="{SITE_URL}/images/home/sarvesh-mopkar-logo.webp"'),
        (r"content='images/home/sarvesh-mopkar-logo\.webp'",
         f"content='{SITE_URL}/images/home/sarvesh-mopkar-logo.webp'"),
    ]
    for pattern, replacement in patterns:
        count = len(re.findall(pattern, content))
        if count:
            content = re.sub(pattern, replacement, content)
            changes.append(f"    🖼️  OG image relative path → full URL  ({count}x)")
    return content, changes


def add_supabase_to_contact(content, supabase_url, supabase_key):
    """Contact.html mein Supabase script add karo."""
    changes = []

    # Check karo already added hai ya nahi
    if 'SUPABASE_URL' in content or 'supabase' in content.lower():
        changes.append("    ⚠️  Supabase script already exists — skip kiya")
        return content, changes

    script = SUPABASE_SCRIPT.format(
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )

    # </body> se pehle add karo
    if '</body>' in content:
        content = content.replace('</body>', script + '\n  </body>')
        changes.append("    🔌 Supabase contact form integration added")
    else:
        changes.append("    ❌ </body> tag nahi mila — manual add karna hoga")

    return content, changes


def process_file(filepath, filename, supabase_url, supabase_key):
    """Ek file ke sabhi fixes karo."""
    content = read_file(filepath)
    original = content
    all_changes = []

    # 1. Spiritual Finance fix
    content, changes = fix_spiritual_finance(content)
    all_changes.extend(changes)

    # 2. GitHub URLs fix
    content, changes = fix_github_urls(content)
    all_changes.extend(changes)

    # 3. Copyright fix
    content, changes = fix_copyright(content)
    all_changes.extend(changes)

    # 4. OG image fix
    content, changes = fix_og_image(content, filename)
    all_changes.extend(changes)

    # 5. Supabase (sirf contact.html mein)
    if filename == 'contact.html' and supabase_url and supabase_key:
        content, changes = add_supabase_to_contact(content, supabase_url, supabase_key)
        all_changes.extend(changes)

    if content != original:
        write_file(filepath, content)

    return all_changes


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Sarvesh Mopkar website ke sabhi issues fix karo"
    )
    parser.add_argument("--folder", required=True, help="Website root folder")
    parser.add_argument("--supabase-url", default="https://yhspeotjjjkeryodqxtn.supabase.co",
                        help="Supabase project URL")
    parser.add_argument("--supabase-key", default="APNI_PUBLISHABLE_KEY_YAHAN_DAALO",
                        help="Supabase anon/publishable key")
    parser.add_argument("--no-backup", action="store_true", help="Backup skip karo")
    args = parser.parse_args()

    folder = os.path.abspath(args.folder)

    if not os.path.isdir(folder):
        print(f"❌ ERROR: Folder nahi mila: {folder}")
        return

    print(f"\n📁 Folder: {folder}")
    print("=" * 60)

    # Backup
    if not args.no_backup:
        backup_folder(folder)

    # Sabhi HTML files
    html_files = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if "_backup_" not in d]
        for file in files:
            if file.endswith((".html", ".htm")):
                html_files.append((os.path.join(root, file), file))

    if not html_files:
        print("⚠️  Koi HTML file nahi mili!")
        return

    print(f"🔍 {len(html_files)} HTML files mili\n")

    total_changed = 0

    for filepath, filename in html_files:
        rel_path = os.path.relpath(filepath, folder)
        changes = process_file(filepath, filename, args.supabase_url, args.supabase_key)

        if changes:
            total_changed += 1
            print(f"✏️  {rel_path}")
            for c in changes:
                print(c)
            print()

    print("=" * 60)
    if total_changed:
        print(f"✅ {total_changed} files fix ho gayi!\n")
        print("📌 Ab karo:")
        print("   1. vercel --prod (deploy karo)")
        print("   2. Google Search Console mein Request Indexing karo")
    else:
        print("ℹ️  Koi issue nahi mila — sab already sahi hai!")

    if args.supabase_key == "APNI_PUBLISHABLE_KEY_YAHAN_DAALO":
        print("\n⚠️  IMPORTANT: Supabase key add nahi ki!")
        print("   Run karo: python fix_website.py --folder . --supabase-key TUMHARI_KEY")


if __name__ == "__main__":
    main()
