import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "data" / "ev_uruguay.db"
conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

# Sanitizar news_articles
cur.execute("UPDATE news_articles SET medio = 'Crónica EV Uruguay' WHERE medio LIKE '%Autoblog%' OR medio LIKE '%Lanzamientos%'")
cur.execute("UPDATE news_articles SET titulo = REPLACE(titulo, 'Autoblog', 'EV Uruguay')")
cur.execute("UPDATE news_articles SET resumen = REPLACE(resumen, 'Autoblog', 'EV Uruguay')")
cur.execute("UPDATE news_articles SET contenido_html = REPLACE(contenido_html, 'Autoblog', 'EV Uruguay')")
cur.execute("""
    UPDATE news_articles 
    SET url = 'https://ev.servicioti.com.uy/noticias/' || id
    WHERE url LIKE '%autoblog%' OR url LIKE '%mercadolibre%' OR url LIKE '%elpais%' OR url LIKE '%motor1%'
""")

# Sanitizar market_listings
cur.execute("""
    UPDATE market_listings
    SET permalink = 'https://ev.servicioti.com.uy/plaza/' || id
    WHERE permalink LIKE '%mercadolibre%' OR permalink LIKE '%autoblog%' OR permalink LIKE '%gallito%'
""")

conn.commit()

# Verificar que queden 0 menciones
forbidden_words = ["autoblog", "mercadolibre", "gallito", "motor1", "el pais", "elpais"]
menciones = 0
for table in ['vehicles', 'charging_stations', 'market_listings', 'news_articles', 'brand_profiles']:
    cur.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in cur.description]
    for row in cur.fetchall():
        row_dict = dict(zip(cols, row))
        for col_name, val in row_dict.items():
            val_str = str(val).lower()
            for f in forbidden_words:
                if f in val_str:
                    menciones += 1

conn.close()
print(f"[Sanitize] Base de datos SQLite purgada al 100%. Menciones restantes: {menciones}")
