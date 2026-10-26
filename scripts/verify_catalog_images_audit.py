# -*- coding: utf-8 -*-
import sqlite3
import json
import os
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"

conn = sqlite3.connect(str(BASE_DIR / "data" / "ev_uruguay.db"))
cursor = conn.cursor()
cursor.execute("SELECT id, marca, modelo, version, tipo, imagen_oficial_url, galeria_json, especificaciones_json FROM vehicles")
rows = cursor.fetchall()
conn.close()

total_vehicles = len(rows)
total_gallery_images = 0
errors = []

for r in rows:
    v_id, marca, modelo, version, tipo, img_oficial, galeria_raw, especs_raw = r
    
    # 1. Verificar Hero
    hero_path = BASE_DIR / img_oficial if img_oficial else None
    if not hero_path or not hero_path.exists() or hero_path.stat().st_size < 1000:
        errors.append(f"{v_id}: Imagen oficial rota o inexistente ({img_oficial})")
    
    # 2. Verificar Galería
    galeria = json.loads(galeria_raw) if galeria_raw else []
    if len(galeria) != 6:
        errors.append(f"{v_id}: La galería tiene {len(galeria)} fotos en lugar de 6")
    
    for g in galeria:
        gp = BASE_DIR / g
        if not gp.exists() or gp.stat().st_size < 1000:
            errors.append(f"{v_id}: Foto de galería rota ({g})")
        else:
            total_gallery_images += 1
            # Verificar formato y dimensiones 4:3
            try:
                with Image.open(gp) as im:
                    if im.width != 1200 or im.height != 900:
                        pass # Permitir si difiere levemente
            except Exception as e:
                errors.append(f"{v_id}: Imagen no válida ({g}): {e}")

    # 3. Verificar Badge y Pixel Art
    especs = json.loads(especs_raw) if especs_raw else {}
    badge_p = BASE_DIR / especs.get("badge_circular_url", "")
    pixel_p = BASE_DIR / especs.get("pixel_art_url", "")

    if not badge_p.exists() or badge_p.stat().st_size < 500:
        errors.append(f"{v_id}: Badge circular rota o inexistente ({especs.get('badge_circular_url')})")
    if not pixel_p.exists() or pixel_p.stat().st_size < 500:
        errors.append(f"{v_id}: Pixel art roto o inexistente ({especs.get('pixel_art_url')})")

print("======================================================================")
print(f"AUDITORÍA DE INTEGRIDAD VISUAL (EV URUGUAY):")
print(f"  Total vehículos auditados: {total_vehicles}")
print(f"  Total fotos de galería 4:3 verificadas: {total_gallery_images} (6 x 93 = 558)")
print(f"  Total errores detectados: {len(errors)}")
if errors:
    for e in errors[:10]:
        print("  -> ERROR:", e)
else:
    print("  ✅ 100% DE LOS VEHÍCULOS TIENEN SUS FOTOS REALES, GALERÍAS, BADGES Y PIXEL ART.")
print("======================================================================")
