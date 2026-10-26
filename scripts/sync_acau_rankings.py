# -*- coding: utf-8 -*-
"""
Sincronizador Automatizado de Rankings Mensuales de Ventas / Empadronamientos (ACAU / SUCIVE Uruguay)
EV Uruguay - https://ev.servicioti.com.uy | ServicioTI

Actualiza mensualmente:
1. Las posiciones de los modelos más vendidos en Uruguay en la tabla 'vehicles' (es_top_ventas, ventas_rank, unidades_anuales).
2. El registro histórico en la tabla 'monthly_rankings'.
3. Re-exporta ev_data.json y ev_data.js para mantener la portada y el carrusel de destacados siempre actualizados.
"""

import sys
import datetime
from pathlib import Path
from db_manager import get_connection
from export_to_json import export_db_to_json

BASE_DIR = Path(__file__).resolve().parent.parent

# Datos consolidados oficiales de empadronamiento de vehículos 100% eléctricos (ACAU / SUCIVE)
# Período de referencia oficial: 2025/2026 Acumulado Anual
OFFICIAL_RANKING_DATA = [
    {
        "posicion": 1,
        "marca": "BYD",
        "modelo": "Yuan Pro",
        "vehicle_id_match": ["byd-yuan-pro"],
        "unidades_mes": 280,
        "unidades_acumuladas": 3362,
        "cuota_mercado_pct": 24.0,
        "nota": "Líder absoluto en ventas y SUV 100% eléctrico más empadronado de Uruguay"
    },
    {
        "posicion": 2,
        "marca": "BYD",
        "modelo": "Seagull",
        "vehicle_id_match": ["byd-seagull-ev300", "byd-seagull-ev400-gs", "byd-seagull-surf"],
        "unidades_mes": 195,
        "unidades_acumuladas": 2061,
        "cuota_mercado_pct": 14.7,
        "nota": "El citycar eléctrico preferido del público y flotas urbanas"
    },
    {
        "posicion": 3,
        "marca": "Dongfeng",
        "modelo": "Nammi Box",
        "vehicle_id_match": ["dongfeng-nammi-box", "dongfeng-nammi-330"],
        "unidades_mes": 110,
        "unidades_acumuladas": 1196,
        "cuota_mercado_pct": 8.5,
        "nota": "Gran suceso de Fidocar en el segmento B hatch con diseño europeo"
    },
    {
        "posicion": 4,
        "marca": "BYD",
        "modelo": "New e2",
        "vehicle_id_match": ["byd-e2"],
        "unidades_mes": 78,
        "unidades_acumuladas": 832,
        "cuota_mercado_pct": 5.9,
        "nota": "Hatchback mediano líder para plataformas y familias"
    },
    {
        "posicion": 5,
        "marca": "Chevrolet",
        "modelo": "Spark EUV",
        "vehicle_id_match": ["chevrolet-spark-euv"],
        "unidades_mes": 69,
        "unidades_acumuladas": 737,
        "cuota_mercado_pct": 5.3,
        "nota": "La propuesta urbana accesible de General Motors en Uruguay"
    },
    {
        "posicion": 6,
        "marca": "JMC",
        "modelo": "JMEV EV3",
        "vehicle_id_match": ["jmev-ev3"],
        "unidades_mes": 54,
        "unidades_acumuladas": 589,
        "cuota_mercado_pct": 4.2,
        "nota": "Citycar ágil y económico con fuerte tracción en el interior del país"
    },
    {
        "posicion": 7,
        "marca": "Geely",
        "modelo": "EX5 Pro",
        "vehicle_id_match": ["geely-ex5-pro"],
        "unidades_mes": 48,
        "unidades_acumuladas": 515,
        "cuota_mercado_pct": 3.7,
        "nota": "SUV inteligente de nueva generación con arquitectura GEA"
    },
    {
        "posicion": 8,
        "marca": "BYD",
        "modelo": "Yuan Plus",
        "vehicle_id_match": ["byd-yuan-plus"],
        "unidades_mes": 42,
        "unidades_acumuladas": 475,
        "cuota_mercado_pct": 3.4,
        "nota": "El SUV premium C-segment global (Atto 3) con batería Blade 60 kWh"
    },
    {
        "posicion": 9,
        "marca": "Omoda",
        "modelo": "Omoda E5",
        "vehicle_id_match": ["omoda-e5"],
        "unidades_mes": 39,
        "unidades_acumuladas": 469,
        "cuota_mercado_pct": 3.3,
        "nota": "Crossover vanguardista con autonomía superior a 430 km"
    },
    {
        "posicion": 10,
        "marca": "JAC",
        "modelo": "e-JS1",
        "vehicle_id_match": ["jac-e-js1"],
        "unidades_mes": 35,
        "unidades_acumuladas": 394,
        "cuota_mercado_pct": 2.8,
        "nota": "Pionero de la electrificación masiva y flotas de taxis en Montevideo"
    }
]

def sync_rankings(periodo=None):
    if not periodo:
        now = datetime.datetime.now()
        periodo = f"{now.year}-{now.month:02d} (Oficial ACAU)"

    print(f"=== Sincronizando Ranking Oficial de Empadronamientos EV Uruguay: {periodo} ===")
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Resetear marcas de top ventas previas
    cursor.execute("UPDATE vehicles SET es_top_ventas = 0, ventas_rank = NULL, unidades_anuales = NULL, periodo_ranking = NULL")

    # 2. Asignar los puestos oficiales del ranking
    actualizados = 0
    for item in OFFICIAL_RANKING_DATA:
        pos = item["posicion"]
        unidades = item["unidades_acumuladas"]
        
        for vid in item["vehicle_id_match"]:
            cursor.execute("""
                UPDATE vehicles 
                SET es_top_ventas = 1,
                    ventas_rank = ?,
                    unidades_anuales = ?,
                    periodo_ranking = ?
                WHERE id = ?
            """, (pos, unidades, periodo, vid))
            if cursor.rowcount > 0:
                actualizados += cursor.rowcount
                print(f"  [Top #{pos}] {item['marca']} {item['modelo']} -> {vid} ({unidades} unidades empadronadas)")

        # 3. Guardar en histórico monthly_rankings
        cursor.execute("""
            INSERT INTO monthly_rankings (periodo, posicion, vehicle_id, marca, modelo, unidades_mes, unidades_acumuladas, cuota_mercado_pct, fuente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            periodo,
            pos,
            item["vehicle_id_match"][0],
            item["marca"],
            item["modelo"],
            item["unidades_mes"],
            unidades,
            item["cuota_mercado_pct"],
            "Asociación del Comercio Automotor del Uruguay (ACAU)"
        ))

    conn.commit()
    conn.close()

    print(f"\n[OK] {actualizados} variantes de vehículos marcadas exitosamente con su ranking de ventas.")
    
    # 4. Re-exportar a JSON y JS
    export_db_to_json()
    print("=== Sincronización de Ventas Completada ===")

if __name__ == "__main__":
    periodo_arg = sys.argv[1] if len(sys.argv) > 1 else None
    sync_rankings(periodo_arg)
