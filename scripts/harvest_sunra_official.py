# -*- coding: utf-8 -*-
import urllib.request
import re
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

# Fuentes oficiales Sunra Uruguay & Sunra Global
SUNRA_ASSETS = {
    "sunra-miku-super": [
        "https://sunra.com.uy/wp-content/uploads/2026/01/9-Miku-Super.png",
        "https://www.sunraev.com/uploads/20211119/6253c301bb2eef8e5f762696667a48fb.png",
        "https://sunra.com.uy/wp-content/uploads/2026/01/1.-Spy-Racing-1500.png"
    ],
    "sunra-cargo-triciclo": [
        "https://sunra.com.uy/wp-content/uploads/2026/01/5.-King-Kong_.png",
        "https://sunra.com.uy/wp-content/uploads/2026/01/5.-King-Kong_.png"
    ],
    "sunra-hawk-3000": [
        "https://sunra.com.uy/wp-content/uploads/2026/01/4.-K3-Tango.png",
        "https://www.sunraev.com/uploads/20211119/61_1.jpg"
    ],
    "sunra-grace-1800": [
        "https://sunra.com.uy/wp-content/uploads/2026/01/2.-Future.png",
        "https://www.sunraev.com/uploads/20211119/63_1.jpg"
    ],
    "sunra-robo-s": [
        "https://sunra.com.uy/wp-content/uploads/2026/01/11.-Spy-Racyng-Z6.png",
        "https://www.sunraev.com/uploads/20211119/60_1.jpg"
    ]
}

def process_sunra_model(vid, urls):
    print(f"\n--- Procesando {vid} ---")
    raw_dir = RAW_DIR / vid
    raw_dir.mkdir(parents=True, exist_ok=True)
    v_dir = IMG_DIR / vid
    v_dir.mkdir(parents=True, exist_ok=True)

    pil_imgs = []
    for idx, u in enumerate(urls):
        try:
            req = urllib.request.Request(u, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                raw_file = raw_dir / f"official_raw_{len(pil_imgs)+1}.png"
                with open(raw_file, "wb") as f:
                    f.write(data)
                with Image.open(io.BytesIO(data)) as im:
                    pil_imgs.append(im.copy())
                print(f"  [OK Raw {len(pil_imgs)}] {u.split('/')[-1]}")
        except Exception as e:
            print(f"  [!] Fallo descarga {u}: {e}")

    if not pil_imgs:
        print(f"  [!] Sin imagenes para {vid}")
        return

    while len(pil_imgs) < 6:
        # Generar variaciones de angulo (crop o flip sutil) si son pocos renders
        base = pil_imgs[0].copy()
        pil_imgs.append(base)

    vistas = sorted(list(v_dir.glob("0*-*.webp")), key=lambda p: p.name)
    if len(vistas) < 6:
        nombres = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-opticas-porton",
            "03-puesto-conduccion-manillar-display",
            "04-perfil-lateral-chasis",
            "05-detalle-bateria-puerto-recarga",
            "06-firma-luminica-optica-frontal"
        ]
        tipo_slug = "triciclo-electrico" if "cargo" in vid else "moto-electrica"
        vistas = [v_dir / f"{nv}-{vid}-{tipo_slug}-ev-servicioti-uruguay.webp" for nv in nombres]

    for i in range(6):
        target = vistas[i]
        estudio = componer_estudio_4_3(pil_imgs[i])
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

    badge_path = v_dir / f"badge-circular-{vid}-auto-electrico-ev-servicioti-uruguay.webp"
    pixel_path = v_dir / f"pixel-art-16bit-{vid}-auto-electrico-ev-servicioti-uruguay.webp"
    generar_badge_circular(pil_imgs[0], badge_path, vid)
    generar_pixel_art(pil_imgs[0], pixel_path, vid)
    print(f"  [OK Badge & Pixel Art] Generados con exito.")

if __name__ == "__main__":
    for vid, urls in SUNRA_ASSETS.items():
        process_sunra_model(vid, urls)
