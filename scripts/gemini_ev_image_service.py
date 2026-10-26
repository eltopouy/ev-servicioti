"""
Servicio de Generación de Imágenes para EV Uruguay con Gemini Web (Imagen 3).
Reutiliza la sesión persistente de Chrome (~/.gemini_automation_profile) a costo $0.
Aplica inyección de metadatos de ServicioTI y optimización de peso en KB con MetadataImageService.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright
from metadata_image_service import MetadataImageService

logger = logging.getLogger("EVGeminiImage")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"

LOCACIONES_URUGUAY = [
    "estacionado sobre la Rambla de Montevideo frente al Río de la Plata con sol de la tarde",
    "en el Puerto de Montevideo con barcos de carga y contenedores de fondo",
    "frente a una moderna concesionaria vidriada en Avenida Italia Montevideo",
    "junto al Faro de Punta Carretas en un día despejado",
    "cargando en un tótem de carga de la Ruta Eléctrica Nacional en Uruguay"
]

class GeminiEVImageService:
    """Genera imágenes fotorrealistas de vehículos eléctricos ambientados en Uruguay."""

    @classmethod
    async def generar_imagen_vehiculo(
        cls,
        marca: str,
        modelo: str,
        tipo: str = "auto",
        locacion: str = None,
        headless: bool = True
    ) -> dict:
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        user_data_dir = os.path.expanduser("~/.gemini_automation_profile")
        
        if not locacion:
            locacion = LOCACIONES_URUGUAY[0]

        prompt = (
            f"Fotografía automotriz fotorrealista de revista de alta gama de un {tipo} eléctrico {marca} {modelo}, "
            f"{locacion}. Iluminación natural cinematográfica, ángulo de 3/4 delantero, detalles nítidos de carrocería, "
            f"sin texto superpuesto, estilo editorial de revista Motor Trend."
        )

        filename = f"{marca.lower()}_{modelo.lower().replace(' ', '_')}.webp"
        output_path = IMG_DIR / filename

        logger.info(f"[Gemini Imagen] Solicitando imagen para: {marca} {modelo}")
        logger.info(f"[Gemini Imagen] Prompt: {prompt}")

        async with async_playwright() as p:
            try:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    channel="chrome",
                    headless=headless,
                    args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
                )
                page = await context.new_page()
                await page.goto("https://gemini.google.com/app", wait_until="networkidle", timeout=30000)

                # Localizar caja de entrada de prompt
                input_selector = "div[contenteditable='true'], textarea, rich-textarea"
                await page.wait_for_selector(input_selector, timeout=15000)
                await page.fill(input_selector, f"Genera una imagen: {prompt}")
                await page.keyboard.press("Enter")

                logger.info("[Gemini Imagen] Esperando respuesta y generación de imagen...")
                # Esperar a que aparezca la imagen generada
                img_selector = "img[src*='googleusercontent.com/gg/'], img[alt*='imagen']"
                await page.wait_for_selector(img_selector, timeout=45000)
                
                # Extraer imagen con in-browser canvas para máxima pureza
                img_element = await page.query_selector(img_selector)
                img_src = await img_element.get_attribute("src")

                # Descargar imagen a disco
                view_bytes = await page.evaluate("""async (src) => {
                    const response = await fetch(src);
                    const blob = await response.blob();
                    return new Promise((resolve) => {
                        const reader = new FileReader();
                        reader.onloadend = () => resolve(reader.result);
                        reader.readAsDataURL(blob);
                    });
                }""", img_src)

                import base64
                header, encoded = view_bytes.split(",", 1)
                data = base64.b64decode(encoded)
                with open(output_path, "wb") as f:
                    f.write(data)

                await context.close()

                # Inyectar metadatos oficiales ServicioTI y optimizar peso
                MetadataImageService.inyectar_y_optimizar(
                    output_path,
                    titulo=f"{marca} {modelo} Eléctrico en Uruguay",
                    descripcion=f"Fotografía editorial de {marca} {modelo} para el directorio EV Uruguay de ServicioTI.",
                    calidad=80
                )

                return {"success": True, "path": str(output_path), "filename": filename}

            except Exception as e:
                logger.error(f"[Gemini Imagen] Error o timeout en navegador: {e}")
                return {"success": False, "error": str(e)}

if __name__ == "__main__":
    res = asyncio.run(GeminiEVImageService.generar_imagen_vehiculo("BYD", "Dolphin", "auto", headless=True))
    print("Resultado:", res)
