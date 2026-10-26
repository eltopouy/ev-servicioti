import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "data" / "ev_uruguay.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

forbidden_words = ["autoblog", "mercadolibre", "gallito", "motor1", "el pais", "elpais"]

found_alerts = []
for table in ['vehicles', 'charging_stations', 'market_listings', 'news_articles']:
    c.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in c.description]
    for row in c.fetchall():
        row_dict = dict(zip(cols, row))
        for col_name, val in row_dict.items():
            val_str = str(val).lower()
            for f in forbidden_words:
                if f in val_str:
                    found_alerts.append((table, row_dict.get('id', 'N/A'), col_name, f, val))

print(f"Total de menciones encontradas: {len(found_alerts)}")
for a in found_alerts:
    print(f"  [{a[0]}] ID: {a[1]} | Col: {a[2]} | Palabra: '{a[3]}' | Valor: {str(a[4])[:100]}")

conn.close()
