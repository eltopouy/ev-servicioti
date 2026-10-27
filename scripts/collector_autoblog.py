"""
Extractor de Novedades y Lanzamientos de Autoblog Uruguay para VoltUY (ev.servicioti.com.uy)
Scraper directo sobre https://www.autoblog.com.uy para obtener las últimas publicaciones
de vehículos eléctricos, híbridos y lanzamientos 0km en Uruguay.
"""

import urllib.request
import re
import hashlib
from bs4 import BeautifulSoup
from db_manager import get_connection

AUTOBLOG_URL = "https://www.autoblog.com.uy"

EV_KEYWORDS = [
    "eléctrico", "eléctrica", "eléctricos", "eléctricas", "ev", "bev", "phev", "mhev",
    "enchufable", "híbrido", "híbrida", "batería", "kwh", "byd", "seagull", "dolphin",
    "yuan", "seal", "nammi", "dongfeng", "zeekr", "geely", "ex5", "jac e-js", "volvo",
    "ex30", "ex40", "c40", "e-tech", "leaf", "e-tron", "bmw i", "mercedes", "eq",
    "tesla", "maxus", "kia ev", "ioniq", "ora"
]

MARCAS_LIST = [
    "BYD", "Volvo", "Geely", "Zeekr", "JAC", "Dongfeng", "Nammi", "Renault",
    "Nissan", "Omoda", "Jaecoo", "GWM", "Chery", "Hyundai", "Kia", "Maxus",
    "BMW", "Audi", "Mercedes-Benz", "Tesla", "Chevrolet", "Volkswagen", "Toyota", "Mazda"
]

def clean_html(raw_html):
    return re.sub(r'<.*?>', '', raw_html).strip()

def is_ev_related(title, snippet):
    text = f"{title} {snippet}".lower()
    return any(keyword in text for keyword in EV_KEYWORDS)

def detect_brands(text):
    text_lower = text.lower()
    detected = [b for b in MARCAS_LIST if b.lower() in text_lower]
    return ", ".join(detected) if detected else "General"

def fetch_autoblog_ev_news():
    print(f"[Autoblog] Consultando portal: {AUTOBLOG_URL}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-UY,es;q=0.9'
    }
    
    req = urllib.request.Request(AUTOBLOG_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[Autoblog] Error al consultar portal: {e}")
        return []

    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.find_all('div', class_='post')
    print(f"[Autoblog] Total de artículos en portada: {len(posts)}")

    conn = get_connection()
    cursor = conn.cursor()
    saved_count = 0
    ev_articles = []

    for post in posts:
        title_tag = post.find(['h2', 'h3'], class_=re.compile(r'post-title|entry-title'))
        if not title_tag:
            continue
        a_tag = title_tag.find('a')
        if not a_tag:
            continue
        
        title = a_tag.get_text(strip=True)
        link = a_tag.get('href', '')
        
        snippet_tag = post.find('div', class_=re.compile(r'post-body|entry-content|snippet'))
        snippet = snippet_tag.get_text(strip=True)[:350] + "..." if snippet_tag else ""
        
        img_tag = post.find('img')
        img_url = img_tag.get('src', '') if img_tag else ""

        if not is_ev_related(title, snippet):
            continue

        title_clean = re.sub(r'(?i)autoblog\s*(uruguay)?', 'EV Uruguay', title).strip()
        snippet_clean = re.sub(r'(?i)autoblog\s*(uruguay)?', 'EV Uruguay', snippet).strip()

        article_id = hashlib.md5(link.encode('utf-8')).hexdigest()
        clean_url = f"https://ev.servicioti.com.uy/noticias/{article_id}"
        brands = detect_brands(f"{title_clean} {snippet_clean}")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_news_feed (
            id TEXT PRIMARY KEY,
            medio TEXT,
            titulo TEXT,
            url TEXT UNIQUE,
            fecha_publicacion TEXT,
            resumen TEXT,
            marcas_mencionadas TEXT,
            imagen_portada TEXT,
            contenido_html TEXT
        )
        """)

        cursor.execute("""
        INSERT INTO market_news_feed (id, medio, titulo, url, fecha_publicacion, resumen, marcas_mencionadas, imagen_portada, contenido_html)
        VALUES (?, 'Crónica EV Uruguay', ?, ?, datetime('now'), ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            titulo=excluded.titulo,
            resumen=excluded.resumen,
            marcas_mencionadas=excluded.marcas_mencionadas,
            imagen_portada=COALESCE(excluded.imagen_portada, market_news_feed.imagen_portada)
        """, (article_id, title_clean, clean_url, snippet_clean, brands, img_url, snippet_clean))
        
        saved_count += 1
        ev_articles.append({
            "titulo": title_clean,
            "link": clean_url,
            "marcas": brands,
            "imagen": img_url
        })

    conn.commit()
    conn.close()
    print(f"[Autoblog] Artículos de movilidad eléctrica indexados: {saved_count}")
    return ev_articles

if __name__ == "__main__":
    articles = fetch_autoblog_ev_news()
    for a in articles:
        print(f" -> [{a['marcas']}] {a['titulo']}")
