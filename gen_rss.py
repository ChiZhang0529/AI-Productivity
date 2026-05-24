"""
gen_rss.py - Generate RSS 2.0 feed from articles.js
"""
import os
import re
import html

JS_FILE = "C:/Users/54463/WorkBuddy/2026-05-13-task-6/static-blog/js/articles.js"
OUTPUT_FILE = "C:/Users/54463/WorkBuddy/2026-05-13-task-6/static-blog/rss.xml"
BASE_URL = "https://vivoaihub.com"

def extract_articles_from_js(js_content):
    """Extract article objects from the JavaScript array."""
    articles = []
    pattern = r'\{\s*\n\s*id:\s*"([^"]+)",\s*\n\s*title:\s*"([^"]+)",\s*\n\s*excerpt:\s*"([^"]+)",\s*\n\s*date:\s*"([^"]+)",\s*\n\s*category:\s*"([^"]+)",\s*\n\s*author:\s*"[^"]+",\s*\n\s*tags:\s*\[([^\]]+)\],\s*\n\s*content:\s*`\n(.*?)\n\s*`\s*\n\s*\}'
    matches = re.findall(pattern, js_content, re.DOTALL)
    
    for match in matches:
        article_id, title, excerpt, date, category, tags_str, content = match
        tags = re.findall(r'"([^"]+)"', tags_str)
        content = content.strip()
        articles.append({
            'id': article_id,
            'title': title,
            'excerpt': excerpt,
            'date': date,
            'category': category,
            'tags': tags,
            'content': content
        })
    return articles

def strip_html(text):
    """Remove HTML tags."""
    return re.sub(r'<[^>]+>', '', text)

def format_date(date_str):
    """Convert YYYY-MM-DD to RFC 822 format."""
    from datetime import datetime
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%a, %d %b %Y 00:00:00 +0000')

def generate_rss():
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    articles = extract_articles_from_js(js_content)
    
    # Sort by date descending
    articles.sort(key=lambda a: a['date'], reverse=True)
    
    items = []
    for article in articles:
        article_url = f"{BASE_URL}/article.html?id={article['id']}"
        content_text = strip_html(article['content'])
        # Truncate description
        desc = article['excerpt'] + '\n\n' + content_text[:500]
        if len(content_text) > 500:
            desc += '...'
        
        rss_date = format_date(article['date'])
        categories = '\n'.join(f'      <category>{html.escape(t)}</category>' for t in article.get('tags', []))
        
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
    
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>AI Productivity</title>
    <link>{BASE_URL}</link>
    <description>Daily AI &amp; tech insights for professionals who want to work smarter, not harder. Expert articles on AI tools, productivity hacks, and workflow optimization.</description>
    <language>en-us</language>
    <lastBuildDate>{format_date(articles[0]['date'])}</lastBuildDate>
    <pubDate>{format_date(articles[0]['date'])}</pubDate>
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
