import os
import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

profile_dir = os.path.expanduser("~/.gemini_automation_profile")
print(f"Probando sesión en perfil: {profile_dir}")

async def test_session():
    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                channel="chrome",
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            page = await context.new_page()
            print("Navegando a https://gemini.google.com/app...")
            await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=25000)
            await page.wait_for_timeout(4000)
            
            title = await page.title()
            url = page.url
            print(f"Página cargada - Título: {title} | URL: {url}")
            
            # Verificar si hay botón de iniciar sesión o si está dentro de la app
            sign_in = await page.query_selector("a[href*='accounts.google.com'], button:has-text('Sign in'), button:has-text('Acceder')")
            if sign_in:
                btn_text = await sign_in.inner_text()
                print(f"[Estado] Sesión NO iniciada (Botón: {btn_text})")
            else:
                input_box = await page.query_selector("div[contenteditable='true'], textarea, rich-textarea")
                if input_box:
                    print("[Estado] ¡Sesión ACTIVA en Gemini Web! Caja de prompt encontrada.")
                else:
                    print("[Estado] En página de Gemini, revisando elementos...")
            
            await context.close()
        except Exception as e:
            print(f"[Error] Falló la prueba: {e}")

if __name__ == "__main__":
    asyncio.run(test_session())
