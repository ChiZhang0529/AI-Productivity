"""
convert_dark.py - Regenerate all posts_html with the new dark theme design.
Reference: https://theainest.com/ style - dark theme, modern aesthetics
"""
import os
import re
from datetime import datetime

PYTHON = "C:/Users/54463/AppData/Local/Programs/Python/Python311/python.exe"
POSTS_DIR = "C:/Users/54463/WorkBuddy/2026-05-13-task-6/static-blog/posts"
OUTPUT_DIR = "C:/Users/54463/WorkBuddy/2026-05-13-task-6/static-blog/posts_html"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Stopwords for tag generation
STOPWORDS = set(['a','an','the','and','or','but','in','on','at','to','for','of','with','by','from','as','is','was','are','were','be','been','being','have','has','had','do','does','did','will','would','could','should','may','might','must','shall','can','need','that','which','who','whom','this','these','those','it','its','they','them','their','we','our','you','your','i','my','me','how','what','when','where','why','all','each','every','both','few','more','most','other','some','such','no','not','only','same','so','than','too','very','just','also','now','here','there','then','if','about','into','through','during','before','after','above','below','between','under','again','further','while','same','get','got','use','using','make','made','take','took','come','came','go','goes','going','went','gone','see','saw','seen','know','knew','known','think','thought','want','wanted','like','look','looked','find','found','give','gave','given','tell','told','say','said','set','put','set','keep','kept','let','begin','began','begun','seem','seemed','help','helped','show','showed','shown','hear','heard','play','played','run','ran','move','moved','live','lived','believe','brought','happened','write','wrote','written','provide','provided','sit','stood','lose','lost','pay','paid','meet','met','include','included','continue','continued','change','changed','watch','watched','follow','followed','stop','stopped','create','created','speak','spoke','spoken','read','allow','allowed','add','added','spend','spent','grow','grew','grown','open','opened','walk','walked','win','won','offer','offered','remember','remembered','love','loved','consider','considered','appear','appeared','buy','bought','wait','waited','serve','served','die','died','send','sent','expect','expected','build','built','stay','stayed','fall','fell','fallen','cut','reach','reached','kill','remained','suggest','suggested','raise','raised','pass','passed','sell','sold','require','required','report','reported','decide','decided','pull','pulled'])

# Category keywords mapping
CAT_KEYWORDS = {
    'ChatGPT': ['chatgpt', 'gpt', 'openai', 'conversation', 'prompt', 'chat'],
    'Productivity': ['productivity', 'productive', 'efficient', 'efficiently', 'workflow', 'focus', 'habit', 'routine'],
    'Automation': ['automation', 'automate', 'zapier', 'make', 'workflow', 'script', 'bot', 'auto'],
    'Writing': ['writing', 'write', 'blog', 'content', 'copy', '文案', '写作'],
    'AI Tools': ['tool', 'app', 'software', 'platform', 'claude', 'gemini', 'midjourney', 'stable', 'runway'],
}

def get_category(title, excerpt):
    text = (title + ' ' + excerpt).lower()
    best_cat = 'General'
    best_score = 0
    for cat, keywords in CAT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_cat = cat
    return best_cat

def get_tags(title, excerpt):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', (title + ' ' + excerpt).lower())
    tags = [w for w in words if w not in STOPWORDS][:6]
    seen = set()
    unique = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique.append(t.title())
    return unique[:6]

def md2html(text):
    lines = text.split('\n')
    html = []
    in_ul = False
    in_ol = False
    in_bq = False
    in_pre = False
    in_table = False
    table_rows = []
    row_cells = []
    
    def close_ul():
        nonlocal in_ul
        if in_ul:
            html.append('</ul>')
            in_ul = False
    
    def close_ol():
        nonlocal in_ol
        if in_ol:
            html.append('</ol>')
            in_ol = False
    
    def close_bq():
        nonlocal in_bq
        if in_bq:
            html.append('</blockquote>')
            in_bq = False
    
    def close_pre():
        nonlocal in_pre
        if in_pre:
            html.append('</code></pre>')
            in_pre = False
    
    def close_table():
        nonlocal in_table, table_rows
        if in_table:
            if table_rows:
                html.append('<table>')
                for i, row in enumerate(table_rows):
                    tag = 'th' if i == 0 else 'td'
                    html.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in row) + '</tr>')
                html.append('</table>')
            in_table = False
            table_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Code block
        if line.strip().startswith('```'):
            close_ul(); close_ol(); close_bq(); close_table()
            if in_pre:
                html.append('</code></pre>')
                in_pre = False
            else:
                lang = line.strip()[3:].strip()
                html.append('<pre><code class="language-' + lang + '">')
                in_pre = True
            i += 1
            continue
        
        if in_pre:
            html.append('\n' + line)
            i += 1
            continue
        
        # Tables
        if '|' in line and line.strip().startswith('|'):
            close_ul(); close_ol(); close_bq()
            row = [c.strip() for c in line.strip().strip('|').split('|')]
            if all(re.match(r'^[-:]+$', c.strip()) for c in row):
                i += 1
                continue
            table_rows.append(row)
            in_table = True
            i += 1
            continue
        else:
            close_table()
        
        # Headings
        m = re.match(r'^(#{1,4})\s+(.+)', line)
        if m:
            close_ul(); close_ol(); close_bq()
            level = len(m.group(1))
            text = m.group(2).strip()
            html.append(f'<h{level}>{inline(text)}</h{level}>')
            i += 1
            continue
        
        # HR
        if re.match(r'^---+$', line.strip()):
            close_ul(); close_ol(); close_bq()
            html.append('<hr>')
            i += 1
            continue
        
        # Blockquote
        if line.strip().startswith('>'):
            close_ul(); close_ol()
            if not in_bq:
                html.append('<blockquote>')
                in_bq = True
            content = line.lstrip('>').strip()
            html.append(f'<p>{inline(content)}</p>')
            i += 1
            continue
        else:
            close_bq()
        
        # UL
        m = re.match(r'^[-*+]\s+(.+)', line)
        if m:
            close_ol()
            if not in_ul:
                html.append('<ul>')
                in_ul = True
            html.append(f'<li>{inline(m.group(1).strip())}</li>')
            i += 1
            continue
        else:
            close_ul()
        
        # OL
        m = re.match(r'^\d+\.\s+(.+)', line)
        if m:
            close_ul()
            if not in_ol:
                html.append('<ol>')
                in_ol = True
            html.append(f'<li>{inline(m.group(1).strip())}</li>')
            i += 1
            continue
        else:
            close_ol()
        
        # Empty line
        if not line.strip():
            close_ul(); close_ol(); close_bq()
            i += 1
            continue
        
        # Paragraph
        html.append(f'<p>{inline(line.strip())}</p>')
        i += 1
    
    close_ul(); close_ol(); close_bq(); close_pre(); close_table()
    return '\n'.join(html)

def inline(text):
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text

def get_meta(text, fname):
    lines = text.split('\n')
    title = fname.replace('.md', '').replace('-', ' ').title()
    excerpt = ''
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    body_lines = []
    capturing = False
    for line in lines:
        if line.startswith('# '):
            capturing = True
            continue
        if capturing:
            line_s = line.strip()
            if line_s and not line_s.startswith('#'):
                body_lines.append(line_s)
        if len(body_lines) >= 2:
            break
    excerpt = ' '.join(body_lines[:2])[:200]
    if not excerpt:
        excerpt = 'Read more about ' + title + ' and how AI can transform your workflow.'
    cat = get_category(title, excerpt)
    tags = get_tags(title, excerpt)
    return title, excerpt, cat, tags

# Dark-themed post HTML template
POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ | AINest</title>
  <meta name="title" content="__TITLE__ | AINest">
  <meta name="description" content="__EXCERPT__">
  <meta name="robots" content="index, follow">
  <meta property="og:type" content="article">
  <meta property="og:title" content="__TITLE__">
  <meta property="og:description" content="__EXCERPT__">
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:title" content="__TITLE__">
  <meta property="twitter:description" content="__EXCERPT__">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
          colors: {
            brand: { 400: '#36b0f7', 500: '#0e8de8', 600: '#0070c4', 700: '#01599f' },
            dark: { 900: '#0a0a0f', 800: '#111118', 700: '#1a1a24', 600: '#22222e', 500: '#2a2a38' }
          }
        }
      }
    }
  </script>
  <style>
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', system-ui, sans-serif; background-color: #0a0a0f; color: #e2e8f0; }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #111118; }
    ::-webkit-scrollbar-thumb { background: #333344; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #4a4a5e; }
    .accent-gradient { background: linear-gradient(135deg, #0e8de8, #7c3aed); }
    .prose h2 { font-size: 1.5rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; color: #f1f5f9; border-bottom: 1px solid #1f1f2e; padding-bottom: 0.75rem; }
    .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; color: #f1f5f9; }
    .prose h4 { font-size: 1.125rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; color: #f1f5f9; }
    .prose p { margin-bottom: 1rem; color: #cbd5e1; line-height: 1.8; }
    .prose ul { list-style-type: disc; list-style-position: inside; margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
    .prose ol { list-style-type: decimal; list-style-position: inside; margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
    .prose li { color: #cbd5e1; }
    .prose strong { font-weight: 600; color: #f1f5f9; }
    .prose em { font-style: italic; }
    .prose blockquote { border-left: 3px solid #0e8de8; padding-left: 1rem; font-style: italic; color: #94a3b8; margin: 1.5rem 0; background: rgba(14,141,232,0.05); padding: 1rem 1.5rem; border-radius: 0 0.5rem 0.5rem 0; }
    .prose code { background: #1a1a24; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.875rem; font-family: 'Fira Code', 'Consolas', monospace; color: #7dd3fc; }
    .prose pre { background: #0d0d14; border: 1px solid #22222e; color: #e2e8f0; padding: 1.25rem; border-radius: 0.75rem; overflow-x: auto; margin: 1.5rem 0; font-size: 0.875rem; line-height: 1.7; }
    .prose pre code { background: transparent; padding: 0; color: inherit; }
    .prose hr { border-color: #1f1f2e; margin: 2rem 0; }
    .prose table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; }
    .prose th { border: 1px solid #2a2a38; background: #111118; padding: 0.625rem 1rem; text-align: left; font-weight: 600; color: #e2e8f0; }
    .prose td { border: 1px solid #2a2a38; padding: 0.625rem 1rem; color: #cbd5e1; }
    .prose tr:nth-child(even) { background: #0f0f18; }
    .prose a { color: #0e8de8; text-decoration: none; border-bottom: 1px solid rgba(14,141,232,0.3); transition: all 0.2s; }
    .prose a:hover { color: #7dd3fc; border-bottom-color: #7dd3fc; }
    .tag-pill { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; background: rgba(14,141,232,0.1); color: #7dd3fc; border: 1px solid rgba(14,141,232,0.2); }
    .category-badge { display: inline-flex; align-items: center; padding: 0.25rem 0.625rem; border-radius: 0.375rem; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .share-btn { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; background: #1a1a24; border: 1px solid #2a2a38; color: #94a3b8; transition: all 0.2s; }
    .share-btn:hover { background: #22222e; color: white; border-color: #3a3a4e; transform: translateY(-2px); }
    .newsletter-input { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; transition: all 0.3s; border-radius: 0.75rem; }
    .newsletter-input:focus { outline: none; border-color: #0e8de8; background: rgba(255,255,255,0.08); box-shadow: 0 0 0 3px rgba(14,141,232,0.15); }
    .newsletter-input::placeholder { color: #64748b; }
    .card-glow:hover { box-shadow: 0 0 40px rgba(14,141,232,0.08), 0 4px 20px rgba(0,0,0,0.4); }
    .hero-gradient { background: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(14,141,232,0.15), transparent); }
  </style>
</head>
<body class="font-sans antialiased min-h-screen flex flex-col">

  <!-- Header -->
  <header class="sticky top-0 z-50 border-b border-white/5 backdrop-blur-xl" style="background: rgba(10,10,15,0.8);">
    <nav class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <a href="index.html" class="flex items-center gap-2 group">
          <div class="w-8 h-8 rounded-lg accent-gradient flex items-center justify-center text-white font-bold text-sm shadow-lg" style="box-shadow: 0 0 20px rgba(14,141,232,0.3);">AI</div>
          <span class="text-lg font-bold text-white group-hover:text-brand-400 transition-colors">AINest</span>
        </a>
        <div class="hidden md:flex items-center gap-1">
          <a href="index.html" class="px-4 py-2 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-all">Home</a>
          <a href="blog.html" class="px-4 py-2 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-all">Blog</a>
          <a href="about.html" class="px-4 py-2 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-all">About</a>
          <a href="contact.html" class="ml-2 px-4 py-2 rounded-lg text-sm font-medium bg-brand-600 hover:bg-brand-500 text-white transition-all shadow-lg" style="box-shadow: 0 0 20px rgba(0,112,196,0.3);">Contact</a>
        </div>
        <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-colors" aria-label="Toggle menu">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </div>
      <div id="mobile-menu" class="hidden md:hidden pb-4 border-t border-white/5 pt-3">
        <div class="flex flex-col gap-1">
          <a href="index.html" class="px-4 py-3 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-colors">Home</a>
          <a href="blog.html" class="px-4 py-3 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-colors">Blog</a>
          <a href="about.html" class="px-4 py-3 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-colors">About</a>
          <a href="contact.html" class="px-4 py-3 rounded-lg text-sm font-medium bg-brand-600 text-white mt-1">Contact</a>
        </div>
      </div>
    </nav>
  </header>

  <!-- Main -->
  <main class="flex-grow py-12 md:py-20">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Breadcrumb -->
      <nav class="mb-8">
        <ol class="flex items-center text-xs text-gray-600 space-x-2">
          <li><a href="index.html" class="hover:text-brand-400 transition-colors">Home</a></li>
          <li><span class="text-gray-700">/</span></li>
          <li><a href="blog.html" class="hover:text-brand-400 transition-colors">Blog</a></li>
          <li><span class="text-gray-700">/</span></li>
          <li class="text-gray-400 truncate max-w-xs">__TITLE__</li>
        </ol>
      </nav>

      <!-- Article Header -->
      <header class="mb-10">
        <div class="flex items-center gap-3 mb-5">
          <span class="category-badge bg-brand-500/10 text-brand-400 border border-brand-500/20">__CATEGORY__</span>
          <span class="text-xs text-gray-600">__DATE__</span>
        </div>
        <h1 class="text-3xl md:text-4xl lg:text-5xl font-extrabold text-white mb-6 leading-tight">__TITLE__</h1>
        <p class="text-lg text-gray-400 leading-relaxed">__EXCERPT__</p>
      </header>

      <!-- Author -->
      <div class="flex items-center gap-4 pb-8 mb-10 border-b border-white/5">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center text-white text-lg font-bold">A</div>
        <div>
          <p class="font-semibold text-white text-sm">__AUTHOR__</p>
          <div class="flex items-center gap-2 text-xs text-gray-500">
            <span>__DATE__</span>
            <span>·</span>
            <span class="flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              __READTIME__ min read
            </span>
          </div>
        </div>
        <div class="ml-auto hidden md:flex items-center gap-2">
          <div class="w-20 h-1 rounded-full overflow-hidden" style="background:#22222e;">
            <div id="reading-progress" class="h-full accent-gradient rounded-full transition-all duration-300" style="width:0%"></div>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="prose max-w-none">
__CONTENT__
      </div>

      <!-- Tags -->
      <div class="mt-12 pt-8 border-t border-white/5">
        <div class="flex flex-wrap gap-2">
__TAGS__
        </div>
      </div>

      <!-- Share -->
      <div class="mt-10 p-6 rounded-2xl" style="background:#111118; border:1px solid rgba(255,255,255,0.05);">
        <h3 class="text-sm font-semibold text-white mb-4">Share this article</h3>
        <div class="flex gap-3">
          <a id="share-twitter" href="#" target="_blank" class="share-btn" aria-label="Twitter">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path></svg>
          </a>
          <a id="share-linkedin" href="#" target="_blank" class="share-btn" aria-label="LinkedIn">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"></path></svg>
          </a>
          <a id="share-facebook" href="#" target="_blank" class="share-btn" aria-label="Facebook">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"></path></svg>
          </a>
          <button onclick="copyLink()" class="share-btn" aria-label="Copy link">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
          </button>
        </div>
      </div>

      <!-- Newsletter -->
      <div class="mt-8 p-6 rounded-2xl" style="background:linear-gradient(135deg,#0c1a2e 0%,#0a0a0f 100%);border:1px solid rgba(14,141,232,0.2);">
        <h3 class="text-base font-semibold text-white mb-1">Enjoyed this article?</h3>
        <p class="text-gray-500 text-sm mb-4">Get more AI productivity insights delivered to your inbox.</p>
        <form class="flex gap-2" onsubmit="event.preventDefault();this.querySelector('button').textContent='Subscribed!';this.querySelector('button').classList.add('bg-emerald-600');this.querySelector('button').classList.remove('bg-brand-600');">
          <input type="email" placeholder="your@email.com" required class="newsletter-input flex-grow px-3.5 py-2.5 rounded-xl text-sm">
          <button type="submit" class="px-5 py-2.5 accent-gradient text-white font-medium text-sm rounded-xl hover:opacity-90 transition-all shadow-lg" style="box-shadow:0 0 20px rgba(14,141,232,0.25);">Subscribe</button>
        </form>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-white/5">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid md:grid-cols-4 gap-8 mb-10">
        <div class="md:col-span-2">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg accent-gradient flex items-center justify-center text-white font-bold text-sm">AI</div>
            <span class="text-lg font-bold text-white">AINest</span>
          </div>
          <p class="text-gray-500 text-sm mb-5 max-w-xs leading-relaxed">Daily AI & tech insights for professionals who want to work smarter, not harder.</p>
          <div class="flex items-center gap-3">
            <a href="#" class="w-9 h-9 rounded-lg flex items-center justify-center transition-all" style="background:#1a1a24;color:#64748b;border:1px solid #2a2a38;" aria-label="Twitter"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path></svg></a>
            <a href="#" class="w-9 h-9 rounded-lg flex items-center justify-center transition-all" style="background:#1a1a24;color:#64748b;border:1px solid #2a2a38;" aria-label="GitHub"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path></svg></a>
            <a href="#" class="w-9 h-9 rounded-lg flex items-center justify-center transition-all" style="background:#1a1a24;color:#64748b;border:1px solid #2a2a38;" aria-label="LinkedIn"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"></path></svg></a>
          </div>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Quick Links</h4>
          <ul class="space-y-2.5">
            <li><a href="index.html" class="text-sm text-gray-500 hover:text-white transition-colors">Home</a></li>
            <li><a href="blog.html" class="text-sm text-gray-500 hover:text-white transition-colors">Blog</a></li>
            <li><a href="about.html" class="text-sm text-gray-500 hover:text-white transition-colors">About</a></li>
            <li><a href="contact.html" class="text-sm text-gray-500 hover:text-white transition-colors">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Legal</h4>
          <ul class="space-y-2.5">
            <li><a href="privacy.html" class="text-sm text-gray-500 hover:text-white transition-colors">Privacy Policy</a></li>
            <li><a href="#" class="text-sm text-gray-500 hover:text-white transition-colors">Terms of Service</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-white/5 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p class="text-xs text-gray-600">© 2025 AINest. All rights reserved.</p>
        <p class="text-xs text-gray-600">Built with AI. Powered by curiosity.</p>
      </div>
    </div>
  </footer>

  <script>
    // Mobile menu
    document.getElementById('mobile-menu-btn').addEventListener('click', function() {
      document.getElementById('mobile-menu').classList.toggle('hidden');
    });
    
    // Copy link
    function copyLink() {
      navigator.clipboard.writeText(window.location.href).then(function() {
        var btn = event.currentTarget;
        btn.innerHTML = '<svg class=\"w-4 h-4 text-emerald-400\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M5 13l4 4L19 7\"></path></svg>';
        btn.style.borderColor = 'rgba(16,185,129,0.5)';
        setTimeout(function() {
          btn.innerHTML = '<svg class=\"w-4 h-4\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3\"></path></svg>';
          btn.style.borderColor = '#2a2a38';
        }, 2000);
      });
    }
    
    // Reading progress
    function updateProgress() {
      var article = document.querySelector('.prose');
      var bar = document.getElementById('reading-progress');
      if (!article || !bar) return;
      var top = article.offsetTop;
      var height = article.offsetHeight;
      var scrolled = window.scrollY - top + window.innerHeight / 2;
      var pct = Math.max(0, Math.min(100, (scrolled / height) * 100));
      bar.style.width = pct + '%';
    }
    window.addEventListener('scroll', updateProgress);
    
    // Share links
    var title = '__TITLE_URL__';
    var url = 'https://theainest.com/__FILENAME__';
    document.getElementById('share-twitter').href = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url);
    document.getElementById('share-facebook').href = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url);
    document.getElementById('share-linkedin').href = 'https://www.linkedin.com/shareArticle?mini=true&url=' + encodeURIComponent(url) + '&title=' + encodeURIComponent(title);
  </script>
</body>
</html>
"""

def make_html(title, excerpt, cat, tags, body, fname, date_str):
    tag_html = '\n'.join(f'          <span class="tag-pill">{t}</span>' for t in tags)
    
    word_count = len(body.split())
    read_time = max(1, word_count // 200)
    
    date_display = date_str
    
    result = POST_TEMPLATE
    result = result.replace('__TITLE__', title)
    result = result.replace('__EXCERPT__', excerpt)
    result = result.replace('__CATEGORY__', cat)
    result = result.replace('__CONTENT__', body)
    result = result.replace('__TAGS__', tag_html)
    result = result.replace('__DATE__', date_display)
    result = result.replace('__AUTHOR__', 'AINest Editorial')
    result = result.replace('__READTIME__', str(read_time))
    result = result.replace('__FILENAME__', fname)
    result = result.replace('__TITLE_URL__', title)
    return result

def process_posts():
    files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')])
    print(f'Found {len(files)} markdown files')
    
    for i, fname in enumerate(files, 1):
        fpath = os.path.join(POSTS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        title, excerpt, cat, tags = get_meta(text, fname)
        
        # Extract date from content if available
        date_match = re.search(r'Published:\s*(\d{4}-\d{2}-\d{2})', text)
        if date_match:
            date_str = date_match.group(1)
        else:
            # Use a default recent date
            date_str = '2025-01-15'
        
        # Find body (everything after the first # title)
        lines = text.split('\n')
        body_lines = []
        skip_first_title = False
        for line in lines:
            if not skip_first_title and line.startswith('# '):
                skip_first_title = True
                continue
            body_lines.append(line)
        body_text = '\n'.join(body_lines).strip()
        
        body_html = md2html(body_text)
        
        out_fname = fname.replace('.md', '.html')
        out_path = os.path.join(OUTPUT_DIR, out_fname)
        
        html = make_html(title, excerpt, cat, tags, body_html, out_fname, date_str)
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'  [{i:02d}] {out_fname} — {cat} — {title[:50]}...')
    
    print(f'\nDone! {len(files)} files generated in {OUTPUT_DIR}/')

if __name__ == '__main__':
    process_posts()
