# -*- coding: utf-8 -*-
import urllib.request
import sys
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
    sdraw.ellipse([(180, 715), (1020, 785)], fill=(0, 0, 0, 50))
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

wheele_targets = {
    "wheele-pocket-20": "https://wheele.com.uy/images/stories/virtuemart/product/pocket_20-portada6.png",
    "wheele-manhattan-flex": "https://wheele.com.uy/images/stories/virtuemart/product/manhattan_flex_20-portada.png"
}

for vid, url in wheele_targets.items():
    print(f"\nProcesando {vid}...")
    req = urllib.request.Request(url, headers=HEADERS)
    raw_data = urllib.request.urlopen(req, timeout=10).read()

    raw_dir = RAW_DIR / vid
    raw_dir.mkdir(parents=True, exist_ok=True)
    with open(raw_dir / "official_raw_1.png", "wb") as f:
        f.write(raw_data)

    img_raw = Image.open(io.BytesIO(raw_data))

    v_dir = IMG_DIR / vid
    # Eliminar cualquier archivo obsoleto sin isometrica
    for obsolete in v_dir.glob("01-vista-frontal-3-4-*.webp"):
        obsolete.unlink()
        print(f"  [Eliminado obsoleto]: {obsolete.name}")

    vistas = sorted(list(v_dir.glob("0*-*.webp")), key=lambda p: p.name)
    print(f"  Vistas a generar: {len(vistas)}")

    for i, target in enumerate(vistas[:6]):
        estudio = componer_estudio_4_3(img_raw)
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
        print(f"  [OK Vista {i+1}] {target.name} ({target.stat().st_size // 1024} KB)")

    # Actualizar badge circular y pixel art
    for b in v_dir.glob("badge-circular-*.webp"):
        generar_badge_circular(img_raw, b, vid)
        print(f"  [OK Badge] {b.name}")
    for pa in v_dir.glob("pixel-art-16bit-*.webp"):
        generar_pixel_art(img_raw, pa, vid)
        print(f"  [OK Pixel Art] {pa.name}")
