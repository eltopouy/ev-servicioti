"""
Gestor de Base de Datos SQLite para EV Uruguay (ev.servicioti.com.uy)
Maneja tablas para vehiculos (con galeria de 5-6 fotos y ficha tecnica detallada),
avisos de mercado, cronicas y red de cargadores de UTE.
"""

import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ev_uruguay.db"

def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Recrear tabla vehicles para actualizar esquema con soporte de galerías y fichas técnicas
    cursor.execute("DROP TABLE IF EXISTS vehicles;")
    cursor.execute("""
    CREATE TABLE vehicles (
        id TEXT PRIMARY KEY,
        tipo TEXT NOT NULL,                -- 'auto', 'triciclo', 'moto', 'bicicleta'
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        version TEXT,
        precio_usd REAL NOT NULL,
        autonomia_km INTEGER,
        bateria_kwh REAL,
        potencia TEXT,
        par_motor_nm INTEGER,
        aceleracion_0_100 TEXT,
        velocidad_maxima TEXT,
        tiempo_carga_ac TEXT,
        tiempo_carga_dc TEXT,
        dimensiones TEXT,
        peso_kg INTEGER,
        capacidad_baul_l INTEGER,
        conector TEXT,
        garantia_vehiculo TEXT,
        garantia_bateria TEXT,
        homologado_ursea INTEGER DEFAULT 1,
        link_fabricante TEXT NOT NULL,
        imagen_oficial_url TEXT,
        galeria_json TEXT,                 -- Lista JSON de 5-6 fotos
        especificaciones_json TEXT,        -- Atributos técnicos completos
        es_top_ventas INTEGER DEFAULT 0,   -- 1 si figura en el ranking oficial ACAU de los más vendidos
        ventas_rank INTEGER,               -- Posición en el ranking (1 a 10)
        unidades_anuales INTEGER,          -- Empadronamientos oficiales
        periodo_ranking TEXT,              -- Período (ej: "2025/2026 Acumulado Oficial ACAU")
        fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 1.1 Tabla histórica de rankings mensuales de empadronamiento (ACAU / SUCIVE)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monthly_rankings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        periodo TEXT NOT NULL,
        posicion INTEGER NOT NULL,
        vehicle_id TEXT,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        unidades_mes INTEGER,
        unidades_acumuladas INTEGER,
        cuota_mercado_pct REAL,
        fuente TEXT DEFAULT 'ACAU / SUCIVE Uruguay',
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Publicaciones de mercado en plaza
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_listings (
        id TEXT PRIMARY KEY,
        tipo TEXT NOT NULL,
        marca TEXT,
        modelo TEXT,
        titulo TEXT NOT NULL,
        precio REAL NOT NULL,
        moneda TEXT DEFAULT 'USD',
        es_0km INTEGER DEFAULT 1,
        vendedor TEXT,
        es_tienda_oficial INTEGER DEFAULT 0,
        permalink TEXT NOT NULL,
        thumbnail TEXT,
        ubicacion TEXT,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Crónicas y novedades
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news_articles (
        id TEXT PRIMARY KEY,
        medio TEXT NOT NULL,
        titulo TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        fecha_publicacion DATETIME,
        resumen TEXT,
        marcas_mencionadas TEXT,
        imagen_portada TEXT,
        galeria_json TEXT DEFAULT '[]',
        contenido_html TEXT,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Red oficial de carga de UTE Mueve
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS charging_stations (
        id TEXT PRIMARY KEY,
        operador TEXT NOT NULL,
        nombre TEXT NOT NULL,
        direccion TEXT,
        departamento TEXT,
        latitud REAL NOT NULL,
        longitud REAL NOT NULL,
        conectores TEXT,
        potencia_kw REAL,
        tipo_carga TEXT,
        fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print(f"[DB] Estructura SQLite verificada y actualizada en: {DB_PATH}")

if __name__ == "__main__":
    init_db()
