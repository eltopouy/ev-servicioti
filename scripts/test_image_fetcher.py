from playwright.sync_api import sync_playwright
import json
import urllib.parse

def search_real_images(query, max_results=6):
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&FORM=HDRSC2"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(1500)
        
        cards = page.query_selector_all("a.iusc")
        urls = []
        for c in cards:
            m_attr = c.get_attribute("m")
            if m_attr:
                try:
                    data = json.loads(m_attr)
                    murl = data.get("murl")
                    if murl and murl.startswith("http"):
                        urls.append(murl)
                except Exception:
                    pass
            if len(urls) >= max_results:
                break
        browser.close()
        return urls

if __name__ == "__main__":
    for vehicle in ["BYD Seagull Surf 2024", "Tesla Model Y Performance", "BAW Pony EV", "Chery eQ1 Little Ant"]:
        print(f"Buscando imágenes reales para: {vehicle}")
        res = search_real_images(vehicle, 3)
        print(f"  Encontradas {len(res)} URLs:")
        for u in res:
            print("   ->", u[:100])
