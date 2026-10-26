# -*- coding: utf-8 -*-
"""
Prototipo de Recolección de Imágenes Auténticas Multifuente
Prueba con 5 modelos representativos:
1. BYD Seagull Surf (Auto)
2. BAW Pony (Citycar económico)
3. Chery eQ1 (Citycar)
4. Trike Cargo 1500 (Triciclo de carga)
5. Sunra Grace (Moto eléctrica)
"""

import sys
import os
import io
import re
import json
import urllib.request
import urllib.parse
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
WIKI_AGENT = 'EVUruguay/1.0 (contacto@servicioti.com.uy; https://ev.servicioti.com.uy)'

def search_wikimedia(query, limit=10):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url|mime&format=json&iiurlwidth=1280"
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            urls = []
            for p in pages.values():
                info = p.get('imageinfo', [])
                if info:
                    u = info[0].get('thumburl') or info[0].get('url')
                    if u and not u.lower().endswith(('.svg', '.ogg', '.pdf')):
                        urls.append(u)
            return urls[:limit]
    except Exception as e:
        return []

def search_bing(query, limit=10):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&FORM=HDRSC2"
    req = urllib.request.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Accept-Language': 'es-UY,es;q=0.9,en;q=0.8'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            clean = [m for m in matches if not any(x in m.lower() for x in ['.svg', '.gif', 'logo', 'icon'])]
            return clean[:limit]
    except Exception:
        return []

def descargar_imagen(url):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) > 8000:
                with Image.open(io.BytesIO(data)) as im:
                    im.verify()
                return data
    except Exception:
        pass
    return None

test_cases = [
    ("BYD", "Seagull", "Surf", "auto"),
    ("BAW", "Pony", "EV", "auto"),
    ("Chery", "eQ1", "Little Ant", "auto"),
    ("Trike", "Cargo 1500", "Cabina Cerrada", "triciclo"),
    ("Sunra", "Grace", "Dual Battery", "moto")
]

for marca, modelo, version, tipo in test_cases:
    print(f"\n==========================================")
    print(f"Probando: {marca} {modelo} ({version}) - Tipo: {tipo}")
    
    # Búsqueda combinada
    candidatos = []
    
    # 1. Búsqueda específica en Bing
    query_bing = f"{marca} {modelo} {tipo} electric"
    res_bing = search_bing(query_bing, 8)
    print(f"  Bing ('{query_bing}'): {len(res_bing)} URLs")
    candidatos.extend(res_bing)
    
    # 2. Búsqueda en Wikimedia
    query_wiki = f"{marca} {modelo}"
    res_wiki = search_wikimedia(query_wiki, 8)
    print(f"  Wikimedia ('{query_wiki}'): {len(res_wiki)} URLs")
    candidatos.extend(res_wiki)
    
    # Si pocos candidatos, consulta alternativa
    if len(candidatos) < 4:
        query_alt = f"{marca} {modelo}"
        candidatos.extend(search_bing(query_alt, 8))
        print(f"  Bing Alt ('{query_alt}'): total acumulado {len(candidatos)}")

    # Probar descargas válidas
    descargadas = 0
    for u in candidatos:
        data = descargar_imagen(u)
        if data:
            descargadas += 1
            with Image.open(io.BytesIO(data)) as im:
                print(f"    ✓ [OK {descargadas}] {im.format} {im.size} -> {u[:80]}")
        if descargadas >= 4:
            break
    print(f"  Total descargadas con éxito: {descargadas}")
