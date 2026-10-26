# -*- coding: utf-8 -*-
import io
import urllib.request
from PIL import Image, ImageDraw, ImageFilter
from metadata_image_service import MetadataImageService

def componer_encuadre_4_3(img_src: Image.Image) -> Image.Image:
    ancho_target, alto_target = 1200, 900
    suelo_y = 620
    apoyo_y = 740

    canvas = Image.new("RGB", (ancho_target, alto_target), (252, 252, 253))
    draw = ImageDraw.Draw(canvas)
    for y in range(suelo_y, alto_target):
        factor = (y - suelo_y) / float(alto_target - suelo_y)
        val = int(252 - factor * 12)
        draw.line([(0, y), (ancho_target, y)], fill=(val, val, val + 1))

    # Sombra suave de contacto
    shadow = Image.new("RGBA", (ancho_target, alto_target), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(int(ancho_target * 0.15), apoyo_y - 30), (int(ancho_target * 0.85), apoyo_y + 50)], fill=(0, 0, 0, 75))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=24))
    canvas.paste(shadow, (0, 0), shadow)

    src_rgb = img_src.convert("RGB")
    ancho_max = int(ancho_target * 0.88)
    alto_max = int(alto_target * 0.70)

    ratio = min(ancho_max / float(src_rgb.width), alto_max / float(src_rgb.height))
    nuevo_ancho = max(10, int(src_rgb.width * ratio))
    nuevo_alto = max(10, int(src_rgb.height * ratio))

    img_scaled = src_rgb.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    pos_x = (ancho_target - nuevo_ancho) // 2
    pos_y = apoyo_y - nuevo_alto
    if pos_y < 50:
        pos_y = (alto_target - nuevo_alto) // 2

    canvas.paste(img_scaled, (pos_x, pos_y))
    return canvas

print("Función de encuadre 4:3 lista.")
