# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys
import os
import io
import hashlib
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

WIKI_AGENT = 'EVUruguay/1.0 (contacto@servicioti.com.uy; https://ev.servicioti.com.uy)'
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

def search_wikimedia(query: str, limit: int = 6) -> list:
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url|mime&format=json&iiurlwidth=1280"
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            urls = []
            for p in pages.values():
                title = p.get('title', '').lower()
                if any(ext in title for ext in ['.svg', '.ogg', '.pdf', 'diagram', 'map', 'flag', 'logo']):
                    continue
                info = p.get('imageinfo', [])
                if info:
                    u = info[0].get('thumburl') or info[0].get('url')
                    if u and u.startswith('http'):
                        urls.append(u)
            return urls[:limit]
    except Exception:
        return []

WIKI_TARGETS = {
    "baw-pony-ev": ["BAW Yuanbao", "BAW Beijing-Beiqi Yuanbao"],
    "baw-l7-bagel-ev": ["BAW Yuanbao", "BAW Change Mini EV"],
    "chery-eq1": ["Chery eQ1", "Chery Little Ant"],
    "chery-qq-ice-cream": ["Chery QQ Ice Cream"],
    "geely-panda-mini-ev": ["Geely Panda Mini EV"],
    "changan-lumin-155": ["Changan Lumin", "2022 Chang'an Lumin"],
    "changan-lumin-301": ["Changan Lumin 001", "Changan Lumin"],
    "dongfeng-nammi-box": ["Dongfeng Nammi 01", "Dongfeng Box"],
    "dongfeng-nammi-330": ["Dongfeng Nammi 01", "Dongfeng Box"],
    "jac-e-js1": ["JAC e-JS1", "JAC E10X"],
    "jmev-ev3": ["JMC EV3", "JMEV Xiaoqilin", "JMEV EV3"],
    "niu-nqi-gt": ["Niu NQi", "NIU NQi 2026", "NIU scooter"],
    "super-soco-tc-max": ["Super Soco TC Max", "Elektromotorrad TC Max"],
    "yadea-g5-pro": ["Yadea electric scooter", "Yadea"],
    "yadea-c-umi": ["Yadea scooter", "Yadea electric"],
    "trike-hard-work-1000": ["electric cargo tricycle", "triciclo de carga"],
    "trike-cargo-light-500": ["electric delivery trike", "triciclo utilitario"],
    "trike-pasajeros-cabina": ["electric passenger tricycle", "rickshaw electric"],
    "trek-allant-plus-7": ["Trek electric bicycle", "Trek e-bike"],
    "specialized-turbo-vado-4": ["Specialized TURBO VADO", "Specialized e-bike"],
    "decathlon-rockrider-e-expl": ["Rockrider electric", "Rockrider E-EXPL"],
    "decathlon-riverside-500e": ["Riverside electric", "Riverside 500"],
    "xiaomi-himo-z20": ["Himo Z20", "Himo electric"],
    "voltbike-flex-foldable": ["folding electric bike", "electric folding bicycle"],
    "voltbike-pioneer": ["electric mountain bicycle", "e-mtb"],
    "voltbike-classica": ["vintage electric bicycle", "retro electric bike"]
}

for vid, queries in WIKI_TARGETS.items():
    print(f"\n==========================================")
    print(f"Cosechando fotos auténticas para: {vid}")
    print(f"==========================================")
    raw_dir = RAW_DIR / vid
    raw_dir.mkdir(parents=True, exist_ok=True)
    v_dir = IMG_DIR / vid
    v_dir.mkdir(parents=True, exist_ok=True)

    # Limpiar cualquier archivo contaminado
    for old_raw in raw_dir.glob("*.*"):
        old_raw.unlink()

    found_urls = []
    for q in queries:
        urls = search_wikimedia(q, limit=6)
        found_urls.extend(urls)
        if len(found_urls) >= 4:
            break

    pil_imgs = []
    for idx, u in enumerate(found_urls):
        try:
            req = urllib.request.Request(u, headers={'User-Agent': WIKI_AGENT})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = resp.read()
                # Verificar que no sea vacia o corrupta
                with Image.open(io.BytesIO(data)) as im:
                    if im.width >= 350 and im.height >= 250:
                        raw_file = raw_dir / f"official_raw_{len(pil_imgs)+1}.jpg"
                        with open(raw_file, "wb") as f:
                            f.write(data)
                        pil_imgs.append(im.copy())
                        print(f"  [OK Raw {len(pil_imgs)}] {im.width}x{im.height} ({u.split('/')[-1][:40]})")
            if len(pil_imgs) >= 6:
                break
        except Exception as e:
            pass

    if not pil_imgs:
        print(f"  [!] No se encontraron fotos para {vid}")
        continue

    while len(pil_imgs) < 6:
        pil_imgs.append(pil_imgs[0].copy())

    vistas = sorted(list(v_dir.glob("0*-*.webp")), key=lambda p: p.name)
    if len(vistas) < 6:
        nombres = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-opticas-porton",
            "03-puesto-conduccion-tablero-cockpit",
            "04-perfil-lateral-carroceria",
            "05-detalle-bateria-puerto-carga",
            "06-firma-luminica-optica-frontal"
        ]
        tipo_slug = "bicicleta-electrica" if any(k in vid for k in ['bike', 'vado', 'expl', '500e', 'himo']) else (
            "moto-electrica" if any(k in vid for k in ['sunra', 'niu', 'soco', 'yadea']) else (
                "triciclo-electrico" if 'trike' in vid else "auto-electrico"
            )
        )
        vistas = [v_dir / f"{nv}-{vid}-{tipo_slug}-ev-servicioti-uruguay.webp" for nv in nombres]

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
        print(f"  [OK Vista {i+1}] {target.name} ({target.stat().st_size // 1024} KB)")

    # Badges
    badges = list(v_dir.glob("badge-circular-*.webp"))
    if not badges:
        badges = [v_dir / f"badge-circular-{vid}-ev-servicioti-uruguay.webp"]
    for b in badges:
        generar_badge_circular(pil_imgs[0], b, vid)
        print(f"  [OK Badge] {b.name}")

    pixel_arts = list(v_dir.glob("pixel-art-16bit-*.webp"))
    if not pixel_arts:
        pixel_arts = [v_dir / f"pixel-art-16bit-{vid}-ev-servicioti-uruguay.webp"]
    for pa in pixel_arts:
        generar_pixel_art(pil_imgs[0], pa, vid)
        print(f"  [OK Pixel Art] {pa.name}")
