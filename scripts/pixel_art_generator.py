# -*- coding: utf-8 -*-
"""
Generador Autónomo de Sprites e Iconos Pixel Art 16-Bit para EV Uruguay (ev.servicioti.com.uy)
Transforma las vistas isométricas oficiales de los vehículos eléctricos en sprites retro
con estética arcade de 16-bit (cuantización a 16 colores, escalado nítido con Nearest-Neighbor)
e inyección de metadatos de autoría de ServicioTI.
"""

import os
import re
import json
import argparse
from pathlib import Path
from PIL import Image
from metadata_image_service import MetadataImageService
from db_manager import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"

def slugify(text: str) -> str:
    text = str(text or "").lower()
    text = re.sub(r"[áàäâã]", "a", text)
    text = re.sub(r"[éèëê]", "e", text)
    text = re.sub(r"[íìïî]", "i", text)
    text = re.sub(r"[óòöôõ]", "o", text)
    text = re.sub(r"[úùüû]", "u", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def generar_pixel_art_sprite(source_path: Path, dest_path: Path, titulo: str) -> bool:
    try:
        with Image.open(source_path) as img:
            # 1. Downscale a 64x64
            small = img.resize((64, 64), Image.Resampling.BILINEAR)
            # 2. Cuantización a 16 colores arcade
            pixelated = small.quantize(colors=16, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
            # 3. Upscale a 128x128 con Nearest-Neighbor para bordes limpios
            retro_sprite = pixelated.resize((128, 128), Image.Resampling.NEAREST)

            temp_pixel = dest_path.parent / "temp_pixel_art.png"
            retro_sprite.save(temp_pixel, format="PNG")

            MetadataImageService.inyectar_y_optimizar(
                temp_pixel,
                titulo=f"Icono Pixel Art 16-Bit - {titulo}",
                descripcion=f"Icono retro estilo arcade de 16-Bit de {titulo} para el catálogo EV Uruguay.",
                calidad=88,
                destino=dest_path,
                formato="WEBP"
            )
            if temp_pixel.exists():
                temp_pixel.unlink()
            return True
    except Exception as e:
        print(f"Error procesando {source_path}: {e}")
        return False

def procesar_todo_catalogo():
    print("=== Generando Iconos Pixel Art 16-Bit para Todo el Catálogo ===")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, marca, modelo, version, tipo FROM vehicles")
    vehiculos = cursor.fetchall()
    conn.close()

    total = len(vehiculos)
    generados = 0

    for idx, v in enumerate(vehiculos, 1):
        v_id = v["id"]
        v_marca = v["marca"]
        v_modelo = v["modelo"]
        v_version = v["version"] or ""
        v_tipo = v["tipo"]

        v_dir = IMG_DIR / v_id
        if not v_dir.exists():
            continue

        # Buscar la foto hero isométrica 01
        hero_files = list(v_dir.glob("01-vista-isometrica-*.webp")) + list(v_dir.glob("01-*.webp"))
        if not hero_files:
            continue

        hero_path = hero_files[0]
        from build_full_galleries import generar_nombre_pixel_art
        pixel_name = generar_nombre_pixel_art(v_marca, v_modelo, v_version, v_tipo)
        pixel_path = v_dir / pixel_name

        if generar_pixel_art_sprite(hero_path, pixel_path, f"{v_marca} {v_modelo}"):
            generados += 1
            if idx % 20 == 0 or idx == total:
                print(f"[{idx}/{total}] Pixel Art: {v_marca} {v_modelo}")

    print(f"\n[Éxito] {generados} iconos Pixel Art generados.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de iconos Pixel Art.")
    parser.add_argument("--all", action="store_true", default=True, help="Procesar todo el catálogo")
    args = parser.parse_args()
    procesar_todo_catalogo()
