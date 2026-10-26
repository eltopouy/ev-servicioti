import urllib.request
from bs4 import BeautifulSoup

urls = [
    'https://autos.mercadolibre.com.uy/electricos/',
    'https://motos.mercadolibre.com.uy/electricas/',
    'https://bicicletas.mercadolibre.com.uy/electricas/'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-UY,es;q=0.9',
    'Referer': 'https://www.google.com/'
}

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', class_='ui-search-layout__item')
        print(f"URL: {u} -> Status 200, items encontrados: {len(items)}")
        for it in items[:3]:
            title_tag = it.find(['h2', 'h3'], class_='poly-component__title') or it.find('h2')
            price_tag = it.find('span', class_='andes-money-amount__fraction')
            title = title_tag.get_text(strip=True) if title_tag else "Sin título"
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            print(f"  - {title} (USD {price})")
    except Exception as e:
        print(f"URL: {u} -> ERROR: {e}")
