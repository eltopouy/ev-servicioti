# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

urls = [
    'https://www.byd.com.uy',
    'https://dongfengmotors.uy/nammi-box/',
    'https://www.chevrolet.com.uy/vehiculos-electricos/blazer-ev',
    'https://bawauto.com',
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'<img[^>]+src=["\']([^"\']+\.(?:jpg|png|webp|jpeg))["\']', html, re.IGNORECASE)
            print(f"{url}: {len(imgs)} imagenes encontradas")
            for img in imgs[:4]:
                full = urllib.parse.urljoin(url, img)
                print("  ->", full)
    except Exception as e:
        print(f"{url}: Error {e}")
