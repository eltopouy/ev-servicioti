# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def test_yahoo(query):
    url = f"https://images.search.yahoo.com/search/images?p={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Yahoo embeds image json with imgurl
            matches = re.findall(r'imgurl=([^&"]+\.(?:jpg|jpeg|png|webp))', html, re.IGNORECASE)
            # unquote
            urls = [urllib.parse.unquote(m) for m in matches if m.startswith('http')]
            return urls
    except Exception as e:
        return []

def test_wikimedia(query):
    # Wikimedia API search
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url|mime&format=json&iiurlwidth=1280"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            urls = []
            for p in pages.values():
                info = p.get('imageinfo', [])
                if info and info[0].get('thumburl'):
                    urls.append(info[0]['thumburl'])
                elif info and info[0].get('url'):
                    urls.append(info[0]['url'])
            return urls
    except Exception as e:
        return []

for q in ['BYD Yuan Pro', 'Dongfeng Nammi Box', 'Chevrolet Blazer EV', 'BAW Pony', 'Chery eQ1', 'Volvo EX30']:
    y_urls = test_yahoo(q)
    w_urls = test_wikimedia(q)
    print(f"{q}:")
    print(f"  Yahoo: {len(y_urls)} -> {y_urls[0] if y_urls else None}")
    print(f"  Wikimedia: {len(w_urls)} -> {w_urls[0] if w_urls else None}")
