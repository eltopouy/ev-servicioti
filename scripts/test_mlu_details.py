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
    print("Found item!")
    a_tag = item.find('a', class_='ui-search-link')
    print("Title attribute in a_tag:", a_tag.get('title') if a_tag else "No a_tag")
    h2 = item.find('h2')
    print("H2 text:", h2.get_text(strip=True) if h2 else "No h2")
    img = item.find('img')
    print("Img src:", img.get('src') or img.get('data-src') if img else "No img")
    price = item.find('span', class_='andes-money-amount__fraction')
    print("Price text:", price.get_text(strip=True) if price else "No price")
    currency = item.find('span', class_='andes-money-amount__currency-symbol')
    print("Currency:", currency.get_text(strip=True) if currency else "No curr")
