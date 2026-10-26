import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "data" / "ev_uruguay.db"
conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

cur.execute("UPDATE news_articles SET medio = 'Crónica EV Uruguay' WHERE medio LIKE '%Autoblog%'")
cur.execute("UPDATE news_articles SET titulo = REPLACE(titulo, 'Autoblog', 'EV Uruguay')")
cur.execute("UPDATE news_articles SET resumen = REPLACE(resumen, 'Autoblog', 'EV Uruguay')")

conn.commit()
conn.close()
print("[Sanitize] Base de datos SQLite purgada de referencias a medios de terceros.")
