# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}

queries = [
    'BYD Yuan Pro EV',
    'BYD Seagull Surf 2024',
    'Dongfeng Nammi Box EV',
    'BAW Pony EV',
    'Chery eQ1 Little Ant',
    'Volvo EX30 electric',
    'Tesla Model Y electric',
    'Sunra Grace scooter electrica',
    'Chevrolet Bolt EUV electric',
    'Trek triciclo electrico carga'
]

for q in queries:
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(q)}&FORM=HDRSC2"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            print(f"{q}: {len(matches)} encontradas -> {matches[0] if matches else 'NONE'}")
    except Exception as e:
        print(f"{q}: Error {e}")
    time.sleep(0.5)
