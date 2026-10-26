# -*- coding: utf-8 -*-
"""
Generador Automatizado de Pixel Art 16-Bit en Lotes con Google Gemini Web (Imagen 3)
Proyecto: EV Uruguay (https://ev.servicioti.com.uy)
Autor: Andrés Franchi Ugartemendía (ServicioTI)

Características:
- 100% Gratuito utilizando el perfil autenticado en ~/.gemini_automation_profile
- Prompts de alta ingeniería adaptados a cada categoría (autos, SUVs, motos, e-bikes, utilitarios)
- Control de cuota, pausas de resiliencia y seguimiento persistente en data/pixel_art_gemini_progress.json
- Reemplazo directo en el archivo SEO de pixel art oficial de cada vehículo
- Inyección de metadatos oficiales UTF-8 XMP de ServicioTI
"""

import os
import sys
import io
import json
import sqlite3
import argparse
import asyncio
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

from playwright.async_api import async_playwright
from metadata_image_service import MetadataImageService

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"
IMG_DIR = BASE_DIR / "assets" / "img"
PROGRESS_FILE = BASE_DIR / "data" / "pixel_art_gemini_progress.json"
PROFILE_DIR = os.path.expanduser("~/.gemini_automation_profile")

def build_prompt(v: dict) -> str:
    marca = v.get("marca", "")
    modelo = v.get("modelo", "")
    tipo = v.get("tipo", "auto").lower()

    if "moto" in tipo:
        return (
            f"16-bit retro arcade pixel art of a {marca} {modelo} electric scooter motorcycle. "
            "Classic SNES and Neo-Geo video game sprite aesthetic, 3/4 isometric side angle view. "
            "Crisp clean pixel grid lines, distinct outlines, detailed wheels and handlebars, iconic styling. "
            "Completely isolated on an entirely pure white background (#ffffff), zero background clutter, "
            "no shadows on walls, no text, no typography, no watermarks. Masterpiece retro video game asset."
        )
    elif "bici" in tipo or "bicicleta" in tipo:
        return (
            f"16-bit retro arcade pixel art of a {marca} {modelo} electric bicycle. "
            "Classic SNES video game sprite aesthetic, isometric 3/4 side profile view. "
            "Crisp clean pixel grid lines, detailed spokes, battery integrated downtube, distinct outlines. "
            "Completely isolated on an entirely pure white background (#ffffff), zero background clutter, "
            "no shadows on walls, no text, no typography, no watermarks. Masterpiece retro video game asset."
        )
    elif "trike" in tipo or "triciclo" in tipo or "utilitario" in tipo:
        return (
            f"16-bit retro arcade pixel art of a {marca} {modelo} electric cargo utility trike. "
            "Classic arcade video game sprite aesthetic, isometric 3/4 front view. "
            "Crisp clean pixel grid lines, distinct outlines, heavy-duty cargo bed, electric motor detail. "
            "Completely isolated on an entirely pure white background (#ffffff), zero background clutter, "
            "no shadows on walls, no text, no typography, no watermarks. Masterpiece retro video game asset."
        )
    else:
        return (
            f"16-bit retro arcade pixel art of a {marca} {modelo} electric car. "
            "Classic SNES and Neo-Geo video game sprite aesthetic, isometric 3/4 angle view. "
            "Crisp clean pixel grid lines, distinct outlines, iconic vibrant color palette, accurate vehicle proportions, "
            "glowing headlights, detailed alloy wheels in pixel art style. "
            "Completely isolated on an entirely pure white background (#ffffff), zero background clutter, "
            "no shadows on walls, no text, no typography, no watermarks. Masterpiece retro video game asset."
        )

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_progress(progress: dict):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

async def generate_batch(limit: int = 5, force: bool = False, filter_ids: list = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT id, marca, modelo, version, tipo, es_top_ventas, ventas_rank, especificaciones_json, imagen_oficial_url 
        FROM vehicles 
        ORDER BY 
            CASE WHEN es_top_ventas = 1 THEN ventas_rank ELSE 999 END ASC,
            tipo ASC
    """
    vehicles = [dict(r) for r in cursor.execute(query).fetchall()]
    conn.close()

    progress = load_progress()

    pending = []
    for v in vehicles:
        vid = v["id"]
        if filter_ids and vid not in filter_ids:
            continue
        if not force and progress.get(vid, {}).get("status") == "success":
            continue
        pending.append(v)

    if not pending:
        print("[Gemini Pixel Art] No hay vehículos pendientes de generación.")
        return

    to_process = pending[:limit]
    print(f"=== Procesando Lote de {len(to_process)} Vehículos con Google Gemini Web ===")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print("[Browser] Conectando con Gemini Web...")
        await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=45000)
        await asyncio.sleep(3)

        success_count = 0
        for idx, v in enumerate(to_process, 1):
            vid = v["id"]
            name = f"{v['marca']} {v['modelo']}"
            print(f"\n[{idx}/{len(to_process)}] Generando Pixel Art para: {name} (ID: {vid})")

            prompt = build_prompt(v)

            try:
                # 1. Iniciar nuevo chat para contexto limpio
                new_chat = page.locator("a[aria-label*='Nuevo chat'], button[aria-label*='Nuevo chat'], a[href='/app']").first
                if await new_chat.count() > 0 and await new_chat.is_visible():
                    await new_chat.click()
                    await asyncio.sleep(2)

                # 2. Rellenar prompt
                textbox = page.locator("div[role='textbox'], rich-textarea div[contenteditable='true']").first
                await textbox.wait_for(state="visible", timeout=15000)
                await textbox.click()
                await textbox.fill(prompt)
                await asyncio.sleep(1)

                send_btn = page.locator("button[aria-label*='Enviar'], button[aria-label*='Send']").first
                if await send_btn.count() > 0 and await send_btn.is_visible():
                    await send_btn.click()
                else:
                    await textbox.press("Enter")

                print("  ⏳ Esperando render de Imagen 3 (hasta 60s)...")
                img_sel = "img[src*='googleusercontent.com/gg/'], single-image img, generated-image img, img[alt*='imagen']"
                img_locator = page.locator(img_sel).first
                await img_locator.wait_for(state="visible", timeout=65000)

                img_src = await img_locator.get_attribute("src")

                raw_data = None
                if img_src and img_src.startswith("http"):
                    resp = await page.request.get(img_src, timeout=30000)
                    if resp.status == 200:
                        raw_data = await resp.body()

                if not raw_data:
                    raw_data = await img_locator.screenshot()

                # Ruta de destino del pixel art oficial
                specs = {}
                try:
                    specs = json.loads(v.get("especificaciones_json") or "{}")
                except Exception:
                    pass
                target_rel = specs.get("pixel_art_url")
                if not target_rel:
                    # Buscar archivo existente en directorio
                    v_dir = IMG_DIR / vid
                    px_files = list(v_dir.glob("pixel-art-16bit-*.webp"))
                    if px_files:
                        target_path = px_files[0]
                        target_rel = str(target_path.relative_to(BASE_DIR)).replace("\\", "/")
                    else:
                        target_rel = f"assets/img/{vid}/pixel-art-16bit-{vid}-auto-electrico-ev-servicioti-uruguay.webp"
                        target_path = BASE_DIR / target_rel.replace("/", os.sep)
                else:
                    target_path = BASE_DIR / target_rel.replace("/", os.sep)

                target_path.parent.mkdir(parents=True, exist_ok=True)

                with Image.open(io.BytesIO(raw_data)) as im:
                    # Redimensionar a sprite cuadrado de 128x128 píxeles nítidos
                    sprite = im.resize((128, 128), Image.Resampling.LANCZOS)
                    temp_p = target_path.parent / f"temp_{vid}.png"
                    sprite.save(temp_p, format="PNG")

                    MetadataImageService.inyectar_y_optimizar(
                        temp_p,
                        titulo=f"Sprite Pixel Art 16-Bit - {name}",
                        descripcion=f"Icono retro estilo arcade de 16-Bit de {name} generado con Google Gemini.",
                        calidad=90,
                        destino=target_path,
                        formato="WEBP"
                    )

                    if temp_p.exists():
                        try:
                            temp_p.unlink()
                        except Exception:
                            pass

                print(f"  ✅ Sprite guardado exitosamente en: {target_rel}")
                progress[vid] = {
                    "status": "success",
                    "file": target_rel,
                    "model": name,
                    "timestamp": asyncio.get_event_loop().time()
                }
                save_progress(progress)
                success_count += 1

                # Pausa amigable entre generaciones
                await asyncio.sleep(6)

            except Exception as e:
                print(f"  ❌ Error generando para {vid}: {e}")
                progress[vid] = {"status": "error", "error": str(e)}
                save_progress(progress)
                await asyncio.sleep(4)

        await context.close()
        print(f"\n=== Lote completado: {success_count}/{len(to_process)} sprites generados con éxito ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador en lotes de Pixel Art con Google Gemini Web")
    parser.add_argument("--limit", type=int, default=5, help="Cantidad de vehículos a procesar en esta tanda")
    parser.add_argument("--force", action="store_true", help="Re-generar incluso los ya completados")
    parser.add_argument("--ids", nargs="*", help="Lista opcional de IDs específicos a generar")

    args = parser.parse_args()
    asyncio.run(generate_batch(limit=args.limit, force=args.force, filter_ids=args.ids))
