import urllib.request
from bs4 import BeautifulSoup

urls = [
    ('auto', 'https://autos.mercadolibre.com.uy/electricos/'),
    ('moto', 'https://listado.mercadolibre.com.uy/moto-electrica'),
    ('bicicleta', 'https://listado.mercadolibre.com.uy/bicicleta-electrica')
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-UY,es;q=0.9'
}

for tipo, u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', class_='ui-search-layout__item')
        print(f"\n[{tipo.upper()}] Encontrados: {len(items)} items en {u}")
        for it in items[:3]:
            title_tag = it.find('a', class_='poly-component__title') or it.find('h2')
            title = title_tag.get_text(strip=True) if title_tag else "Sin título"
            seller_tag = it.find('span', class_='poly-component__seller')
            seller = seller_tag.get_text(strip=True) if seller_tag else "Particular"
            price_tag = it.find('span', class_='andes-money-amount__fraction')
            price = price_tag.get_text(strip=True) if price_tag else "0"
            loc_tag = it.find('span', class_='poly-component__location')
            loc = loc_tag.get_text(strip=True) if loc_tag else "Uruguay"
            print(f"  * {title} | USD {price} | Vendedor: {seller} ({loc})")
    except Exception as e:
        print(f"Error en {u}: {e}")
