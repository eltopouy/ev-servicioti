from pathlib import Path
from playwright.sync_api import sync_playwright

import sys

# Forzar salida utf-8 para caracteres especiales en terminales Windows
sys.stdout.reconfigure(encoding='utf-8')

html_path = Path(__file__).resolve().parent.parent / "index.html"
file_url = html_path.as_uri()

print("=== Iniciando Verificación de Top Ventas, Variantes y Triciclos ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(file_url, wait_until="networkidle")

    # 1. Verificar el showcase de Top 10 Líderes en Ventas
    top_cards = page.locator("#top-sales-cards > div")
    top_count = top_cards.count()
    print(f"Modelos en Showcase Top Ventas ACAU: {top_count}")
    assert top_count >= 8, f"Se esperaban al menos 8 modelos destacados en el showcase, pero hay {top_count}"
    
    first_top_title = top_cards.first.locator("h4").inner_text()
    print(f"  Puesto #1 en Showcase: {first_top_title}")
    assert "Yuan Pro" in first_top_title, "El puesto #1 debería ser BYD Yuan Pro"

    # 2. Verificar que los primeros vehículos del catálogo general son los líderes de ventas
    first_catalog_card = page.locator("#catalog-grid > div").first
    card_badge = first_catalog_card.locator(".bg-gradient-to-r").inner_text()
    print(f"Insignia de la primera tarjeta del catálogo: {card_badge}")
    assert "MÁS VENDIDO EN URUGUAY" in card_badge, "La primera tarjeta del catálogo debe ser un líder de ventas"

    # 3. Probar filtro "⭐ Más Vendidos"
    page.locator("button[data-cat='top_ventas']").click()
    page.wait_for_timeout(400)
    filtered_top = page.locator("#catalog-grid > div").count()
    print(f"Tarjetas filtradas por '⭐ Más Vendidos': {filtered_top}")
    assert filtered_top >= 10, "El filtro de más vendidos debe mostrar al menos 10 vehículos"

    # 4. Probar filtro "Triciclos & Utilitarios"
    page.locator("button[data-cat='triciclo']").click()
    page.wait_for_timeout(400)
    trike_count = page.locator("#catalog-grid > div").count()
    print(f"Modelos en categoría Triciclos & Utilitarios: {trike_count}")
    assert trike_count >= 3, f"Se esperaban al menos 3 triciclos, se encontraron {trike_count}"
    
    trike_titles = [page.locator("#catalog-grid > div").nth(i).locator("h3").inner_text() for i in range(trike_count)]
    print(f"  Triciclos: {trike_titles}")

    # 5. Probar búsqueda de BYD Seagull Surf (Variante específica con fotos dedicadas)
    page.locator("button[data-cat='todos']").click()
    page.wait_for_timeout(300)
    search_input = page.locator("#catalog-search")
    search_input.fill("Seagull Surf")
    page.wait_for_timeout(400)
    
    seagull_cards = page.locator("#catalog-grid > div")
    print(f"Tarjetas para 'Seagull Surf': {seagull_cards.count()}")
    assert seagull_cards.count() == 1, "Debe aparecer exactamente la variante Seagull Surf"
    
    # Abrir modal de Seagull Surf
    seagull_cards.first.click()
    page.wait_for_timeout(500)
    modal = page.locator("#vehicle-modal")
    assert modal.is_visible(), "El modal de Seagull Surf no se abrió"
    
    modal_title = page.locator("#modal-title").inner_text()
    modal_power = page.locator("#spec-power").inner_text()
    modal_top_badge = page.locator("#modal-top-sales-badge").inner_text()
    print(f"Modal abierto: {modal_title} | Potencia: {modal_power}")
    print(f"Badge en modal: {modal_top_badge}")
    assert "88 CV" in modal_power or "65 kW" in modal_power, "La potencia de Seagull Surf debe ser 88 CV"
    assert "Top #" in modal_top_badge or "Líder de Ventas" in modal_top_badge, "Debe mostrar el badge oficial de ventas"
    
    # Comprobar nombres de archivos SEO en las 6 fotos + botón Pixel Art
    thumbs = page.locator("#modal-thumbs img")
    print(f"Fotos/Sprites en galería de Seagull Surf: {thumbs.count()}")
    assert thumbs.count() >= 6, f"La galería debe tener al menos 6 fotos, se encontraron {thumbs.count()}"
    for i in range(6):
        src = thumbs.nth(i).get_attribute("src")
        assert "seagull-surf" in src, f"Foto {i+1} debe incluir 'seagull-surf' en el nombre"
        assert "servicioti-uruguay" in src, "Debe incluir el branding de la web"
        assert src.endswith(".webp"), "Debe ser formato WebP"

    # Verificar que el badge circular oficial está presente en el modal
    modal_badge = page.locator("#modal-circular-badge")
    assert modal_badge.is_visible(), "El badge circular oficial debe ser visible en el header del modal"
    assert "badge-circular" in modal_badge.get_attribute("src"), "Debe apuntar a la miniatura circular oficial"
    
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)

    # 5.1 Probar alternancia de Modo Pixel Art 16-Bit
    print("Probando selector de Modo Pixel Art 16-Bit...")
    pixel_btn = page.locator("#view-mode-pixel")
    assert pixel_btn.is_visible(), "El botón de Pixel Art debe estar presente"
    pixel_btn.click()
    page.wait_for_timeout(400)
    
    first_card_img = page.locator("#catalog-grid img").first
    assert "pixel-art" in first_card_img.get_attribute("src"), "La imagen debe conmutar al sprite Pixel Art"
    
    # Volver a modo Foto Estudio 4:5
    page.locator("#view-mode-photo").click()
    page.wait_for_timeout(300)

    # 6. Probar búsqueda de BAW (debe mostrar L7 Bagel y Pony)
    search_input.fill("BAW")
    page.wait_for_timeout(400)
    baw_cards = page.locator("#catalog-grid > div")
    print(f"Modelos BAW encontrados: {baw_cards.count()}")
    assert baw_cards.count() >= 2, f"Se esperaban al menos 2 modelos BAW (L7 y Pony), hay {baw_cards.count()}"

    # 7. Probar búsqueda de Chery (debe mostrar eQ1 y QQ Ice Cream)
    search_input.fill("Chery")
    page.wait_for_timeout(400)
    chery_cards = page.locator("#catalog-grid > div")
    print(f"Modelos Chery encontrados: {chery_cards.count()}")
    assert chery_cards.count() >= 2, f"Se esperaban al menos 2 modelos Chery, hay {chery_cards.count()}"

    # 8. Probar búsqueda de Tesla Model Y Performance
    search_input.fill("Model Y Performance")
    page.wait_for_timeout(400)
    tesla_cards = page.locator("#catalog-grid > div")
    print(f"Modelos Tesla Model Y Performance: {tesla_cards.count()}")
    assert tesla_cards.count() == 1, "Debe encontrarse la versión Model Y Performance"

    # 9. Limpiar búsqueda y verificar carga de imágenes con scroll
    search_input.fill("")
    page.wait_for_timeout(300)
    
    page.evaluate('''async () => {
        const imgs = Array.from(document.querySelectorAll('#catalog-grid img'));
        imgs.forEach(img => img.loading = 'eager');
        window.scrollTo(0, document.body.scrollHeight);
        await Promise.all(imgs.map(img => {
            if (img.complete) return Promise.resolve();
            return new Promise(res => {
                img.onload = img.onerror = res;
                setTimeout(res, 2500);
            });
        }));
    }''')
    
    broken_imgs = page.evaluate('''() => {
        const imgs = Array.from(document.querySelectorAll('#catalog-grid img'));
        return imgs.map(img => ({
            src: img.src,
            complete: img.complete,
            naturalWidth: img.naturalWidth
        })).filter(img => !img.complete || img.naturalWidth === 0);
    }''')
    
    total_cards = page.locator("#catalog-grid > div").count()
    print(f"\nTotal tarjetas en catálogo general: {total_cards}")
    print(f"Imágenes rotas encontradas: {len(broken_imgs)}")
    assert len(broken_imgs) == 0, f"Hay {len(broken_imgs)} imágenes rotas"
    
    print("\n[OK] ¡TODAS las pruebas de Top Ventas, Variantes y Triciclos aprobadas al 100%!")
    browser.close()
