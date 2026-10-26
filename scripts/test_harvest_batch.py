# -*- coding: utf-8 -*-
"""
Script de prueba para cosecha de imágenes reales por lote
Verifica la calidad visual, encuadre 4:3, metadatos y sprites de los primeros 10 vehículos.
"""

import os
import io
import re
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from metadata_image_service import MetadataImageService
from pixel_art_generator import generar_pixel_art_sprite
from db_manager import get_connection

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
WIKI_AGENT = 'EVUruguay/1.0 (contacto@servicioti.com.uy; https://ev.servicioti.com.uy)'

def componer_encuadre_4_3(img_src: Image.Image) -> Image.Image:
    """Encuadra la imagen en relación 4:3 (1200x900) con fondo de estudio y sombra de contacto."""
    ancho_target, alto_target = 1200, 900
    suelo_y = 620
    apoyo_y = 740

    canvas = Image.new("RGB", (ancho_target, alto_target), (252, 252, 253))
    draw = ImageDraw.Draw(canvas)
    for y in range(suelo_y, alto_target):
        factor = (y - suelo_y) / float(alto_target - suelo_y)
        val = int(252 - factor * 12)
        draw.line([(0, y), (ancho_target, y)], fill=(val, val, val + 1))

    # Sombra suave de contacto
    shadow = Image.new("RGBA", (ancho_target, alto_target), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(int(ancho_target * 0.12), apoyo_y - 25), (int(ancho_target * 0.88), apoyo_y + 45)], fill=(0, 0, 0, 65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=22))
    canvas.paste(shadow, (0, 0), shadow)

    src_rgb = img_src.convert("RGB")
    ancho_max = int(ancho_target * 0.88)
    alto_max = int(alto_target * 0.70)

    ratio = min(ancho_max / float(src_rgb.width), alto_max / float(src_rgb.height))
    nuevo_ancho = max(10, int(src_rgb.width * ratio))
    nuevo_alto = max(10, int(src_rgb.height * ratio))

    img_scaled = src_rgb.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    pos_x = (ancho_target - nuevo_ancho) // 2
    pos_y = apoyo_y - nuevo_alto
    if pos_y < 50:
        pos_y = (alto_target - nuevo_alto) // 2

    canvas.paste(img_scaled, (pos_x, pos_y))
    return canvas

def generar_badge_circular(img_hero: Image.Image, output_path: Path, titulo: str) -> bool:
    try:
        thumb = img_hero.resize((128, 128), Image.Resampling.LANCZOS).convert("RGBA")
        mask = Image.new("L", (128, 128), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((2, 2, 126, 126), fill=255)

        badge = Image.new("RGBA", (128, 128), (255, 255, 255, 0))
        badge.paste(thumb, (0, 0), mask=mask)

        bdraw = ImageDraw.Draw(badge)
        bdraw.ellipse((2, 2, 126, 126), outline=(17, 24, 39, 210), width=2)

        final_rgb = Image.new("RGB", (128, 128), (255, 255, 255))
        final_rgb.paste(badge, (0, 0), badge)

        temp_p = output_path.parent / "temp_badge.png"
        final_rgb.save(temp_p, format="PNG")
        MetadataImageService.inyectar_y_optimizar(
            temp_p,
            titulo=f"Badge Oficial Circular - {titulo}",
            descripcion=f"Badge oficial de {titulo} para el catálogo EV Uruguay.",
            calidad=88,
            destino=output_path,
            formato="WEBP"
        )
        if temp_p.exists():
            temp_p.unlink()
        return True
    except Exception as e:
        print(f"Error generando badge circular: {e}")
        return False

print("Módulo de composición de prueba listo.")
