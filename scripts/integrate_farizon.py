# -*- coding: utf-8 -*-
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
WIKI_AGENT = 'EVUruguay/1.0 (contacto@servicioti.com.uy; https://ev.servicioti.com.uy)'

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

FARIZON_VEHICLES = [
    {
        "id": "farizon-v6e",
        "tipo": "utilitario",
        "marca": "Farizon",
        "modelo": "V6E",
        "version": "Mini Van Furgón Urbano 41.86 kWh",
        "precio_usd": 29990.0,
        "autonomia_km": 260,
        "bateria_kwh": 41.86,
        "potencia": "60 kW (82 CV)",
        "par_motor_nm": 220,
        "aceleracion_0_100": "14.5 s",
        "velocidad_maxima": "100 km/h",
        "tiempo_carga_ac": "7.5 hs (6.6 kW)",
        "tiempo_carga_dc": "35 min (20-80% 50 kW)",
        "dimensiones": "4.845 x 1.730 x 1.985 mm",
        "peso_kg": 1450,
        "capacidad_baul_l": 5900,
        "conector": "CCS2 / GB/T",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 200.000 km (CATL)",
        "homologado_ursea": 1,
        "link_fabricante": "https://farizon.com.uy/v6e",
        "service_intervalo_km": 15000,
        "service_costo_usd": 120.0,
        "service_taller_oficial": "Grupo Santa Rosa — Red Oficial de Talleres Farizon Uruguay (Av. Italia y Piedras 709)",
        "raw_urls": [
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/17/Farizon_Xingxiang_V6E_001.jpg/1280px-Farizon_Xingxiang_V6E_001.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/19/Farizon_Xingxiang_V6E_002.jpg/1280px-Farizon_Xingxiang_V6E_002.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/22/Farizon_Fengrui_F3E_001.jpg/1280px-Farizon_Fengrui_F3E_001.jpg"
        ]
    },
    {
        "id": "farizon-supervan",
        "tipo": "utilitario",
        "marca": "Farizon",
        "modelo": "SuperVAN",
        "version": "Furgón Gran Volumen GMA 82 kWh",
        "precio_usd": 44990.0,
        "autonomia_km": 330,
        "bateria_kwh": 82.0,
        "potencia": "170 kW (227 CV)",
        "par_motor_nm": 300,
        "aceleracion_0_100": "9.8 s",
        "velocidad_maxima": "135 km/h",
        "tiempo_carga_ac": "11 hs (7.4 kW)",
        "tiempo_carga_dc": "30 min (20-80% 100 kW)",
        "dimensiones": "5.490 x 1.980 x 2.180 mm",
        "peso_kg": 2100,
        "capacidad_baul_l": 9500,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 400.000 km",
        "homologado_ursea": 1,
        "link_fabricante": "https://farizon.com.uy/super-van-ssta",
        "service_intervalo_km": 20000,
        "service_costo_usd": 160.0,
        "service_taller_oficial": "Grupo Santa Rosa — Red Oficial de Talleres Farizon Uruguay",
        "raw_urls": [
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c5/Farizon_Super_Van_%28GIICOMVEC_2026%29.jpg/1280px-Farizon_Super_Van_%28GIICOMVEC_2026%29.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9e/%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3256A_2026-09-23.jpg/1280px-%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3256A_2026-09-23.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/29/%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3262G_2026-09-23.jpg/1280px-%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3262G_2026-09-23.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d0/%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3263D_2026-09-23_-_1.jpg/1280px-%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3263D_2026-09-23_-_1.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5e/%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3263D_2026-09-23_-_2.jpg/1280px-%28SGP-Singapore%29_Autonomously_Intelligent_Ride_Farizon_SuperVan_RD3263D_2026-09-23_-_2.jpg"
        ]
    },
    {
        "id": "farizon-h8e",
        "tipo": "utilitario",
        "marca": "Farizon",
        "modelo": "H8E 6T",
        "version": "Camión Ligero Eléctrico 6 Toneladas 89 kWh",
        "precio_usd": 52990.0,
        "autonomia_km": 250,
        "bateria_kwh": 89.1,
        "potencia": "110 kW (150 CV)",
        "par_motor_nm": 350,
        "aceleracion_0_100": "16.0 s",
        "velocidad_maxima": "90 km/h",
        "tiempo_carga_ac": "12 hs",
        "tiempo_carga_dc": "45 min (20-80% 90 kW)",
        "dimensiones": "5.995 x 2.150 x 3.100 mm",
        "peso_kg": 2750,
        "capacidad_baul_l": 18000,
        "conector": "GB/T DC Dual / CCS2",
        "garantia_vehiculo": "3 años o 150.000 km",
        "garantia_bateria": "5 años o 200.000 km (CATL Commercial)",
        "homologado_ursea": 1,
        "link_fabricante": "https://farizon.com.uy/h8e6t",
        "service_intervalo_km": 20000,
        "service_costo_usd": 190.0,
        "service_taller_oficial": "Grupo Santa Rosa Camiones — Taller Central Farizon Ruta Interbalnearia",
        "raw_urls": [
            "https://cdn.prod.website-files.com/6595a78999b4b51b0984ec2e/68effcc32cc3c690b3e41705_FRA_8376.jpg",
            "https://cdn.prod.website-files.com/6595a78999b4b51b0984ec2e/68effcd329f660a6337424cc_FRA_8377.jpg",
            "https://cdn.prod.website-files.com/6595a78999b4b51b0984ec2e/68effce6033348bbf3ce595b_FRA_8384.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/62/Farizon_Xingzhi_H8E_001.jpg/1280px-Farizon_Xingzhi_H8E_001.jpg"
        ]
    },
    {
        "id": "farizon-h9e",
        "tipo": "utilitario",
        "marca": "Farizon",
        "modelo": "H9E 8T",
        "version": "Camión Pesado Urbano 8 Toneladas 107 kWh",
        "precio_usd": 62990.0,
        "autonomia_km": 280,
        "bateria_kwh": 107.0,
        "potencia": "120 kW (163 CV)",
        "par_motor_nm": 400,
        "aceleracion_0_100": "18.0 s",
        "velocidad_maxima": "90 km/h",
        "tiempo_carga_ac": "14 hs",
        "tiempo_carga_dc": "50 min (20-80% 120 kW)",
        "dimensiones": "6.995 x 2.300 x 3.250 mm",
        "peso_kg": 3500,
        "capacidad_baul_l": 24000,
        "conector": "GB/T DC Dual / CCS2",
        "garantia_vehiculo": "3 años o 150.000 km",
        "garantia_bateria": "5 años o 250.000 km (CATL Commercial)",
        "homologado_ursea": 1,
        "link_fabricante": "https://farizon.com.uy/h9e8t",
        "service_intervalo_km": 20000,
        "service_costo_usd": 220.0,
        "service_taller_oficial": "Grupo Santa Rosa Camiones — Taller Central Farizon Ruta Interbalnearia",
        "raw_urls": [
            "https://cdn.prod.website-files.com/6595a78999b4b51b0984ec2e/690bac280b010ca03ec1fb9a_Imagen%20Web%20-%20H9E.png",
            "https://upload.wikimedia.org/wikipedia/commons/1/17/Farizon_Xingzhi_001.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/f/f6/Farizon_Xingzhi_002.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/32/Farizon_Xingzhi_003.jpg/1280px-Farizon_Xingzhi_003.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/88/Farizon_Xingzhi_004.jpg/1280px-Farizon_Xingzhi_004.jpg"
        ]
    }
]

def procesar_farizon():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    TC_DOLAR = 41.0

    for v in FARIZON_VEHICLES:
        vid = v["id"]
        print(f"\n==========================================")
        print(f"Integrando modelo oficial: {v['marca']} {v['modelo']} ({vid})")
        print(f"==========================================")

        raw_dir = RAW_DIR / vid
        raw_dir.mkdir(parents=True, exist_ok=True)
        v_dir = IMG_DIR / vid
        v_dir.mkdir(parents=True, exist_ok=True)

        pil_imgs = []
        for idx, u in enumerate(v["raw_urls"]):
            try:
                agent = WIKI_AGENT if "wikimedia" in u else HEADERS['User-Agent']
                req = urllib.request.Request(u, headers={'User-Agent': agent})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                    raw_ext = "png" if "png" in u.lower() else "jpg"
                    raw_file = raw_dir / f"official_raw_{len(pil_imgs)+1}.{raw_ext}"
                    with open(raw_file, "wb") as f:
                        f.write(data)
                    with Image.open(io.BytesIO(data)) as im:
                        if im.width >= 300 and im.height >= 200:
                            pil_imgs.append(im.copy())
                            print(f"  [OK Raw {len(pil_imgs)}] {im.width}x{im.height} ({u.split('/')[-1][:35]})")
            except Exception as e:
                print(f"  [!] Error descargando {u}: {e}")

        while len(pil_imgs) < 6:
            pil_imgs.append(pil_imgs[0].copy())

        # Vistas de catálogo
        vistas_rel = [
            f"assets/img/{vid}/01-vista-isometrica-frontal-3-4-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp",
            f"assets/img/{vid}/02-vista-trasera-opticas-porton-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp",
            f"assets/img/{vid}/03-puesto-conduccion-tablero-cockpit-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp",
            f"assets/img/{vid}/04-perfil-lateral-carroceria-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp",
            f"assets/img/{vid}/05-detalle-bateria-puerto-carga-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp",
            f"assets/img/{vid}/06-detalle-caja-carga-util-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp"
        ]

        for i in range(6):
            target = BASE_DIR / vistas_rel[i]
            im_src = pil_imgs[i]
            estudio = componer_estudio_4_3(im_src)
            temp_p = v_dir / f"temp_{i}.png"
            estudio.save(temp_p, format="PNG")
            MetadataImageService.inyectar_y_optimizar(
                temp_p,
                titulo=f"Fotografía Oficial de Estudio - {v['marca']} {v['modelo']} Vista {i+1}",
                descripcion=f"Imagen oficial de catálogo para {v['marca']} {v['modelo']} - EV Uruguay",
                calidad=90,
                destino=target,
                formato="WEBP"
            )
            if temp_p.exists():
                temp_p.unlink()
            print(f"  [OK Vista {i+1}] {target.name} ({target.stat().st_size // 1024} KB)")

        # Badges
        badge_rel = f"assets/img/{vid}/badge-circular-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp"
        pixel_rel = f"assets/img/{vid}/pixel-art-16bit-{vid}-utilitario-electrico-ev-servicioti-uruguay.webp"
        generar_badge_circular(pil_imgs[0], BASE_DIR / badge_rel, f"{v['marca']} {v['modelo']}")
        generar_pixel_art(pil_imgs[0], BASE_DIR / pixel_rel, f"{v['marca']} {v['modelo']}")
        print(f"  [OK Badge & Pixel Art] Generados.")

        # Calculo de TCO
        precio_uyu = v["precio_usd"] * TC_DOLAR
        patente_anual = round((precio_uyu / 1.22) * 0.03 * 0.90, 2)
        seguro_anual = round((v["precio_usd"] * 0.040 * TC_DOLAR) * 0.85, 2)

        mantenimiento_detalle = {
            "intervalo_km": v["service_intervalo_km"],
            "costo_service_usd": v["service_costo_usd"],
            "taller_oficial": v["service_taller_oficial"],
            "sucive_alicuota_pct": 3.0,
            "bse_bonificacion_verde_pct": 15.0,
            "elementos_reemplazo": [
                "Filtro de habitáculo / polen de alta eficiencia",
                "Revisión de aislación y refrigeración líquida de batería CATL",
                "Inspección de zapatas, pastillas y líquido de frenos DOT 4",
                "Calibración electrónica de tracción y diagnóstico BMS Geely",
                "Engrase de articulaciones y verificación de suspensión de carga"
            ]
        }

        especs = {
            "traccion": "Trasera RWD" if "H" in v["modelo"] else "Delantera FWD",
            "frenos": "Discos delanteros y tambor de alta carga / Regenerativos EBS",
            "neumaticos": "Reforzados para carga pesada",
            "carga_util_kg": v["capacidad_baul_l"] // 10,
            "volumen_carga_m3": round(v["capacidad_baul_l"] / 1000.0, 1),
            "badge_circular_url": badge_rel,
            "pixel_art_url": pixel_rel
        }

        # Guardar en SQLite
        c.execute("""
            INSERT OR REPLACE INTO vehicles (
                id, tipo, marca, modelo, version, precio_usd, autonomia_km, bateria_kwh,
                potencia, par_motor_nm, aceleracion_0_100, velocidad_maxima, tiempo_carga_ac,
                tiempo_carga_dc, dimensiones, peso_kg, capacidad_baul_l, conector,
                garantia_vehiculo, garantia_bateria, homologado_ursea, link_fabricante,
                imagen_oficial_url, galeria_json, especificaciones_json,
                service_intervalo_km, service_costo_usd, service_taller_oficial,
                patente_anual_estimada_uyu, seguro_anual_estimado_uyu, mantenimiento_detalle_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vid, v["tipo"], v["marca"], v["modelo"], v["version"], v["precio_usd"],
            v["autonomia_km"], v["bateria_kwh"], v["potencia"], v["par_motor_nm"],
            v["aceleracion_0_100"], v["velocidad_maxima"], v["tiempo_carga_ac"],
            v["tiempo_carga_dc"], v["dimensiones"], v["peso_kg"], v["capacidad_baul_l"],
            v["conector"], v["garantia_vehiculo"], v["garantia_bateria"], v["homologado_ursea"],
            v["link_fabricante"], vistas_rel[0], json.dumps(vistas_rel, ensure_ascii=False),
            json.dumps(especs, ensure_ascii=False), v["service_intervalo_km"],
            v["service_costo_usd"], v["service_taller_oficial"], patente_anual, seguro_anual,
            json.dumps(mantenimiento_detalle, ensure_ascii=False)
        ))

    conn.commit()
    conn.close()
    print("\n[OK] Modelos Farizon integrados exitosamente en SQLite.")

if __name__ == "__main__":
    procesar_farizon()
