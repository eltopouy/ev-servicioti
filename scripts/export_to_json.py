"""
Exportador de SQLite a JSON estático para EV Uruguay (ev.servicioti.com.uy)
Desempaqueta las galerías de 5-6 fotos y las fichas técnicas completas
para el modal interactivo y SEO en el frontend.
"""

import json
from pathlib import Path
from db_manager import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
JSON_OUTPUT = DATA_DIR / "ev_data.json"

def export_db_to_json():
    conn = get_connection()
    cursor = conn.cursor()

    # 0. Perfiles de marcas e importadores oficiales en Uruguay
    cursor.execute("SELECT * FROM brand_profiles ORDER BY nombre ASC")
    raw_brands = [dict(row) for row in cursor.fetchall()]
    brand_profiles = []
    marca_to_profile = {}
    for bp in raw_brands:
        try:
            matched_marcas = json.loads(bp.get("marcas_json") or "[]")
        except Exception:
            matched_marcas = []
        bp["marcas_coincidentes"] = matched_marcas
        brand_profiles.append(bp)
        for m in matched_marcas:
            marca_to_profile[m.lower().strip()] = bp
        marca_to_profile[bp["nombre"].lower().strip()] = bp
        marca_to_profile[bp["id"].lower().strip()] = bp

    # 1. Vehículos oficiales con galerías y fichas, priorizando líderes de ventas
    cursor.execute("""
        SELECT * FROM vehicles 
        ORDER BY 
            CASE WHEN es_top_ventas = 1 THEN ventas_rank ELSE 999 END ASC,
            tipo ASC,
            precio_usd ASC
    """)
    raw_vehicles = [dict(row) for row in cursor.fetchall()]
    
    vehicles = []
    for v in raw_vehicles:
        v_dict = dict(v)
        # Parsear JSON de galeria y especificaciones
        try:
            v_dict["galeria"] = json.loads(v_dict.get("galeria_json") or "[]")
        except Exception:
            v_dict["galeria"] = []
        
        try:
            v_dict["especificaciones"] = json.loads(v_dict.get("especificaciones_json") or "{}")
        except Exception:
            v_dict["especificaciones"] = {}

        # Asociar perfil de marca oficial e Instagram verificado
        marca_key = (v_dict.get("marca") or "").lower().strip()
        prof = marca_to_profile.get(marca_key)
        if not prof:
            for k, p in marca_to_profile.items():
                if k in marca_key or marca_key in k:
                    prof = p
                    break
        prof = prof or {}
        v_dict["brand_id"] = prof.get("id", "")
        v_dict["brand_name"] = prof.get("nombre", v_dict.get("marca", ""))
        v_dict["brand_logo_url"] = prof.get("logo_path", "")
        v_dict["brand_instagram_handle"] = prof.get("instagram_handle", "")
        v_dict["brand_instagram_url"] = prof.get("instagram_url", "")
        v_dict["brand_importador"] = prof.get("importador_oficial", "")
        v_dict["brand_sitio_oficial"] = prof.get("sitio_oficial", "")
            
        vehicles.append(v_dict)

    # 1.1 Líderes en ventas para carrusel / destacados
    cursor.execute("""
        SELECT * FROM vehicles 
        WHERE es_top_ventas = 1 
        ORDER BY ventas_rank ASC
    """)
    raw_top = [dict(row) for row in cursor.fetchall()]
    top_sales = []
    for t in raw_top:
        t_dict = dict(t)
        try:
            t_dict["galeria"] = json.loads(t_dict.get("galeria_json") or "[]")
        except Exception:
            t_dict["galeria"] = []
        try:
            t_dict["especificaciones"] = json.loads(t_dict.get("especificaciones_json") or "{}")
        except Exception:
            t_dict["especificaciones"] = {}
        
        marca_key = (t_dict.get("marca") or "").lower().strip()
        prof = marca_to_profile.get(marca_key) or {}
        t_dict["brand_id"] = prof.get("id", "")
        t_dict["brand_name"] = prof.get("nombre", t_dict.get("marca", ""))
        t_dict["brand_logo_url"] = prof.get("logo_path", "")
        t_dict["brand_instagram_handle"] = prof.get("instagram_handle", "")
        t_dict["brand_instagram_url"] = prof.get("instagram_url", "")
        t_dict["brand_importador"] = prof.get("importador_oficial", "")
        t_dict["brand_sitio_oficial"] = prof.get("sitio_oficial", "")

        top_sales.append(t_dict)

    # 1.2 Histórico de rankings mensuales ACAU
    cursor.execute("SELECT * FROM monthly_rankings ORDER BY periodo DESC, posicion ASC")
    monthly_ranks = [dict(row) for row in cursor.fetchall()]

    # 2. Publicaciones de mercado
    cursor.execute("SELECT * FROM market_listings ORDER BY precio ASC")
    market = [dict(row) for row in cursor.fetchall()]

    # 3. Noticias / Crónicas
    cursor.execute("SELECT * FROM news_articles ORDER BY fecha_publicacion DESC")
    raw_news = [dict(row) for row in cursor.fetchall()]
    news = []
    for n in raw_news:
        n_dict = dict(n)
        try:
            n_dict["galeria"] = json.loads(n_dict.get("galeria_json") or "[]")
        except Exception:
            n_dict["galeria"] = []
        news.append(n_dict)

    # 4. Cargadores públicos UTE Mueve
    cursor.execute("SELECT * FROM charging_stations")
    chargers = [dict(row) for row in cursor.fetchall()]

    # 5. Tarifas de energía y combustibles (MIEM / URSEA / UTE)
    cursor.execute("SELECT * FROM energy_tariffs")
    tariffs = [dict(row) for row in cursor.fetchall()]

    conn.close()

    payload = {
        "metadata": {
            "title": "EV Uruguay - Revista & Directorio de Movilidad Eléctrica",
            "subdomain": "https://ev.servicioti.com.uy",
            "author": "Andrés Franchi Ugartemendía (ServicioTI)",
            "total_vehicles": len(vehicles),
            "total_brands": len(brand_profiles),
            "total_market": len(market),
            "total_news": len(news),
            "total_chargers": len(chargers),
            "total_tariffs": len(tariffs)
        },
        "brand_profiles": brand_profiles,
        "vehicles": vehicles,
        "top_sales": top_sales,
        "monthly_rankings": monthly_ranks,
        "market_listings": market,
        "news": news,
        "chargers": chargers,
        "energy_tariffs": tariffs
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Exportar JSON estándar
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # 1.1 Exportar base de marcas independiente (data/brand_profiles.json)
    brands_output = DATA_DIR / "brand_profiles.json"
    with open(brands_output, "w", encoding="utf-8") as f:
        json.dump(brand_profiles, f, ensure_ascii=False, indent=2)

    # 2. Exportar JS (ev_data.js) para compatibilidad total con file:/// sin bloqueo de CORS
    js_output = DATA_DIR / "ev_data.js"
    with open(js_output, "w", encoding="utf-8") as f:
        f.write("window.EV_DATA = " + json.dumps(payload, ensure_ascii=False) + ";\n")

    print(f"[Export] Base exportada a: {JSON_OUTPUT}")
    print(f"[Export] Archivo JS offline exportado a: {js_output}")
    print(f"         - {len(vehicles)} vehículos con galerías de 5 fotos y fichas técnicas")
    print(f"         - {len(market)} avisos de plaza")
    print(f"         - {len(news)} crónicas editoriales")
    print(f"         - {len(chargers)} cargadores de UTE")

if __name__ == "__main__":
    export_db_to_json()
