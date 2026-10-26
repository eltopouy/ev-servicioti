# -*- coding: utf-8 -*-
import urllib.request
import re
import sys
import os
import io
from pathlib import Path
from bs4 import BeautifulSoup
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

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

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
    sdraw.ellipse([(150, 710), (1050, 785)], fill=(0, 0, 0, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))
    canvas.paste(shadow, (0, 0), shadow)

    src_rgb = img_src.convert("RGB")
    ancho_max = int(ancho_target * 0.90)
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

# Mapeo a modelos del catálogo
PAGES = {
    "byd-seal-awd": "https://byd.com.uy/autos/byd-seal/",
    "byd-han-ev": "https://byd.com.uy/autos/byd-han/",
    "byd-tang-ev": "https://byd.com.uy/autos/byd-new-tang/",
    "byd-yuan-plus": "https://byd.com.uy/autos/byd-yuan-plus/",
    "byd-shark": "https://byd.com.uy/autos/byd-shark/",
    "byd-new-e2-x-gs": "https://byd.com.uy/autos/byd-new-e2-x/"
}

for vid, url in PAGES.items():
    print(f"\nRelevando {vid} desde {url}...")
    try:
        html = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=10).read().decode('utf-8', errors='ignore')
        all_imgs = set(re.findall(r'https://byd\.com\.uy/wp-content/uploads/[^"\'\)\s]+\.(?:webp|jpg|png)', html))
        # Filtrar imagenes de autos reales (excluir iconos y thumbnails genericos de menu)
        model_imgs = [im for im in all_imgs if not any(k in im.lower() for k in ['logo', 'icon', 'cropped', 'favicon', 'destacada', 'img_dest'])]
        # Priorizar imagenes grandes
        model_imgs = sorted(model_imgs, key=lambda x: (('cta' in x or 'ext' in x or 'int' in x) * 10, len(x)), reverse=True)
        print(f"  Encontradas {len(model_imgs)} imagenes para {vid}")

        raw_dir = RAW_DIR / vid
        raw_dir.mkdir(parents=True, exist_ok=True)
        v_dir = IMG_DIR / vid
        v_dir.mkdir(parents=True, exist_ok=True)

        pil_imgs = []
        for idx, img_url in enumerate(model_imgs[:8]):
            try:
                req = urllib.request.Request(img_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                    raw_file = raw_dir / f"official_raw_{len(pil_imgs)+1}.webp"
                    with open(raw_file, "wb") as f:
                        f.write(data)
                    with Image.open(io.BytesIO(data)) as im:
                        if im.width >= 400 and im.height >= 250:
                            pil_imgs.append(im.copy())
                            print(f"    [OK Raw {len(pil_imgs)}] {img_url.split('/')[-1]} ({im.width}x{im.height})")
                if len(pil_imgs) >= 6:
                    break
            except Exception as e:
                pass

        if not pil_imgs:
            print(f"  [!] No se pudieron descargar imagenes validas para {vid}")
            continue

        while len(pil_imgs) < 6:
            pil_imgs.append(pil_imgs[0].copy())

        vistas = sorted(list(v_dir.glob("0*-*.webp")), key=lambda p: p.name)
        if len(vistas) < 6:
            nombres_vistas = [
                "01-vista-isometrica-frontal-3-4",
                "02-vista-trasera-opticas-porton",
                "03-interior-tablero-consola-cockpit",
                "04-perfil-lateral-carroceria",
                "05-detalle-bateria-conector-carga",
                "06-detalle-frontal-firma-luminica"
            ]
            slug = vid
            vistas = [v_dir / f"{nv}-{slug}-auto-electrico-ev-servicioti-uruguay.webp" for nv in nombres_vistas]

        for i in range(6):
            target = vistas[i]
            im_src = pil_imgs[i]
            estudio = componer_estudio_4_3(im_src)
            temp_p = v_dir / f"temp_{i}.png"
            estudio.save(temp_p, format="PNG")

            MetadataImageService.inyectar_y_optimizar(
                temp_p,
                titulo=f"Fotografía Oficial de Estudio - {vid}",
                descripcion=f"Imagen oficial de catálogo para {vid} - EV Uruguay",
                calidad=90,
                destino=target,
                formato="WEBP"
            )
            if temp_p.exists():
                temp_p.unlink()
            print(f"    [OK Vista {i+1}] {target.name} ({target.stat().st_size // 1024} KB)")

        badge_path = v_dir / f"badge-circular-{vid}-auto-electrico-ev-servicioti-uruguay.webp"
        pixel_path = v_dir / f"pixel-art-16bit-{vid}-auto-electrico-ev-servicioti-uruguay.webp"
        generar_badge_circular(pil_imgs[0], badge_path, vid)
        generar_pixel_art(pil_imgs[0], pixel_path, vid)
        print(f"    [OK Badge & Pixel Art] Generados con exito para {vid}.")

    except Exception as e:
        print(f"Error procesando {vid}: {e}")
