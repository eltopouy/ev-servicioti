# -*- coding: utf-8 -*-
import urllib.request
import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

pages = [
    ("v6e", "https://farizon.com.uy/v6e"),
    ("super-van", "https://farizon.com.uy/super-van-ssta"),
    ("h8e", "https://farizon.com.uy/h8e6t"),
    ("h9e", "https://farizon.com.uy/h9e8t")
]

for name, u in pages:
    print(f"\n==========================================")
    print(f"Modelo: {name} -> {u}")
    print(f"==========================================")
    try:
        html = urllib.request.urlopen(urllib.request.Request(u, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Titulo y textos destacados
        h1 = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)]
        print("Títulos/Cabezales:", h1[:8])
        
        # Imagenes de CDN
        imgs = set(re.findall(r'https://cdn\.prod\.website-files\.com/[^\s"\'\)\>]+', html))
        imgs_clean = [i for i in imgs if any(ext in i.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']) and not any(k in i.lower() for k in ['logo', 'icon', 'whatsapp', 'facebook', 'instagram', 'arrow'])]
        print(f"Imágenes de producto encontradas: {len(imgs_clean)}")
        for im in sorted(imgs_clean)[:10]:
            print("  ->", im)
            
    except Exception as e:
        print(f"Error {name}: {e}")
