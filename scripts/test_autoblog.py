import urllib.request
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-UY,es;q=0.9'
}

req = urllib.request.Request('https://www.autoblog.com.uy', headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
    
    soup = BeautifulSoup(html, 'html.parser')
    posts = []
    
    for post in soup.find_all('div', class_='post'):
        title_tag = post.find(['h2', 'h3'], class_=re.compile(r'post-title|entry-title'))
        if not title_tag:
            continue
        a_tag = title_tag.find('a')
        if not a_tag:
            continue
        title = a_tag.get_text(strip=True)
        link = a_tag.get('href', '')
        snippet_tag = post.find('div', class_=re.compile(r'post-body|entry-content|snippet'))
        snippet = snippet_tag.get_text(strip=True)[:200] if snippet_tag else ""
        img_tag = post.find('img')
        img_url = img_tag.get('src', '') if img_tag else ""
        
        posts.append({'title': title, 'link': link, 'snippet': snippet, 'img': img_url})

    print(f"Total posts encontrados en Autoblog: {len(posts)}")
    for p in posts[:6]:
        print(f"* {p['title']}")
        print(f"  Link: {p['link']}")
except Exception as e:
    print(f"Error: {e}")
