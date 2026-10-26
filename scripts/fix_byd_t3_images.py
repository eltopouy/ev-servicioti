# -*- coding: utf-8 -*-
"""
Reemplazo estricto de imágenes de BYD T3 (furgón utilitario eléctrico)
Elimina cualquier foto de ómnibus y coloca fotos oficiales del furgón real.
"""
import sqlite3
import urllib.request
import urllib.parse
import json
import sys
import os
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from metadata_image_service import MetadataImageService

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img" / "byd-t3"
RAW_DIR = BASE_DIR / "assets" / "raw" / "byd-t3"
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"

IMG_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

WIKI_AGENT = 'EVUruguay/1.0 (contacto@servicioti.com.uy; https://ev.servicioti.com.uy)'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Títulos exactos del furgón utilitario BYD T3 / ETP3
T3_WIKI_FILES = [
    ("01-vista-isometrica-frontal-3-4", "File:BYD T3 001.jpg", "Vista Isométrica Frontal 3/4 Furgón"),
    ("02-vista-trasera-opticas-porton", "File:BYD T3 002.jpg", "Vista Trasera y Portón de Carga"),
    ("03-interior-tablero-consola-cockpit", "File:BYD ETP 3 152919.jpg", "Puesto de Conducción y Cockpit"),
    ("04-perfil-lateral-carroceria", "File:BYD T3 003.jpg", "Perfil Lateral Furgón Utilitario"),
    ("05-detalle-bateria-conector-carga", "File:BYD ETP 3 153037.jpg", "Área de Carga Útil y Capacidad"),
    ("06-detalle-frontal-firma-luminica", "File:2023 BYD ETP3.jpg", "Detalle Frontal y Conexión de Recarga")
]

def obtener_url_wikimedia(file_title: str) -> str:
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json"
    req = urllib.request.Request(api_url, headers={'User-Agent': WIKI_AGENT})
    data = json.loads(urllib.request.urlopen(req, timeout=12).read().decode('utf-8'))
    pages = data.get('query', {}).get('pages', {})
    for pid, pdata in pages.items():
        imginfo = pdata.get('imageinfo', [])
        if imginfo:
            return imginfo[0].get('thumburl') or imginfo[0].get('url')
    return None

def componer_estudio_4_3(img_src: Image.Image) -> Image.Image:
    ancho_target, alto_target = 1200, 900
    canvas = Image.new("RGB", (ancho_target, alto_target), (250, 251, 252))
    draw = ImageDraw.Draw(canvas)
    for y in range(600, alto_target):
        factor = (y - 600) / float(alto_target - 600)
        val = int(250 - factor * 14)
        draw.line([(0, y), (ancho_target, y)], fill=(val, val, val + 1))

    shadow = Image.new("RGBA", (ancho_target, alto_target), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(160, 715), (1040, 785)], fill=(0, 0, 0, 48))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))
    canvas.paste(shadow, (0, 0), shadow)

    src_rgb = img_src.convert("RGB")
    ancho_max = int(ancho_target * 0.88)
    alto_max = int(alto_target * 0.72)
    ratio = min(ancho_max / float(src_rgb.width), alto_max / float(src_rgb.height))
    nuevo_ancho = max(10, int(src_rgb.width * ratio))
    nuevo_alto = max(10, int(src_rgb.height * ratio))
    img_scaled = src_rgb.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    pos_x = (ancho_target - nuevo_ancho) // 2
    pos_y = 750 - nuevo_alto
    canvas.paste(img_scaled, (pos_x, pos_y))
    return canvas

def main():
    print("=================================================================")
    print("REEMPLAZANDO FOTOS DE BYD T3 CON EL FURGÓN UTILITARIO GENUINO")
    print("=================================================================")

    # 1. Limpiar fotos anteriores
    for f in IMG_DIR.glob("*.*"):
        try: f.unlink()
        except Exception: pass
    for f in RAW_DIR.glob("*.*"):
        try: f.unlink()
        except Exception: pass

    downloaded = []
    galeria_paths = []

    for idx, (slug, wiki_file, desc) in enumerate(T3_WIKI_FILES):
        print(f"Descargando {wiki_file} ({desc})...")
        img_url = obtener_url_wikimedia(wiki_file)
        if not img_url:
            print(f"  [ERROR] No se pudo obtener URL para {wiki_file}")
            continue

        req = urllib.request.Request(img_url, headers={'User-Agent': WIKI_AGENT})
        data = urllib.request.urlopen(req, timeout=15).read()
        raw_path = RAW_DIR / f"raw_t3_{idx+1}.jpg"
        with open(raw_path, "wb") as f_out:
            f_out.write(data)

        src_im = Image.open(io.BytesIO(data))
        downloaded.append(src_im)

        # Componer estudio 4:3
        canvas = componer_estudio_4_3(src_im)
        filename = f"{slug}-byd-t3-furgon-utilitario-el-auto-electrico-ev-servicioti-uruguay.webp"
        out_file = IMG_DIR / filename
        temp_file = IMG_DIR / f"temp_{slug}.png"
        canvas.save(temp_file, format="PNG")

        MetadataImageService.inyectar_y_optimizar(
            temp_file,
            titulo=f"BYD T3 Furgón Eléctrico - {desc}",
            descripcion=f"{desc} oficial de BYD T3 furgón comercial 100% eléctrico en Uruguay. ServicioTI.",
            calidad=85,
            destino=out_file,
            formato="WEBP"
        )
        if temp_file.exists():
            temp_file.unlink()

        galeria_paths.append(f"assets/img/byd-t3/{filename}")
        print(f"  ✔ Guardado: {filename}")

    if not downloaded:
        print("[CRITICO] No se pudo descargar ninguna foto oficial de BYD T3")
        return

    hero = downloaded[0]

    # Crear alias 01-vista-frontal-3-4...
    iso_name = f"01-vista-isometrica-frontal-3-4-byd-t3-furgon-utilitario-el-auto-electrico-ev-servicioti-uruguay.webp"
    alias_name = f"01-vista-frontal-3-4-byd-t3-furgon-utilitario-el-auto-electrico-ev-servicioti-uruguay.webp"
    import shutil
    shutil.copyfile(IMG_DIR / iso_name, IMG_DIR / alias_name)

    # Badge circular
    badge_path = IMG_DIR / f"badge-circular-byd-t3-furgon-utilitario-el-auto-electrico-ev-servicioti-uruguay.webp"
    thumb = hero.resize((128, 128), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (128, 128), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((2, 2, 126, 126), fill=255)
    badge = Image.new("RGBA", (128, 128), (255, 255, 255, 0))
    badge.paste(thumb, (0, 0), mask=mask)
    bdraw = ImageDraw.Draw(badge)
    bdraw.ellipse((2, 2, 126, 126), outline=(17, 24, 39, 210), width=2)
    final_rgb = Image.new("RGB", (128, 128), (255, 255, 255))
    final_rgb.paste(badge, (0, 0), badge)
    temp_badge = IMG_DIR / "temp_badge.png"
    final_rgb.save(temp_badge, format="PNG")
    MetadataImageService.inyectar_y_optimizar(
        temp_badge,
        titulo="Badge Circular - BYD T3 Furgón",
        descripcion="Badge circular BYD T3 furgón eléctrico ServicioTI Uruguay",
        calidad=85,
        destino=badge_path,
        formato="WEBP"
    )
    if temp_badge.exists(): temp_badge.unlink()

    # Pixel Art 16-bit
    pixel_path = IMG_DIR / f"pixel-art-16bit-byd-t3-furgon-utilitario-el-auto-electrico-ev-servicioti-uruguay.webp"
    small = hero.resize((64, 64), Image.Resampling.BILINEAR)
    pixelated = small.quantize(colors=16, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    retro_sprite = pixelated.resize((128, 128), Image.Resampling.NEAREST)
    temp_pixel = IMG_DIR / "temp_pixel.png"
    retro_sprite.save(temp_pixel, format="PNG")
    MetadataImageService.inyectar_y_optimizar(
        temp_pixel,
        titulo="Pixel Art 16-Bit - BYD T3",
        descripcion="Icono pixel art 16-bit BYD T3 furgón ServicioTI",
        calidad=88,
        destino=pixel_path,
        formato="WEBP"
    )
    if temp_pixel.exists(): temp_pixel.unlink()

    # Actualizar base de datos SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hero_rel_url = f"assets/img/byd-t3/{iso_name}"
    galeria_json = json.dumps(galeria_paths, ensure_ascii=False)
    cursor.execute("""
        UPDATE vehicles
        SET imagen_oficial_url = ?, galeria_json = ?
        WHERE id = 'byd-t3'
    """, (hero_rel_url, galeria_json))
    conn.commit()
    conn.close()

    print("\n[OK] BYD T3 actualizado exitosamente con fotos del furgón real.")

if __name__ == "__main__":
    main()
