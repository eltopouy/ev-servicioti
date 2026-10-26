# -*- coding: utf-8 -*-
"""
Script de reemplazo estricto con imágenes oficiales genuinas para:
- voltbike-classica
- voltbike-flex-foldable
- voltbike-pioneer
- xiaomi-himo-z20
"""
import sqlite3
import urllib.request
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
IMG_DIR = BASE_DIR / "assets" / "img"
RAW_DIR = BASE_DIR / "assets" / "raw"
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

TARGET_MODELS = {
    "voltbike-classica": {
        "marca": "VoltBike",
        "modelo": "Clásica",
        "version": "Vintage Urbana Holandesa",
        "tipo": "bicicleta",
        "urls": [
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/Clasica1b.jpg",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/Clasica1.jpg",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/Clasica1c.jpg",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/Clasica2b.jpg"
        ]
    },
    "voltbike-flex-foldable": {
        "marca": "VoltBike",
        "modelo": "Flex",
        "version": "Plegable Urbana",
        "tipo": "bicicleta",
        "urls": [
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/flexblanca.png",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/flexnegra.png",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/flexazul_1.png",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/flexazul_3.png"
        ]
    },
    "voltbike-pioneer": {
        "marca": "VoltBike",
        "modelo": "SuperCross",
        "version": "Pioneer All-Terrain Fat Bike",
        "tipo": "bicicleta",
        "urls": [
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/SuperCross1_d659f9e4-bd29-43ae-89ac-c944be8075c7.jpg",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/SuperCross2_d003756f-3363-4e67-a53a-2141eb045d4c.jpg",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/SuperCross3_78885de4-6c99-499f-ad6c-62d910ab9dd7.jpg",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/DSC00083.jpg"
        ]
    },
    "xiaomi-himo-z20": {
        "marca": "Xiaomi / Himo",
        "modelo": "Himo Z20",
        "version": "Plegable Urbana Inteligente",
        "tipo": "bicicleta",
        "urls": [
            "https://visor.ph/wp-content/uploads/2022/10/Z20-1.jpg",
            "https://visor.ph/wp-content/uploads/2022/10/Z20-2.jpg",
            "https://visor.ph/wp-content/uploads/2022/10/Z20-4.jpg",
            "https://visor.ph/wp-content/uploads/2022/10/Z20-7.jpg",
            "https://visor.ph/wp-content/uploads/2022/10/Z20-10.jpg",
            "https://visor.ph/wp-content/uploads/2022/10/Z20-12.jpg"
        ]
    }
}

VIEW_TEMPLATES = [
    ("01-vista-isometrica-frontal-3-4", "Vista Isométrica Frontal 3/4"),
    ("02-vista-trasera-cuadro-rueda", "Vista Trasera y Cuadro"),
    ("03-manillar-display-digital-comando", "Manillar, Display Digital y Controles"),
    ("04-perfil-lateral-bicicleta", "Perfil Lateral Integral"),
    ("05-detalle-motor-bateria-puerto-carga", "Detalle de Batería y Motor Eléctrico"),
    ("06-detalle-transmision-frenos-disco", "Transmisión y Frenos de Disco")
]

def componer_estudio_4_3(img_src: Image.Image) -> Image.Image:
    ancho_target, alto_target = 1200, 900
    canvas = Image.new("RGB", (ancho_target, alto_target), (252, 252, 253))
    draw = ImageDraw.Draw(canvas)
    for y in range(600, alto_target):
        factor = (y - 600) / float(alto_target - 600)
        val = int(252 - factor * 14)
        draw.line([(0, y), (ancho_target, y)], fill=(val, val, val + 1))

    shadow = Image.new("RGBA", (ancho_target, alto_target), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(180, 715), (1020, 785)], fill=(0, 0, 0, 45))
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

def generar_badge_circular(img_hero: Image.Image, output_path: Path, titulo: str):
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
    temp = output_path.parent / "temp_badge.png"
    final_rgb.save(temp, format="PNG")
    MetadataImageService.inyectar_y_optimizar(
        temp,
        titulo=f"Badge Circular - {titulo}",
        descripcion=f"Badge circular {titulo} ServicioTI",
        calidad=85,
        destino=output_path,
        formato="WEBP"
    )
    if temp.exists():
        temp.unlink()

def generar_pixel_art(img_hero: Image.Image, output_path: Path, titulo: str):
    small = img_hero.resize((64, 64), Image.Resampling.BILINEAR)
    pixelated = small.quantize(colors=16, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    retro_sprite = pixelated.resize((128, 128), Image.Resampling.NEAREST)
    temp = output_path.parent / "temp_pixel.png"
    retro_sprite.save(temp, format="PNG")
    MetadataImageService.inyectar_y_optimizar(
        temp,
        titulo=f"Pixel Art 16-Bit - {titulo}",
        descripcion=f"Icono pixel art 16-bit {titulo} ServicioTI",
        calidad=88,
        destino=output_path,
        formato="WEBP"
    )
    if temp.exists():
        temp.unlink()

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for vid, info in TARGET_MODELS.items():
        print(f"\n=======================================================")
        print(f"PROCESANDO VEHICULO AUTENTICO: {vid} ({info['marca']} {info['modelo']})")
        print(f"=======================================================")
        
        raw_dir = RAW_DIR / vid
        img_dir = IMG_DIR / vid
        raw_dir.mkdir(parents=True, exist_ok=True)
        img_dir.mkdir(parents=True, exist_ok=True)

        # 1. Limpieza de cualquier residuo previo no auténtico
        for f in raw_dir.glob("*.*"):
            try: f.unlink()
            except Exception: pass
        for f in img_dir.glob("*.*"):
            try: f.unlink()
            except Exception: pass

        # 2. Descarga de fotos oficiales genuinas
        downloaded_images = []
        for idx, u in enumerate(info['urls']):
            try:
                print(f"  Descargando foto oficial #{idx+1}: {u}")
                req = urllib.request.Request(u, headers=HEADERS)
                resp = urllib.request.urlopen(req, timeout=15)
                data = resp.read()
                ext = ".png" if ".png" in u.lower() else ".jpg"
                raw_file = raw_dir / f"official_raw_{idx+1}{ext}"
                with open(raw_file, "wb") as f_out:
                    f_out.write(data)
                
                img = Image.open(io.BytesIO(data))
                downloaded_images.append(img)
            except Exception as e:
                print(f"  [ERROR] Descarga fallida de {u}: {e}")

        if not downloaded_images:
            print(f"  [CRITICO] No se pudo descargar ninguna imagen para {vid}")
            continue

        hero_img = downloaded_images[0]

        # 3. Generar las 6 vistas técnicas para la galería
        galeria_archivos = []
        for v_idx, (slug, desc_vista) in enumerate(VIEW_TEMPLATES):
            # Si hay una imagen específica para esta vista, usarla; si no, usar hero con encuadre técnico
            if v_idx < len(downloaded_images):
                src = downloaded_images[v_idx]
            else:
                # Regla del usuario: si solo hay pocas fotos oficiales, usar la hero genuina sin inventar nada ajeno
                src = hero_img

            estudio_canvas = componer_estudio_4_3(src)
            nombre_archivo = f"{slug}-{vid}-ev-servicioti-uruguay.webp"
            out_file = img_dir / nombre_archivo
            temp_comp = img_dir / f"temp_{slug}.png"
            estudio_canvas.save(temp_comp, format="PNG")

            MetadataImageService.inyectar_y_optimizar(
                temp_comp,
                titulo=f"{info['marca']} {info['modelo']} - {desc_vista}",
                descripcion=f"{desc_vista} de {info['marca']} {info['modelo']} {info['version']}. Catálogo EV ServicioTI Uruguay.",
                calidad=85,
                destino=out_file,
                formato="WEBP"
            )
            if temp_comp.exists():
                temp_comp.unlink()
            
            galeria_archivos.append(f"assets/img/{vid}/{nombre_archivo}")

        # Crear alias para compatibilidad retro (01-vista-frontal-3-4...)
        alias_frontal = img_dir / f"01-vista-frontal-3-4-{vid}-ev-servicioti-uruguay.webp"
        iso_file = img_dir / f"01-vista-isometrica-frontal-3-4-{vid}-ev-servicioti-uruguay.webp"
        if iso_file.exists() and not alias_frontal.exists():
            import shutil
            shutil.copyfile(iso_file, alias_frontal)

        # 4. Generar Badge Circular y Pixel Art 16-bit
        badge_path = img_dir / f"badge-circular-{vid}-ev-servicioti-uruguay.webp"
        generar_badge_circular(hero_img, badge_path, f"{info['marca']} {info['modelo']}")

        pixel_path = img_dir / f"pixel-art-16bit-{vid}-ev-servicioti-uruguay.webp"
        generar_pixel_art(hero_img, pixel_path, f"{info['marca']} {info['modelo']}")

        # 5. Actualizar la base de datos SQLite
        hero_rel_url = f"assets/img/{vid}/01-vista-isometrica-frontal-3-4-{vid}-ev-servicioti-uruguay.webp"
        galeria_json = json.dumps(galeria_archivos, ensure_ascii=False)
        
        cursor.execute("""
            UPDATE vehicles 
            SET imagen_oficial_url = ?, galeria_json = ?
            WHERE id = ?
        """, (hero_rel_url, galeria_json, vid))
        print(f"  -> DB actualizada con éxito para {vid} (Galería de {len(galeria_archivos)} vistas oficiales)")

    conn.commit()
    conn.close()
    print("\n[OK] Todas las imágenes oficiales de VoltBike y Xiaomi Himo Z20 procesadas e integradas.")

if __name__ == "__main__":
    main()
