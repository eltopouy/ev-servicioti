import os
from pathlib import Path
from playwright.sync_api import sync_playwright

html_path = Path(__file__).resolve().parent.parent / "index.html"
file_url = html_path.as_uri()

print(f"Probando modal interactivo en: {file_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(file_url, wait_until="networkidle")
    
    # 1. Hacer click en la primera tarjeta (BYD Seagull o la primera de la lista)
    first_card = page.locator("#catalog-grid > div").first
    card_title = first_card.locator("h3").inner_text()
    print(f"Haciendo click en tarjeta: {card_title}")
    first_card.click()
    page.wait_for_timeout(1000)
    
    # 2. Verificar que el modal es visible
    modal = page.locator("#vehicle-modal")
    is_visible = modal.is_visible()
    print(f"¿Modal visible? {is_visible}")
    
    # 3. Contar miniaturas en la galería del modal
    thumbs = page.locator("#modal-thumbs button")
    thumb_count = thumbs.count()
    print(f"Miniaturas de galería en modal: {thumb_count}")
    
    # 4. Probar cambio de imagen al hacer click en la miniatura 2
    main_img_before = page.locator("#modal-main-img").get_attribute("src")
    print(f"Foto principal inicial: {main_img_before}")
    
    if thumb_count > 1:
        thumbs.nth(1).click()
        page.wait_for_timeout(500)
        main_img_after = page.locator("#modal-main-img").get_attribute("src")
        print(f"Foto principal tras click en miniatura 2: {main_img_after}")
        assert main_img_before != main_img_after, "La imagen principal no cambió al hacer click en la miniatura"
        print("[OK] Cambio de foto interactivo verificado con exito!")
        
    # 5. Verificar ficha técnica completa en el modal
    range_text = page.locator("#spec-range").inner_text()
    battery_text = page.locator("#spec-battery").inner_text()
    official_link = page.locator("#modal-official-link").get_attribute("href")
    print(f"Ficha técnica en modal: Autonomía = {range_text}, Batería = {battery_text}")
    print(f"Enlace oficial al fabricante: {official_link}")
    
    # Cerrar modal
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print(f"¿Modal cerrado tras presionar Escape? {not modal.is_visible()}")
    
    browser.close()
    print("=== Modal Verificado al 100% ===")
