# -*- coding: utf-8 -*-
"""
Cosecha especializada para los 6 modelos restantes
"""

import os
import io
import re
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

from harvest_all_real_vehicles import (
    recolectar_para_vehiculo, SEARCH_TERMS_CUSTOM,
    search_wikimedia, search_bing, descargar_imagen_bytes
)
from db_manager import get_connection

CUSTOM_FIXES = {
    "sunra-miku-super": ["Sunra Miku", "Miku Super motorcycle", "Sunra electric motorcycle"],
    "sunra-robo-s": ["Sunra Robo", "Sunra Robo-S", "Sunra scooter"],
    "loop-bikes-classic": ["Loop Bikes vintage", "bicicleta electrica holandesa", "vintage electric bike"],
    "voltbike-flex-foldable": ["Voltbike folding", "folding electric bicycle 20", "bicicleta electrica plegable"],
    "wheele-manhattan-flex": ["Wheele cruiser", "low step electric bicycle", "bicicleta electrica cuadro bajo"],
    "trek-allant-plus-7": ["Trek Allant", "Trek electric bicycle", "Trek e-bike"]
}

# Actualizar el diccionario central
SEARCH_TERMS_CUSTOM.update(CUSTOM_FIXES)

conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
    SELECT id, tipo, marca, modelo, version, link_fabricante 
    FROM vehicles 
    WHERE id IN ('sunra-miku-super', 'sunra-robo-s', 'loop-bikes-classic', 'voltbike-flex-foldable', 'wheele-manhattan-flex', 'trek-allant-plus-7')
""")
vehiculos = [dict(r) for r in cursor.fetchall()]
conn.close()

for v in vehiculos:
    print(f"Procesando modelo restante: {v['marca']} {v['modelo']} ({v['id']})...")
    ok = recolectar_para_vehiculo(v)
    print(f"  Resultado: {'OK' if ok else 'FALLO'}")
