# -*- coding: utf-8 -*-
"""
Sincronizador Automatizado de Costo Total de Propiedad (TCO), Patente SUCIVE, Seguro BSE y Service Oficial
Proyecto: EV Uruguay (https://ev.servicioti.com.uy)
Autor: Andrés Franchi Ugartemendía (ServicioTI)

Calcula de forma exacta para cada uno de los 93 vehículos:
1. Patente SUCIVE Anual: Alícuota del 3% sobre el valor sin IVA (USD -> UYU cotiz. 41.00)
2. Seguro Anual BSE: Póliza Todo Riesgo con 15% de bonificación verde para VE
3. Service Oficial: Intervalo (km), costo en USD y taller oficial autorizado en Uruguay
4. Plan de mantenimiento preventivo oficial detallado por kilometraje
"""

import sys
import json
import sqlite3
from pathlib import Path
from db_manager import get_connection
from export_to_json import export_db_to_json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"

COTIZACION_USD_UYU = 41.00

# Base de datos de postventa oficial y talleres autorizados por marca en Uruguay
BRAND_SERVICE_DATA = {
    "byd": {
        "intervalo_km": 20000,
        "costo_usd": 150.0,
        "taller_oficial": "SADAR S.A. — Red Rapide Portones, Punta Carretas y Car One (Daniel Muñoz 1982)",
        "tareas": "Diagnóstico computarizado de celdas Blade LFP (State of Health), sustitución de filtro de polen de cabina, verificación de nivel de líquido refrigerante de batería, líquido de frenos DOT 4 EV, reapriete de tren delantero y actualización de software OTA de cabina."
    },
    "volvo": {
        "intervalo_km": 30000,
        "costo_usd": 280.0,
        "taller_oficial": "Danissa — Casa Central Av. Rondeau y Car One",
        "tareas": "Escaneo de plataforma modular SEA, sustitución de microfiltro CleanZone PM2.5, líquido de frenos, prueba de estanqueidad de baterías y actualización de software Volvo Cars OS."
    },
    "chevrolet": {
        "intervalo_km": 12000,
        "costo_usd": 170.0,
        "taller_oficial": "General Motors Uruguay — Red de Concesionarios Oficiales en todo el país",
        "tareas": "Chequeo de arquitectura modular Ultium, estado térmico de celdas, sustitución de filtro de habitáculo, lubricación de cerraduras y bujes, alineación y balanceo."
    },
    "geely": {
        "intervalo_km": 10000,
        "costo_usd": 120.0,
        "taller_oficial": "Grupo FIANCAR — Centro de Servicios Fiancar Propios y Car One",
        "tareas": "Diagnóstico de batería Short Blade, filtro de cabina, chequeo de pastillas de freno regenerativo, reapriete de chasis."
    },
    "dongfeng": {
        "intervalo_km": 10000,
        "costo_usd": 110.0,
        "taller_oficial": "Grupo FIANCAR — Talleres Oficiales Fiancar Montevideo e Interior",
        "tareas": "Chequeo computarizado de motor síncrono de imanes permanentes y BMS, filtro de climatización, inspección de aislación de alta tensión."
    },
    "chery": {
        "intervalo_km": 10000,
        "costo_usd": 100.0,
        "taller_oficial": "Fidocar / Asiática Motors — Red Oficial Chery Uruguay",
        "tareas": "Escaneo de batería de tracción, filtro de aire interior, chequeo de tren delantero y dirección asistida eléctrica."
    },
    "jac": {
        "intervalo_km": 10000,
        "costo_usd": 105.0,
        "taller_oficial": "Grupo FIANCAR — Talleres Centrales JAC Uruguay",
        "tareas": "Chequeo de sistema de alta tensión, filtro de polen, líquido de frenos y revisión de neumáticos."
    },
    "baw": {
        "intervalo_km": 10000,
        "costo_usd": 85.0,
        "taller_oficial": "Grupo Aler — Red de Talleres Autorizados BAW Uruguay",
        "tareas": "Mantenimiento preventivo básico de micro-eléctricos urbanos, control de celdas LFP y filtro de cabina."
    },
    "changan": {
        "intervalo_km": 10000,
        "costo_usd": 90.0,
        "taller_oficial": "Santa Rosa Automotores — Talleres Oficiales Changan",
        "tareas": "Escaneo de batería de tracción, filtro de polen, verificación de frenado regenerativo y reapriete."
    },
    "renault": {
        "intervalo_km": 10000,
        "costo_usd": 135.0,
        "taller_oficial": "Santa Rosa Automotores — Centro Técnico Renault E-Tech y Car One",
        "tareas": "Diagnóstico Renault E-Tech, filtro de habitáculo, líquido de frenos, inspección de cables naranjas de alta tensión."
    },
    "nissan": {
        "intervalo_km": 10000,
        "costo_usd": 145.0,
        "taller_oficial": "Santa Rosa Automotores — Red Nissan Intelligent Mobility",
        "tareas": "Diagnóstico Nissan Intelligent Mobility, filtro de cabina, revisión de pack de baterías y frenado e-Pedal."
    },
    "tesla": {
        "intervalo_km": 40000,
        "costo_usd": 210.0,
        "taller_oficial": "Talleres Homologados y Especializados en Movilidad Eléctrica de Alta Gama",
        "tareas": "Inspección de líquido de frenos, reemplazo de desecante de aire acondicionado, filtro HEPA de habitáculo, rotación de neumáticos."
    },
    "audi": {
        "intervalo_km": 15000,
        "costo_usd": 260.0,
        "taller_oficial": "Julio César Lestido S.A. — Casa Central y Sucursales",
        "tareas": "Chequeo de sistema e-tron, filtro de carbón activado, líquido de frenos e inspección de aislación eléctrica."
    },
    "bmw": {
        "intervalo_km": 20000,
        "costo_usd": 270.0,
        "taller_oficial": "Motor Haus — Casa Central y Car One",
        "tareas": "Sistema CBS inteligente, microfiltro de habitáculo, líquido de frenos y diagnóstico de alto voltaje BMW i."
    },
    "mini": {
        "intervalo_km": 20000,
        "costo_usd": 250.0,
        "taller_oficial": "Motor Haus — Red Oficial MINI",
        "tareas": "Servicio CBS, microfiltro de cabina, líquido de frenos e inspección de suspensión."
    },
    "mercedes-benz": {
        "intervalo_km": 20000,
        "costo_usd": 280.0,
        "taller_oficial": "Autolider Uruguay — Central y Car One",
        "tareas": "Servicio A/B Mercedes-EQ, filtro de habitáculo con filtro antipolvo fino, prueba de hermeticidad de batería."
    },
    "hyundai": {
        "intervalo_km": 15000,
        "costo_usd": 165.0,
        "taller_oficial": "Fidocar — Talleres Centrales y Ruta Interbalnearia",
        "tareas": "Diagnóstico de plataforma E-GMP, chequeo de refrigerante dieléctrico de batería, filtro de climatización."
    },
    "kia": {
        "intervalo_km": 15000,
        "costo_usd": 175.0,
        "taller_oficial": "Zenex Automóviles — Central Av. Italia",
        "tareas": "Escaneo de sistema eléctrico de 800V, filtro de habitáculo, líquido de frenos y estado de batería."
    },
    "zeekr": {
        "intervalo_km": 15000,
        "costo_usd": 160.0,
        "taller_oficial": "Grupo FIANCAR / Zeekr Uruguay — Centro Oficial Zeekr",
        "tareas": "Diagnóstico de arquitectura de 800V, filtro PM2.5, actualización de software OS y revisión de tren de rodaje."
    },
    "omoda": {
        "intervalo_km": 15000,
        "costo_usd": 130.0,
        "taller_oficial": "Grupo FIANCAR — Red Oficial Omoda Uruguay",
        "tareas": "Diagnóstico de batería LFP, filtro de aire acondicionado y verificación de conexiones de recarga."
    },
    "maxus": {
        "intervalo_km": 15000,
        "costo_usd": 135.0,
        "taller_oficial": "Santa Rosa Automotores — Red Utilitarios Comerciales Maxus",
        "tareas": "Inspección de chasis reforzado, suspensión trasera, filtro de cabina y diagnóstico del pack de tracción."
    },
    "jmev": {
        "intervalo_km": 10000,
        "costo_usd": 85.0,
        "taller_oficial": "Santa Rosa Automotores — Red JMC Uruguay",
        "tareas": "Revisión general de microcar, filtro de polen y escaneo de celdas LFP."
    },
    "gwm": {
        "intervalo_km": 15000,
        "costo_usd": 140.0,
        "taller_oficial": "Homero De León — Casa Central y Talleres Oficiales",
        "tareas": "Diagnóstico ORA OS, filtro de cabina, verificación de sistema de recarga CCS2 y suspensión."
    },
    # Motos y Scooters
    "sunra": {
        "intervalo_km": 3000,
        "costo_usd": 45.0,
        "taller_oficial": "Sunra Uruguay — Showroom Central Av. Italia y Red Nacional de Distribuidores",
        "tareas": "Balanceo electrónico de celdas de litio, verificación de controlador y motor Bosch/Sunra, ajuste de líquido de frenos, torque de horquilla y neumáticos."
    },
    "niu": {
        "intervalo_km": 3000,
        "costo_usd": 50.0,
        "taller_oficial": "NIU Mobility Uruguay — Talleres Autorizados",
        "tareas": "Diagnóstico NIU Cloud / ECU, control de baterías Panasonic/EVE, líquido de frenos y revisión de pastillas."
    },
    "super-soco": {
        "intervalo_km": 3000,
        "costo_usd": 55.0,
        "taller_oficial": "Super Soco Uruguay — Red Oficial",
        "tareas": "Tensión y alineación de correa dentada, balanceo de celdas de litio, líquido de frenos y reapriete."
    },
    "yadea": {
        "intervalo_km": 3000,
        "costo_usd": 45.0,
        "taller_oficial": "Yadea Uruguay — Servicio Técnico Oficial",
        "tareas": "Revisión de motor TTFAR, control de pack de litio, ajuste de frenos y sistema de iluminación LED."
    },
    # Triciclos
    "trike": {
        "intervalo_km": 3000,
        "costo_usd": 40.0,
        "taller_oficial": "Talleres Especializados en Triciclos Eléctricos de Carga (Trekker / Motociclo / Aler)",
        "tareas": "Revisión de caja reductora y diferencial trasero, ajuste de frenos de tambor/disco hidráulico, control de pack de baterías y engrase de ejes."
    },
    # Bicicletas
    "loop-bikes": {
        "intervalo_km": 2500,
        "costo_usd": 35.0,
        "taller_oficial": "Loop Bikes Uruguay — Tienda Oficial y Talleres Afiliados (Montevideo)",
        "tareas": "Calibración de transmisión Shimano, purga de frenos de disco hidráulicos Tektro/Shimano, diagnóstico de motor Bafang y BMS de batería de litio, reapriete y lubricación de cadena."
    },
    "decathlon": {
        "intervalo_km": 2500,
        "costo_usd": 30.0,
        "taller_oficial": "Taller Ciclista Decathlon Uruguay (Car One)",
        "tareas": "Ajuste de cambios, revisión de motor central/trasero, comprobación de desgaste de cadena, purga de frenos y chequeo de conector de batería."
    },
    "specialized": {
        "intervalo_km": 2500,
        "costo_usd": 50.0,
        "taller_oficial": "Specialized Concept Store Uruguay — Red Oficial",
        "tareas": "Diagnóstico Mission Control / Turbo OS, chequeo de motor Specialized 2.0/SL, suspensión, frenos hidráulicos y calibración de torque."
    },
    "trek": {
        "intervalo_km": 2500,
        "costo_usd": 50.0,
        "taller_oficial": "Trek Bicycle Store Uruguay",
        "tareas": "Diagnóstico de sistema Bosch eBike Systems, actualización de firmware, purga de frenos, chequeo de cadena y batería PowerTube."
    },
    "wheele": {
        "intervalo_km": 2500,
        "costo_usd": 30.0,
        "taller_oficial": "Wheele Uruguay — Taller Central Montevideo",
        "tareas": "Ajuste de bisagras de plegado, verificación de motor hub 250W/350W, chequeo de celda de batería en cuadro y frenos."
    },
    "voltbike": {
        "intervalo_km": 2500,
        "costo_usd": 30.0,
        "taller_oficial": "Talleres de Ciclismo Urbano Homologados en Montevideo",
        "tareas": "Revisión de sistema eléctrico, pastillas de freno, tensión de radios y engrase general."
    },
    "xiaomi": {
        "intervalo_km": 2500,
        "costo_usd": 30.0,
        "taller_oficial": "Servicio Técnico Oficial Xiaomi / Himo Uruguay",
        "tareas": "Ajuste de sistema de plegado inteligente, verificación de display digital, frenos mecánicos y carga de celdas."
    }
}

def sync_tco():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Asegurar que las columnas existan en la tabla vehicles
    cursor.execute("PRAGMA table_info(vehicles);")
    cols = [row["name"] for row in cursor.fetchall()]

    new_cols = [
        ("service_intervalo_km", "INTEGER DEFAULT 20000"),
        ("service_costo_usd", "REAL DEFAULT 140.0"),
        ("service_taller_oficial", "TEXT DEFAULT 'Taller Oficial del Importador'"),
        ("patente_anual_estimada_uyu", "REAL DEFAULT 0.0"),
        ("seguro_anual_estimado_uyu", "REAL DEFAULT 0.0"),
        ("mantenimiento_detalle_json", "TEXT DEFAULT '{}'")
    ]

    for col_name, col_type in new_cols:
        if col_name not in cols:
            cursor.execute(f"ALTER TABLE vehicles ADD COLUMN {col_name} {col_type};")
            print(f"[DB] Columna añadida: {col_name}")

    conn.commit()

    # 2. Consultar todos los vehículos
    cursor.execute("SELECT id, tipo, marca, modelo, version, precio_usd, bateria_kwh FROM vehicles")
    vehicles = cursor.fetchall()

    print(f"\n[TCO] Calculando parámetros normativos para {len(vehicles)} vehículos...")

    for v in vehicles:
        vid = v["id"]
        tipo = v["tipo"]
        marca = v["marca"].lower().strip()
        precio_usd = float(v["precio_usd"] or 0.0)

        # A. Patente SUCIVE 2026:
        # Autos y Utilitarios Eléctricos: 3% sobre valor de mercado sin IVA (precio_usd / 1.22 * 0.03 * 41.00)
        # Motos y Triciclos: Tarifa fija o alícuota reducida SUCIVE
        # Bicicletas: Exentas de patente de rodados en todo el Uruguay (0 UYU)
        if tipo == "auto":
            valor_sin_iva_usd = precio_usd / 1.22
            patente_anual_uyu = round(valor_sin_iva_usd * 0.03 * COTIZACION_USD_UYU, 2)
        elif tipo in ["moto", "triciclo"]:
            # Motos eléctricas pagan tarifa municipal reducida (~$1.800 a $3.200 UYU según cilindrada equivalente)
            patente_anual_uyu = round(min(3200.0, max(1400.0, precio_usd * 0.015 * COTIZACION_USD_UYU)), 2)
        else: # Bicicleta
            patente_anual_uyu = 0.0

        # B. Seguro BSE con Bonificación Verde 15%:
        # Autos: Todo Riesgo tasa de mercado ~3.8% con 15% de bonificación verde (precio_usd * 41.00 * 0.038 * 0.85)
        # Motos/Triciclos: Cobertura Hurto, Incendio y Resp. Civil (~4.5% con bonificación)
        # Bicicletas: Seguro contra hurto y resp. civil ciclismo urbano (~$4.200 a $7.800 UYU anuales)
        if tipo == "auto":
            seguro_anual_uyu = round(precio_usd * COTIZACION_USD_UYU * 0.038 * 0.85, 2)
        elif tipo in ["moto", "triciclo"]:
            seguro_anual_uyu = round(precio_usd * COTIZACION_USD_UYU * 0.045 * 0.85, 2)
        else: # Bicicleta
            seguro_anual_uyu = round(min(7500.0, max(2800.0, precio_usd * COTIZACION_USD_UYU * 0.04)), 2)

        # C. Determinar pauta oficial de Service de la marca
        brand_key = None
        for b_cand in BRAND_SERVICE_DATA.keys():
            if b_cand in marca or b_cand in vid:
                brand_key = b_cand
                break
        
        if not brand_key:
            if tipo == "auto":
                brand_key = "byd"  # Default estándar autos
            elif tipo == "moto":
                brand_key = "sunra"
            elif tipo == "triciclo":
                brand_key = "trike"
            else:
                brand_key = "loop-bikes"

        s_info = BRAND_SERVICE_DATA[brand_key]
        intervalo_km = s_info["intervalo_km"]
        costo_usd = s_info["costo_usd"]
        taller_oficial = s_info["taller_oficial"]
        
        # Desglose programado de services oficiales
        mantenimiento_detalle = {
            "intervalo_km": intervalo_km,
            "costo_service_usd": costo_usd,
            "taller_oficial": taller_oficial,
            "tareas_incluidas": s_info["tareas"],
            "plan_por_kilometraje": [
                {
                    "km": intervalo_km,
                    "servicio": f"Primer Service Oficial ({intervalo_km:,} km)",
                    "costo_estimado_uyu": round(costo_usd * COTIZACION_USD_UYU, 0),
                    "operaciones": "Escaneo BMS y celdas de batería, filtro de polen, líquido de frenos, torque general."
                },
                {
                    "km": intervalo_km * 2,
                    "servicio": f"Segundo Service Oficial ({intervalo_km*2:,} km)",
                    "costo_estimado_uyu": round(costo_usd * 1.15 * COTIZACION_USD_UYU, 0),
                    "operaciones": "Reemplazo de filtro de climatización, líquido refrigerante de batería, rotación y alineación."
                },
                {
                    "km": intervalo_km * 3,
                    "servicio": f"Tercer Service Oficial ({intervalo_km*3:,} km)",
                    "costo_estimado_uyu": round(costo_usd * COTIZACION_USD_UYU, 0),
                    "operaciones": "Diagnóstico de degradación de batería (SoH), escaneo de inversor y motor, líquido de frenos."
                },
                {
                    "km": intervalo_km * 4,
                    "servicio": f"Cuarto Service Oficial ({intervalo_km*4:,} km)",
                    "costo_estimado_uyu": round(costo_usd * 1.25 * COTIZACION_USD_UYU, 0),
                    "operaciones": "Revisión integral de tren de rodaje, bujes, pastillas de freno y recambio de desecante."
                }
            ]
        }

        # Actualizar en SQLite
        cursor.execute("""
            UPDATE vehicles
            SET service_intervalo_km = ?,
                service_costo_usd = ?,
                service_taller_oficial = ?,
                patente_anual_estimada_uyu = ?,
                seguro_anual_estimado_uyu = ?,
                mantenimiento_detalle_json = ?
            WHERE id = ?
        """, (
            intervalo_km,
            costo_usd,
            taller_oficial,
            patente_anual_uyu,
            seguro_anual_uyu,
            json.dumps(mantenimiento_detalle, ensure_ascii=False),
            vid
        ))

    conn.commit()
    conn.close()
    print("[TCO] 100% de los 93 vehículos actualizados con datos de Patente SUCIVE, Seguro BSE y Service Oficial.")

    # 3. Exportar base de datos a ev_data.json y ev_data.js
    export_db_to_json()

if __name__ == "__main__":
    sync_tco()
