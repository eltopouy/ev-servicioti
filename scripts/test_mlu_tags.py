import urllib.request
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-UY,es;q=0.9'
}

req = urllib.request.Request('https://autos.mercadolibre.com.uy/electricos/', headers=headers)
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
item = soup.find('li', class_='ui-search-layout__item')
if item:
    for tag in item.find_all(['a', 'span', 'p']):
        text = tag.get_text(strip=True)
        if len(text) > 5 and not tag.find_all(['span', 'p']):
            print(f"Tag <{tag.name} class='{tag.get('class')}'> -> {text}")
