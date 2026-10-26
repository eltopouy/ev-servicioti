import urllib.request
from bs4 import BeautifulSoup

urls = [
    ('motos', 'https://motos.mercadolibre.com.uy/scooters-y-ciclomotores/electricas/'),
    ('motos_search', 'https://motos.mercadolibre.com.uy/electrica'),
    ('bicis_cat', 'https://deportes.mercadolibre.com.uy/ciclismo/bicicletas/bicicletas-electricas/'),
    ('bicis_search', 'https://deportes.mercadolibre.com.uy/ciclismo/bicicleta-electrica')
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-UY,es;q=0.9'
}

for label, u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', class_='ui-search-layout__item')
        print(f"[{label}] -> Encontrados: {len(items)} items")
        if items:
            t = items[0].find('a', class_='poly-component__title') or items[0].find('h2')
            print("  Top item:", t.get_text(strip=True) if t else "N/A")
    except Exception as e:
        print(f"[{label}] Error: {e}")
