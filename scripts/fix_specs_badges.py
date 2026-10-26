# -*- coding: utf-8 -*-
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"
IMG_DIR = BASE_DIR / "assets" / "img"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for vid in ["xiaomi-himo-z20", "voltbike-flex-foldable", "voltbike-classica", "voltbike-pioneer"]:
    cursor.execute("SELECT especificaciones_json FROM vehicles WHERE id = ?", (vid,))
    row = cursor.fetchone()
    if not row: continue
    
    specs = json.loads(row[0] or "{}")
    
    # Buscar el badge y pixel art reales en disco
    v_dir = IMG_DIR / vid
    badge_files = list(v_dir.glob("badge-circular-*.webp"))
    pixel_files = list(v_dir.glob("pixel-art-16bit-*.webp"))
    
    if badge_files:
        specs["badge_circular_url"] = f"assets/img/{vid}/{badge_files[0].name}"
    if pixel_files:
        specs["pixel_art_url"] = f"assets/img/{vid}/{pixel_files[0].name}"
        
    cursor.execute("""
        UPDATE vehicles 
        SET especificaciones_json = ?
        WHERE id = ?
    """, (json.dumps(specs, ensure_ascii=False), vid))
    print(f"Actualizado {vid} -> badge: {specs.get('badge_circular_url')}")

conn.commit()
conn.close()
print("Sincronización de badges y pixel art completada.")
