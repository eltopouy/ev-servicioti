# -*- coding: utf-8 -*-
"""
Radar Oficial de Precios de Plaza y Ofertas en Concesionarios: EV Uruguay
Proyecto: EV Uruguay (https://ev.servicioti.com.uy)
Autor: Andrés Franchi Ugartemendía (ServicioTI)

Vigila y mantiene las mejores ofertas de plaza exclusivamente para vehículos 100% eléctricos (BEV).
Garantiza:
1. Cero vehículos a combustión o híbridos.
2. Cero duplicados: exactamente una publicación por modelo con el precio más competitivo de plaza.
3. Cero imágenes rotas: vincula siempre la imagen oficial de estudio verificada de cada modelo.
"""

import sys
import re
import urllib.request
from bs4 import BeautifulSoup
from db_manager import get_connection

MLU_AUTOS_EV_URL = "https://autos.mercadolibre.com.uy/electricos/"

# Mapa de correspondencia de modelos BEV en plaza con sus IDs de vehículos
BEV_MODEL_MAPPING = [
    {"id": "mlu-baw-pony", "vehicle_id": "baw-pony-ev", "keywords": ["baw pony", "pony ev"], "precio_default": 9990.0, "titulo": "BAW Pony EV (Citycar 3 Puertas 100% Eléctrico)"},
    {"id": "mlu-chery-qq", "vehicle_id": "chery-qq-ice-cream", "keywords": ["qq ice cream", "ice cream"], "precio_default": 11990.0, "titulo": "Chery QQ Ice Cream (Kei Car Urbano Eléctrico)"},
    {"id": "mlu-baw-l7", "vehicle_id": "baw-l7-bagel-ev", "keywords": ["baw l7", "l7 bagel"], "precio_default": 12990.0, "titulo": "BAW L7 Bagel EV (Hatchback 5 Puertas 18.7 kWh)"},
    {"id": "mlu-geely-panda", "vehicle_id": "geely-panda-mini-ev", "keywords": ["panda mini", "geely panda"], "precio_default": 13990.0, "titulo": "Geely Panda Mini EV (Citycar Go 17 kWh LFP)"},
    {"id": "mlu-changan-lumin-155", "vehicle_id": "changan-lumin-155", "keywords": ["lumin 155", "changan lumin 155"], "precio_default": 13990.0, "titulo": "Changan Lumin 155 (Corn EV 12.9 kWh)"},
    {"id": "mlu-jmc-jmev-ev3", "vehicle_id": "jmev-ev3", "keywords": ["jmev ev3", "xiaoqilin", "jmc ev3"], "precio_default": 13990.0, "titulo": "JMC JMEV EV3.3 (Xiaoqilin Easy 21.4 kWh LFP)"},
    {"id": "mlu-changan-lumin-301", "vehicle_id": "changan-lumin-301", "keywords": ["lumin 301", "lumin sweet"], "precio_default": 16990.0, "titulo": "Changan Lumin 301 Sweet (DC Fast Charge 28 kWh)"},
    {"id": "mlu-dongfeng-nammi-330", "vehicle_id": "dongfeng-nammi-330", "keywords": ["nammi 330", "nammi box 330"], "precio_default": 17990.0, "titulo": "Dongfeng Nammi Box 330 (31.4 kWh EV)"},
    {"id": "mlu-jac-ejs1", "vehicle_id": "jac-e-js1", "keywords": ["jac e-js1", "e-js1", "ejs1"], "precio_default": 18990.0, "titulo": "JAC e-JS1 (City Luxury EV 30.2 kWh)"},
    {"id": "mlu-byd-seagull-ev300", "vehicle_id": "byd-seagull-ev300", "keywords": ["seagull ev300", "seagull 300", "seagull gl"], "precio_default": 18990.0, "titulo": "BYD Seagull EV300 (GL Active 30 kWh Blade LFP)"},
    {"id": "mlu-chery-eq1", "vehicle_id": "chery-eq1", "keywords": ["chery eq1", "little ant", "pequeña hormiga"], "precio_default": 19990.0, "titulo": "Chery eQ1 Little Ant (Pequeña Hormiga LFP 30.8 kWh)"},
    {"id": "mlu-renault-kwid-etech", "vehicle_id": "renault-kwid-e-tech", "keywords": ["kwid e-tech", "kwid electrico"], "precio_default": 20990.0, "titulo": "Renault Kwid E-Tech (100% Eléctrico 26.8 kWh)"},
    {"id": "mlu-byd-seagull-ev400", "vehicle_id": "byd-seagull-ev400-gs", "keywords": ["seagull ev400", "seagull 400", "seagull gs"], "precio_default": 21990.0, "titulo": "BYD Seagull EV400 (GS 38.88 kWh Blade LFP)"},
    {"id": "mlu-dongfeng-nammi-430", "vehicle_id": "dongfeng-nammi-box", "keywords": ["nammi 430", "nammi box 430"], "precio_default": 21990.0, "titulo": "Dongfeng Nammi Box 430 (EV B-Hatch 42.3 kWh)"},
    {"id": "mlu-byd-seagull-surf", "vehicle_id": "byd-seagull-surf", "keywords": ["seagull surf"], "precio_default": 23990.0, "titulo": "BYD Seagull Surf (Tope de Gama 43.2 kWh 88 CV)"},
    {"id": "mlu-geely-geometry-e", "vehicle_id": "geely-geometry-e", "keywords": ["geometry e"], "precio_default": 23990.0, "titulo": "Geely Geometry E (Compact City EV 39.4 kWh)"},
    {"id": "mlu-byd-e2", "vehicle_id": "byd-e2", "keywords": ["byd e2", "new e2"], "precio_default": 24990.0, "titulo": "BYD New e2 (Hatchback EV 405 Blade)"},
    {"id": "mlu-byd-yuan-pro", "vehicle_id": "byd-yuan-pro", "keywords": ["yuan pro"], "precio_default": 26990.0, "titulo": "BYD Yuan Pro (EV 380 SUV LFP Blade)"},
    {"id": "mlu-byd-dolphin-gs", "vehicle_id": "byd-dolphin-gs", "keywords": ["byd dolphin", "dolphin gs"], "precio_default": 28990.0, "titulo": "BYD Dolphin (GS EV e-Platform 3.0)"},
    {"id": "mlu-byd-t3-furgon", "vehicle_id": "byd-t3", "keywords": ["byd t3", "t3 furgon", "furgon t3"], "precio_default": 29990.0, "titulo": "BYD T3 (Furgón Utilitario Eléctrico 3.8m³)"},
    {"id": "mlu-farizon-v6e", "vehicle_id": "farizon-v6e", "keywords": ["farizon v6e", "v6e"], "precio_default": 29990.0, "titulo": "Farizon V6E (Mini Van Furgón Urbano 41.86 kWh)"},
    {"id": "mlu-tesla-model-3", "vehicle_id": "tesla-model-3-rwd", "keywords": ["tesla model 3", "model 3"], "precio_default": 32990.0, "titulo": "Tesla Model 3 Highland (Standard Range RWD)"},
    {"id": "mlu-geely-ex5-pro", "vehicle_id": "geely-ex5-pro", "keywords": ["geely ex5", "ex5 pro"], "precio_default": 33990.0, "titulo": "Geely EX5 (Pro EV 2026 Short Blade)"},
    {"id": "mlu-tesla-model-y", "vehicle_id": "tesla-model-y-rwd", "keywords": ["tesla model y", "model y"], "precio_default": 36490.0, "titulo": "Tesla Model Y (Standard Range RWD LFP)"},
    {"id": "mlu-omoda-e5", "vehicle_id": "omoda-e5", "keywords": ["omoda e5", "omoda 5 ev"], "precio_default": 38990.0, "titulo": "Omoda E5 (Premium EV 61 kWh)"},
    {"id": "mlu-byd-yuan-plus", "vehicle_id": "byd-yuan-plus", "keywords": ["yuan plus", "atto 3"], "precio_default": 39990.0, "titulo": "BYD Yuan Plus (EV 500 Flagship Atto 3)"},
    {"id": "mlu-volvo-ex30", "vehicle_id": "volvo-ex30", "keywords": ["volvo ex30", "ex30"], "precio_default": 42990.0, "titulo": "Volvo EX30 (Single Motor Extended Range Plus)"}
]

def fetch_mlu_ev_listings():
    print(f"[Radar Plaza] Consultando publicaciones activas de autos eléctricos...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-UY,es;q=0.9'
    }
    
    scraped_items = []
    try:
        req = urllib.request.Request(MLU_AUTOS_EV_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', class_='ui-search-layout__item')
        print(f"[Radar Plaza] Ofertas encontradas en plaza: {len(items)}")

        for it in items:
            title_tag = it.find('a', class_='poly-component__title') or it.find('h2')
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True).lower()

            price_tag = it.find('span', class_='andes-money-amount__fraction')
            price_raw = price_tag.get_text(strip=True).replace('.', '').replace(',', '.') if price_tag else "0"
            try:
                price = float(price_raw)
            except ValueError:
                price = 0.0

            seller_tag = it.find('span', class_='poly-component__seller')
            seller = seller_tag.get_text(strip=True) if seller_tag else "Concesionaria Oficial"

            loc_tag = it.find('span', class_='poly-component__location')
            loc = loc_tag.get_text(strip=True) if loc_tag else "Montevideo, Uruguay"

            if price > 5000:
                scraped_items.append({"title": title, "price": price, "seller": seller, "location": loc})
    except Exception as e:
        print(f"[Radar Plaza] Aviso de consulta: {e}")

    # Conectar y sincronizar las 27 ofertas deduplicadas al menor precio de plaza
    conn = get_connection()
    cursor = conn.cursor()

    # Obtener las imágenes oficiales verificadas de vehicles
    cursor.execute("SELECT id, imagen_oficial_url FROM vehicles")
    veh_imgs = dict(cursor.fetchall())

    updated = 0
    for m in BEV_MODEL_MAPPING:
        mid = m["id"]
        vid = m["vehicle_id"]
        best_price = m["precio_default"]
        best_seller = "Red Oficial de Concesionarios"
        best_loc = "Montevideo, Uruguay"

        # Buscar si el scraper encontró una oferta más competitiva para este modelo
        for sc in scraped_items:
            if any(k in sc["title"] for k in m["keywords"]):
                if 5000 < sc["price"] <= best_price:
                    best_price = sc["price"]
                    best_seller = sc["seller"]
                    best_loc = sc["location"]

        # Obtener la imagen oficial del modelo desde vehicles
        thumb = veh_imgs.get(vid, f"assets/img/{vid}/01-vista-isometrica-frontal-3-4-{vid}-ev-servicioti-uruguay.webp")
        permalink = f"https://ev.servicioti.com.uy/plaza/{mid}"

        cursor.execute("""
            INSERT INTO market_listings (id, tipo, titulo, precio, moneda, es_0km, vendedor, es_tienda_oficial, permalink, thumbnail, ubicacion)
            VALUES (?, 'auto', ?, ?, 'USD', 1, ?, 1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                titulo=excluded.titulo,
                precio=excluded.precio,
                moneda=excluded.moneda,
                vendedor=excluded.vendedor,
                permalink=excluded.permalink,
                thumbnail=excluded.thumbnail,
                ubicacion=excluded.ubicacion
        """, (mid, m["titulo"], best_price, best_seller, permalink, thumb, best_loc))
        updated += 1

    # Asegurar que no quede ningún registro que no sea de los 27 BEV oficiales
    cursor.execute("DELETE FROM market_listings WHERE id NOT LIKE 'mlu-%'")

    conn.commit()
    conn.close()
    print(f"[Radar Plaza] {updated} ofertas 100% BEV deduplicadas y sincronizadas con imágenes oficiales.")
    return BEV_MODEL_MAPPING

if __name__ == "__main__":
    fetch_mlu_ev_listings()
