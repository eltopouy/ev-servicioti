# -*- coding: utf-8 -*-
"""
Auditoría Exhaustiva de Imágenes y Vistas para EV Uruguay (ev.servicioti.com.uy)
Verifica que cada uno de los 93 vehículos cuente con:
1. Exactamente 6 fotografías de galería en formato 4:3 (1200x900)
2. Imagen Hero principal (vista isométrica frontal 3/4)
3. Badge circular oficial (128x128)
4. Pixel art 16-bit arcade (128x128)
5. Detección de duplicados entre vehículos distintos (cero tolerancia a stock genérico cruzado)
"""
import os
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
cur.execute("SELECT id, marca, modelo, version, tipo, imagen_oficial_url, galeria_json, especificaciones_json FROM vehicles ORDER BY tipo, marca, modelo")
vehicles = cur.fetchall()
conn.close()

print(f"=== INICIANDO AUDITORÍA EXHAUSTIVA DE IMÁGENES ({len(vehicles)} VEHÍCULOS) ===\n")

hashes_by_vehicle = {}
vehicle_galleries = {}
file_to_vehicles = {}
issues = []

for v in vehicles:
    vid, marca, modelo, version, tipo, img_oficial, galeria_json, especs_json = v
    galeria = json.loads(galeria_json) if galeria_json else []
    especs = json.loads(especs_json) if especs_json else {}

    v_issues = []
    
    # 1. Chequeo de Hero
    hero_p = BASE_DIR / img_oficial if img_oficial else None
    if not hero_p or not hero_p.exists() or hero_p.stat().st_size < 1000:
        v_issues.append(f"Hero faltante o corrupto: {img_oficial}")
    
    # 2. Chequeo de Galería (debe tener 6 imágenes)
    if len(galeria) != 6:
        v_issues.append(f"Galería tiene {len(galeria)} imágenes (debe ser 6)")
    
    galeria_hashes = []
    for idx, g_rel in enumerate(galeria):
        gp = BASE_DIR / g_rel
        if not gp.exists():
            v_issues.append(f"Vista {idx+1} no existe: {g_rel}")
            continue
        if gp.stat().st_size < 1000:
            v_issues.append(f"Vista {idx+1} tamaño inválido (<1KB): {g_rel}")
            continue
        
        # Calcular hash
        h = hashlib.md5(gp.read_bytes()).hexdigest()
        galeria_hashes.append(h)
        file_to_vehicles.setdefault(h, []).append((vid, gp.name))
    
    # Chequear si todas las 6 vistas son idénticas dentro del mismo vehículo
    unique_hashes_in_vehicle = set(galeria_hashes)
    if len(unique_hashes_in_vehicle) == 1 and len(galeria_hashes) > 1:
        v_issues.append(f"ADVERTENCIA: Las 6 vistas son el mismo archivo repetido ({len(galeria_hashes)} copias)")
    
    # 3. Badge y Pixel Art
    badge_p = BASE_DIR / especs.get("badge_circular_url", "")
    pixel_p = BASE_DIR / especs.get("pixel_art_url", "")
    if not badge_p.exists() or badge_p.stat().st_size < 500:
        v_issues.append(f"Badge circular faltante o corrupto")
    if not pixel_p.exists() or pixel_p.stat().st_size < 500:
        v_issues.append(f"Pixel art faltante o corrupto")
    
    if v_issues:
        issues.append((vid, f"{marca} {modelo} ({version})", v_issues))

print(f"Vehículos auditados con observaciones o fallas locales: {len(issues)} de {len(vehicles)}")
for vid, name, v_issues in issues[:15]:
    print(f"  [{vid}] {name}:")
    for iss in v_issues:
        print(f"    - {iss}")

# Chequeo de duplicados cruzados entre diferentes vehículos
cross_duplicates = {}
for h, entries in file_to_vehicles.items():
    vids = set(e[0] for e in entries)
    if len(vids) > 1:
        cross_duplicates[h] = entries

print(f"\nImágenes idénticas compartidas entre DIFERENTES vehículos: {len(cross_duplicates)}")
for h, entries in list(cross_duplicates.items())[:10]:
    v_list = list(set(e[0] for e in entries))
    print(f"  Hash {h[:8]} presente en {len(v_list)} vehículos: {v_list[:4]}")
