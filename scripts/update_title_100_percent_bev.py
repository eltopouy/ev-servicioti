# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
"""
Script para actualizar los títulos y encabezados de index.html
resaltando que es exclusivamente un Catálogo de Vehículos 100% Eléctricos a Batería (BEV).
"""

def main():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Title tag
    html = html.replace(
        "<title>EV Uruguay | Revista & Catálogo de Movilidad Eléctrica</title>",
        "<title>EV Uruguay | Catálogo Oficial de Vehículos 100% Eléctricos a Batería</title>"
    )

    # 2. Meta tags OpenGraph y Twitter
    html = html.replace(
        '<meta property="og:title" content="EV Uruguay | Revista & Catálogo de Movilidad Eléctrica">',
        '<meta property="og:title" content="EV Uruguay | Catálogo Oficial de Vehículos 100% Eléctricos a Batería">'
    )
    html = html.replace(
        '<meta property="og:description" content="Información técnica completa, galerías de 6 fotos de estudio 4:5, badges, precios y red de carga de autos, motos y e-bikes en Uruguay.">',
        '<meta property="og:description" content="Directorio técnico oficial y exclusivo de vehículos 100% eléctricos a batería (BEV) en Uruguay. Cero emisiones, sin motores a combustión.">'
    )
    html = html.replace(
        '<meta name="twitter:title" content="EV Uruguay | Movilidad Eléctrica">',
        '<meta name="twitter:title" content="EV Uruguay | Vehículos 100% Eléctricos a Batería">'
    )
    html = html.replace(
        '<meta name="twitter:description" content="Catálogo homologado, galerías fotográficas y precios en plaza uruguaya.">',
        '<meta name="twitter:description" content="Catálogo homologado exclusivo de vehículos 100% eléctricos a batería (BEV) en Uruguay.">'
    )

    # 3. Subtítulo en Masthead (header de la revista)
    html = html.replace(
        "Revista, Catálogo Homologado & Radar de Movilidad Eléctrica",
        "Revista & Catálogo Exclusivo de Vehículos 100% Eléctricos a Batería"
    )

    # 4. Encabezado de la Sección Catálogo (#catalogo)
    catalog_old = """      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-neutral-900 pb-2">
        <div>
          <h2 class="text-2xl sm:text-3xl font-bold font-editorial text-neutral-900">
            Catálogo Homologado
          </h2>
          <p class="text-xs text-muted mt-1">Haga clic en cualquier modelo para ver su galería oficial de 6 fotos en formato vertical 4:5, badges, ficha técnica profunda y enlace oficial</p>
        </div>"""

    catalog_new = """      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-neutral-900 pb-2">
        <div>
          <div class="flex items-center gap-2 mb-1.5 flex-wrap">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider bg-emerald-100 text-emerald-950 border border-emerald-300 px-2 py-0.5 rounded shadow-2xs">
              ⚡ 100% Eléctricos a Batería (BEV)
            </span>
            <span class="text-[11px] text-muted font-mono hidden sm:inline">
              Cero Emisiones · Sin Motores de Combustión
            </span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-bold font-editorial text-neutral-900">
            Catálogo Homologado — Vehículos 100% Eléctricos a Batería
          </h2>
          <p class="text-xs text-muted mt-1">Directorio técnico exclusivo de vehículos propulsados 100% a batería en Uruguay. Fichas oficiales con química de celdas, galerías 4:5, badges y costos de plaza</p>
        </div>"""

    if catalog_old in html:
        html = html.replace(catalog_old, catalog_new)
        print("✓ Encabezado de sección de catálogo reemplazado con éxito.")
    else:
        # Intento normalizando saltos de línea
        html_unified = html.replace("\r\n", "\n")
        catalog_old_unified = catalog_old.replace("\r\n", "\n")
        catalog_new_unified = catalog_new.replace("\r\n", "\n")
        if catalog_old_unified in html_unified:
            html = html_unified.replace(catalog_old_unified, catalog_new_unified)
            print("✓ Encabezado de sección de catálogo reemplazado tras normalizar saltos de línea.")
        else:
            print("⚠️ No se encontró catalog_old en html exacto, revisando...")

    # 5. Schema.org description
    html = html.replace(
        '"description": "Revista, catálogo y radar de vehículos eléctricos en Uruguay."',
        '"description": "Revista y catálogo oficial exclusivo de vehículos 100% eléctricos a batería (BEV) en Uruguay."'
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html guardado exitosamente!")

if __name__ == "__main__":
    main()
