# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def search_wikimedia(query):
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url|mime&format=json&iiurlwidth=1280"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            urls = []
            for p in pages.values():
                info = p.get('imageinfo', [])
                if info and info[0].get('thumburl'):
                    urls.append((p.get('title', ''), info[0]['thumburl']))
                elif info and info[0].get('url'):
                    urls.append((p.get('title', ''), info[0]['url']))
            return urls
    except Exception as e:
        return []

motos_and_bikes = [
    'Sunra Grace electric scooter',
    'Niu NQi GTS electric scooter',
    'Yadea G5 electric scooter',
    'Super Soco TC Max electric motorcycle',
    'Trek Powerfly electric bicycle',
    'Specialized Turbo Vado electric bicycle',
    'Decathlon Rockrider E-ST 500',
    'Himo C26 electric bicycle',
    'electric cargo tricycle rickshaw'
]

for item in motos_and_bikes:
    res = search_wikimedia(item)
    print(f"{item}: {len(res)} encontradas")
    if res:
        print(f"   -> {res[0][0]}: {res[0][1][:110]}")
