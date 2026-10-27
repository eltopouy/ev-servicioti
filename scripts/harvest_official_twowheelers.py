import os
import sys
import io
import json
import sqlite3
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
from metadata_image_service import MetadataImageService

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_bytes(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def process_studio_image(img_bytes, target_width=1200, target_height=900, bg_color=(245, 245, 247)):
    """Convierte la imagen a estudio centrado con fondo profesional."""
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    
    # Redimensionar conservando proporción para que entre dentro del lienzo con un margen
    max_w = int(target_width * 0.88)
    max_h = int(target_height * 0.88)
    
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    
    # Crear lienzo de estudio
    studio = Image.new("RGBA", (target_width, target_height), (*bg_color, 255))
    
    # Centrar imagen
    offset_x = (target_width - img.width) // 2
    offset_y = (target_height - img.height) // 2
    
    studio.paste(img, (offset_x, offset_y), img)
    return studio.convert("RGB")

def create_official_placeholder(marca, modelo, logo_path=None, target_width=1200, target_height=900):
    """Crea un placeholder de estudio elegante con el logo de la marca cuando la foto oficial está en verificación."""
    canvas = Image.new("RGB", (target_width, target_height), (245, 245, 247))
    draw = ImageDraw.Draw(canvas)
    
    # Dibujar marco sutil
    draw.rectangle([(20, 20), (target_width - 20, target_height - 20)], outline=(220, 220, 225), width=2)
    
    # Si existe logo de la marca, pegarlo
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((320, 160), Image.Resampling.LANCZOS)
            offset_x = (target_width - logo.width) // 2
            offset_y = target_height // 2 - 120
            canvas.paste(logo, (offset_x, offset_y), logo)
        except Exception:
            pass

    # Textos informativos
    title_text = f"{marca.upper()} {modelo.upper()}"
    subtitle_text = "FOTOGRAFÍA OFICIAL EN PROCESO DE VERIFICACIÓN TÉCNICA"
    sub_sub = "Homologación y catálogo en plaza Uruguay · EV ServicioTI"
    
    # Usar fuente por defecto
    draw.text((target_width // 2, target_height // 2 + 80), title_text, fill=(30, 30, 30), anchor="mm")
    draw.text((target_width // 2, target_height // 2 + 120), subtitle_text, fill=(100, 100, 100), anchor="mm")
    draw.text((target_width // 2, target_height // 2 + 150), sub_sub, fill=(140, 140, 140), anchor="mm")
    
    return canvas

def make_badge(img, out_path, size=256):
    """Crea miniatura circular badge."""
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    cropped = img.crop((left, top, left + min_dim, top + min_dim))
    cropped = cropped.resize((size, size), Image.Resampling.LANCZOS)
    cropped.save(out_path, "WEBP", quality=85)

# Tareas de Cosecha Oficial Verificada
OFFICIAL_TASKS = {
    # SUNRA URUGUAY (sunra.com.uy)
    "sunra-miku-super": {
        "marca": "Sunra",
        "modelo": "Miku Super",
        "oficial_url": "https://sunra.com.uy/moto-electrica-miku-super/",
        "source_hero_url": "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_MIKU_SUPER_IMG-4.jpg",
        "gallery_sources": [
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_MIKU_SUPER_IMG-4.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_MIKU_SUPER_IMG-2.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_MIKU_SUPER_TRIADA1.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_MIKU_SUPER_TRIADA2.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_MIKU_SUPER_TRIADA3.jpg"
        ]
    },
    "sunra-cargo-triciclo": {
        "marca": "Sunra",
        "modelo": "Cargo King",
        "oficial_url": "https://sunra.com.uy/moto-eletrica-cargo-king-kong/",
        "source_hero_url": "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_KINGKONG_IMG-4.jpg",
        "gallery_sources": [
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_KINGKONG_IMG-4.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_KINGKONG_2_IMG-2.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_KINGKONG_2_TRIADA1.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_KINGKONG_2_TRIADA2.jpg",
            "https://sunra.com.uy/wp-content/uploads/2026/02/SUNRA_KINGKONG_2_TRIADA3.jpg"
        ]
    },
    
    # VOLTBIKE (voltbike.uy - Shopify CDN)
    "voltbike-classica": {
        "marca": "VoltBike",
        "modelo": "Classica",
        "oficial_url": "https://voltbike.uy/products/clasica",
        "source_hero_url": "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/Clasica1b.jpg?v=1765325725",
        "gallery_sources": [
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/Clasica1b.jpg?v=1765325725",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/Clasica1.jpg?v=1765325725"
        ]
    },
    "voltbike-flex-foldable": {
        "marca": "VoltBike",
        "modelo": "Flex",
        "oficial_url": "https://voltbike.uy/products/flex",
        "source_hero_url": "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/flexblanca.png?v=1786473344",
        "gallery_sources": [
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/flexblanca.png?v=1786473344",
            "https://cdn.shopify.com/s/files/1/0792/0831/7146/files/flexnegra.png?v=1786473344"
        ]
    },

    # LOOP BIKES (shop.loop-bikes.com - Shopify CDN)
    "loop-bikes-slim-pro": {
        "marca": "Loop Bikes",
        "modelo": "Slim Pro",
        "oficial_url": "https://shop.loop-bikes.com/products/loop-slim-pro",
        "source_hero_url": "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/verde.jpg?v=1791382684",
        "gallery_sources": [
            "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/verde.jpg?v=1791382684",
            "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/negra.jpg?v=1791382684"
        ]
    },
    "loop-bikes-soda-bike": {
        "marca": "Loop Bikes",
        "modelo": "Soda Bike",
        "oficial_url": "https://shop.loop-bikes.com/products/soda-bike",
        "source_hero_url": "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/soda-bike-sand-bicicleta-electrica-portada_284b2a75-52fe-43a6-9379-ca2ce6a3e0a9.jpg?v=1742824586",
        "gallery_sources": [
            "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/soda-bike-sand-bicicleta-electrica-portada_284b2a75-52fe-43a6-9379-ca2ce6a3e0a9.jpg?v=1742824586",
            "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/IMG-4006.jpg?v=1742834952"
        ]
    },
    "loop-bikes-classic": {
        "marca": "Loop Bikes",
        "modelo": "Classic / Cruiser",
        "oficial_url": "https://shop.loop-bikes.com/products/loop-bikes-cruiser",
        "source_hero_url": "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/Loop_Cuiser_Copper_2.jpg?v=1769802802",
        "gallery_sources": [
            "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/Loop_Cuiser_Copper_2.jpg?v=1769802802",
            "https://cdn.shopify.com/s/files/1/0593/1856/7084/files/Loop_Cuiser_Grey_1.jpg?v=1769803272"
        ]
    },

    # YADEA URUGUAY (motosyadea.com.uy)
    "yadea-g5-pro": {
        "marca": "Yadea",
        "modelo": "G5",
        "oficial_url": "https://motosyadea.com.uy",
        "source_hero_url": "https://motosyadea.com.uy/yadea/modelo_g5.jpg",
        "gallery_sources": [
            "https://motosyadea.com.uy/yadea/modelo_g5.jpg",
            "https://motosyadea.com.uy/yadea/yadea1.jpg"
        ]
    },
    "yadea-c-umi": {
        "marca": "Yadea",
        "modelo": "C-Umi",
        "oficial_url": "https://motosyadea.com.uy",
        "source_hero_url": "https://motosyadea.com.uy/yadea/modelo1.jpg",
        "gallery_sources": [
            "https://motosyadea.com.uy/yadea/modelo1.jpg",
            "https://motosyadea.com.uy/yadea/yadea3.jpg"
        ]
    }
}

# Modelos en Cuarentena (No listados actualmente en los portales activos del importador)
UNVERIFIED_MODELS = [
    {
        "id": "sunra-hawk-3000",
        "marca": "Sunra",
        "modelo": "Hawk 3000W",
        "motivo": "Modelo no listado en el catálogo activo de sunra.com.uy (discontinuado o fuera de stock en plaza)",
        "url_monitoreada": "https://sunra.com.uy",
        "fecha": "2026-10-27"
    },
    {
        "id": "sunra-grace-1800",
        "marca": "Sunra",
        "modelo": "Grace 1800W",
        "motivo": "Modelo no listado en el catálogo activo de sunra.com.uy (discontinuado o fuera de stock en plaza)",
        "url_monitoreada": "https://sunra.com.uy",
        "fecha": "2026-10-27"
    },
    {
        "id": "sunra-robo-s",
        "marca": "Sunra",
        "modelo": "Robo-S",
        "motivo": "Modelo no listado en el catálogo activo de sunra.com.uy (discontinuado o fuera de stock en plaza)",
        "url_monitoreada": "https://sunra.com.uy",
        "fecha": "2026-10-27"
    }
]

def main():
    conn = sqlite3.connect('data/ev_uruguay.db')
    c = conn.cursor()

    # 1. Procesar tareas oficiales verificadas
    for vid, task in OFFICIAL_TASKS.items():
        print(f"\n[COSECHA OFICIAL] Procesando {task['marca']} {task['modelo']} ({vid})...")
        out_dir = os.path.join("assets", "img", vid)
        os.makedirs(out_dir, exist_ok=True)
        
        # Descargar hero image
        try:
            hero_bytes = download_bytes(task['source_hero_url'])
            studio_hero = process_studio_image(hero_bytes)
            hero_filename = f"01-vista-isometrica-frontal-3-4-{vid}-ev-servicioti-uruguay.webp"
            hero_relpath = f"assets/img/{vid}/{hero_filename}"
            hero_abspath = os.path.join(out_dir, hero_filename)
            
            studio_hero.save(hero_abspath, "WEBP", quality=88)
            MetadataImageService.inyectar_y_optimizar(
                Path(hero_abspath),
                titulo=f"{task['marca']} {task['modelo']} - Vehículo Eléctrico Oficial en Uruguay",
                descripcion=f"Fotografía oficial de estudio de {task['marca']} {task['modelo']} extraída del importador oficial para EV Uruguay.",
                calidad=88
            )
            print(f"  [OK] Hero oficial guardado: {hero_abspath}")

            # Badge
            badge_filename = f"badge-circular-{vid}-ev-servicioti-uruguay.webp"
            badge_abspath = os.path.join(out_dir, badge_filename)
            make_badge(studio_hero, badge_abspath)
            MetadataImageService.inyectar_y_optimizar(
                Path(badge_abspath),
                titulo=f"Badge {task['marca']} {task['modelo']}",
                descripcion="Badge Oficial ServicioTI",
                calidad=85
            )

            # Procesar galería
            galeria_paths = [hero_relpath]
            for idx, g_url in enumerate(task['gallery_sources'][1:], start=2):
                try:
                    g_bytes = download_bytes(g_url)
                    g_img = process_studio_image(g_bytes)
                    g_name = f"0{idx}-detalle-vista-{vid}-ev-servicioti-uruguay.webp"
                    g_path = os.path.join(out_dir, g_name)
                    g_img.save(g_path, "WEBP", quality=88)
                    MetadataImageService.inyectar_y_optimizar(
                        Path(g_path),
                        titulo=f"{task['marca']} Detalle {idx}",
                        descripcion="Fotografía Oficial",
                        calidad=88
                    )
                    galeria_paths.append(f"assets/img/{vid}/{g_name}")
                except Exception as ge:
                    print(f"  [WARN] Error en galería {g_url}: {ge}")

            # Actualizar DB
            c.execute("""
                UPDATE vehicles 
                SET imagen_oficial_url = ?, galeria_json = ?, link_fabricante = ?
                WHERE id = ?
            """, (hero_relpath, json.dumps(galeria_paths), task['oficial_url'], vid))
            print(f"  [OK] Base de datos actualizada para {vid}")
            
        except Exception as e:
            print(f"  [ERROR] Error cosechando {vid}: {e}")

    # 2. Procesar modelos en Cuarentena (Placeholder con logo oficial y registro en log)
    sunra_logo = "assets/img/logos_marcas/sunra.webp"
    for unv in UNVERIFIED_MODELS:
        vid = unv['id']
        print(f"\n[POLÍTICA CUARENTENA] Aplicando placeholder oficial a {unv['marca']} {unv['modelo']} ({vid})...")
        out_dir = os.path.join("assets", "img", vid)
        os.makedirs(out_dir, exist_ok=True)
        
        placeholder = create_official_placeholder(unv['marca'], unv['modelo'], logo_path=sunra_logo)
        hero_filename = f"01-vista-isometrica-frontal-3-4-{vid}-ev-servicioti-uruguay.webp"
        hero_relpath = f"assets/img/{vid}/{hero_filename}"
        hero_abspath = os.path.join(out_dir, hero_filename)
        
        placeholder.save(hero_abspath, "WEBP", quality=88)
        MetadataImageService.inyectar_y_optimizar(
            Path(hero_abspath),
            titulo=f"{unv['marca']} {unv['modelo']} - Fotografía Oficial en Verificación Técnica",
            descripcion=f"Registro oficial homologado en EV Uruguay. Fotografía del fabricante en proceso de verificación.",
            calidad=88
        )
        
        badge_filename = f"badge-circular-{vid}-ev-servicioti-uruguay.webp"
        badge_abspath = os.path.join(out_dir, badge_filename)
        make_badge(placeholder, badge_abspath)
        MetadataImageService.inyectar_y_optimizar(
            Path(badge_abspath),
            titulo=f"Badge {unv['marca']}",
            descripcion="Badge Oficial ServicioTI",
            calidad=85
        )

        # Galería con placeholder
        galeria_paths = [hero_relpath]
        c.execute("""
            UPDATE vehicles 
            SET imagen_oficial_url = ?, galeria_json = ?
            WHERE id = ?
        """, (hero_relpath, json.dumps(galeria_paths), vid))
        print(f"  [OK] Cuarentena aplicada a {vid} (eliminadas fotos no oficiales de Bing)")

    conn.commit()
    conn.close()

    # 3. Guardar log estructurado de auditoría
    with open('data/missing_official_images.json', 'w', encoding='utf-8') as f:
        json.dump(UNVERIFIED_MODELS, f, indent=2, ensure_ascii=False)
    print("\n✔ Log de pendientes guardado en data/missing_official_images.json")

    # 4. Sincronizar feeds estáticos
    print("\nSincronizando feeds ev_data.json y ev_data.js...")
    os.system("python scripts/export_to_json.py")
    print("✔ Feeds sincronizados.")

if __name__ == '__main__':
    main()
