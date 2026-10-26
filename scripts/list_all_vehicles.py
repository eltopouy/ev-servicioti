# -*- coding: utf-8 -*-
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('C:/Users/Andrés/.gemini/antigravity/scratch/ev_servicioti/data/ev_uruguay.db')
c = conn.cursor()
c.execute('SELECT id, tipo, marca, modelo, version, link_fabricante FROM vehicles ORDER BY tipo, marca, modelo')
rows = [{'id': r[0], 'tipo': r[1], 'marca': r[2], 'modelo': r[3], 'version': r[4], 'link': r[5]} for r in c.fetchall()]
print(f'Total vehicles: {len(rows)}')
by_tipo = {}
for r in rows:
    by_tipo.setdefault(r['tipo'], []).append(r)
for t, vs in by_tipo.items():
    print(f'=== Tipo: {t} ({len(vs)}) ===')
    for v in vs:
        print(f"  {v['id']}: {v['marca']} {v['modelo']} ({v['version']})")
