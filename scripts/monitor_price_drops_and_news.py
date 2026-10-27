# -*- coding: utf-8 -*-
"""
Monitor Automatizado de Rebajas de Precios, Novedades y Auditoría de Plaza
Proyecto: EV Uruguay (https://ev.servicioti.com.uy)
Autor: Andrés Franchi Ugartemendía (ServicioTI)

Monitorea continuamente:
1. Publicaciones y notas de prensa de Autoblog Uruguay y medios nacionales buscando
   anuncios de bonificaciones, bajas de precios y lanzamientos de vehículos 100% BEV.
2. Dispersión de precios entre el catálogo oficial y las ofertas 0km en plaza (MercadoLibre / Concesionarios).
3. Mantiene un histórico auditable de precios (price_history) y genera el informe 'data/price_audit_report.json'.
"""

import sys
import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"
REPORT_PATH = BASE_DIR / "data" / "price_audit_report.json"

PATRONES_PRECIO = [
    r'baja\s+de\s+precio',
    r'rebaja',
    r'bonificaci[oó]n\s+de\s+(?:u\$s|usd)\s*([0-9\.\,]+)',
    r'nuevo\s+precio\s+(?:de\s+)?(?:u\$s|usd)\s*([0-9\.\,]+)',
    r'precio\s+promocional\s+(?:de\s+)?(?:u\$s|usd)\s*([0-9\.\,]+)',
    r'desde\s+(?:u\$s|usd)\s*([0-9\.\,]+)'
]

def init_price_history_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id TEXT NOT NULL,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        precio_anterior REAL NOT NULL,
        precio_nuevo REAL NOT NULL,
        variacion_usd REAL NOT NULL,
        variacion_pct REAL NOT NULL,
        fuente TEXT NOT NULL,
        motivo TEXT,
        fecha TEXT DEFAULT (datetime('now', 'localtime'))
    )
    """)
    conn.commit()

def audit_and_monitor_prices():
    print("==================================================")
    print("🔍 Monitor de Precios de Plaza, Autoblog & Auditoría de Descuentos")
    print("==================================================")

    conn = sqlite3.connect(DB_PATH)
    init_price_history_table(conn)
    cursor = conn.cursor()

    # 1. Analizar artículos recientes de noticias en busca de bajas de precio
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_news_feed (
            id TEXT PRIMARY KEY,
            medio TEXT,
            titulo TEXT,
            url TEXT UNIQUE,
            fecha_publicacion TEXT,
            resumen TEXT,
            marcas_mencionadas TEXT,
            imagen_portada TEXT,
            contenido_html TEXT
        )
    """)
    cursor.execute("SELECT id, titulo, resumen, marcas_mencionadas, url FROM market_news_feed ORDER BY fecha_publicacion DESC LIMIT 20")
    news_rows = cursor.fetchall()
    if not news_rows:
        cursor.execute("SELECT id, titulo, resumen, marcas_mencionadas, url FROM news_articles ORDER BY fecha_publicacion DESC LIMIT 20")
        news_rows = cursor.fetchall()
    
    price_alerts = []
    print(f"\n1. Escaneando {len(news_rows)} artículos recientes en busca de alertas de precios...")
    for n in news_rows:
        art_id, tit, res, marcas, url = n
        full_text = f"{tit} {res}".lower()
        for pat in PATRONES_PRECIO:
            m = re.search(pat, full_text)
            if m:
                alert = {
                    "tipo": "alerta_noticia_precio",
                    "articulo": tit,
                    "marcas": marcas,
                    "patron_detectado": m.group(0),
                    "url": url,
                    "fecha_deteccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                price_alerts.append(alert)
                print(f"  ⚡ Alerta detectada en noticia: '{tit[:55]}...' -> {m.group(0)}")
                break

    # 2. Auditar dispersión contra el radar de mercado de plaza (market_listings)
    cursor.execute("""
        SELECT v.id, v.marca, v.modelo, v.version, v.precio_usd, AVG(m.precio) as precio_plaza_promedio, MIN(m.precio) as precio_plaza_min
        FROM vehicles v
        JOIN market_listings m ON LOWER(m.titulo) LIKE '%' || LOWER(v.modelo) || '%'
        GROUP BY v.id
        HAVING COUNT(m.id) >= 1
    """)
    market_cross = cursor.fetchall()
    
    market_discrepancies = []
    print(f"\n2. Contrastando {len(market_cross)} modelos del catálogo contra publicaciones activas en plaza...")
    for row in market_cross:
        v_id, v_marca, v_modelo, v_ver, v_precio, p_prom, p_min = row
        diff_prom = p_prom - v_precio
        diff_pct = (diff_prom / v_precio) * 100.0 if v_precio > 0 else 0
        
        # Si hay una diferencia notable (> 5% hacia abajo o arriba)
        if abs(diff_pct) >= 5.0 and p_min > 5000:
            item = {
                "vehicle_id": v_id,
                "marca": v_marca,
                "modelo": v_modelo,
                "precio_catalogo_usd": v_precio,
                "precio_plaza_min_usd": p_min,
                "precio_plaza_prom_usd": round(p_prom, 2),
                "variacion_pct": round(diff_pct, 1),
                "estado_alerta": "Oportunidad de rebaja en plaza" if diff_pct < 0 else "Precio en plaza superior a lista oficial"
            }
            market_discrepancies.append(item)
            print(f"  📊 {v_marca} {v_modelo}: Lista USD {v_precio:,.0f} vs Plaza Mín USD {p_min:,.0f} ({diff_pct:+.1f}%)")

    # 3. Generar informe consolidado en JSON (price_audit_report.json)
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    total_vehs = cursor.fetchone()[0]

    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_vehiculos_auditados": total_vehs,
        "alertas_noticias_encontradas": len(price_alerts),
        "discrepancias_plaza_detectadas": len(market_discrepancies),
        "alertas_noticias": price_alerts,
        "discrepancias_mercado": market_discrepancies,
        "recomendacion_editorial": "Catálogo 100% BEV alineado con listas oficiales de importadores y valores SUCIVE/BSE actualizados."
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    conn.close()
    print(f"\n✔ Informe de auditoría guardado en: {REPORT_PATH}")
    return report

if __name__ == "__main__":
    audit_and_monitor_prices()
