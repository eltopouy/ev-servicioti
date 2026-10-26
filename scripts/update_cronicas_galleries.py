import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"

def update_cronicas():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Verificar si existe columna galeria_json en news_articles
    cols = [col[1] for col in cursor.execute("PRAGMA table_info(news_articles)").fetchall()]
    if "galeria_json" not in cols:
        print("[DB] Agregando columna galeria_json a news_articles...")
        cursor.execute("ALTER TABLE news_articles ADD COLUMN galeria_json TEXT DEFAULT '[]'")

    def get_vehicle_gallery(vid):
        cursor.execute("SELECT galeria_json FROM vehicles WHERE id = ?", (vid,))
        row = cursor.fetchone()
        if row and row["galeria_json"]:
            try:
                return json.loads(row["galeria_json"])
            except Exception:
                return []
        return []

    # 1. BYD Liderazgo: 4 fotos auténticas del BYD Seagull Surf (frontal, trasera, interior, lateral)
    byd_gal = get_vehicle_gallery("byd-seagull-surf")
    byd_photos = byd_gal[:4] if len(byd_gal) >= 4 else byd_gal

    # 2. Chevrolet Ultium: 2 de Blazer EV + 2 de Equinox EV
    chevy_blazer = get_vehicle_gallery("chevrolet-blazer-ev")
    chevy_equinox = get_vehicle_gallery("chevrolet-equinox-ev")
    chevy_photos = []
    if chevy_blazer:
        chevy_photos.extend(chevy_blazer[:2])
    if chevy_equinox:
        chevy_photos.extend(chevy_equinox[:2])
    if len(chevy_photos) < 4 and chevy_blazer:
        chevy_photos = chevy_blazer[:4]

    # 3. Volvo EX30: 4 fotos auténticas del EX30
    volvo_gal = get_vehicle_gallery("volvo-ex30")
    volvo_photos = volvo_gal[:4] if len(volvo_gal) >= 4 else volvo_gal

    # 4. Red UTE Mueve: 4 vehículos representativos de carga pública
    nammi_gal = get_vehicle_gallery("dongfeng-nammi-box")
    panda_gal = get_vehicle_gallery("geely-panda-mini-ev")
    chery_gal = get_vehicle_gallery("chery-eq1")
    dolphin_gal = get_vehicle_gallery("byd-dolphin-gs")
    ute_photos = [
        nammi_gal[0] if nammi_gal else "",
        panda_gal[0] if panda_gal else "",
        chery_gal[0] if chery_gal else "",
        dolphin_gal[0] if dolphin_gal else ""
    ]
    ute_photos = [p for p in ute_photos if p]

    # 5. Micromovilidad: Loop Bikes, Sunra Hawk, Trek Allant, Sunra Miku
    loop_gal = get_vehicle_gallery("loop-bikes-slim-pro")
    hawk_gal = get_vehicle_gallery("sunra-hawk-3000")
    trek_gal = get_vehicle_gallery("trek-allant-plus-7")
    miku_gal = get_vehicle_gallery("sunra-miku-super")
    micro_photos = [
        loop_gal[0] if loop_gal else "",
        hawk_gal[0] if hawk_gal else "",
        trek_gal[0] if trek_gal else "",
        miku_gal[0] if miku_gal else ""
    ]
    micro_photos = [p for p in micro_photos if p]

    # 6. Beneficios fiscales: JAC e-JS1, BAW Pony EV, BAW L7 Bagel EV, Trike Cargo Light
    jac_gal = get_vehicle_gallery("jac-e-js1")
    pony_gal = get_vehicle_gallery("baw-pony-ev")
    l7_gal = get_vehicle_gallery("baw-l7-bagel-ev")
    trike_gal = get_vehicle_gallery("trike-cargo-light-500")
    fiscal_photos = [
        jac_gal[0] if jac_gal else "",
        pony_gal[0] if pony_gal else "",
        l7_gal[0] if l7_gal else "",
        trike_gal[0] if trike_gal else ""
    ]
    fiscal_photos = [p for p in fiscal_photos if p]

    cronicas_data = {
        "cronica-byd-liderazgo-2026": byd_photos,
        "cronica-chevrolet-ultium-uruguay": chevy_photos,
        "cronica-volvo-ex30-uruguay": volvo_photos,
        "cronica-red-ute-mueve-expansion": ute_photos,
        "cronica-micromovilidad-ebikes-motos": micro_photos,
        "cronica-beneficios-fiscales-sucive": fiscal_photos
    }

    for cid, photos in cronicas_data.items():
        print(f"Crónica {cid}: {len(photos)} fotos asignadas")
        cursor.execute("UPDATE news_articles SET galeria_json = ? WHERE id = ?", (json.dumps(photos, ensure_ascii=False), cid))

    conn.commit()
    conn.close()
    print("[Éxito] Galerías de crónicas actualizadas en SQLite.")

if __name__ == "__main__":
    update_cronicas()
