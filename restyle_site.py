#!/usr/bin/env python3
"""Restyle all HTML pages to MotionSites light + lime theme."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FAVICON = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
    "<rect width='100' height='100' rx='20' fill='%23111111'/>"
    "<text x='50' y='66' text-anchor='middle' font-size='40' font-family='system-ui' "
    "font-weight='800' fill='%23C8F542'>AI</text></svg>"
)

TAILWIND_CONFIG = """
<script>
  tailwind.config = {
    theme: {
      extend: {
        fontFamily: {
          display: ['Syne', 'sans-serif'],
          sans: ['Space Grotesk', 'system-ui', 'sans-serif'],
        },
        colors: {
          canvas: '#F4F4F5',
          ink: '#111111',
          mute: '#6B6B6B',
          line: '#E4E4E7',
          lime: { DEFAULT: '#C8F542', dim: '#A8D12A', soft: 'rgba(200, 245, 66, 0.2)' },
          panel: '#0A0A0A',
        }
      }
    }
  }
</script>
""".strip()


def head_assets(prefix: str) -> str:
    return f"""
  <link rel="icon" type="image/svg+xml" href="{FAVICON}">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@600;700;800&display=swap" rel="stylesheet">
  {TAILWIND_CONFIG}
  <link rel="stylesheet" href="{prefix}css/site.css">
""".rstrip()


def header(prefix: str, active: str) -> str:
    def link(name: str, href: str, is_cta: bool = False) -> str:
        url = prefix + href
        if is_cta:
            cls = "ml-2 cta-lime !py-2 !px-4 !text-sm"
            return f'<a href="{url}" class="{cls}" data-magnetic>{name}</a>'
        on = name.lower() == active
        cls = "px-3 py-2 text-sm font-medium" + ("" if on else " text-mute hover:text-ink transition-colors")
        return f'<a href="{url}" class="{cls}">{name}</a>'

    return f"""
  <div class="scroll-progress" data-scroll-progress aria-hidden="true"></div>
  <div class="page-spotlight" data-spotlight aria-hidden="true"></div>

  <header data-nav class="fixed top-0 inset-x-0 z-50">
    <nav class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-14 md:h-16">
        <a href="{prefix}index.html" class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-lg bg-ink text-lime font-display font-bold text-xs flex items-center justify-center">AI</span>
          <span class="font-display font-bold text-[15px] tracking-tight">AI Productivity</span>
        </a>
        <div class="hidden md:flex items-center gap-1">
          {link('Home', 'index.html')}
          {link('Blog', 'blog.html')}
          {link('About', 'about.html')}
          {link('Contact', 'contact.html', True)}
        </div>
        <button id="mobile-menu-btn" class="md:hidden p-2 text-ink" aria-label="Toggle menu">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 7h16M4 12h16M4 17h16"/>
          </svg>
        </button>
      </div>
      <div id="mobile-menu" class="hidden md:hidden pb-4 border-t border-line pt-3">
        <div class="flex flex-col gap-1">
          <a href="{prefix}index.html" class="px-3 py-3 text-sm font-medium">Home</a>
          <a href="{prefix}blog.html" class="px-3 py-3 text-sm font-medium text-mute">Blog</a>
          <a href="{prefix}about.html" class="px-3 py-3 text-sm font-medium text-mute">About</a>
          <a href="{prefix}contact.html" class="px-3 py-3 text-sm font-semibold">Contact</a>
        </div>
      </div>
    </nav>
  </header>
""".rstrip()


def footer(prefix: str) -> str:
    return f"""
  <footer class="site-footer">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
      <div class="grid md:grid-cols-4 gap-10 mb-12">
        <div class="md:col-span-2">
          <div class="flex items-center gap-2.5 mb-4">
            <span class="w-8 h-8 rounded-lg bg-ink text-lime font-display font-bold text-xs flex items-center justify-center">AI</span>
            <span class="font-display text-lg font-bold">AI Productivity</span>
          </div>
          <p class="text-mute text-sm mb-5 max-w-xs leading-relaxed">Daily AI &amp; tech insights for professionals who want to work smarter, not harder.</p>
        </div>
        <div>
          <h4 class="text-xs font-semibold mb-4 uppercase tracking-wider">Quick Links</h4>
          <ul class="space-y-2.5">
            <li><a href="{prefix}index.html" class="text-sm text-mute hover:text-ink transition-colors">Home</a></li>
            <li><a href="{prefix}blog.html" class="text-sm text-mute hover:text-ink transition-colors">Blog</a></li>
            <li><a href="{prefix}about.html" class="text-sm text-mute hover:text-ink transition-colors">About</a></li>
            <li><a href="{prefix}contact.html" class="text-sm text-mute hover:text-ink transition-colors">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-xs font-semibold mb-4 uppercase tracking-wider">Legal</h4>
          <ul class="space-y-2.5">
            <li><a href="{prefix}privacy.html" class="text-sm text-mute hover:text-ink transition-colors">Privacy Policy</a></li>
            <li><a href="{prefix}terms.html" class="text-sm text-mute hover:text-ink transition-colors">Terms of Service</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-line pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p class="text-xs text-mute">© 2025 AI Productivity. All rights reserved.</p>
        <p class="text-xs text-mute">Built with AI. Powered by curiosity.</p>
      </div>
    </div>
  </footer>
""".rstrip()


REPLACEMENTS = [
    # colors / surfaces
    (r"\bbg-dark-900\b", "bg-canvas"),
    (r"\bbg-dark-800\b", "bg-white"),
    (r"\bbg-dark-700\b", "bg-white"),
    (r"\bbg-dark-600\b", "bg-white"),
    (r"\bbg-dark-800/50\b", "bg-white"),
    (r"\bbg-dark-800/40\b", "bg-white"),
    (r"\bbg-dark-800/60\b", "bg-white"),
    (r"\btext-white\b", "text-ink"),
    (r"\btext-gray-300\b", "text-ink"),
    (r"\btext-gray-400\b", "text-mute"),
    (r"\btext-gray-500\b", "text-mute"),
    (r"\btext-gray-600\b", "text-mute"),
    (r"\btext-brand-400\b", "text-ink"),
    (r"\btext-brand-300\b", "text-ink"),
    (r"\bhover:text-brand-400\b", "hover:text-ink"),
    (r"\bhover:text-brand-300\b", "hover:text-ink"),
    (r"\bhover:text-white\b", "hover:text-ink"),
    (r"\bborder-white/5\b", "border-line"),
    (r"\bborder-white/10\b", "border-line"),
    (r"\bbg-brand-600\b", "bg-ink"),
    (r"\bhover:bg-brand-500\b", "hover:bg-ink"),
    (r"\bshadow-brand-500/20\b", ""),
    (r"\bshadow-brand-500/25\b", ""),
    (r"\bshadow-lg\b", ""),
    (r"\bshadow-xl\b", ""),
    (r"\baccent-gradient\b", "cta-lime"),
    (r"\bhero-gradient\b", "page-hero"),
    (r'style="background:\s*rgba\(10,10,15,0\.8\);?"', ""),
    (r'style="background:\s*linear-gradient\([^"]*\);?"', ""),
    (r'style="box-shadow:\s*[^"]*"', ""),
]


def strip_old_head_assets(html: str) -> str:
    # remove favicon / tailwind / fonts / config / style blocks commonly used
    html = re.sub(
        r'\s*<link rel="icon"[^>]*>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'\s*<script src="https://cdn\.tailwindcss\.com"></script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'\s*<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com"[^>]*>\s*'
        r'<link href="https://fonts\.googleapis\.com/css2\?family=Inter[^"]*" rel="stylesheet">',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'\s*<script>\s*tailwind\.config\s*=\s*\{.*?\}\s*</script>',
        "",
        html,
        flags=re.S | re.I,
    )
    # remove first big style block in head (page styles) — site.css replaces it
    html = re.sub(r"<style>.*?</style>", "", html, count=1, flags=re.S | re.I)
    return html


def replace_header(html: str, prefix: str, active: str) -> str:
    # from <!-- Header --> or <header to end of </header>
    pattern = re.compile(
        r"(?:<!--\s*Header\s*-->\s*)?<header\b[\s\S]*?</header>",
        re.I,
    )
    new = header(prefix, active)
    if pattern.search(html):
        return pattern.sub(new, html, count=1)
    # insert after <body...>
    return re.sub(r"(<body[^>]*>)", r"\1\n" + new, html, count=1, flags=re.I)


def replace_footer(html: str, prefix: str) -> str:
    pattern = re.compile(
        r"(?:<!--\s*Footer\s*-->\s*)?<footer\b[\s\S]*?</footer>",
        re.I,
    )
    new = footer(prefix)
    if pattern.search(html):
        return pattern.sub(new, html, count=1)
    return html


def inject_scripts(html: str, prefix: str) -> str:
    scripts = f"""
  <script src="{prefix}js/ui.js"></script>
  <script src="{prefix}js/motion.js"></script>
""".rstrip()
    # avoid duplicate
    if f'{prefix}js/motion.js' in html or "js/motion.js" in html:
        if f'{prefix}js/ui.js' not in html and "js/ui.js" not in html:
            html = html.replace(
                f'<script src="{prefix}js/motion.js"></script>',
                f'<script src="{prefix}js/ui.js"></script>\n  <script src="{prefix}js/motion.js"></script>',
            )
            html = html.replace(
                '<script src="js/motion.js"></script>',
                '<script src="js/ui.js"></script>\n  <script src="js/motion.js"></script>',
            )
        return html
    if re.search(r"</body>", html, re.I):
        return re.sub(r"</body>", scripts + "\n</body>", html, count=1, flags=re.I)
    return html + scripts


def apply_class_replacements(html: str) -> str:
    for pat, repl in REPLACEMENTS:
        html = re.sub(pat, repl, html)
    # cleanup double spaces in class attrs
    html = re.sub(r'class="\s+', 'class="', html)
    html = re.sub(r'\s{2,}', " ", html)
    html = re.sub(r' class="\s*"', "", html)
    return html


def detect_active(path: Path) -> str:
    name = path.name.lower()
    if "blog" in name:
        return "blog"
    if "about" in name:
        return "about"
    if "contact" in name:
        return "contact"
    if name.startswith("index"):
        return "home"
    return "blog" if "article" in name or path.parent.name == "posts_html" else "home"


def process_file(path: Path, skip_index_body: bool = False) -> None:
    rel = path.relative_to(ROOT)
    prefix = "../" if path.parent.name == "posts_html" else ""
    active = detect_active(path)
    html = path.read_text(encoding="utf-8")

    # For index.html keep structure but still refresh chrome if needed
    if path.name == "index.html":
        # index already styled — just ensure site.css link + ui.js
        if "css/site.css" not in html:
            html = re.sub(
                r"(</head>)",
                f'  <link rel="stylesheet" href="css/site.css">\n\\1',
                html,
                count=1,
                flags=re.I,
            )
        html = inject_scripts(html, "")
        # ensure body padding for fixed nav already handled
        path.write_text(html, encoding="utf-8")
        print(f"patched {rel}")
        return

    html = strip_old_head_assets(html)

    # inject head assets before </head>
    assets = head_assets(prefix)
    if "css/site.css" not in html:
        html = re.sub(r"</head>", assets + "\n</head>", html, count=1, flags=re.I)

    html = replace_header(html, prefix, active)
    html = replace_footer(html, prefix)
    html = apply_class_replacements(html)

    # body class
    html = re.sub(
        r'<body[^>]*>',
        '<body class="font-sans antialiased min-h-screen flex flex-col">',
        html,
        count=1,
        flags=re.I,
    )

    # fix sticky/old header remnants already replaced
    # page hero padding: add pt for fixed nav if page-hero
    html = html.replace('class="page-hero relative overflow-hidden"', 'class="page-hero"')

    # replace old mobile menu script blocks that only toggle menu — ui.js handles it
    html = re.sub(
        r"<script>\s*// Mobile menu toggle[\s\S]*?</script>",
        "",
        html,
        flags=re.I,
    )

    html = inject_scripts(html, prefix)

    # posts: fix root-relative index links already handled via prefix in header/footer
    # but in-content href="index.html" in posts need ../
    if prefix:
        for name in (
            "index.html",
            "blog.html",
            "about.html",
            "contact.html",
            "privacy.html",
            "terms.html",
            "article.html",
        ):
            html = html.replace(f'href="{name}"', f'href="{prefix}{name}"')
            # avoid double prefix
            html = html.replace(f'href="{prefix}{prefix}{name}"', f'href="{prefix}{name}"')

    path.write_text(html, encoding="utf-8")
    print(f"updated {rel}")


def main() -> None:
    # Main pages are hand-styled; only batch posts + adsense variants
    skip = {
        "index.html",
        "blog.html",
        "about.html",
        "contact.html",
        "privacy.html",
        "terms.html",
        "article.html",
    }
    files = [
        f
        for f in list(ROOT.glob("*.html")) + list((ROOT / "posts_html").glob("*.html"))
        if f.name not in skip
    ]
    for f in sorted(files):
        process_file(f)
    print(f"done — {len(files)} files")


if __name__ == "__main__":
    main()
