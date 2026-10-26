# -*- coding: utf-8 -*-
"""
Prueba de Generación con Google Gemini Web para el Líder de Ventas #1: BYD Yuan Pro
Utilizando page.request.get(target_url) de Playwright para descarga con cookies de sesión.
"""

import os
import sys
import io
import asyncio
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

from playwright.async_api import async_playwright
from metadata_image_service import MetadataImageService

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"
PROFILE_DIR = os.path.expanduser("~/.gemini_automation_profile")

async def generar_con_gemini_web(vehicle_id: str = "byd-yuan-pro"):
    print(f"=== Iniciando Prueba de Generación en Gemini Web para {vehicle_id} ===")
    prompt = (
        "Crea una fotografía de estudio automotriz de alta gama de un auto eléctrico BYD Yuan Pro SUV 2024. "
        "Vista isométrica frontal 3/4 con el vehículo perfectamente centrado sobre un piso de estudio fotográfico "
        "blanco minimalista con sombra suave y realista bajo los neumáticos. "
        "Fotorrealismo 4K, proporciones exactas del modelo oficial, sin texto, sin letras, sin marcas de agua."
    )

    async with async_playwright() as p:
        print("[1/5] Lanzando Chrome con perfil persistente...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        page = context.pages[0] if context.pages else await context.new_page()

        try:
            print("[2/5] Accediendo a Gemini Web...")
            await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=45000)
            await asyncio.sleep(3)

            # Verificar si hay que pulsar Nuevo Chat
            new_chat = page.locator("a[aria-label*='Nuevo chat'], button[aria-label*='Nuevo chat'], a[href='/app']").first
            if await new_chat.count() > 0 and await new_chat.is_visible():
                await new_chat.click()
                await asyncio.sleep(2)

            print("[3/5] Localizando cuadro de entrada de texto...")
            textbox = page.locator("div[role='textbox'], rich-textarea div[contenteditable='true']").first
            await textbox.wait_for(state="visible", timeout=15000)
            await textbox.click()
            await textbox.fill(prompt)
            await asyncio.sleep(1)

            print("[4/5] Enviando prompt a Gemini Web (Imagen 3)...")
            send_btn = page.locator("button[aria-label*='Enviar'], button[aria-label*='Send']").first
            if await send_btn.count() > 0 and await send_btn.is_visible():
                await send_btn.click()
            else:
                await textbox.press("Enter")

            print("[5/5] Esperando generación de imagen de Gemini (hasta 60s)...")
            img_sel = "img[src*='googleusercontent.com/gg/'], single-image img, generated-image img, img[alt*='imagen']"
            img_locator = page.locator(img_sel).first
            await img_locator.wait_for(state="visible", timeout=60000)

            img_src = await img_locator.get_attribute("src")
            print(f"  ✓ Imagen generada detectada! SRC: {img_src[:80]}...")

            raw_data = None
            if img_src.startswith("http"):
                resp = await page.request.get(img_src, timeout=30000)
                if resp.status == 200:
                    raw_data = await resp.body()

            if not raw_data:
                # Screenshot del elemento
                raw_data = await img_locator.screenshot()

            output_file = IMG_DIR / vehicle_id / "gemini_generated_hero_test.webp"
            with Image.open(io.BytesIO(raw_data)) as im:
                print(f"  ✓ Dimensiones de imagen: {im.size}, formato: {im.format}")
                temp_p = IMG_DIR / vehicle_id / "temp_gemini_raw.png"
                im.save(temp_p, format="PNG")
                MetadataImageService.inyectar_y_optimizar(
                    temp_p,
                    titulo="BYD Yuan Pro EV - Generación Gemini Web Estudio Editorial",
                    descripcion="Prueba de generación editorial de estudio con Google Gemini Web Imagen 3.",
                    calidad=85,
                    destino=output_file,
                    formato="WEBP"
                )
                if temp_p.exists():
                    temp_p.unlink()

            print(f"  ✅ Imagen de Gemini guardada y optimizada en: {output_file} ({output_file.stat().st_size / 1024:.1f} KB)")
            await context.close()
            return True

        except Exception as e:
            print(f"  [AVISO / EXCEPCIÓN en Gemini Web]: {e}")
            await context.close()
            return False

if __name__ == "__main__":
    v_id = sys.argv[1] if len(sys.argv) > 1 else "byd-yuan-pro"
    asyncio.run(generar_con_gemini_web(v_id))
