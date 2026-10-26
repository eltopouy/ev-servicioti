import os
from pathlib import Path
from playwright.sync_api import sync_playwright

html_path = Path(__file__).resolve().parent.parent / "index.html"
file_url = html_path.as_uri()

print(f"Abriendo URL: {file_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    console_logs = []
    page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: console_logs.append(f"[ERROR] {err}"))
    
    page.goto(file_url, wait_until="networkidle")
    
    title = page.title()
    print(f"Título: {title}")
    
    # Verificar cantidad de tarjetas renderizadas
    cards = page.locator("#catalog-grid > div").count()
    print(f"Tarjetas en catálogo: {cards}")
    
    # Desplazar la página suavemente para activar el lazy-loading de todas las tarjetas
    page.evaluate('''async () => {
        // Cambiar imágenes a eager para forzar la verificación inmediata de carga
        const imgs = Array.from(document.querySelectorAll('#catalog-grid img'));
        imgs.forEach(img => img.loading = 'eager');
        
        // Desplazarse al final
        window.scrollTo(0, document.body.scrollHeight);
        
        await Promise.all(imgs.map(img => {
            if (img.complete) return Promise.resolve();
            return new Promise(res => {
                img.onload = img.onerror = res;
                setTimeout(res, 2500);
            });
        }));
    }''')
    
    # Verificar si hay imágenes rotas
    broken_images = page.evaluate("""
        () => {
            const imgs = Array.from(document.querySelectorAll('#catalog-grid img'));
            return imgs.map(img => ({
                src: img.src,
                complete: img.complete,
                naturalWidth: img.naturalWidth
            })).filter(img => !img.complete || img.naturalWidth === 0);
        }
    """)
    print(f"Imágenes rotas encontradas tras carga: {len(broken_images)}")
    if not broken_images:
        print("[OK] Todas las tarjetas del catálogo cargan sus imágenes WebP perfectamente.")
    for b in broken_images[:5]:
        print(f"  - Rota: {b['src']}")
        
    print("\nLogs de consola:")
    for l in console_logs:
        print(f"  {l}")
        
    browser.close()
