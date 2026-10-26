"""
Rotador de Perfiles de Google Chrome y Orquestador de Lotes para Gemini Web (Imagen 3).
Permite generar imágenes de vehículos ambientadas en Uruguay sin saturar las cuotas
rotando de forma transparente entre los perfiles configurados en el equipo de Andrés.
Aplica retardos inteligentes y optimización con MetadataImageService.
"""

import os
import sys
import time
import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright
from metadata_image_service import MetadataImageService
from db_manager import get_connection

logger = logging.getLogger("GeminiRotator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"

# Perfiles de Chrome identificados en el sistema de Andrés
CHROME_USER_DATA_DIR = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
AVAILABLE_PROFILES = [
    os.path.expanduser("~/.gemini_automation_profile"),  # Perfil dedicado de automatización
    "Default",
    "Profile 1",
    "Profile 2",
    "Profile 4",
    "Profile 5",
    "Profile 6",
    "Profile 7",
    "Profile 8",
    "Profile 9",
    "Profile 10"
]

LOCACIONES_URUGUAY = [
    "estacionado sobre la Rambla de Pocitos en Montevideo frente al Río de la Plata con atardecer dorado",
    "en el Puerto de Montevideo con grúas portuarias y contenedores marítimos de fondo",
    "junto al Faro de Punta Carretas en un día despejado con cielo azul límpido",
    "en una estación de carga de la Ruta Eléctrica Nacional de UTE con tótem verde iluminado",
    "frente a las fachadas patrimoniales de Carrasco en Montevideo"
]

class GeminiProfileRotator:
    """Gestiona la cola de generación con rotación de perfiles y rate-limiting."""

    def __init__(self, delay_between_generations: int = 20):
        self.delay = delay_between_generations
        self.current_profile_idx = 0

    def get_current_profile_target(self):
        target = AVAILABLE_PROFILES[self.current_profile_idx % len(AVAILABLE_PROFILES)]
        return target

    def rotate_profile(self):
        self.current_profile_idx = (self.current_profile_idx + 1) % len(AVAILABLE_PROFILES)
        next_target = self.get_current_profile_target()
        logger.info(f"[Rotador] Conmutando al siguiente perfil de Google: {next_target}")
        return next_target

    async def generate_localized_image(self, vehicle_id: str, marca: str, modelo: str, tipo: str = "auto") -> dict:
        v_dir = IMG_DIR / vehicle_id
        v_dir.mkdir(parents=True, exist_ok=True)
        output_webp = v_dir / "00_uruguay.webp"

        locacion = LOCACIONES_URUGUAY[hash(vehicle_id) % len(LOCACIONES_URUGUAY)]
        prompt = (
            f"Fotografía automotriz fotorrealista de revista de un {tipo} eléctrico {marca} {modelo}, "
            f"{locacion}. Iluminación natural nítida, carrocería impecable con reflejos limpios, "
            f"ángulo de 3/4 delantero a nivel de calle, estilo editorial Motor Trend, ultra alta definición."
        )

        logger.info(f"[Pipeline] Generando ambientación uruguaya para: {marca} {modelo}")
        logger.info(f"[Pipeline] Prompt: {prompt}")

        profile_target = self.get_current_profile_target()
        
        # Determinar si es ruta absoluta o nombre de subdirectorio de Chrome
        if os.path.isabs(profile_target):
            user_data_path = profile_target
            profile_dir = None
        else:
            user_data_path = CHROME_USER_DATA_DIR
            profile_dir = profile_target

        async with async_playwright() as p:
            try:
                launch_args = ["--disable-blink-features=AutomationControlled", "--no-sandbox"]
                if profile_dir:
                    launch_args.append(f"--profile-directory={profile_dir}")

                context = await p.chromium.launch_persistent_context(
                    user_data_dir=user_data_path,
                    channel="chrome",
                    headless=True,
                    args=launch_args
                )

                page = await context.new_page()
                await page.goto("https://gemini.google.com/app", wait_until="networkidle", timeout=30000)

                input_sel = "div[contenteditable='true'], textarea, rich-textarea"
                await page.wait_for_selector(input_sel, timeout=12000)
                await page.fill(input_sel, f"Genera una imagen: {prompt}")
                await page.keyboard.press("Enter")

                logger.info(f"[Gemini Web] Esperando generación con perfil '{profile_target}'...")
                img_sel = "img[src*='googleusercontent.com/gg/'], img[alt*='imagen']"
                await page.wait_for_selector(img_sel, timeout=40000)

                img_elem = await page.query_selector(img_sel)
                img_src = await img_elem.get_attribute("src")

                # Extracción limpia mediante canvas
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
                with open(output_webp, "wb") as f:
                    f.write(data)

                await context.close()

                # Inyectar metadatos oficiales de ServicioTI y comprimir WebP
                MetadataImageService.inyectar_y_optimizar(
                    output_webp,
                    titulo=f"{marca} {modelo} Eléctrico en Uruguay",
                    descripcion=f"Ambientación editorial de {marca} {modelo} en Montevideo - EV Uruguay (ev.servicioti.com.uy).",
                    calidad=80
                )

                logger.info(f"[Éxito] Imagen ambientada creada y optimizada: {output_webp.name}")
                return {"success": True, "path": str(output_webp)}

            except Exception as e:
                logger.warning(f"[Alerta] Perfil '{profile_target}' encontró limitación o timeout: {e}")
                self.rotate_profile()
                return {"success": False, "error": str(e)}

async def run_batch_generation(limit: int = 3):
    rotator = GeminiProfileRotator(delay_between_generations=20)
    print("=== Plan de Generación Gradual con Rotación de Perfiles ===")
    
    # Prioridad: los 3 modelos más vendidos
    top_models = [
        ("byd-seagull-ev", "BYD", "Seagull", "auto"),
        ("byd-dolphin-gs", "BYD", "Dolphin", "auto"),
        ("volvo-ex30", "Volvo", "EX30", "auto")
    ]

    for v_id, marca, modelo, tipo in top_models[:limit]:
        print(f"\n[Cola] Procesando vehículo: {marca} {modelo}...")
        res = await rotator.generate_localized_image(v_id, marca, modelo, tipo)
        if res.get("success"):
            print(f"  -> Generada exitosamente.")
        else:
            print(f"  -> Conmutado de perfil de respaldo.")
        
        print(f"[Pausa de cortesía] Esperando {rotator.delay}s para no saturar cuota...")
        await asyncio.sleep(rotator.delay)

if __name__ == "__main__":
    asyncio.run(run_batch_generation(limit=1))
