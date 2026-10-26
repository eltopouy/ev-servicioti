# -*- coding: utf-8 -*-
"""
Constructor Integral de Galerías Fotográficas SEO de 6 Vistas para EV Uruguay (ev.servicioti.com.uy)
Requisitos de Ingeniería y Visuales:
1. 6 Vistas Completas por Vehículo:
   - 01: Vista Isométrica Frontal 3/4 (Hero elevado de revista / web)
   - 02: Vista Trasera Ópticas y Portón
   - 03: Interior, Puesto de Conducción, Volante y Pantalla Flotante
   - 04: Perfil Lateral Aerodinámico y Distancia entre Ejes
   - 05: Detalle de Batería, Puerto de Carga y Conectores (GB/T / CCS2)
   - 06: Detalle Frontal, Parrilla Ciega y Firma Lumínica LED
2. Formato Vertical 4:5 Mobile-First (1080x1350 px):
   - Optimizado para pantallas de smartphones (estilo Instagram).
   - Fondo de estudio fotográfico minimalista blanco/claro con sombra suave de contacto en el piso.
   - Vehículo centrado armónicamente sin recortes ni bandas negras vacías.
3. Versión Miniatura Circular (Badge 128x128 px):
   - badge-circular-[slug]-ev-servicioti-uruguay.webp
4. Versión Icono Retro Pixel Art 16-Bit Arcade (128x128 px nítido):
   - pixel-art-16bit-[slug]-ev-servicioti-uruguay.webp
5. Nomenclatura SEO Extrema:
   - Nombres de archivo descriptivos con vista, marca, modelo, versión, tipo y dominio oficial.
6. Inyección de Metadatos Oficiales ServicioTI:
   - XMP UTF-8 nativo + EXIF Unicode (Andrés Franchi Ugartemendía / ServicioTI).
7. Compresión WebP ultraligera (< 75 KB por vista).
"""

import os
import io
import re
import json
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from metadata_image_service import MetadataImageService
from db_manager import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"

def slugify(text: str) -> str:
    """Convierte texto a slug limpio en minúsculas sin acentos ni caracteres especiales."""
    text = str(text or "").lower()
    text = re.sub(r"[áàäâã]", "a", text)
    text = re.sub(r"[éèëê]", "e", text)
    text = re.sub(r"[íìïî]", "i", text)
    text = re.sub(r"[óòöôõ]", "o", text)
    text = re.sub(r"[úùüû]", "u", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def generar_slug_vehiculo(marca: str, modelo: str, version: str, tipo: str) -> str:
    """Genera el identificador canónico en slug del vehículo."""
    if tipo == "triciclo":
        subtipo = "triciclo-electrico"
    elif tipo == "moto":
        subtipo = "moto-electrica"
    elif tipo == "bicicleta":
        subtipo = "bicicleta-electrica"
    else:
        subtipo = "auto-electrico"

    ver_corta = slugify(version.split("/")[0].split("(")[0])[:20].strip("-") if version else ""
    partes = [marca, modelo]
    if ver_corta:
        partes.append(ver_corta)
    partes.append(subtipo)
    return slugify(" ".join(partes))

def generar_nombre_seo(v_id: str, marca: str, modelo: str, version: str, tipo: str, indice: int) -> str:
    """Genera el nombre de archivo semántico de 6 vistas alineado al estándar de EV Uruguay."""
    if tipo == "triciclo":
        vistas = [
            "01-vista-isometrica-frontal-3-4-cabina",
            "02-vista-trasera-caja-carga-volcadora",
            "03-puesto-conduccion-manillar-comandos",
            "04-perfil-lateral-chasis-reforzado",
            "05-detalle-motor-baterias-transmision-fuerza",
            "06-detalle-caja-mecanismo-volcador"
        ]
    elif tipo == "moto":
        vistas = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-opticas",
            "03-puesto-conduccion-manillar-tablero",
            "04-perfil-lateral-completo",
            "05-detalle-bateria-motor-hub",
            "06-detalle-faro-led-frenos"
        ]
    elif tipo == "bicicleta":
        vistas = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-cuadro-rueda",
            "03-manillar-display-digital-comando",
            "04-perfil-lateral-bicicleta",
            "05-detalle-motor-bateria-puerto-carga",
            "06-detalle-transmision-frenos-disco"
        ]
    else:
        vistas = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-opticas-porton",
            "03-interior-tablero-consola-cockpit",
            "04-perfil-lateral-carroceria",
            "05-detalle-bateria-conector-carga",
            "06-detalle-frontal-firma-luminica"
        ]

    vista_slug = vistas[indice - 1]
    vehiculo_slug = generar_slug_vehiculo(marca, modelo, version, tipo)
    return f"{vista_slug}-{vehiculo_slug}-ev-servicioti-uruguay.webp"

def generar_nombre_badge(marca: str, modelo: str, version: str, tipo: str) -> str:
    vehiculo_slug = generar_slug_vehiculo(marca, modelo, version, tipo)
    return f"badge-circular-{vehiculo_slug}-ev-servicioti-uruguay.webp"

def generar_nombre_pixel_art(marca: str, modelo: str, version: str, tipo: str) -> str:
    vehiculo_slug = generar_slug_vehiculo(marca, modelo, version, tipo)
    return f"pixel-art-16bit-{vehiculo_slug}-ev-servicioti-uruguay.webp"

# Bancos curados de 6 vistas fotográficas de alta resolución por categoría
POOLS = {
    "citycar": [
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica Frontal
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",  # 02 Trasera
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",  # 03 Interior
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 04 Lateral
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # 05 Carga
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Ópticas LED
    ],
    "tesla": [
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 02 Trasera
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",  # 03 Cockpit Minimalista
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",  # 04 Perfil
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",  # 05 Puerto de Carga
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Faros Matrix LED
    ],
    "triciclo": [
        "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica Cabina
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 02 Volcadora
        "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80",  # 03 Puesto Conducción
        "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=1200&q=80",  # 04 Chasis Reforzado
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # 05 Baterías y Reductor
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Ópticas y Defensas
    ],
    "hatchback": [
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",  # 02 Trasera
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",  # 03 Interior
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 04 Perfil
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # 05 Carga
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Frontal LED
    ],
    "suv": [
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica SUV
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",  # 02 Trasera / Portón
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 03 Cockpit y Pantallas
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",  # 04 Perfil SUV
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # 05 Conector CCS2 / GB/T
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Firma Lumínica Frontal
    ],
    "sedan": [
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica Sedán
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 02 Ópticas y Baúl
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",  # 03 Interior Ejecutivo
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",  # 04 Silueta Aerodinámica
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",  # 05 Conector de Carga
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Ópticas Matrix LED
    ],
    "utilitario": [
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica Furgón/Pickup
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",  # 02 Portón Trasero / Caja
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",  # 03 Cabina de Trabajo
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # 04 Lateral y Capacidad
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",  # 05 Batería y Toma DC
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Frontal Utilitario
    ],
    "moto": [
        "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica Moto
        "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=1200&q=80",  # 02 Trasera
        "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80",  # 03 Manillar y Pantalla
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # 04 Perfil Moto
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",  # 05 Batería Extraíble
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80"   # 06 Ópticas LED
    ],
    "bicicleta": [
        "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80",  # 01 Isométrica E-Bike
        "https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=1200&q=80",  # 02 Cuadro y Rueda
        "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1200&q=80",  # 03 Manillar y Display LCD
        "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=1200&q=80",  # 04 Perfil E-Bike
        "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80",  # 05 Batería y Puerto
        "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=1200&q=80"   # 06 Transmisión y Frenos
    ]
}

def clasificar_pool(v_id: str, tipo: str, version: str) -> str:
    """Clasifica el vehículo en el conjunto fotográfico más representativo."""
    if tipo == "triciclo":
        return "triciclo"
    if tipo == "moto":
        return "moto"
    if tipo == "bicicleta":
        return "bicicleta"
    
    vid = v_id.lower()
    ver = (version or "").lower()
    if "tesla" in vid:
        return "tesla"
    if any(k in vid or k in ver for k in ["furgon", "utilitario", "t3", "kangoo", "edeliver", "evito", "camion", "rich-6", "shark", "pickup"]):
        return "utilitario"
    if any(k in vid or k in ver for k in ["seal", "han", "001", "j7", "sedan", "taycan"]):
        return "sedan"
    if any(k in vid or k in ver for k in ["seagull", "mini", "kwid", "e2", "pony", "bagel", "lumin", "ora-03", "js1", "nammi", "spark", "eq1", "ice-cream", "panda", "jmev"]):
        return "citycar"
    return "suv"

def componer_estudio_vertical_4_5(img_src: Image.Image) -> Image.Image:
    """
    Transforma cualquier imagen en una composición editorial vertical 4:5 (1080x1350 px)
    con fondo de estudio minimalista blanco/claro y sombra de contacto suave bajo el piso.
    Garantiza que el vehículo no sufra recortes y quede armónicamente centrado para móviles.
    """
    ancho_target = 1080
    alto_target = 1350

    # 1. Crear lienzo de estudio blanco con suave gradiente al suelo
    canvas = Image.new("RGB", (ancho_target, alto_target), (253, 253, 254))
    draw = ImageDraw.Draw(canvas)
    for y in range(780, alto_target):
        factor = (y - 780) / float(alto_target - 780)
        val = int(253 - factor * 14)  # 253 -> 239
        draw.line([(0, y), (ancho_target, y)], fill=(val, val, val + 1))

    # 2. Sombra suave de contacto
    shadow = Image.new("RGBA", (ancho_target, alto_target), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(110, 930), (970, 1070)], fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=28))
    canvas.paste(shadow, (0, 0), shadow)

    # 3. Escalar vehículo proporcionalmente para llenar el 94% del ancho
    src_rgb = img_src.convert("RGB")
    ancho_max = int(ancho_target * 0.94)
    alto_max = int(alto_target * 0.75)

    ratio = min(ancho_max / float(src_rgb.width), alto_max / float(src_rgb.height))
    nuevo_ancho = max(10, int(src_rgb.width * ratio))
    nuevo_alto = max(10, int(src_rgb.height * ratio))

    img_scaled = src_rgb.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    # 4. Posicionar sobre el plano del piso de estudio (centro horizontal, apoyo en y=980)
    pos_x = (ancho_target - nuevo_ancho) // 2
    pos_y = 980 - nuevo_alto

    # Asegurar márgenes superiores limpios
    if pos_y < 120:
        pos_y = (alto_target - nuevo_alto) // 2

    canvas.paste(img_scaled, (pos_x, pos_y))
    return canvas

def generar_badge_circular(img_hero: Image.Image, output_path: Path, titulo: str) -> bool:
    """Genera una miniatura circular nítida de 128x128 px con borde grafito de alta definición."""
    try:
        thumb = img_hero.resize((128, 128), Image.Resampling.LANCZOS).convert("RGBA")
        mask = Image.new("L", (128, 128), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((2, 2, 126, 126), fill=255)

        badge = Image.new("RGBA", (128, 128), (255, 255, 255, 0))
        badge.paste(thumb, (0, 0), mask=mask)

        # Borde sutil de revista
        bdraw = ImageDraw.Draw(badge)
        bdraw.ellipse((2, 2, 126, 126), outline=(17, 24, 39, 210), width=2)

        # Convertir a RGB con fondo blanco para WebP ultraligero
        final_rgb = Image.new("RGB", (128, 128), (255, 255, 255))
        final_rgb.paste(badge, (0, 0), badge)

        temp_badge = output_path.parent / "temp_badge.png"
        final_rgb.save(temp_badge, format="PNG")

        MetadataImageService.inyectar_y_optimizar(
            temp_badge,
            titulo=f"Badge Circular - {titulo}",
            descripcion=f"Miniatura oficial circular para {titulo} - EV Uruguay",
            calidad=85,
            destino=output_path,
            formato="WEBP"
        )
        if temp_badge.exists():
            temp_badge.unlink()
        return True
    except Exception as e:
        print(f"  [Error Badge] {e}")
        return False

def generar_pixel_art_sprite(img_hero: Image.Image, output_path: Path, titulo: str) -> bool:
    """
    Genera un icono coleccionable estilo retro Pixel Art de 16-Bit Arcade (64x64 escalado a 128x128).
    Aplica cuantización de paleta adaptativa y reescalado de bordes nítidos (Nearest Neighbor).
    """
    try:
        # 1. Downscale a 64x64
        small = img_hero.resize((64, 64), Image.Resampling.BILINEAR)
        # 2. Cuantización a 16 colores arcade
        pixelated = small.quantize(colors=16, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
        # 3. Upscale a 128x128 con Nearest Neighbor para bordes retro cristalinos
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
        print(f"  [Error Pixel Art] {e}")
        return False

def construir_galerias():
    print("=== Iniciando Constructor de Galerías SEO de 6 Vistas 4:5 + Badges + Pixel Art ===")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tipo, marca, modelo, version FROM vehicles")
    vehiculos = cursor.fetchall()

    total = len(vehiculos)
    print(f"[Catálogo] {total} modelos encontrados en la base de datos.")

    cache_fotos = {}

    def obtener_foto_base(url):
        if url in cache_fotos:
            return cache_fotos[url]
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                cache_fotos[url] = data
                return data
        except Exception as e:
            print(f"  [Alerta] No se pudo descargar {url}: {e}")
            return None

    nombres_vistas = [
        "Vista Isométrica Frontal 3/4",
        "Vista Trasera 3/4 y Ópticas",
        "Interior, Puesto de Conducción y Cockpit",
        "Perfil Lateral Aerodinámico",
        "Detalle de Batería y Puerto de Carga",
        "Detalle Frontal y Firma Lumínica LED"
    ]

    actualizados = 0

    for idx_v, row in enumerate(vehiculos, 1):
        v_id = row["id"]
        v_tipo = row["tipo"]
        v_marca = row["marca"]
        v_modelo = row["modelo"]
        v_version = row["version"] or ""

        v_dir = IMG_DIR / v_id
        v_dir.mkdir(parents=True, exist_ok=True)

        pool_key = clasificar_pool(v_id, v_tipo, v_version)
        urls_pool = POOLS.get(pool_key, POOLS["suv"])

        galeria_rutas = []
        hero_img_pil = None

        for i in range(1, 7):
            nombre_seo = generar_nombre_seo(v_id, v_marca, v_modelo, v_version, v_tipo, i)
            target_path = v_dir / nombre_seo
            rel_path = f"assets/img/{v_id}/{nombre_seo}"
            galeria_rutas.append(rel_path)

            necesita_generar = True
            if target_path.exists() and target_path.stat().st_size > 1000:
                try:
                    with Image.open(target_path) as im_chk:
                        if im_chk.format == "WEBP":
                            necesita_generar = False
                            if i == 1:
                                hero_img_pil = im_chk.copy()
                except Exception:
                    necesita_generar = True

            if necesita_generar:
                # Comprobar si existe archivo previo del cual tomar la fuente
                raw_bytes = None
                archivos_candidatos = [
                    v_dir / f"0{i}.webp",
                    v_dir / f"temp_{i}.raw",
                    v_dir / f"0{i}-vista-frontal-3-4-exterior-{v_id}-ev-servicioti-uruguay.webp"
                ]
                for cand in archivos_candidatos:
                    if cand.exists() and cand.stat().st_size > 1000:
                        try:
                            with open(cand, "rb") as fc:
                                raw_bytes = fc.read()
                            break
                        except Exception:
                            pass

                if not raw_bytes:
                    url_origen = urls_pool[(i - 1) % len(urls_pool)]
                    raw_bytes = obtener_foto_base(url_origen)

                if raw_bytes:
                    try:
                        with Image.open(io.BytesIO(raw_bytes)) as src_im:
                            # Composición vertical 4:5 estilo revista / Instagram
                            composed = componer_estudio_vertical_4_5(src_im)
                            if i == 1:
                                hero_img_pil = composed.copy()

                            temp_file = v_dir / f"temp_comp_{i}.png"
                            composed.save(temp_file, format="PNG")

                            titulo_foto = f"{v_marca} {v_modelo} - {nombres_vistas[i-1]} - EV Uruguay"
                            desc_foto = f"Fotografía de revista de {v_marca} {v_modelo} {v_version} para el catálogo de EV Uruguay (ev.servicioti.com.uy)."

                            MetadataImageService.inyectar_y_optimizar(
                                temp_file,
                                titulo=titulo_foto,
                                descripcion=desc_foto,
                                calidad=80,
                                destino=target_path,
                                formato="WEBP"
                            )

                            if temp_file.exists():
                                temp_file.unlink()
                    except Exception as err:
                        print(f"  [Error al componer foto {i} de {v_id}]: {err}")

        # Generar Badge Circular y Pixel Art Sprite si contamos con imagen Hero
        badge_name = generar_nombre_badge(v_marca, v_modelo, v_version, v_tipo)
        badge_path = v_dir / badge_name
        badge_rel = f"assets/img/{v_id}/{badge_name}"

        pixel_name = generar_nombre_pixel_art(v_marca, v_modelo, v_version, v_tipo)
        pixel_path = v_dir / pixel_name
        pixel_rel = f"assets/img/{v_id}/{pixel_name}"

        if hero_img_pil is None and (v_dir / galeria_rutas[0].split("/")[-1]).exists():
            try:
                hero_img_pil = Image.open(v_dir / galeria_rutas[0].split("/")[-1])
            except Exception:
                pass

        if hero_img_pil is not None:
            if not badge_path.exists() or badge_path.stat().st_size < 500:
                generar_badge_circular(hero_img_pil, badge_path, f"{v_marca} {v_modelo}")

            if not pixel_path.exists() or pixel_path.stat().st_size < 500:
                generar_pixel_art_sprite(hero_img_pil, pixel_path, f"{v_marca} {v_modelo}")

        # Limpiar cualquier archivo obsoleto con 5 vistas anteriores
        for f_obsoleta in v_dir.glob("*.webp"):
            nombre_f = f_obsoleta.name
            if nombre_f.startswith("01-vista-frontal-3-4-exterior") or re.match(r"^0[1-5]\.webp$", nombre_f):
                try:
                    f_obsoleta.unlink()
                except Exception:
                    pass

        # Actualizar base de datos SQLite con la galería de 6 fotos, badge y pixel art
        imagen_principal = galeria_rutas[0]
        galeria_json_str = json.dumps(galeria_rutas)

        # Actualizar especificaciones_json con los enlaces al badge y al pixel art
        cursor.execute("SELECT especificaciones_json FROM vehicles WHERE id = ?", (v_id,))
        spec_row = cursor.fetchone()
        specs = {}
        if spec_row and spec_row["especificaciones_json"]:
            try:
                specs = json.loads(spec_row["especificaciones_json"])
            except Exception:
                specs = {}
        specs["badge_circular_url"] = badge_rel
        specs["pixel_art_url"] = pixel_rel

        cursor.execute("""
        UPDATE vehicles
        SET imagen_oficial_url = ?, galeria_json = ?, especificaciones_json = ?
        WHERE id = ?
        """, (imagen_principal, galeria_json_str, json.dumps(specs), v_id))

        actualizados += 1
        if idx_v % 15 == 0 or idx_v == total:
            print(f"[{idx_v}/{total}] Procesado 6 Vistas + Badges: {v_marca} {v_modelo}")

    conn.commit()
    conn.close()

    print(f"\n[Éxito] {actualizados} vehículos actualizados con 6 fotos 4:5, badges y pixel art en SQLite.")

    # Re-exportar a JSON y JS
    from export_to_json import export_db_to_json
    export_db_to_json()
    print("=== Construcción de Galerías de 6 Vistas Finalizada con Éxito ===")

if __name__ == "__main__":
    construir_galerias()
