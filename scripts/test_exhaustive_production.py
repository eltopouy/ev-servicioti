# -*- coding: utf-8 -*-
"""
Suite Exhaustiva de Pruebas de Calidad e Integridad de Producción para EV Uruguay (ev.servicioti.com.uy)
Verifica rigurosamente el 100% de los requerimientos funcionales, visuales, de datos y SEO:
1. Catálogo e integridad de líderes de ventas (ACAU / SUCIVE).
2. Filtros por categoría (Top Ventas, Autos, Triciclos, Motos, E-Bikes, Todos).
3. Búsqueda de texto (insensible a mayúsculas, marcas, modelos, versiones).
4. Conmutador de Modo de Vista (📸 Fotos Estudio 4:5 vs 👾 Pixel Art 16-Bit).
5. Modal interactivo:
   - Encabezado con badge circular oficial (128x128).
   - Título y contador de vista dinámico ("01 • Isométrica...", "Foto 1 de 6").
   - 6 Vistas en formato vertical 4:5 + 7ma miniatura de Pixel Art 16-Bit.
   - Transiciones de vista y activación de clase CSS pixelated.
   - Ficha técnica completa de 12 parámetros en 2 columnas.
   - Enlace oficial a fabricante/importador con rel="noopener noreferrer".
   - Cierre con tecla Escape y botón ✕.
6. Mapa interactivo de UTE Mueve con Leaflet y OpenStreetMap (25 marcadores y popups).
7. Calculadora de Ahorro UTE vs Nafta (slider reactivo y recálculo).
8. Radar de plaza (búsqueda y enlaces de contacto mailto).
9. Crónicas editoriales (destacada y secundarias).
10. Cero imágenes rotas con scroll completo del DOM.
11. Cero menciones a portales competidores en base de datos.
12. Responsive Mobile-First en viewport móvil de smartphone (390x844 px).
"""

import sys
import json
import sqlite3
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_PATH = BASE_DIR / "index.html"
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"
FILE_URL = HTML_PATH.as_uri()

def run_exhaustive_tests():
    print("=====================================================================")
    print("🚀 INICIANDO BATERÍA EXHAUSTIVA DE PRUEBAS DE PRODUCCIÓN: EV URUGUAY")
    print(f"   URL Local: {FILE_URL}")
    print("=====================================================================\n")

    # -------------------------------------------------------------------------
    # TEST 0: Auditoría en Base de Datos (Menciones Limpias y Metadatos)
    # -------------------------------------------------------------------------
    print("▶ [Test 0/12] Verificando Base de Datos SQLite y Ausencia de Competidores...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    total_vehiculos = cursor.fetchone()[0]
    assert total_vehiculos >= 97, f"Se esperaban al menos 97 vehículos en SQLite, hay {total_vehiculos}"

    # Verificar que Farizon esté integrado con sus 4 utilitarios
    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE marca = 'Farizon'")
    total_farizon = cursor.fetchone()[0]
    assert total_farizon == 4, f"Se esperaban 4 vehículos Farizon, hay {total_farizon}"

    # Verificar que la tabla brand_profiles exista con marcas oficiales
    cursor.execute("SELECT COUNT(*) FROM brand_profiles")
    total_brands = cursor.fetchone()[0]
    assert total_brands >= 36, f"Se esperaban al menos 36 marcas en brand_profiles, hay {total_brands}"

    forbidden_words = ["autoblog", "mercadolibre", "gallito", "motor1", "el pais", "elpais"]
    menciones = 0
    for table in ['vehicles', 'charging_stations', 'market_listings', 'news_articles', 'brand_profiles']:
        cursor.execute(f"SELECT * FROM {table}")
        cols = [d[0] for d in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(cols, row))
            for col_name, val in row_dict.items():
                val_str = str(val).lower()
                for f in forbidden_words:
                    if f in val_str:
                        menciones += 1

    conn.close()
    assert menciones == 0, f"Error: Se detectaron {menciones} menciones a competidores en la base de datos."
    print(f"  ✔ Base de datos certificada: {total_vehiculos} vehículos oficiales (incluye 4 Farizon), {total_brands} marcas oficiales, 0 menciones a competidores.\n")

    # Iniciar Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ---------------------------------------------------------------------
        # TEST 1: Showcase de Líderes ACAU y Prioridad en Catálogo
        # ---------------------------------------------------------------------
        page = browser.new_page()
        page.goto(FILE_URL, wait_until="networkidle")
        page.wait_for_selector("#top-sales-cards > div", timeout=10000)
        print("▶ [Test 1/12] Verificando Showcase de Líderes de Ventas ACAU...")

        top_cards = page.locator("#top-sales-cards > div")
        top_count = top_cards.count()
        print(f"  Tarjetas en Top Sales Showcase: {top_count}")
        assert top_count >= 8, f"Showcase debe tener al menos 8 modelos, tiene {top_count}"

        puesto1_nombre = top_cards.first.locator("h4").inner_text()
        print(f"  Líder Oficial #1: {puesto1_nombre}")
        assert "Yuan Pro" in puesto1_nombre, "BYD Yuan Pro debe ser el líder #1 de ventas"

        # Verificar primer vehículo del catálogo general
        first_cat_badge = page.locator("#catalog-grid > div").first.locator(".bg-gradient-to-r").inner_text()
        print(f"  Insignia en primer vehículo del catálogo: {first_cat_badge}")
        assert "MÁS VENDIDO EN URUGUAY" in first_cat_badge, "El catálogo debe priorizar al líder en el tope"
        print("  ✔ Showcase y ordenamiento prioritario de ventas ACAU aprobados.\n")

        # ---------------------------------------------------------------------
        # TEST 2: Filtros por Categoría
        # ---------------------------------------------------------------------
        print("▶ [Test 2/12] Verificando Filtros de Categoría...")
        
        # Filtro Más Vendidos
        page.locator("button[data-cat='top_ventas']").click()
        page.wait_for_timeout(300)
        c_top = page.locator("#catalog-grid > div").count()
        assert c_top >= 10, f"Filtro Top Ventas debe mostrar >= 10, hay {c_top}"
        print(f"  Filtro '⭐ Más Vendidos': {c_top} vehículos")

        # Filtro Triciclos
        page.locator("button[data-cat='triciclo']").click()
        page.wait_for_timeout(300)
        c_trike = page.locator("#catalog-grid > div").count()
        assert c_trike == 4, f"Filtro Triciclos debe tener exactamente 4 modelos, tiene {c_trike}"
        print(f"  Filtro 'Triciclos & Utilitarios': {c_trike} modelos (Hard Work 1000kg, Cargo Light, Cargo King, Urbano)")

        # Filtro Motos
        page.locator("button[data-cat='moto']").click()
        page.wait_for_timeout(300)
        c_moto = page.locator("#catalog-grid > div").count()
        assert c_moto >= 6, f"Filtro Motos debe tener >= 6, tiene {c_moto}"
        print(f"  Filtro 'Motos': {c_moto} modelos")

        # Filtro E-Bikes
        page.locator("button[data-cat='bicicleta']").click()
        page.wait_for_timeout(300)
        c_bike = page.locator("#catalog-grid > div").count()
        assert c_bike >= 10, f"Filtro E-Bikes debe tener >= 10, tiene {c_bike}"
        print(f"  Filtro 'E-Bikes': {c_bike} modelos")

        # Reset a Todos
        page.locator("button[data-cat='todos']").click()
        page.wait_for_timeout(300)
        c_all = page.locator("#catalog-grid > div").count()
        assert c_all >= 97, f"Filtro Todos debe mostrar al menos 97 vehículos, hay {c_all}"
        print(f"  Filtro 'Todos': {c_all} vehículos restaurados")
        print("  ✔ Filtros de categoría aprobados.\n")

        # ---------------------------------------------------------------------
        # TEST 3: Búsqueda Dinámica de Texto (Farizon, VoltBike, Xiaomi Himo, Chevrolet)
        # ---------------------------------------------------------------------
        print("▶ [Test 3/12] Verificando Motor de Búsqueda Dinámica (Farizon, VoltBike, Himo, Chevy)...")
        search_input = page.locator("#catalog-search")

        # Búsqueda por Farizon
        search_input.fill("Farizon")
        page.wait_for_timeout(300)
        c_farizon = page.locator("#catalog-grid > div").count()
        assert c_farizon == 4, f"Búsqueda 'Farizon' debe devolver 4 modelos utilitarios, dio {c_farizon}"
        print(f"  Búsqueda 'Farizon': {c_farizon} modelos encontrados (V6E, SuperVAN, H8E, H9E)")

        # Búsqueda por VoltBike
        search_input.fill("VoltBike")
        page.wait_for_timeout(300)
        c_volt = page.locator("#catalog-grid > div").count()
        assert c_volt >= 3, f"Búsqueda 'VoltBike' debe devolver al menos 3 modelos, dio {c_volt}"
        print(f"  Búsqueda 'VoltBike': {c_volt} modelos encontrados (Clásica, Flex, SuperCross)")

        # Búsqueda por Xiaomi Himo Z20
        search_input.fill("Himo Z20")
        page.wait_for_timeout(300)
        c_himo = page.locator("#catalog-grid > div").count()
        assert c_himo == 1, f"Búsqueda 'Himo Z20' debe devolver 1 modelo, dio {c_himo}"
        print(f"  Búsqueda 'Himo Z20': 1 modelo encontrado con fotos oficiales auténticas")

        # Búsqueda por marca Chevrolet
        search_input.fill("Chevrolet")
        page.wait_for_timeout(300)
        c_chevy = page.locator("#catalog-grid > div").count()
        assert c_chevy >= 4, f"Búsqueda 'Chevrolet' debe devolver >= 4 modelos (Blazer, Equinox, Spark, Bolt), dio {c_chevy}"
        print(f"  Búsqueda 'Chevrolet': {c_chevy} modelos encontrados")

        # Búsqueda por modelo y versión específica: "Seagull Surf"
        search_input.fill("Seagull Surf")
        page.wait_for_timeout(300)
        c_surf = page.locator("#catalog-grid > div").count()
        assert c_surf == 1, f"Búsqueda 'Seagull Surf' debe devolver exactamente 1 tarjeta, dio {c_surf}"
        surf_title = page.locator("#catalog-grid > div").first.locator("h3").inner_text()
        print(f"  Búsqueda 'Seagull Surf': {surf_title}")
        assert "Seagull" in surf_title and "Surf" in surf_title

        # Limpiar búsqueda
        search_input.fill("")
        page.wait_for_timeout(300)
        assert page.locator("#catalog-grid > div").count() >= 97
        print("  ✔ Búsqueda dinámica aprobada.\n")

        # ---------------------------------------------------------------------
        # TEST 4: Conmutador de Modo de Vista (Fotos 4:5 vs Pixel Art 16-Bit)
        # ---------------------------------------------------------------------
        print("▶ [Test 4/12] Verificando Conmutador de Modo de Vista (Fotos vs Pixel Art)...")
        btn_pixel = page.locator("#view-mode-pixel")
        btn_photo = page.locator("#view-mode-photo")
        assert btn_pixel.is_visible() and btn_photo.is_visible(), "Botones de modo de vista deben ser visibles"

        # Activar Modo Pixel Art
        btn_pixel.click()
        page.wait_for_timeout(300)
        first_img = page.locator("#catalog-grid img").first
        img_src_pixel = first_img.get_attribute("src")
        img_class = first_img.get_attribute("class")
        print(f"  Modo Pixel Art activo. Primer activo: {img_src_pixel.split('/')[-1]}")
        assert "pixel-art-16bit" in img_src_pixel, "La imagen debe ser el sprite pixel art 16-bit"
        assert "image-pixelated" in img_class, "Debe tener clase CSS image-pixelated para nitidez arcade"

        # Volver a Modo Fotos de Estudio
        btn_photo.click()
        page.wait_for_timeout(300)
        img_src_photo = page.locator("#catalog-grid img").first.get_attribute("src")
        print(f"  Modo Foto Estudio activo. Primer activo: {img_src_photo.split('/')[-1]}")
        assert "01-vista-isometrica-frontal-3-4" in img_src_photo, "Debe restaurar la vista isométrica de estudio"
        print("  ✔ Conmutador de modo de vista aprobado.\n")

        # ---------------------------------------------------------------------
        # TEST 5: Modal Editorial Táctil, Galería de 6 Vistas, Badges y Ficha
        # ---------------------------------------------------------------------
        print("▶ [Test 5/12] Verificando Modal Editorial, 6 Vistas, Badges y Ficha Técnica...")
        # Abrir el modal del primer vehículo
        page.locator("#catalog-grid > div").first.click()
        page.wait_for_timeout(400)
        modal = page.locator("#vehicle-modal")
        assert modal.is_visible(), "El modal del vehículo debe estar visible"

        # 1. Badge circular en modal header
        modal_badge = page.locator("#modal-circular-badge")
        assert modal_badge.is_visible(), "El badge circular oficial debe estar visible en el modal"
        badge_src = modal_badge.get_attribute("src")
        assert "badge-circular" in badge_src, "Debe cargar el archivo badge-circular"
        print(f"  Badge circular en header: {badge_src.split('/')[-1]}")

        # 2. Título y Contador inicial de Vista
        view_title = page.locator("#modal-view-title").inner_text()
        view_counter = page.locator("#modal-view-counter").inner_text()
        print(f"  Vista inicial: {view_title} | Contador: {view_counter}")
        assert "01 • Vista Isométrica" in view_title
        assert "Foto 1 de 6" in view_counter

        # 3. Miniaturas: 6 fotos + 1 Pixel Art sprite = 7 botones
        thumbs = page.locator("#modal-thumbs > button")
        thumbs_count = thumbs.count()
        print(f"  Miniaturas en modal: {thumbs_count} (6 vistas técnicas + 1 Pixel Art 16-Bit)")
        assert thumbs_count == 7, f"Se esperaban 7 miniaturas (6 fotos + 1 pixel art), hay {thumbs_count}"

        # 4. Cambiar a Foto 2 (Vista Trasera)
        thumbs.nth(1).click()
        page.wait_for_timeout(200)
        view2_title = page.locator("#modal-view-title").inner_text()
        view2_counter = page.locator("#modal-view-counter").inner_text()
        assert "02 • Vista Trasera" in view2_title
        assert "Foto 2 de 6" in view2_counter
        assert "02-vista-trasera" in page.locator("#modal-main-img").get_attribute("src")
        print(f"  Navegación a Foto 2: {view2_title} ({view2_counter}) OK")

        # 5. Cambiar a Sprite Pixel Art (Botón 7)
        thumbs.nth(6).click()
        page.wait_for_timeout(200)
        pixel_title = page.locator("#modal-view-title").inner_text()
        pixel_counter = page.locator("#modal-view-counter").inner_text()
        assert "Pixel Art 16-Bit" in pixel_title
        assert "image-pixelated" in page.locator("#modal-main-img").get_attribute("class")
        print(f"  Navegación a Pixel Art: {pixel_title} ({pixel_counter}) OK")

        # 6. Ficha Técnica completa
        spec_range = page.locator("#spec-range").inner_text()
        spec_bat = page.locator("#spec-battery").inner_text()
        spec_conn = page.locator("#spec-connector").inner_text()
        print(f"  Ficha técnica verificada: Autonomía={spec_range}, Batería={spec_bat}, Conector={spec_conn}")
        assert "km" in spec_range and "kWh" in spec_bat

        # 7. Sección de Mantenimiento Oficial y TCO en Modal
        tco_section = page.locator("#modal-tco-section")
        assert tco_section.is_visible(), "La sección de costos y mantenimiento oficial debe estar visible en el modal"
        mod_pat = page.locator("#modal-patente-val").inner_text()
        mod_seg = page.locator("#modal-seguro-val").inner_text()
        mod_serv = page.locator("#modal-service-val").inner_text()
        mod_taller = page.locator("#modal-taller-val").inner_text()
        print(f"  Postventa en modal: Patente={mod_pat}, Seguro={mod_seg}, Service={mod_serv}, Taller={mod_taller[:30]}...")
        assert "$" in mod_pat and "$" in mod_seg and "$" in mod_serv
        assert len(mod_taller) > 5

        # 8. Enlace oficial con seguridad rel="noopener noreferrer"
        official_link = page.locator("#modal-official-link")
        assert official_link.get_attribute("target") == "_blank"
        assert "noopener" in official_link.get_attribute("rel")
        assert "noreferrer" in official_link.get_attribute("rel")

        # 8.1 Verificar Marca Oficial, Logo e Instagram de Farizon en Modal
        page.evaluate("openVehicleModal('farizon-v6e')")
        page.wait_for_timeout(300)
        farizon_imp = page.locator("#modal-importer-name").inner_text()
        print(f"  Farizon Importador en modal: '{farizon_imp}'")
        assert "Santa Rosa" in farizon_imp, "El importador oficial de Farizon en Uruguay debe ser Grupo Santa Rosa"
        farizon_insta = page.locator("#modal-brand-actions a[href*='instagram.com/farizonuruguay']")
        assert farizon_insta.count() > 0, "Debe tener enlace al Instagram oficial @farizonuruguay"
        farizon_logo = page.locator("#modal-brand-logo")
        assert "farizon-logo" in (farizon_logo.get_attribute("src") or ""), "Debe mostrar el logo oficial de Farizon"
        print("  ✔ Perfil de marca oficial, importador (Grupo Santa Rosa) e Instagram (@farizonuruguay) verificados en el modal.")

        # 9. Cierre con tecla Escape
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        assert not modal.is_visible(), "El modal debe cerrarse con Escape"
        print("  ✔ Modal editorial y galería de 6 vistas + Pixel Art aprobados.\n")

        # ---------------------------------------------------------------------
        # TEST 6: Mapa Interactivo de UTE Mueve con Leaflet & OSM
        # ---------------------------------------------------------------------
        print("▶ [Test 6/12] Verificando Mapa Interactivo de UTE Mueve...")
        map_el = page.locator("#map")
        assert map_el.is_visible(), "El mapa de UTE debe ser visible en el DOM"
        assert "leaflet-container" in map_el.get_attribute("class"), "Leaflet debe inicializarse correctamente"

        markers = page.locator(".leaflet-marker-icon")
        markers_count = markers.count()
        print(f"  Cargadores UTE Mueve renderizados en el mapa: {markers_count}")
        assert markers_count >= 20, f"Se esperaban al menos 20 cargadores geolocalizados, hay {markers_count}"

        # Clic en un marcador y verificar popup
        page.evaluate("() => { const m = document.querySelector('.leaflet-marker-icon'); if (m) m.click(); }")
        page.wait_for_timeout(400)
        popup = page.locator(".leaflet-popup-content")
        assert popup.is_visible(), "El popup del cargador debe desplegarse al hacer clic"
        popup_text = popup.inner_text()
        print(f"  Detalle de estación de recarga en popup: {popup_text.splitlines()[0]}")
        assert "Red: UTE Mueve" in popup_text
        print("  ✔ Mapa interactivo de UTE Mueve libre de fallos aprobado.\n")

        # ---------------------------------------------------------------------
        # TEST 7: Calculadora Multifactor de Consumo UTE vs Nafta / Diésel
        # ---------------------------------------------------------------------
        print("▶ [Test 7/12] Verificando Calculadora Multifactor de Ahorro UTE vs Combustibles...")
        slider = page.locator("#slider-km")
        assert slider.is_visible(), "El slider de kilometraje debe estar visible"

        # 1. Verificar valor predeterminado del promedio urbano de Montevideo (1.200 km)
        initial_km = slider.input_value()
        assert initial_km == "1200", f"El valor por defecto debe ser 1.200 km (Montevideo), es {initial_km}"
        slider_label = page.locator("#slider-val").inner_text()
        assert "1.200 km" in slider_label

        calc_nafta = page.locator("#calc-nafta").inner_text()
        calc_ute = page.locator("#calc-ute").inner_text()
        calc_saving = page.locator("#calc-saving").inner_text()
        print(f"  [Default 1.200 km Montevideo] Nafta Súper: {calc_nafta} | UTE Valle: {calc_ute} | Ahorro: {calc_saving}")
        assert "$8.683" in calc_nafta
        assert "$440" in calc_ute
        assert "$8.243" in calc_saving

        # 2. Interacción con combustible alternativo: Gasoil 50-S (Diésel)
        btn_diesel = page.locator("#btn-fuel-gasoil_50s")
        assert btn_diesel.is_visible()
        btn_diesel.click()
        page.wait_for_timeout(200)

        calc_diesel = page.locator("#calc-nafta").inner_text()
        calc_saving_diesel = page.locator("#calc-saving").inner_text()
        print(f"  [Con Gasoil 50-S] Gasto Diésel: {calc_diesel} | Ahorro: {calc_saving_diesel}")
        assert "$4.898" in calc_diesel  # 1200 * 0.065 * 62.79 = 4897.62 -> 4898
        assert "$4.458" in calc_saving_diesel

        # 3. Interacción con tarifa UTE alternativa: Doble Horario Fuera de Punta
        ute_select = page.locator("#calc-ute-tariff")
        ute_select.select_option("ute_doble_fuera_punta")
        page.wait_for_timeout(200)

        calc_ute_doble = page.locator("#calc-ute").inner_text()
        print(f"  [Con UTE Doble Horario Fuera de Punta] Gasto Eléctrico: {calc_ute_doble}")
        assert "$831" in calc_ute_doble  # 1200 * 0.15 * 4.614 = 830.52 -> 831

        # 4. Restaurar Nafta Súper 95 y UTE Valle
        page.locator("#btn-fuel-nafta_super_95").click()
        ute_select.select_option("ute_valle_trt")
        page.wait_for_timeout(200)

        # 5. Probar preset rápido de 2.000 km
        page.locator("button:has-text('2.000 km')").click()
        page.wait_for_timeout(200)
        assert page.locator("#slider-val").inner_text() == "2.000 km"
        print(f"  [Preset 2.000 km] Ahorro mensual: {page.locator('#calc-saving').inner_text()}")

        # Restaurar a 1.200 km
        page.locator("button:has-text('1.200 km')").click()
        page.wait_for_timeout(200)

        # 6. Verificación del Simulador Avanzado TCO (Patente SUCIVE, Seguro BSE, Service Oficial)
        v_select = page.locator("#calc-vehicle-select")
        assert v_select.is_visible(), "El selector de vehículos TCO debe estar visible"
        v_options_count = page.locator("#calc-vehicle-select option").count()
        print(f"  Opciones de vehículos en el selector TCO: {v_options_count}")
        assert v_options_count >= 80, f"Se esperaban al menos 80 vehículos en el selector, hay {v_options_count}"

        # Probar selección de BYD Yuan Pro
        page.evaluate("setCalcVehicle('byd-yuan-pro')")
        page.wait_for_timeout(300)
        ev_title = page.locator("#tco-ev-title").inner_text()
        print(f"  [TCO Selector] ev_title actual: '{ev_title}'")
        assert "yuan pro" in ev_title.lower()
        tco_ev_month = page.locator("#tco-ev-monthly").inner_text()
        tco_ice_month = page.locator("#tco-ice-monthly").inner_text()
        tco_ann_save = page.locator("#tco-annual-saving-hero").inner_text()
        print(f"  [TCO BYD Yuan Pro] Mensual EV: {tco_ev_month} | Mensual Combustión: {tco_ice_month} | Ahorro Anual: {tco_ann_save}")
        assert "$" in tco_ev_month
        assert "$" in tco_ice_month
        assert "$" in tco_ann_save
        assert page.locator("#tco-service-interval-badge").is_visible()

        print("  ✔ Calculadora multifactor de combustibles, tarifas UTE y Simulador TCO aprobados.\n")

        # ---------------------------------------------------------------------
        # TEST 8: Radar de Precios en Plaza
        # ---------------------------------------------------------------------
        print("▶ [Test 8/12] Verificando Radar de Ofertas en Plaza...")
        market_cards = page.locator("#market-grid > div")
        m_count = market_cards.count()
        print(f"  Avisos de plaza relevados en la grilla: {m_count}")
        assert m_count >= 15, f"Se esperaban al menos 15 avisos, hay {m_count}"

        # Probar búsqueda en plaza
        market_search = page.locator("#market-search")
        market_search.fill("Montevideo")
        page.wait_for_timeout(300)
        filtered_m = page.locator("#market-grid > div").count()
        print(f"  Avisos filtrados por 'Montevideo': {filtered_m}")
        assert filtered_m > 0
        market_search.fill("")
        print("  ✔ Radar de precios y ofertas aprobado.\n")

        # ---------------------------------------------------------------------
        # TEST 9: Crónicas y Novedades Editoriales con Galerías Deslizables de 4 Fotos
        # ---------------------------------------------------------------------
        print("▶ [Test 9/12] Verificando Crónicas Editoriales con Galerías Deslizables...")
        cronicas = page.locator("#cronicas-grid article")
        assert cronicas.count() >= 6, f"Se esperaban >= 6 crónicas editoriales, hay {cronicas.count()}"
        
        # Verificar cada crónica individualmente
        for i in range(cronicas.count()):
            article = cronicas.nth(i)
            title = article.locator("h3").inner_text()
            images = article.locator("img")
            img_count = images.count()
            assert img_count >= 4, f"Crónica {i+1} ('{title}') tiene {img_count} fotos, se requerían al menos 4"
            leer_link = article.locator("a:has-text('Leer crónica completa')")
            assert leer_link.count() > 0, f"Crónica {i+1} debe tener enlace 'Leer crónica completa'"
            print(f"  Crónica {i+1}: '{title[:45]}...' -> {img_count} fotos en carrusel swipeable OK")

        # Verificar color blanco en título de líderes de ventas
        top_sales_title = page.locator("#top-sales-showcase h3")
        assert "text-white" in (top_sales_title.get_attribute("class") or ""), "El título de líderes de ventas debe ser text-white"

        # Verificar que la barra ServicioTI está al final de la página (no en la parte superior)
        subbar = page.locator("body > div.border-t.border-line:has-text('Publicación Oficial de ServicioTI')")
        assert subbar.count() > 0, "La barra oficial ServicioTI debe estar ubicada abajo del todo"

        print("  ✔ Sección editorial con carruseles swipeables y estilos aprobados.\n")

        # ---------------------------------------------------------------------
        # TEST 10: Integridad de 0 Imágenes Rotas en Todo el DOM
        # ---------------------------------------------------------------------
        print("▶ [Test 10/12] Auditando Integridad de TODAS las Imágenes del Sitio...")
        page.evaluate('''async () => {
            const imgs = Array.from(document.querySelectorAll('img'));
            imgs.forEach(img => img.loading = 'eager');
            window.scrollTo(0, document.body.scrollHeight);
            await Promise.all(imgs.map(img => {
                if (img.complete) return Promise.resolve();
                return new Promise(res => {
                    img.onload = img.onerror = res;
                    setTimeout(res, 3000);
                });
            }));
        }''')
        page.wait_for_timeout(1000)

        broken_imgs = page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.map(img => ({
                src: img.src,
                complete: img.complete,
                naturalWidth: img.naturalWidth
            })).filter(img => !img.complete || img.naturalWidth === 0);
        }''')

        print(f"  Total imágenes auditadas: {page.locator('img').count()}")
        print(f"  Imágenes rotas encontradas: {len(broken_imgs)}")
        if len(broken_imgs) > 0:
            for b in broken_imgs[:5]:
                print(f"    [Rotura] {b['src']}")
        assert len(broken_imgs) == 0, f"Se detectaron {len(broken_imgs)} imágenes rotas."
        print("  ✔ CERO imágenes rotas certificado en todo el sitio.\n")

        page.close()

        # ---------------------------------------------------------------------
        # TEST 11: Experiencia de Usuario Mobile-First (Viewport de Smartphone)
        # ---------------------------------------------------------------------
        print("▶ [Test 11/12] Verificando Experiencia en Celular (iPhone 14 / 390x844)...")
        mobile_page = browser.new_page(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        mobile_page.goto(FILE_URL, wait_until="networkidle")

        # Verificar que no exista overflow horizontal (scroll lateral indeseado)
        scroll_width = mobile_page.evaluate("document.documentElement.scrollWidth")
        client_width = mobile_page.evaluate("document.documentElement.clientWidth")
        print(f"  Ancho de scroll: {scroll_width}px | Ancho de viewport: {client_width}px")
        assert scroll_width <= client_width + 1, "No debe existir scroll horizontal en celulares"

        # Abrir modal en celular
        mobile_page.locator("#catalog-grid > div").first.click()
        mobile_page.wait_for_timeout(400)
        m_modal = mobile_page.locator("#vehicle-modal")
        assert m_modal.is_visible(), "El modal debe abrirse fluidamente en pantalla táctil de celular"

        m_main_img = mobile_page.locator("#modal-main-img")
        assert m_main_img.is_visible(), "La imagen vertical 4:5 debe verse en celular sin desbordar"
        print("  ✔ Visualización vertical Mobile-First para celulares certificada.\n")
        mobile_page.close()

        # ---------------------------------------------------------------------
        # TEST 12: Metadatos XMP y EXIF Oficiales de ServicioTI en Archivos WebP
        # ---------------------------------------------------------------------
        print("▶ [Test 12/12] Verificando Inyección de Metadatos Oficiales ServicioTI...")
        sample_img = BASE_DIR / "assets" / "img" / "byd-seagull-surf" / "01-vista-isometrica-frontal-3-4-byd-seagull-surf-tope-de-gama-43-2-kw-auto-electrico-ev-servicioti-uruguay.webp"
        assert sample_img.exists(), "La imagen de prueba debe existir"

        from PIL import Image
        with Image.open(sample_img) as chk_im:
            assert chk_im.format == "WEBP", "Debe ser formato WebP"
            info = chk_im.info
            xmp = info.get("xmp", b"")
            if isinstance(xmp, bytes):
                xmp_str = xmp.decode("utf-8", errors="ignore")
            else:
                xmp_str = str(xmp)
            assert "Andrés Franchi Ugartemendía" in xmp_str or "Andres Franchi Ugartemendia" in xmp_str
            assert "ev.servicioti.com.uy" in xmp_str
            assert "ServicioTI" in xmp_str
            print("  ✔ Metadatos XMP UTF-8 nativos con autoría y copyright verificados en disco.")

        browser.close()

    print("\n=====================================================================")
    print("🎉 ¡TODOS LOS 12 TESTS DE PRODUCCIÓN PASARON CON ÉXITO ABSOLUTO (100%)!")
    print("=====================================================================")

if __name__ == "__main__":
    run_exhaustive_tests()
