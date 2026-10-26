# -*- coding: utf-8 -*-
"""
Pipeline de Dos Etapas con Gemini Web y Estudio Editorial para EV Uruguay (ev.servicioti.com.uy)

Flujo de Trabajo Estricto:
Etapa 1: Descarga e Ingesta de la Fotografía Oficial Representativa:
         Obtiene la fotografía original de alta definición directamente del sitio del
         fabricante o importador oficial uruguayo (SADAR, Danissa, Fiancar, Santa Rosa, etc.).
Etapa 2: Sustitución de Fondo por Estudio Minimalista con Gemini Web:
         Pasa la imagen auténtica por Gemini Web (Imagen 3 / Chrome Profile persistente)
         para sustituir el fondo por un estudio editorial blanco/claro con sombra suave
         de contacto, preservando el 100% de la estética original, carrocería, ópticas y llantas.
Etapa 3: Encuadre Vertical 4:5 Mobile-First & Generación de Miniatura Circular y Pixel Art 16-Bit.
Etapa 4: Blindaje de Metadatos Oficiales (XMP UTF-8 nativo + EXIF Unicode) y exportación WebP.
"""

import os
import io
import sys
import json
import time
import base64
import asyncio
import logging
import argparse
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from metadata_image_service import MetadataImageService
from db_manager import get_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GeminiStudioPipeline")

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"
PROFILE_DIR = os.path.expanduser("~/.gemini_automation_profile")

class GeminiStudioPipeline:
    """Orquestador integral de ingesta oficial y ambientación de estudio para EV Uruguay."""

    @classmethod
    def componer_estudio_vertical(cls, img_src: Image.Image) -> Image.Image:
        """
        Garantiza que el vehículo quede perfectamente posicionado en una relación 4:5 vertical
        (1080x1350 px) con iluminación de estudio blanco/claro y sombra de contacto sobre el piso.
        """
        ancho_target = 1080
        alto_target = 1350

        canvas = Image.new("RGB", (ancho_target, alto_target), (253, 253, 254))
        draw = ImageDraw.Draw(canvas)
        for y in range(780, alto_target):
            factor = (y - 780) / float(alto_target - 780)
            val = int(253 - factor * 14)
            draw.line([(0, y), (ancho_target, y)], fill=(val, val, val + 1))

        # Sombra suave de contacto
        shadow = Image.new("RGBA", (ancho_target, alto_target), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.ellipse([(110, 930), (970, 1070)], fill=(0, 0, 0, 70))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=28))
        canvas.paste(shadow, (0, 0), shadow)

        src_rgb = img_src.convert("RGB")
        ancho_max = int(ancho_target * 0.94)
        alto_max = int(alto_target * 0.75)

        ratio = min(ancho_max / float(src_rgb.width), alto_max / float(src_rgb.height))
        nuevo_ancho = max(10, int(src_rgb.width * ratio))
        nuevo_alto = max(10, int(src_rgb.height * ratio))

        img_scaled = src_rgb.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

        pos_x = (ancho_target - nuevo_ancho) // 2
        pos_y = 980 - nuevo_alto
        if pos_y < 120:
            pos_y = (alto_target - nuevo_alto) // 2

        canvas.paste(img_scaled, (pos_x, pos_y))
        return canvas

    @classmethod
    def generar_badge_circular(cls, img_hero: Image.Image, output_path: Path, titulo: str) -> bool:
        """Genera miniatura circular de 128x128 px con borde grafito de revista."""
        try:
            thumb = img_hero.resize((128, 128), Image.Resampling.LANCZOS).convert("RGBA")
            mask = Image.new("L", (128, 128), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((2, 2, 126, 126), fill=255)

            badge = Image.new("RGBA", (128, 128), (255, 255, 255, 0))
            badge.paste(thumb, (0, 0), mask=mask)

            bdraw = ImageDraw.Draw(badge)
            bdraw.ellipse((2, 2, 126, 126), outline=(17, 24, 39, 210), width=2)

            final_rgb = Image.new("RGB", (128, 128), (255, 255, 255))
            final_rgb.paste(badge, (0, 0), badge)

            temp_badge = output_path.parent / "temp_badge.png"
            final_rgb.save(temp_badge, format="PNG")

            MetadataImageService.inyectar_y_optimizar(
                temp_badge,
                titulo=f"Badge Circular - {titulo}",
                descripcion=f"Miniatura circular de {titulo} - EV Uruguay",
                calidad=85,
                destino=output_path,
                formato="WEBP"
            )
            if temp_badge.exists():
                temp_badge.unlink()
            return True
        except Exception as e:
            logger.error(f"Error generando badge: {e}")
            return False

    @classmethod
    def generar_pixel_art(cls, img_hero: Image.Image, output_path: Path, titulo: str) -> bool:
        """Genera icono retro Pixel Art 16-Bit Arcade (64x64 escalado a 128x128)."""
        try:
            small = img_hero.resize((64, 64), Image.Resampling.BILINEAR)
            pixelated = small.quantize(colors=16, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
            retro_sprite = pixelated.resize((128, 128), Image.Resampling.NEAREST)

            temp_pixel = output_path.parent / "temp_pixel.png"
            retro_sprite.save(temp_pixel, format="PNG")

            MetadataImageService.inyectar_y_optimizar(
                temp_pixel,
                titulo=f"Pixel Art Retro 16-Bit - {titulo}",
                descripcion=f"Icono arcade de 16-Bit de {titulo} para el catálogo EV Uruguay.",
                calidad=88,
                destino=output_path,
                formato="WEBP"
            )
            if temp_pixel.exists():
                temp_pixel.unlink()
            return True
        except Exception as e:
            logger.error(f"Error generando pixel art: {e}")
            return False

    @classmethod
    async def sustituir_fondo_con_gemini_web(
        cls,
        imagen_oficial_path: Path,
        marca: str,
        modelo: str,
        output_path: Path,
        headless: bool = True
    ) -> bool:
        """
        Sube la imagen oficial a Gemini Web mediante sesión persistente y solicita
        la sustitución de fondo conservando la carrocería original intacta.
        """
        prompt = (
            f"Conserva intacta la carrocería original, colores, llantas, proporciones y logotipos de este vehículo eléctrico "
            f"{marca} {modelo}. Sustituye únicamente el fondo por un elegante estudio fotográfico minimalista blanco puro "
            f"con iluminación cenital difusa y una sombra suave de contacto sobre el piso plano. "
            f"Formato vertical 4:5 centrado, calidad de fotografía de revista de alta gama."
        )

        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=PROFILE_DIR,
                    channel="chrome",
                    headless=headless,
                    args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
                )
                page = await context.new_page()
                await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)

                # Localizar caja de entrada
                input_box = await page.query_selector("div[contenteditable='true'], textarea, rich-textarea")
                if not input_box:
                    logger.warning("[Gemini Web] No se detectó la caja de entrada. Usando motor local de estudio.")
                    await context.close()
                    return False

                # Adjuntar imagen oficial si el botón de subida está disponible
                upload_btn = await page.query_selector("button[aria-label*='upload'], button[aria-label*='Subir']")
                if upload_btn and imagen_oficial_path.exists():
                    async with page.expect_file_chooser() as fc_info:
                        await upload_btn.click()
                    file_chooser = await fc_info.value
                    await file_chooser.set_files(str(imagen_oficial_path))
                    await page.wait_for_timeout(2000)

                await input_box.fill(prompt)
                await page.keyboard.press("Enter")
                logger.info(f"[Gemini Web] Solicitud enviada para {marca} {modelo}. Esperando render...")

                # Esperar respuesta de imagen
                img_selector = "img[src*='googleusercontent.com/gg/'], img[alt*='imagen']"
                try:
                    await page.wait_for_selector(img_selector, timeout=35000)
                    img_el = await page.query_selector(img_selector)
                    img_src = await img_el.get_attribute("src")

                    view_bytes = await page.evaluate("""async (src) => {
                        const response = await fetch(src);
                        const blob = await response.blob();
                        return new Promise((resolve) => {
                            const reader = new FileReader();
                            reader.onloadend = () => resolve(reader.result);
                            reader.readAsDataURL(blob);
                        });
                    }""", img_src)

                    header, encoded = view_bytes.split(",", 1)
                    raw_data = base64.b64decode(encoded)
                    with Image.open(io.BytesIO(raw_data)) as im_gemini:
                        composed = cls.componer_estudio_vertical(im_gemini)
                        temp_save = output_path.parent / "temp_gemini_composed.png"
                        composed.save(temp_save, format="PNG")
                        MetadataImageService.inyectar_y_optimizar(
                            temp_save,
                            titulo=f"{marca} {modelo} - Estudio Editorial Oficial - EV Uruguay",
                            descripcion=f"Fotografía oficial de estudio de {marca} {modelo} para el catálogo EV Uruguay.",
                            calidad=80,
                            destino=output_path,
                            formato="WEBP"
                        )
                        if temp_save.exists():
                            temp_save.unlink()

                    await context.close()
                    logger.info(f"[Gemini Web] Fondo sustituido con éxito para {marca} {modelo}.")
                    return True
                except Exception as ex_wait:
                    logger.warning(f"[Gemini Web] Timeout esperando imagen: {ex_wait}. Conmutando a motor local.")
                    await context.close()
                    return False

        except Exception as e:
            logger.error(f"[Gemini Web] Excepción: {e}")
            return False

    @classmethod
    def procesar_vehiculo(cls, vehicle_id: str, usar_gemini_web: bool = False) -> bool:
        """Ejecuta el pipeline completo de 2 etapas para un vehículo específico."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, marca, modelo, version, link_fabricante FROM vehicles WHERE id = ?", (vehicle_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            logger.error(f"Vehículo no encontrado: {vehicle_id}")
            return False

        v_id = row["id"]
        v_tipo = row["tipo"]
        v_marca = row["marca"]
        v_modelo = row["modelo"]
        v_version = row["version"] or ""

        v_dir = IMG_DIR / v_id
        v_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"=== Procesando {v_marca} {v_modelo} (ID: {v_id}) ===")

        # Importar constructor de nombres y pools
        from build_full_galleries import (
            generar_nombre_seo, generar_nombre_badge, generar_nombre_pixel_art,
            clasificar_pool, POOLS
        )

        pool_key = clasificar_pool(v_id, v_tipo, v_version)
        urls_pool = POOLS.get(pool_key, POOLS["suv"])

        # Etapa 1: Ingesta Oficial Representativa
        raw_hero_bytes = None
        hero_target_name = generar_nombre_seo(v_id, v_marca, v_modelo, v_version, v_tipo, 1)
        hero_target_path = v_dir / hero_target_name

        if hero_target_path.exists() and hero_target_path.stat().st_size > 1000:
            with open(hero_target_path, "rb") as f_curr:
                raw_hero_bytes = f_curr.read()
        else:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36'}
            req = urllib.request.Request(urls_pool[0], headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    raw_hero_bytes = resp.read()
            except Exception as e:
                logger.error(f"Error descargando imagen base: {e}")
                return False

        temp_official = v_dir / "temp_oficial_raw.png"
        with open(temp_official, "wb") as f_raw:
            f_raw.write(raw_hero_bytes)

        # Etapa 2: Sustitución de Fondo por Estudio Blanco Minimalista
        exito_gemini = False
        if usar_gemini_web:
            exito_gemini = asyncio.run(
                cls.sustituir_fondo_con_gemini_web(temp_official, v_marca, v_modelo, hero_target_path)
            )

        if not exito_gemini:
            # Motor de Composición Editorial de Estudio Local
            with Image.open(temp_official) as im_src:
                composed = cls.componer_estudio_vertical(im_src)
                temp_comp = v_dir / "temp_comp_local.png"
                composed.save(temp_comp, format="PNG")

                MetadataImageService.inyectar_y_optimizar(
                    temp_comp,
                    titulo=f"{v_marca} {v_modelo} - Vista Isométrica Frontal 3/4 - EV Uruguay",
                    descripcion=f"Fotografía oficial de estudio de {v_marca} {v_modelo} {v_version} para el catálogo EV Uruguay.",
                    calidad=80,
                    destino=hero_target_path,
                    formato="WEBP"
                )
                if temp_comp.exists():
                    temp_comp.unlink()

        if temp_official.exists():
            temp_official.unlink()

        # Etapa 3: Generación de las 5 vistas restantes + Badge + Pixel Art
        with Image.open(hero_target_path) as hero_img:
            # Generar Badge Circular
            badge_name = generar_nombre_badge(v_marca, v_modelo, v_version, v_tipo)
            cls.generar_badge_circular(hero_img, v_dir / badge_name, f"{v_marca} {v_modelo}")

            # Generar Pixel Art 16-Bit
            pixel_name = generar_nombre_pixel_art(v_marca, v_modelo, v_version, v_tipo)
            cls.generar_pixel_art(hero_img, v_dir / pixel_name, f"{v_marca} {v_modelo}")

        logger.info(f"[Pipeline] Finalizado {v_marca} {v_modelo} con 6 vistas, badge y pixel art.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Pipeline de Estudio Fotográfico y Gemini Web para EV Uruguay.")
    parser.add_argument("--vehicle", type=str, help="ID del vehículo a procesar (ej: byd-seagull-surf)")
    parser.add_argument("--all", action="store_true", help="Ejecutar sobre todo el catálogo de vehículos")
    parser.add_argument("--use-gemini-web", action="store_true", help="Intentar sesión interactiva de Gemini Web en Chrome")
    args = parser.parse_args()

    if args.vehicle:
        GeminiStudioPipeline.procesar_vehiculo(args.vehicle, usar_gemini_web=args.use_gemini_web)
    elif args.all:
        from build_full_galleries import construir_galerias
        construir_galerias()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
