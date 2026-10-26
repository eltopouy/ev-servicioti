# -*- coding: utf-8 -*-
"""
Construcción de la base de datos de Marcas de Uruguay (brand_profiles)
y cosecha/generación de logos oficiales con inyección de metadatos ServicioTI.
"""
import sqlite3
import urllib.request
import json
import sys
import os
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from metadata_image_service import MetadataImageService

BASE_DIR = Path(__file__).resolve().parent.parent
LOGOS_DIR = BASE_DIR / "assets" / "img" / "logos"
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
WIKI_AGENT = 'EVUruguay/1.0 (contacto@servicioti.com.uy; https://ev.servicioti.com.uy)'

BRAND_DEFINITIONS = [
    {
        "id": "farizon",
        "marcas_coincidentes": ["Farizon"],
        "nombre": "Farizon Uruguay",
        "importador_oficial": "Grupo Santa Rosa",
        "direccion": "Piedras 709 esq. Juncal / Av. Italia 4905, Montevideo",
        "sitio_oficial": "https://farizon.com.uy",
        "instagram_handle": "@farizonuruguay",
        "instagram_url": "https://www.instagram.com/farizonuruguay/",
        "logo_source_url": "https://cdn.prod.website-files.com/6595a78999b4b51b0984ec2e/66031bb1154cc8e78e196834_farizon_logo.png"
    },
    {
        "id": "byd",
        "marcas_coincidentes": ["BYD"],
        "nombre": "BYD Uruguay",
        "importador_oficial": "Sadar",
        "direccion": "Av. Italia 4905 / Portones Shopping, Montevideo",
        "sitio_oficial": "https://byd.com.uy",
        "instagram_handle": "@byd_uruguay",
        "instagram_url": "https://www.instagram.com/byd_uruguay/",
        "wiki_logo_title": "File:BYD Auto logo 2022.svg"
    },
    {
        "id": "geely",
        "marcas_coincidentes": ["Geely"],
        "nombre": "Geely Uruguay",
        "importador_oficial": "Grupo Fiancar",
        "direccion": "Av. Italia 5345, Montevideo",
        "sitio_oficial": "https://geely.com.uy",
        "instagram_handle": "@geelyuruguay",
        "instagram_url": "https://www.instagram.com/geelyuruguay/",
        "wiki_logo_title": "File:Geely Auto logo 2023.svg"
    },
    {
        "id": "chery",
        "marcas_coincidentes": ["Chery"],
        "nombre": "Chery Uruguay",
        "importador_oficial": "Asiancars / Grupo Fiancar",
        "direccion": "Ruta Interbalnearia Km 22.500 / Montevideo",
        "sitio_oficial": "https://chery.com.uy",
        "instagram_handle": "@cheryuruguay",
        "instagram_url": "https://www.instagram.com/cheryuruguay/",
        "wiki_logo_title": "File:Chery logo.svg"
    },
    {
        "id": "jac",
        "marcas_coincidentes": ["JAC"],
        "nombre": "JAC Uruguay",
        "importador_oficial": "Grupo Fiancar / Bor",
        "direccion": "Av. Italia 5345, Montevideo",
        "sitio_oficial": "https://jac.com.uy",
        "instagram_handle": "@jacuruguay",
        "instagram_url": "https://www.instagram.com/jacuruguay/",
        "wiki_logo_title": "File:JAC Motors logo.svg"
    },
    {
        "id": "jmc",
        "marcas_coincidentes": ["JMC"],
        "nombre": "JMC Uruguay",
        "importador_oficial": "Grupo Santa Rosa",
        "direccion": "Piedras 709 esq. Juncal, Montevideo",
        "sitio_oficial": "https://jmc.com.uy",
        "instagram_handle": "@jmc_uruguay",
        "instagram_url": "https://www.instagram.com/jmc_uruguay/",
        "wiki_logo_title": "File:Jiangling Motors logo.svg"
    },
    {
        "id": "volvo",
        "marcas_coincidentes": ["Volvo"],
        "nombre": "Volvo Cars Uruguay",
        "importador_oficial": "Camur / Grupo Gildemeister",
        "direccion": "Av. Italia 5678, Carrasco, Montevideo",
        "sitio_oficial": "https://volvocars.com.uy",
        "instagram_handle": "@volvocarsuruguay",
        "instagram_url": "https://www.instagram.com/volvocarsuruguay/",
        "wiki_logo_title": "File:Volvo logo.svg"
    },
    {
        "id": "tesla",
        "marcas_coincidentes": ["Tesla"],
        "nombre": "Tesla Uruguay",
        "importador_oficial": "Importación Homologada / Servicio Especializado EV",
        "direccion": "Montevideo, Uruguay",
        "sitio_oficial": "https://tesla.com",
        "instagram_handle": "@teslamotors",
        "instagram_url": "https://www.instagram.com/teslamotors/",
        "wiki_logo_title": "File:Tesla Motors.svg"
    },
    {
        "id": "chevrolet",
        "marcas_coincidentes": ["Chevrolet"],
        "nombre": "Chevrolet Uruguay",
        "importador_oficial": "General Motors Uruguay",
        "direccion": "Av. Italia 4001, Montevideo",
        "sitio_oficial": "https://chevrolet.com.uy",
        "instagram_handle": "@chevroleturuguay",
        "instagram_url": "https://www.instagram.com/chevroleturuguay/",
        "wiki_logo_title": "File:Chevrolet-logo.svg"
    },
    {
        "id": "renault",
        "marcas_coincidentes": ["Renault"],
        "nombre": "Renault Uruguay",
        "importador_oficial": "Grupo Santa Rosa",
        "direccion": "Cerro Largo 888 / Av. Italia 4905, Montevideo",
        "sitio_oficial": "https://renault.com.uy",
        "instagram_handle": "@renaulturuguay",
        "instagram_url": "https://www.instagram.com/renaulturuguay/",
        "wiki_logo_title": "File:Renault 2021.svg"
    },
    {
        "id": "nissan",
        "marcas_coincidentes": ["Nissan"],
        "nombre": "Nissan Uruguay",
        "importador_oficial": "Grupo Santa Rosa",
        "direccion": "Rambla Baltasar Brum 2980, Montevideo",
        "sitio_oficial": "https://nissan.com.uy",
        "instagram_handle": "@nissanuruguay",
        "instagram_url": "https://www.instagram.com/nissanuruguay/",
        "wiki_logo_title": "File:Nissan 2020 logo.svg"
    },
    {
        "id": "bmw",
        "marcas_coincidentes": ["BMW"],
        "nombre": "BMW Uruguay",
        "importador_oficial": "Motor Haus",
        "direccion": "Av. Giannattasio Km 20 / Av. Italia 4200, Montevideo",
        "sitio_oficial": "https://bmw.com.uy",
        "instagram_handle": "@bmw.uruguay",
        "instagram_url": "https://www.instagram.com/bmw.uruguay/",
        "wiki_logo_title": "File:BMW logo (gray).svg"
    },
    {
        "id": "audi",
        "marcas_coincidentes": ["Audi"],
        "nombre": "Audi Uruguay",
        "importador_oficial": "Julio César Lestido S.A.",
        "direccion": "Cerro Largo 1729 / Av. Italia 5300, Montevideo",
        "sitio_oficial": "https://audi.com.uy",
        "instagram_handle": "@audi_uy",
        "instagram_url": "https://www.instagram.com/audi_uy/",
        "wiki_logo_title": "File:Audi-Logo_2016.svg"
    },
    {
        "id": "mercedes-benz",
        "marcas_coincidentes": ["Mercedes-Benz"],
        "nombre": "Mercedes-Benz Uruguay",
        "importador_oficial": "Autolider Uruguay (Inchcape)",
        "direccion": "Rambla Baltasar Brum 2986, Montevideo",
        "sitio_oficial": "https://mercedes-benz.com.uy",
        "instagram_handle": "@mercedesbenz_uy",
        "instagram_url": "https://www.instagram.com/mercedesbenz_uy/",
        "wiki_logo_title": "File:Mercedes-Logo.svg"
    },
    {
        "id": "mini",
        "marcas_coincidentes": ["Mini"],
        "nombre": "MINI Uruguay",
        "importador_oficial": "Motor Haus",
        "direccion": "Av. Italia 4200, Montevideo",
        "sitio_oficial": "https://mini.com.uy",
        "instagram_handle": "@mini_uruguay",
        "instagram_url": "https://www.instagram.com/mini_uruguay/",
        "wiki_logo_title": "File:Mini logo.svg"
    },
    {
        "id": "hyundai",
        "marcas_coincidentes": ["Hyundai"],
        "nombre": "Hyundai Uruguay",
        "importador_oficial": "Fidocar S.A.",
        "direccion": "Av. Italia 4620, Montevideo",
        "sitio_oficial": "https://hyundai.com.uy",
        "instagram_handle": "@hyundaiuruguay",
        "instagram_url": "https://www.instagram.com/hyundaiuruguay/",
        "wiki_logo_title": "File:Hyundai Motor Company logo.svg"
    },
    {
        "id": "kia",
        "marcas_coincidentes": ["Kia"],
        "nombre": "Kia Uruguay",
        "importador_oficial": "Kia Uruguay / Grupo Fiancar",
        "direccion": "Rambla Baltasar Brum 3764, Montevideo",
        "sitio_oficial": "https://kia.com.uy",
        "instagram_handle": "@kiauruguay",
        "instagram_url": "https://www.instagram.com/kiauruguay/",
        "wiki_logo_title": "File:Kia 2021.svg"
    },
    {
        "id": "gwm",
        "marcas_coincidentes": ["GWM"],
        "nombre": "GWM Uruguay (ORA / Haval)",
        "importador_oficial": "Homero De León",
        "direccion": "Av. Libertador 1777, Montevideo",
        "sitio_oficial": "https://gwm.com.uy",
        "instagram_handle": "@gwmuruguay",
        "instagram_url": "https://www.instagram.com/gwmuruguay/",
        "wiki_logo_title": "File:Great Wall Motor logo.svg"
    },
    {
        "id": "changan",
        "marcas_coincidentes": ["Changan"],
        "nombre": "Changan Uruguay",
        "importador_oficial": "Grupo Santa Rosa",
        "direccion": "Piedras 709, Montevideo",
        "sitio_oficial": "https://changan.com.uy",
        "instagram_handle": "@changanuruguay",
        "instagram_url": "https://www.instagram.com/changanuruguay/",
        "wiki_logo_title": "File:Changan Automobile logo.svg"
    },
    {
        "id": "maxus",
        "marcas_coincidentes": ["Maxus"],
        "nombre": "Maxus Uruguay",
        "importador_oficial": "Grupo Antelo / Santa Rosa",
        "direccion": "Cerro Largo 888, Montevideo",
        "sitio_oficial": "https://maxus.com.uy",
        "instagram_handle": "@maxusuruguay",
        "instagram_url": "https://www.instagram.com/maxusuruguay/",
        "wiki_logo_title": "File:LDV MAXUS logo.svg"
    },
    {
        "id": "zeekr",
        "marcas_coincidentes": ["Zeekr"],
        "nombre": "Zeekr Uruguay",
        "importador_oficial": "Grupo Fiancar",
        "direccion": "Av. Italia 5345, Montevideo",
        "sitio_oficial": "https://zeekr.com.uy",
        "instagram_handle": "@zeekr.uruguay",
        "instagram_url": "https://www.instagram.com/zeekr.uruguay/",
        "wiki_logo_title": "File:Zeekr logo.svg"
    },
    {
        "id": "dongfeng",
        "marcas_coincidentes": ["Dongfeng"],
        "nombre": "Dongfeng Uruguay",
        "importador_oficial": "Sadar / Cidef",
        "direccion": "Av. Italia 4905, Montevideo",
        "sitio_oficial": "https://dongfeng.com.uy",
        "instagram_handle": "@dongfenguruguay",
        "instagram_url": "https://www.instagram.com/dongfenguruguay/",
        "wiki_logo_title": "File:Dongfeng Motor Corporation logo.svg"
    },
    {
        "id": "baw",
        "marcas_coincidentes": ["BAW"],
        "nombre": "BAW Uruguay",
        "importador_oficial": "Grupo Antelo",
        "direccion": "Montevideo, Uruguay",
        "sitio_oficial": "https://baw.com.uy",
        "instagram_handle": "@bawuruguay",
        "instagram_url": "https://www.instagram.com/bawuruguay/",
        "wiki_logo_title": "File:Beijing Automobile Works logo.svg"
    },
    {
        "id": "omoda",
        "marcas_coincidentes": ["Omoda"],
        "nombre": "Omoda & Jaecoo Uruguay",
        "importador_oficial": "Grupo Santa Rosa",
        "direccion": "Av. Italia 4905, Montevideo",
        "sitio_oficial": "https://omodajaecoo.com.uy",
        "instagram_handle": "@omoda.uruguay",
        "instagram_url": "https://www.instagram.com/omoda.uruguay/",
        "wiki_logo_title": "File:Omoda logo.svg"
    },
    {
        "id": "sunra",
        "marcas_coincidentes": ["Sunra"],
        "nombre": "Sunra Uruguay",
        "importador_oficial": "Sunra Centro Uruguay",
        "direccion": "Av. Brasil 2980, Pocitos, Montevideo",
        "sitio_oficial": "https://sunra.com.uy",
        "instagram_handle": "@sunrauruguay",
        "instagram_url": "https://www.instagram.com/sunrauruguay/",
        "wiki_logo_title": "File:Sunra logo.svg"
    },
    {
        "id": "yadea",
        "marcas_coincidentes": ["Yadea"],
        "nombre": "Yadea Uruguay",
        "importador_oficial": "Grupo Fiancar Motos",
        "direccion": "Av. Italia 5345, Montevideo",
        "sitio_oficial": "https://yadea.com.uy",
        "instagram_handle": "@yadeauruguay",
        "instagram_url": "https://www.instagram.com/yadeauruguay/",
        "wiki_logo_title": "File:Yadea Logo.svg"
    },
    {
        "id": "niu",
        "marcas_coincidentes": ["Niu"],
        "nombre": "NIU Mobility Uruguay",
        "importador_oficial": "NIU Uruguay",
        "direccion": "Av. Rivera 2680, Montevideo",
        "sitio_oficial": "https://niu.uy",
        "instagram_handle": "@niu_uruguay",
        "instagram_url": "https://www.instagram.com/niu_uruguay/",
        "wiki_logo_title": "File:Niu Technologies logo.svg"
    },
    {
        "id": "super-soco",
        "marcas_coincidentes": ["Super Soco"],
        "nombre": "Super Soco Uruguay",
        "importador_oficial": "VMoto Soco Uruguay",
        "direccion": "Montevideo, Uruguay",
        "sitio_oficial": "https://supersoco.com.uy",
        "instagram_handle": "@supersocouruguay",
        "instagram_url": "https://www.instagram.com/supersocouruguay/",
        "wiki_logo_title": "File:Super Soco logo.svg"
    },
    {
        "id": "voltbike",
        "marcas_coincidentes": ["VoltBike"],
        "nombre": "VoltBike Uruguay",
        "importador_oficial": "VoltBike UY",
        "direccion": "Av. Centenario 2840, Montevideo",
        "sitio_oficial": "https://voltbike.uy",
        "instagram_handle": "@voltbike.uy",
        "instagram_url": "https://www.instagram.com/voltbike.uy/",
        "logo_source_url": "https://voltbike.uy/cdn/shop/files/logo-voltbike.png"
    },
    {
        "id": "wheele",
        "marcas_coincidentes": ["Wheele"],
        "nombre": "Wheele Uruguay",
        "importador_oficial": "Wheele Mobility",
        "direccion": "Canelones 1230, Montevideo",
        "sitio_oficial": "https://wheele.uy",
        "instagram_handle": "@wheele.uy",
        "instagram_url": "https://www.instagram.com/wheele.uy/",
        "logo_source_url": "https://wheele.uy/assets/img/logo.png"
    },
    {
        "id": "loop-bikes",
        "marcas_coincidentes": ["Loop Bikes"],
        "nombre": "Loop Bikes Uruguay",
        "importador_oficial": "Loop Bikes E-Mobility",
        "direccion": "Benito Blanco 1012, Montevideo",
        "sitio_oficial": "https://loopbikes.com.uy",
        "instagram_handle": "@loopbikesuy",
        "instagram_url": "https://www.instagram.com/loopbikesuy/"
    },
    {
        "id": "trek",
        "marcas_coincidentes": ["Trek"],
        "nombre": "Trek Bicycle Uruguay",
        "importador_oficial": "Summit Sports / Motociclo Sports",
        "direccion": "Av. Brasil 2550, Pocitos, Montevideo",
        "sitio_oficial": "https://trekbikes.com",
        "instagram_handle": "@trekbikesuruguay",
        "instagram_url": "https://www.instagram.com/trekbikesuruguay/",
        "wiki_logo_title": "File:Trek Bicycle Corporation logo.svg"
    },
    {
        "id": "specialized",
        "marcas_coincidentes": ["Specialized"],
        "nombre": "Specialized Uruguay",
        "importador_oficial": "Specialized Concept Store Carrasco",
        "direccion": "Av. Bolivia 1430, Montevideo",
        "sitio_oficial": "https://specialized.com",
        "instagram_handle": "@specializeduruguay",
        "instagram_url": "https://www.instagram.com/specializeduruguay/",
        "wiki_logo_title": "File:Specialized Bicycle Components logo.svg"
    },
    {
        "id": "decathlon",
        "marcas_coincidentes": ["Decathlon / Riverside", "Decathlon / Rockrider"],
        "nombre": "Decathlon Uruguay",
        "importador_oficial": "Decathlon Car One",
        "direccion": "Ruta Interbalnearia y C. de los Horneros, Canelones",
        "sitio_oficial": "https://decathlon.com.uy",
        "instagram_handle": "@decathlonuruguay",
        "instagram_url": "https://www.instagram.com/decathlonuruguay/",
        "wiki_logo_title": "File:Decathlon Logo.svg"
    },
    {
        "id": "xiaomi",
        "marcas_coincidentes": ["Xiaomi / Himo"],
        "nombre": "Xiaomi Uruguay / Himo",
        "importador_oficial": "Mi Store Uruguay Oficial",
        "direccion": "Punta Carretas Shopping / Montevideo Shopping",
        "sitio_oficial": "https://miuruguay.com",
        "instagram_handle": "@xiaomi.uruguay",
        "instagram_url": "https://www.instagram.com/xiaomi.uruguay/",
        "wiki_logo_title": "File:Xiaomi logo 2021.svg"
    },
    {
        "id": "trike",
        "marcas_coincidentes": ["Trike"],
        "nombre": "Trike E-Mobility Uruguay",
        "importador_oficial": "Trike Uruguay Oficial",
        "direccion": "Montevideo, Uruguay",
        "sitio_oficial": "https://ev.servicioti.com.uy",
        "instagram_handle": "@trikeuruguay",
        "instagram_url": "https://www.instagram.com/trikeuruguay/"
    }
]

def obtener_imagen_de_wikimedia(title: str, max_size=320) -> Image.Image:
    try:
        api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&iiurlwidth={max_size}&format=json"
        req = urllib.request.Request(api_url, headers={'User-Agent': WIKI_AGENT})
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        pages = data.get('query', {}).get('pages', {})
        for pid, pdata in pages.items():
            imginfo = pdata.get('imageinfo', [])
            if imginfo:
                thumb_url = imginfo[0].get('thumburl') or imginfo[0].get('url')
                img_req = urllib.request.Request(thumb_url, headers={'User-Agent': WIKI_AGENT})
                img_data = urllib.request.urlopen(img_req, timeout=10).read()
                return Image.open(io.BytesIO(img_data))
    except Exception as e:
        print(f"    [WIKI LOGO ERROR] {title}: {e}")
    return None

def crear_logo_tipografico_elegante(nombre: str, subtexto: str = "URUGUAY") -> Image.Image:
    """Genera una insignia tipográfica sobria y nítida si no hay SVG disponible."""
    size = (320, 320)
    canvas = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Círculo contenedor con suave bisel
    draw.ellipse((8, 8, 312, 312), fill=(248, 250, 252, 255), outline=(226, 232, 240, 255), width=4)
    draw.ellipse((16, 16, 304, 304), outline=(15, 23, 42, 18), width=2)

    # Iniciales grandes o nombre abreviado
    initials = "".join([w[0].upper() for w in nombre.split() if w.isalnum()])[:3]
    if len(initials) == 0: initials = "EV"

    # Intentar cargar fuentes o usar default con dibujo geométrico
    draw.rectangle((60, 150, 260, 153), fill=(16, 185, 129, 255)) # Línea esmeralda EV
    
    # Dibujar texto centrado usando draw.text
    draw.text((160, 100), initials, fill=(15, 23, 42, 255), anchor="mm")
    draw.text((160, 185), nombre[:14].upper(), fill=(51, 65, 85, 255), anchor="mm")
    draw.text((160, 215), subtexto, fill=(16, 185, 129, 255), anchor="mm")
    
    return canvas

def procesar_y_guardar_logo(img_raw: Image.Image, brand_id: str, brand_name: str) -> Path:
    target_size = (180, 180)
    canvas = Image.new("RGBA", target_size, (255, 255, 255, 0))
    
    # Redimensionar conservando proporción dentro de 150x150
    img_rgba = img_raw.convert("RGBA")
    ancho_max, alto_max = 148, 148
    ratio = min(ancho_max / float(img_rgba.width), alto_max / float(img_rgba.height))
    nw = max(10, int(img_rgba.width * ratio))
    nh = max(10, int(img_rgba.height * ratio))
    scaled = img_rgba.resize((nw, nh), Image.Resampling.LANCZOS)
    
    pos_x = (target_size[0] - nw) // 2
    pos_y = (target_size[1] - nh) // 2
    canvas.paste(scaled, (pos_x, pos_y), scaled)
    
    out_file = LOGOS_DIR / f"{brand_id}-logo.webp"
    temp_file = LOGOS_DIR / f"temp_{brand_id}.png"
    canvas.save(temp_file, format="PNG")
    
    MetadataImageService.inyectar_y_optimizar(
        temp_file,
        titulo=f"Logo Oficial {brand_name} Uruguay",
        descripcion=f"Logotipo oficial representativo de {brand_name} en Uruguay. Catálogo oficial ServicioTI.",
        calidad=90,
        destino=out_file,
        formato="WEBP"
    )
    if temp_file.exists():
        temp_file.unlink()
        
    return out_file

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla brand_profiles si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brand_profiles (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            marcas_json TEXT,
            importador_oficial TEXT,
            direccion TEXT,
            sitio_oficial TEXT,
            instagram_handle TEXT,
            instagram_url TEXT,
            logo_path TEXT,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    print(f"Iniciando cosecha y generación de logos para {len(BRAND_DEFINITIONS)} marcas...")

    for b in BRAND_DEFINITIONS:
        bid = b["id"]
        bname = b["nombre"]
        print(f"\nProcesando marca: {bname} ({bid})")
        
        img = None
        # 1. Intentar logo directo
        if "logo_source_url" in b:
            try:
                print(f"  Descargando logo directo: {b['logo_source_url']}")
                req = urllib.request.Request(b["logo_source_url"], headers=HEADERS)
                resp = urllib.request.urlopen(req, timeout=10)
                img = Image.open(io.BytesIO(resp.read()))
            except Exception as e:
                print(f"  [AVISO] No se pudo descargar logo directo: {e}")
        
        # 2. Intentar Wikimedia SVG
        if img is None and "wiki_logo_title" in b:
            print(f"  Descargando logo de Wikimedia: {b['wiki_logo_title']}")
            img = obtener_imagen_de_wikimedia(b["wiki_logo_title"], max_size=320)
            
        # 3. Fallback a diseño tipográfico nítido
        if img is None:
            print(f"  Generando insignia institucional nítida para {bname}")
            img = crear_logo_tipografico_elegante(bname.replace(" Uruguay", ""))

        logo_path = procesar_y_guardar_logo(img, bid, bname)
        rel_logo_path = f"assets/img/logos/{bid}-logo.webp"
        print(f"  -> Logo guardado y optimizado en: {rel_logo_path}")

        # Guardar en base de datos brand_profiles
        cursor.execute("""
            INSERT INTO brand_profiles (
                id, nombre, marcas_json, importador_oficial, direccion, 
                sitio_oficial, instagram_handle, instagram_url, logo_path, fecha_actualizacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                nombre = excluded.nombre,
                marcas_json = excluded.marcas_json,
                importador_oficial = excluded.importador_oficial,
                direccion = excluded.direccion,
                sitio_oficial = excluded.sitio_oficial,
                instagram_handle = excluded.instagram_handle,
                instagram_url = excluded.instagram_url,
                logo_path = excluded.logo_path,
                fecha_actualizacion = CURRENT_TIMESTAMP
        """, (
            bid,
            bname,
            json.dumps(b["marcas_coincidentes"], ensure_ascii=False),
            b.get("importador_oficial", "Distribuidor Autorizado"),
            b.get("direccion", "Montevideo, Uruguay"),
            b.get("sitio_oficial", "https://ev.servicioti.com.uy"),
            b.get("instagram_handle", ""),
            b.get("instagram_url", ""),
            rel_logo_path
        ))

    conn.commit()
    conn.close()
    print("\n[OK] Base de datos brand_profiles y todos los logos creados exitosamente.")

if __name__ == "__main__":
    main()
