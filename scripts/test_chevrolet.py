from pathlib import Path
from playwright.sync_api import sync_playwright

html_path = Path(__file__).resolve().parent.parent / "index.html"
file_url = html_path.as_uri()

print("Verificando integración de Chevrolet...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(file_url, wait_until="networkidle")
    
    # 1. Buscar Chevrolet en el catálogo
    search_input = page.locator("#catalog-search")
    search_input.fill("Chevrolet")
    page.wait_for_timeout(500)
    
    cards = page.locator("#catalog-grid > div")
    count = cards.count()
    print(f"Modelos Chevrolet mostrados en catálogo: {count}")
    assert count == 4, f"Se esperaban 4 modelos de Chevrolet, pero se encontraron {count}"
    
    for i in range(count):
        title = cards.nth(i).locator("h3").inner_text()
        print(f"  [{i+1}] {title}")
        
    # 2. Abrir modal del Blazer EV
    blazer_card = page.locator("#catalog-grid > div", has_text="Blazer EV")
    blazer_card.click()
    page.wait_for_timeout(600)
    
    modal = page.locator("#vehicle-modal")
    assert modal.is_visible(), "El modal de Blazer EV no se abrió"
    
    # 3. Comprobar las 5 fotos en la galería y sus nombres de archivo SEO
    thumbs = page.locator("#modal-thumbs img")
    assert thumbs.count() == 5, f"Se esperaban 5 fotos en la galería, hay {thumbs.count()}"
    
    print("\nGalería SEO de Chevrolet Blazer EV:")
    for i in range(thumbs.count()):
        src = thumbs.nth(i).get_attribute("src")
        alt = thumbs.nth(i).get_attribute("alt")
        print(f"  Foto {i+1}: {src}")
        assert "chevrolet-blazer-ev" in src, "El nombre del archivo no incluye el modelo"
        assert "servicioti-uruguay" in src, "El nombre del archivo no incluye la marca de la web"
        assert src.endswith(".webp"), "La imagen no tiene formato .webp"
        assert alt and len(alt) > 10, "Falta texto alternativo descriptivo"
        
    official_link = page.locator("#modal-official-link").get_attribute("href")
    print(f"\nEnlace oficial: {official_link}")
    assert "chevrolet.com.uy" in official_link, "El enlace oficial no corresponde a Chevrolet Uruguay"
    
    print("\n[OK] Todos los requerimientos de Chevrolet verificados exitosamente con Playwright!")
    browser.close()
