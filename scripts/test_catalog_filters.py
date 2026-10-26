import os
from pathlib import Path
from playwright.sync_api import sync_playwright

html_path = Path(__file__).resolve().parent.parent / "index.html"
file_url = html_path.as_uri()

print(f"Probando filtros y buscador en: {file_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(file_url, wait_until="networkidle")
    
    # 1. Total inicial
    total_initial = page.locator("#catalog-grid > div").count()
    print(f"Total vehículos en 'todos': {total_initial}")
    assert total_initial >= 70, f"Esperados >= 70, encontrados {total_initial}"
    
    # 2. Filtrar por autos
    page.locator("button.cat-btn[data-cat='auto']").click()
    page.wait_for_timeout(300)
    autos_count = page.locator("#catalog-grid > div").count()
    print(f"Total autos filtrados: {autos_count}")
    assert autos_count > 30, "Fallo en filtro autos"
    
    # 3. Filtrar por motos
    page.locator("button.cat-btn[data-cat='moto']").click()
    page.wait_for_timeout(300)
    motos_count = page.locator("#catalog-grid > div").count()
    print(f"Total motos filtradas: {motos_count}")
    assert motos_count >= 8, "Fallo en filtro motos"
    
    # 4. Filtrar por bicicletas
    page.locator("button.cat-btn[data-cat='bicicleta']").click()
    page.wait_for_timeout(300)
    bicis_count = page.locator("#catalog-grid > div").count()
    print(f"Total bicicletas filtradas: {bicis_count}")
    assert bicis_count >= 10, "Fallo en filtro bicicletas"
    
    # 5. Volver a todos y probar buscador
    page.locator("button.cat-btn[data-cat='todos']").click()
    page.wait_for_timeout(300)
    
    search_input = page.locator("#catalog-search")
    search_input.fill("Loop")
    page.wait_for_timeout(300)
    loop_count = page.locator("#catalog-grid > div").count()
    print(f"Búsqueda 'Loop' arrojó: {loop_count} modelos")
    assert loop_count >= 3, "Buscador falló con Loop"
    
    search_input.fill("Seagull")
    page.wait_for_timeout(300)
    seagull_count = page.locator("#catalog-grid > div").count()
    print(f"Búsqueda 'Seagull' arrojó: {seagull_count} modelos")
    assert seagull_count >= 1, "Buscador falló con Seagull"
    
    browser.close()
    print("[OK] Todos los filtros y buscador funcionan perfectamente!")
