"""
gen_rss.py - Generate RSS 2.0 feed from posts_html/*.html files.
Reads meta tags from each HTML file and builds the RSS feed.
"""
import os
import re
import html
from datetime import datetime

POSTS_DIR = "C:/Users/54463/WorkBuddy/2026-05-13-task-6/static-blog/posts_html"
OUTPUT_FILE = "C:/Users/54463/WorkBuddy/2026-05-13-task-6/static-blog/rss.xml"
BASE_URL = "https://vivoaihub.com"

def format_date(date_str):
    """Convert YYYY-MM-DD to RFC 822 format."""
    try:
        dt = datetime.strptime(date_str.strip(), '%Y-%m-%d')
    except ValueError:
        dt = datetime(2025, 1, 1)
    return dt.strftime('%a, %d %b %Y 00:00:00 +0000')

def extract_meta_from_html(filepath):
    """Extract article metadata from an HTML file's meta tags and content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Title: from <title> tag (strip site name suffix)
    title_match = re.search(r'<title>(.+?)\s*\|\s*AI Productivity</title>', content)
    if not title_match:
        title_match = re.search(r'<title>(.+?)</title>', content)
    title = title_match.group(1).strip() if title_match else 'Untitled'
    
    # Description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    excerpt = desc_match.group(1) if desc_match else ''
    
    # Date: from datePublished in JSON-LD, or article:published_time, or <time> element
    date_match = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', content)
    if not date_match:
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
    date_str = date_match.group(1) if date_match else '2025-01-01'
    
    # Tags
    tags = re.findall(r'<meta\s+property="article:tag"\s+content="([^"]+)"', content)
    
    # Content: extract body text from .prose div for description
    body_match = re.search(r'<div class="prose[^"]*">(.*?)</div>\s*(?:<!--\s*Tags|<!-- Tags)', content, re.DOTALL)
    if not body_match:
        body_match = re.search(r'class="prose[^"]*"[^>]*>(.*?)(?:</div>\s*<div class="mt-12|</div>\s*<!-- Tags)', content, re.DOTALL)
    
    body_text = ''
    if body_match:
        body_html = body_match.group(1)
        body_text = re.sub(r'<[^>]+>', ' ', body_html)
        body_text = re.sub(r'\s+', ' ', body_text).strip()
    
    return {
        'title': title,
        'excerpt': excerpt,
        'date': date_str,
        'tags': tags,
        'body_text': body_text
    }

def generate_rss():
    html_files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.html')])
    
    articles = []
    for fname in html_files:
        filepath = os.path.join(POSTS_DIR, fname)
        meta = extract_meta_from_html(filepath)
        meta['filename'] = fname
        articles.append(meta)
    
    # Sort by date descending
    articles.sort(key=lambda a: a['date'], reverse=True)
    
    items = []
    for article in articles:
        article_url = f"{BASE_URL}/posts_html/{article['filename']}"
        
        # Description: excerpt + first 500 chars of body
        desc = article['excerpt']
        if article['body_text']:
            desc += '\n\n' + article['body_text'][:500]
            if len(article['body_text']) > 500:
                desc += '...'
        
        rss_date = format_date(article['date'])
        categories = '\n'.join(
            f'      <category>{html.escape(t)}</category>' 
            for t in article.get('tags', [])
        )
        
        item = f"""    <item>
      <title>{html.escape(article['title'])}</title>
      <link>{article_url}</link>
      <guid isPermaLink="true">{article_url}</guid>
      <description>{html.escape(desc)}</description>
      <author>maye@vivoaihub.com (Maye Zhang)</author>
      <pubDate>{rss_date}</pubDate>
{categories}
      <source url="{BASE_URL}/rss.xml">AI Productivity</source>
    </item>"""
        items.append(item)
    
    latest_date = format_date(articles[0]['date'])
    
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>AI Productivity</title>
    <link>{BASE_URL}</link>
    <description>Daily AI &amp; tech insights for professionals who want to work smarter, not harder. Expert articles on AI tools, productivity hacks, and workflow optimization.</description>
    <language>en-us</language>
    <lastBuildDate>{latest_date}</lastBuildDate>
    <pubDate>{latest_date}</pubDate>
    <webMaster>maye@vivoaihub.com (Maye Zhang)</webMaster>
    <managingEditor>maye@vivoaihub.com (Maye Zhang)</managingEditor>
    <image>
      <url>{BASE_URL}/og-image.jpg</url>
      <title>AI Productivity</title>
      <link>{BASE_URL}</link>
    </image>
    <atom:link href="{BASE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>"""
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(rss)
    
    print(f'RSS feed generated: {OUTPUT_FILE}')
    print(f'  {len(articles)} articles')
    print(f'  Latest: {articles[0]["title"][:60]}...')
    print(f'  File size: {os.path.getsize(OUTPUT_FILE):,} bytes')

if __name__ == '__main__':
    generate_rss()
