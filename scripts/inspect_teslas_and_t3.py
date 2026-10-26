# -*- coding: utf-8 -*-
import sqlite3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/ev_uruguay.db')
cursor = conn.cursor()

cursor.execute("SELECT id, marca, modelo, version, tipo, precio_usd, imagen_oficial_url FROM vehicles WHERE marca LIKE '%Tesla%' OR id LIKE '%tesla%'")
teslas = cursor.fetchall()
print(f"Teslas en DB: {len(teslas)}")
for t in teslas:
    print("  ->", t)

cursor.execute("SELECT id, marca, modelo, version, imagen_oficial_url, galeria_json FROM vehicles WHERE id LIKE '%t3%' OR modelo LIKE '%T3%'")
t3 = cursor.fetchall()
print(f"T3 en DB: {len(t3)}")
for row in t3:
    print("  ->", row[0], row[1], row[2], row[4])
    try:
        gal = json.loads(row[5] or "[]")
        print("     Galeria:", gal[:2])
    except Exception:
        pass

conn.close()
