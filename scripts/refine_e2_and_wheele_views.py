# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from metadata_image_service import MetadataImageService

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "assets" / "img"
RAW_DIR = BASE_DIR / "assets" / "raw"

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

# 1. Copiar las 6 vistas oficiales de byd-new-e2-x-gs a byd-e2
e2_gs_dir = IMG_DIR / "byd-new-e2-x-gs"
e2_dir = IMG_DIR / "byd-e2"
e2_vistas = sorted(list(e2_dir.glob("0*-*.webp")), key=lambda p: p.name)
gs_vistas = sorted(list(e2_gs_dir.glob("0*-*.webp")), key=lambda p: p.name)

if len(gs_vistas) >= 6 and len(e2_vistas) >= 6:
    for i in range(6):
        im = Image.open(gs_vistas[i])
        temp_p = e2_dir / f"temp_{i}.png"
        im.save(temp_p, format="PNG")
        MetadataImageService.inyectar_y_optimizar(
            temp_p,
            titulo=f"BYD e2 Hatchback EV 405 - Vista Oficial {i+1}",
            descripcion=f"Imagen oficial de catálogo para BYD e2 - EV Uruguay",
            calidad=90,
            destino=e2_vistas[i],
            formato="WEBP"
        )
        if temp_p.exists():
            temp_p.unlink()
    print("[OK] byd-e2 actualizado con las 6 vistas oficiales distintas de SADAR.")

# 2. Generar vistas de detalle (zoom técnico) para Wheele
for vid in ["wheele-pocket-20", "wheele-manhattan-flex"]:
    v_dir = IMG_DIR / vid
    raw_p = RAW_DIR / vid / "official_raw_1.png"
    if not raw_p.exists():
        continue
    img_raw = Image.open(raw_p)
    W, H = img_raw.size

    # Crops tecnicos especificos
    crops = [
        img_raw,                                # 1: Hero completo
        img_raw.crop((0, int(H*0.2), int(W*0.55), H)), # 2: Rueda trasera y cuadro
        img_raw.crop((int(W*0.4), 0, int(W*0.8), int(H*0.55))), # 3: Manillar y display
        img_raw,                                # 4: Perfil lateral
        img_raw.crop((int(W*0.25), int(H*0.35), int(W*0.75), int(H*0.85))), # 5: Motor y bateria
        img_raw.crop((int(W*0.5), int(H*0.35), W, H))  # 6: Transmision y frenos
    ]

    vistas = sorted(list(v_dir.glob("0*-*.webp")), key=lambda p: p.name)
    for i in range(6):
        estudio = componer_estudio_4_3(crops[i])
        temp_p = v_dir / f"temp_{i}.png"
        estudio.save(temp_p, format="PNG")
        MetadataImageService.inyectar_y_optimizar(
            temp_p,
            titulo=f"Fotografía Oficial de Estudio - {vid} Vista {i+1}",
            descripcion=f"Imagen oficial de catálogo para {vid} - EV Uruguay",
            calidad=90,
            destino=vistas[i],
            formato="WEBP"
        )
        if temp_p.exists():
            temp_p.unlink()
    print(f"[OK] {vid} actualizado con 6 vistas técnicas diferenciadas.")
