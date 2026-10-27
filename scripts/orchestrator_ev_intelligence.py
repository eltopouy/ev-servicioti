# -*- coding: utf-8 -*-
"""
Orquestador Central de Inteligencia de Mercado y Actualizaciones Continuas: EV Uruguay
Proyecto: EV Uruguay (https://ev.servicioti.com.uy)
Autor: Andrés Franchi Ugartemendía (ServicioTI)

Ejecuta el ciclo integral de vigilancia y actualización:
1. Extracción de novedades de Autoblog Uruguay y medios del sector.
2. Homologaciones y etiquetado vehicular oficial de URSEA (UNIT 1130:2020).
3. Radar de precios de plaza y ofertas 0km (MercadoLibre / Concesionarios).
4. Monitor de auditoría de precios y alertas de rebajas.
5. Sincronización de tarifas de combustibles (MIEM/URSEA) y tarifas eléctricas (UTE).
6. Recálculo normativo en cascada de Patente SUCIVE, Seguro BSE y TCO.
7. Exportación masiva de datos a JSON y JS estático (data/ev_data.js).
"""

import sys
import time
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent

# Importar módulos especializados del pipeline
from collector_autoblog import fetch_autoblog_ev_news
from collector_ursea_homologaciones import sync_ursea_homologaciones
from collector_mercadolibre import fetch_mlu_ev_listings
from monitor_price_drops_and_news import audit_and_monitor_prices
from sync_fuel_tariffs import sync_tariffs
from sync_acau_rankings import sync_rankings
from sync_tco_parameters import sync_tco

def run_ev_intelligence_pipeline():
    start_time = time.time()
    print("=====================================================================")
    print("🚀 EJECUTANDO PIPELINE INTEGRAL DE INTELIGENCIA DE MERCADO EV URUGUAY")
    print("   Subdominio: https://ev.servicioti.com.uy")
    print("   Titular: Andrés Franchi Ugartemendía (ServicioTI)")
    print("=====================================================================\n")

    print("▶ PASO 1/7: Rastreo de Novedades y Bajas de Precio en Autoblog Uruguay...")
    try:
        fetch_autoblog_ev_news()
    except Exception as e:
        print(f"  ⚠ Advertencia en colector de Autoblog: {e}")

    print("\n▶ PASO 2/7: Auditoría de Homologaciones y Etiquetado URSEA (UNIT 1130:2020)...")
    try:
        sync_ursea_homologaciones()
    except Exception as e:
        print(f"  ⚠ Advertencia en colector URSEA: {e}")

    print("\n▶ PASO 3/7: Radar de Precios de Plaza y Ofertas en Concesionarios...")
    try:
        fetch_mlu_ev_listings()
    except Exception as e:
        print(f"  ⚠ Advertencia en radar de plaza: {e}")

    print("\n▶ PASO 4/7: Análisis de Dispersión de Precios y Detección de Descuentos...")
    try:
        audit_and_monitor_prices()
    except Exception as e:
        print(f"  ⚠ Advertencia en auditoría de precios: {e}")

    print("\n▶ PASO 5/7: Sincronización de Tarifas UTE Mueve y Precios MIEM de Combustibles...")
    try:
        sync_tariffs()
    except Exception as e:
        print(f"  ⚠ Advertencia en tarifas energéticas: {e}")

    print("\n▶ PASO 6/7: Sincronización de Ventas y Cuotas de Mercado ACAU / SUCIVE...")
    try:
        sync_rankings()
    except Exception as e:
        print(f"  ⚠ Advertencia en rankings ACAU: {e}")

    print("\n▶ PASO 7/7: Recálculo en Cascada de Patente SUCIVE, Seguro BSE, TCO y Exportación JSON/JS...")
    try:
        import subprocess
        subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "sanitize_db.py")], check=True)
        sync_tco()
    except Exception as e:
        print(f"  ⚠ Advertencia en recálculo TCO y exportación: {e}")

    elapsed = round(time.time() - start_time, 2)
    print("\n=====================================================================")
    print(f"🎉 PIPELINE DE INTELIGENCIA DE MERCADO COMPLETADO CON ÉXITO EN {elapsed}s")
    print("=====================================================================")

if __name__ == "__main__":
    run_ev_intelligence_pipeline()
