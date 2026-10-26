"""
Extractor de Vehículos Eléctricos desde Mercado Libre Uruguay para VoltUY (ev.servicioti.com.uy)
Scraper directo sobre https://autos.mercadolibre.com.uy/electricos/ para obtener
precios en USD, marcas, modelos y concesionarias/vendedores en Uruguay.
Costo $0 - Sin API key.
"""

import urllib.request
import re
import hashlib
from bs4 import BeautifulSoup
from db_manager import get_connection

MLU_AUTOS_EV_URL = "https://autos.mercadolibre.com.uy/electricos/"

def fetch_mlu_ev_listings():
    print(f"[MLU] Consultando listado de autos eléctricos: {MLU_AUTOS_EV_URL}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-UY,es;q=0.9'
    }
    
    req = urllib.request.Request(MLU_AUTOS_EV_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[MLU] Error al consultar MLU: {e}")
        return []

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='ui-search-layout__item')
    print(f"[MLU] Publicaciones activas encontradas en portada: {len(items)}")

    conn = get_connection()
    cursor = conn.cursor()
    saved = 0
    listings = []

    for it in items:
        title_tag = it.find('a', class_='poly-component__title') or it.find('h2')
        if not title_tag:
            continue
        
        title = title_tag.get_text(strip=True)
        permalink = title_tag.get('href', '') if title_tag.name == 'a' else ''
        if not permalink:
            a_any = it.find('a', href=True)
            permalink = a_any['href'] if a_any else ''

        item_id = hashlib.md5(permalink.encode('utf-8')).hexdigest() if permalink else f"mlu-{saved}"

        seller_tag = it.find('span', class_='poly-component__seller')
        seller = seller_tag.get_text(strip=True) if seller_tag else "Particular / Concesionaria"

        price_tag = it.find('span', class_='andes-money-amount__fraction')
        price_raw = price_tag.get_text(strip=True).replace('.', '').replace(',', '.') if price_tag else "0"
        try:
            price = float(price_raw)
        except ValueError:
            price = 0.0

        currency_tag = it.find('span', class_='andes-money-amount__currency-symbol')
        currency = "USD" if currency_tag and "U$S" in currency_tag.get_text(strip=True) or "$" in currency_tag.get_text(strip=True) else "USD"

        loc_tag = it.find('span', class_='poly-component__location')
        location = loc_tag.get_text(strip=True) if loc_tag else "Uruguay"

        img_tag = it.find('img')
        img_url = img_tag.get('src') or img_tag.get('data-src') or '' if img_tag else ''

        cursor.execute("""
        INSERT INTO market_listings (id, tipo, titulo, precio, moneda, es_0km, vendedor, es_tienda_oficial, permalink, thumbnail, ubicacion)
        VALUES (?, 'auto', ?, ?, ?, 1, ?, 0, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            precio=excluded.precio,
            moneda=excluded.moneda,
            thumbnail=excluded.thumbnail,
            ubicacion=excluded.ubicacion
        """, (item_id, title, price, currency, seller, permalink, img_url, location))
        saved += 1
        listings.append({"titulo": title, "precio": price, "vendedor": seller, "ubicacion": location})

    conn.commit()
    conn.close()
    print(f"[MLU] {saved} publicaciones de autos eléctricos guardadas en SQLite.")
    return listings

if __name__ == "__main__":
    fetch_mlu_ev_listings()
