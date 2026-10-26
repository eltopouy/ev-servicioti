# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

for url in ['https://sunra.com.uy', 'https://sunra.com.uy/productos/', 'https://trike.uy']:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'<img[^>]+src=["\']([^"\']+\.(?:jpg|png|webp|jpeg))["\']', html, re.I)
            print(f"{url}: {len(imgs)} imagenes")
            for img in imgs[:5]:
                print("  ->", urllib.parse.urljoin(url, img))
    except Exception as e:
        print(f"{url}: Error {e}")
