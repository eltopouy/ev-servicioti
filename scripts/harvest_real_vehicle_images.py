# -*- coding: utf-8 -*-
"""
Recolector de Fotografías Reales y Auténticas para Catálogo de EV Uruguay
Busca y descarga imágenes 100% reales de cada modelo específico (BYD, Tesla, Chevrolet, BAW, Chery, etc.)
asegurando que cada vista corresponda estrictamente al vehículo en cuestión.
"""

import os
import io
import re
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright
from metadata_image_service import MetadataImageService
from db_manager import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"

def search_real_images(query: str, max_results: int = 5) -> list:
    """Busca URLs de imágenes reales de alta resolución para un vehículo específico."""
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&FORM=HDRSC2"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=18000)
            page.wait_for_timeout(1200)
            cards = page.query_selector_all("a.iusc")
            urls = []
            for c in cards:
                m_attr = c.get_attribute("m")
                if m_attr:
                    try:
                        data = json.loads(m_attr)
                        murl = data.get("murl")
                        if murl and murl.startswith("http") and not any(ext in murl.lower() for ext in [".svg", ".gif"]):
                            urls.append(murl)
                    except Exception:
                        pass
                if len(urls) >= max_results:
                    break
            browser.close()
            return urls
        except Exception as e:
            print(f"  [Error búsqueda Bing para '{query}']: {e}")
            browser.close()
            return []

def descargar_imagen_valida(urls: list) -> bytes:
    """Descarga e inspecciona los bytes de una imagen válida entre una lista de candidatos."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) > 5000:
                    with Image.open(io.BytesIO(data)) as im:
                        im.verify()
                    return data
        except Exception:
            continue
    return None

def componer_encuadre_instagram(img_src: Image.Image, formato: str = "4:5") -> Image.Image:
    """
    Encuadra la imagen real en relación 4:5 (1080x1350) o 4:3 (1200x900)
    con fondo de estudio limpio blanco/gris claro y sombra suave de contacto.
    """
    if formato == "4:3":
        ancho_target, alto_target = 1200, 900
        suelo_y = 650
        apoyo_y = 720
    else:
        ancho_target, alto_target = 1080, 1350
        suelo_y = 800
        apoyo_y = 980

    canvas = Image.new("RGB", (ancho_target, alto_target), (252, 252, 253))
    draw = ImageDraw.Draw(canvas)
    for y in range(suelo_y, alto_target):
        factor = (y - suelo_y) / float(alto_target - suelo_y)
        val = int(252 - factor * 14)
        draw.line([(0, y), (ancho_target, y)], fill=(val, val, val + 1))

    # Sombra suave de contacto
    shadow = Image.new("RGBA", (ancho_target, alto_target), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(int(ancho_target * 0.1), apoyo_y - 40), (int(ancho_target * 0.9), apoyo_y + 80)], fill=(0, 0, 0, 65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=25))
    canvas.paste(shadow, (0, 0), shadow)

    src_rgb = img_src.convert("RGB")
    ancho_max = int(ancho_target * 0.92)
    alto_max = int(alto_target * 0.72)

    ratio = min(ancho_max / float(src_rgb.width), alto_max / float(src_rgb.height))
    nuevo_ancho = max(10, int(src_rgb.width * ratio))
    nuevo_alto = max(10, int(src_rgb.height * ratio))

    img_scaled = src_rgb.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    pos_x = (ancho_target - nuevo_ancho) // 2
    pos_y = apoyo_y - nuevo_alto
    if pos_y < 80:
        pos_y = (alto_target - nuevo_alto) // 2

    canvas.paste(img_scaled, (pos_x, pos_y))
    return canvas

if __name__ == "__main__":
    print("Prueba del recolector de imágenes reales.")
