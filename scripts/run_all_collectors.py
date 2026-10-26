# -*- coding: utf-8 -*-
"""
Orquestador Central de Recolección y Procesamiento de Datos para EV Uruguay (ev.servicioti.com.uy)
Ejecuta la base de datos, el catálogo exhaustivo (+98% del mercado), la construcción
de galerías fotográficas de 5 vistas con metadatos de ServicioTI, avisos de plaza
y la red nacional de cargadores de UTE Mueve.
"""

import sys
from pathlib import Path

# Asegurar encoding UTF-8
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from db_manager import init_db
from catalog_exhaustive_uy import poblar_catalogo_completo
from build_full_galleries import construir_galerias
from collector_mercadolibre import fetch_mlu_ev_listings
from map_chargers_sync import seed_chargers
from export_to_json import export_db_to_json

def run_pipeline():
    print("==================================================")
    print("⚡ EV Uruguay | Revista & Catálogo de Movilidad Eléctrica")
    print("   Subdominio: https://ev.servicioti.com.uy")
    print("==================================================\n")

    print("1/5. Inicializando Base de Datos SQLite...")
    init_db()

    print("\n2/5. Sembrando Catálogo Exhaustivo Homologado (+98% del mercado) y Crónicas...")
    poblar_catalogo_completo()

    print("\n3/5. Verificando y Optimizando Galerías de 5 Vistas con Metadatos ServicioTI...")
    construir_galerias()

    print("\n4/5. Sincronizando Red Nacional de Cargadores UTE Mueve en 19 Departamentos...")
    seed_chargers()

    print("\n5/5. Exportando Base Maestra a JSON y JS Offline (data/ev_data.js)...")
    export_db_to_json()

    print("\n==================================================")
    print("✅ ¡Pipeline Maestro de EV Uruguay Completado con Éxito!")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()
