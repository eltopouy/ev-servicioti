# -*- coding: utf-8 -*-
"""
Publicador y Sincronizador de Crónicas Editoriales en Blogger (servicioti.com.uy)
Proyecto: EV Uruguay (https://ev.servicioti.com.uy)
Autor: Andrés Franchi Ugartemendía (ServicioTI)
Blog ID: 8220787747664379807 (https://www.servicioti.com.uy)

Publica las 6 crónicas completas con formato editorial enriquecido en Blogger
y crea/actualiza la página estática centralizadora 'Movilidad Eléctrica Uruguay'.
Actualiza las URLs en SQLite y ev_data.js para monetización con Google AdSense.
"""

import sys
import os
import json
import sqlite3
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"
SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '8220787747664379807'
TOKEN_PATH = Path("C:/Users/Andrés/.gemini/antigravity/scratch/seo_blogger_automation/token.json")

# Artículos Editoriales Extensos y Enriquecidos para Blogger
CRONICAS_EDITORIALES = [
    {
        "id": "cronica-byd-liderazgo-2026",
        "titulo": "BYD consolida su liderazgo en Uruguay: el Seagull encabeza las ventas de vehículos 100% eléctricos",
        "labels": ["Movilidad Eléctrica", "BYD", "Autos Eléctricos Uruguay", "ServicioTI"],
        "slug": "byd-seagull-liderazgo-autos-electricos-uruguay",
        "html": """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8; font-size: 16px;">
    <p style="font-size: 18px; color: #475569; font-weight: 500;">
        El mercado uruguayo de vehículos livianos atraviesa una transformación histórica: más del 15% de los empadronamientos totales de cero kilómetros ya corresponden a modelos 100% eléctricos a batería (BEV), liderados contundentemente por la gama Ocean de BYD a través de su representante oficial SADAR S.A.
    </p>

    <div style="background: #f8fafc; border-left: 4px solid #0284c7; padding: 18px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <h4 style="margin: 0 0 8px 0; color: #0369a1; font-size: 17px;">📌 Cifras Clave del Mercado Uruguayo (ACAU / SUCIVE 2026)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #334155;">
            <li><strong>Líder absoluto:</strong> BYD Seagull (versiones EV300, EV400 GS y Surf) con más de 2.060 unidades registradas.</li>
            <li><strong>SUV más vendido:</strong> BYD Yuan Pro EV 380 con 3.362 unidades empadronadas.</li>
            <li><strong>Tecnología:</strong> Celdas Blade LFP (Fosfato de Hierro y Litio) integradas estructuralmente (Cell-to-Body).</li>
            <li><strong>Costo por kilómetro:</strong> Aproximadamente $0,45 UYU/km cargando en Tarifa Inteligente de UTE (Valle), frente a más de $7,20 UYU/km en un naftero equivalente.</li>
        </ul>
    </div>

    <h3 style="color: #0f172a; margin-top: 30px; font-size: 22px;">La fórmula del éxito urbano: Autonomía real y seguridad estructural</h3>
    <p>
        El BYD Seagull ha captado al comprador uruguayo tanto para uso particular como para movilidad profesional y flotas de servicios. Su arquitectura sobre la e-Platform 3.0 entrega una distancia entre ejes optimizada de 2.500 mm que brinda una habitabilidad propia de un segmento superior, manteniendo unas dimensiones exteriores compactas ideales para circular y estacionar en Ciudad Vieja, Pocitos o el Centro de Montevideo.
    </p>
    <p>
        En materia de almacenamiento, las baterías Blade LiFePO4 de FinDreams ofrecen la máxima tranquilidad contra eventos térmicos o perforaciones, permitiendo cargas habituales al 100% sin degradación acelerada y garantizando 8 años o 500.000 km de respaldo oficial en los centros autorizados de SADAR.
    </p>

    <div style="text-align: center; margin: 35px 0;">
        <a href="https://ev.servicioti.com.uy" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #0f172a; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: 700; font-size: 15px; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(15,23,42,0.25);">
            ⚡ Ver Ficha Técnica Completa y Costos en EV Uruguay (ev.servicioti.com.uy) →
        </a>
    </div>

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;" />
    <p style="font-size: 13px; color: #64748b;">
        <em>Publicación editorial elaborada por Andrés Franchi Ugartemendía para el ecosistema ServicioTI. Datos oficiales homologados ante URSEA, SUCIVE y ACAU.</em>
    </p>
</div>
"""
    },
    {
        "id": "cronica-chevrolet-ultium-uruguay",
        "titulo": "General Motors desembarca con su arquitectura Ultium: Blazer EV y Equinox EV aceleran la plaza uruguaya",
        "labels": ["Movilidad Eléctrica", "Chevrolet", "Autos Eléctricos Uruguay", "ServicioTI"],
        "slug": "chevrolet-ultium-blazer-ev-equinox-uruguay",
        "html": """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8; font-size: 16px;">
    <p style="font-size: 18px; color: #475569; font-weight: 500;">
        General Motors Uruguay ha puesto en marcha su mayor ofensiva tecnológica hasta la fecha: el despliegue comercial de sus SUVs eléctricos de última generación sobre la plataforma modular Ultium, integrando las nuevas Blazer EV y Equinox EV en la red oficial de concesionarios.
    </p>

    <div style="background: #f8fafc; border-left: 4px solid #b45309; padding: 18px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <h4 style="margin: 0 0 8px 0; color: #92400e; font-size: 17px;">⚡ Arquitectura Ultium en Números</h4>
        <ul style="margin: 0; padding-left: 20px; color: #334155;">
            <li><strong>Capacidad de batería:</strong> Packs de 85 kWh a 102 kWh útiles con química NCMA de baja proporción de cobalto.</li>
            <li><strong>Potencia máxima:</strong> Hasta 565 CV en modo Wide Open Watts (WOW) con tracción integral e-AWD.</li>
            <li><strong>Autonomía en ruta:</strong> Más de 480 km reales en ciclo mixto uruguayo.</li>
            <li><strong>Carga ultrarrápida:</strong> Soporte de corriente continua (DC) hasta 190 kW, permitiendo recuperar 120 km en apenas 10 minutos.</li>
        </ul>
    </div>

    <h3 style="color: #0f172a; margin-top: 30px; font-size: 22px;">Innovación inalámbrica en la gestión de batería (wBMS)</h3>
    <p>
        Uno de los hitos tecnológicos más relevantes que General Motors introduce en Uruguay con Ultium es su sistema inalámbrico de gestión de batería (wBMS). Al eliminar el 90% de los cables internos del pack, se reducen puntos potenciales de fricción o falla, se optimiza la distribución de peso y se facilita la reparación o reutilización de módulos individuales a lo largo de los años.
    </p>

    <div style="text-align: center; margin: 35px 0;">
        <a href="https://ev.servicioti.com.uy" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #0f172a; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: 700; font-size: 15px; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(15,23,42,0.25);">
            ⚡ Consultar Especificaciones de Chevrolet Ultium en EV Uruguay →
        </a>
    </div>

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;" />
    <p style="font-size: 13px; color: #64748b;">
        <em>Informe técnico oficial ServicioTI · Cobertura de movilidad cero emisiones en Uruguay.</em>
    </p>
</div>
"""
    },
    {
        "id": "cronica-volvo-ex30-uruguay",
        "titulo": "Volvo EX30: anatomía del SUV compacto de lujo que batió récords de matriculación en Uruguay",
        "labels": ["Movilidad Eléctrica", "Volvo", "Autos Eléctricos Uruguay", "ServicioTI"],
        "slug": "volvo-ex30-anatomia-suv-compacto-uruguay",
        "html": """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8; font-size: 16px;">
    <p style="font-size: 18px; color: #475569; font-weight: 500;">
        Importado por Danissa S.A. y comercializado a través de su red oficial en Montevideo y Car One, el Volvo EX30 se ha transformado en el vehículo eléctrico premium más vendido del país, combinando la huella de carbono más reducida en la historia del fabricante sueco con prestaciones de superdeportivo.
    </p>

    <div style="background: #f8fafc; border-left: 4px solid #10b981; padding: 18px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <h4 style="margin: 0 0 8px 0; color: #065f46; font-size: 17px;">📊 Ficha Técnica Destacada (Versiones Uruguay)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #334155;">
            <li><strong>Single Motor Extended Range:</strong> 272 CV, batería NMC de 69 kWh, 476 km de autonomía homologada URSEA.</li>
            <li><strong>Twin Motor Performance Ultra:</strong> 428 CV, tracción integral AWD, 0 a 100 km/h en 3,6 segundos.</li>
            <li><strong>Sustentabilidad:</strong> 25% de aluminio reciclado, 17% de acero reciclado y tapizados en materiales biológicos nórdicos.</li>
        </ul>
    </div>

    <div style="text-align: center; margin: 35px 0;">
        <a href="https://ev.servicioti.com.uy" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #0f172a; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: 700; font-size: 15px; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(15,23,42,0.25);">
            ⚡ Ver Prueba, Galería 4:5 y Simulador TCO del Volvo EX30 →
        </a>
    </div>

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;" />
    <p style="font-size: 13px; color: #64748b;">
        <em>Análisis de mercado realizado por Andrés Franchi Ugartemendía para ServicioTI.</em>
    </p>
</div>
"""
    },
    {
        "id": "cronica-red-ute-mueve-expansion",
        "titulo": "La Red UTE Mueve expande sus cargadores ultrarrápidos de corriente continua a todo el país",
        "labels": ["Movilidad Eléctrica", "UTE Mueve", "Infraestructura Uruguay", "ServicioTI"],
        "slug": "red-ute-mueve-cargadores-ultrarrapidos-uruguay",
        "html": """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8; font-size: 16px;">
    <p style="font-size: 18px; color: #475569; font-weight: 500;">
        Con más de 300 puntos de carga operativos a lo largo de las rutas nacionales 1, 2, 3, 5, 8, 9 e Interbalnearia, la empresa estatal UTE consolida una de las redes de carga pública más densas de América Latina por habitante, garantizando un punto de recarga cada menos de 60 kilómetros.
    </p>

    <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 18px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <h4 style="margin: 0 0 8px 0; color: #1e40af; font-size: 17px;">🔌 Puntos Clave de la Red UTE Mueve</h4>
        <ul style="margin: 0; padding-left: 20px; color: #334155;">
            <li><strong>Conectores estándar:</strong> GB/T (dominante en vehículos asiáticos) y CCS2 (estándar europeo/norteamericano) con potencias de 50 kW a 120 kW en corriente continua.</li>
            <li><strong>Gestión móvil:</strong> Activación y cobro instantáneo mediante la aplicación móvil UTE Mueve y tarjeta RFID interoperable.</li>
            <li><strong>Tarifa oficial de ruta:</strong> $11,80 UYU por kWh en postes DC de alta velocidad.</li>
        </ul>
    </div>

    <div style="text-align: center; margin: 35px 0;">
        <a href="https://ev.servicioti.com.uy" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #0f172a; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: 700; font-size: 15px; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(15,23,42,0.25);">
            ⚡ Consultar el Mapa Interactivo de Cargadores UTE Mueve en EV Uruguay →
        </a>
    </div>

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;" />
    <p style="font-size: 13px; color: #64748b;">
        <em>Informe técnico oficial de infraestructura eléctrica ServicioTI.</em>
    </p>
</div>
"""
    },
    {
        "id": "cronica-micromovilidad-ebikes-motos",
        "titulo": "Revolución urbana sobre dos ruedas: e-bikes de ingeniería nacional y scooters lideran la movilidad diaria",
        "labels": ["Movilidad Eléctrica", "Micromovilidad", "E-Bikes Uruguay", "ServicioTI"],
        "slug": "micromovilidad-ebikes-motos-electricas-uruguay",
        "html": """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8; font-size: 16px;">
    <p style="font-size: 18px; color: #475569; font-weight: 500;">
        La Rambla de Montevideo y las principales avenidas del interior han adoptado masivamente las bicicletas asistidas y motocicletas 100% eléctricas. Empresas nacionales como Loop Bikes y VoltBike, junto a referentes globales como Sunra y Yadea, han demostrado que la transición ecológica es accesible y enormemente rentable para el traslado diario.
    </p>

    <div style="background: #f8fafc; border-left: 4px solid #84cc16; padding: 18px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <h4 style="margin: 0 0 8px 0; color: #4d7c0f; font-size: 17px;">🚲 Ventajas Económicas en la Ciudad</h4>
        <ul style="margin: 0; padding-left: 20px; color: #334155;">
            <li><strong>Costo de carga:</strong> Menos de $15 UYU por recarga completa de batería (40 a 70 km de autonomía).</li>
            <li><strong>Mantenimiento:</strong> Ausencia total de aceites, bujías, correas de transmisión y embragues.</li>
            <li><strong>Portabilidad:</strong> Baterías extraíbles de iones de litio recargables en cualquier enchufe doméstico Schuko de 220V.</li>
        </ul>
    </div>

    <div style="text-align: center; margin: 35px 0;">
        <a href="https://ev.servicioti.com.uy" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #0f172a; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: 700; font-size: 15px; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(15,23,42,0.25);">
            ⚡ Explorar el Catálogo Homologado de E-Bikes y Motos en EV Uruguay →
        </a>
    </div>

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;" />
    <p style="font-size: 13px; color: #64748b;">
        <em>Relevamiento de micromovilidad urbana · ServicioTI / Andrés Franchi Ugartemendía.</em>
    </p>
</div>
"""
    },
    {
        "id": "cronica-beneficios-fiscales-sucive",
        "titulo": "Régimen fiscal y exoneración de patente SUCIVE: el beneficio económico de pasarse a cero emisiones",
        "labels": ["Movilidad Eléctrica", "Economía Uruguay", "SUCIVE Patente", "ServicioTI"],
        "slug": "beneficios-fiscales-exoneracion-patente-sucive-autos-electricos",
        "html": """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8; font-size: 16px;">
    <p style="font-size: 18px; color: #475569; font-weight: 500;">
        Uruguay cuenta con uno de los marcos de incentivos fiscales más favorables de la región para la adquisición y posesión de vehículos 100% eléctricos a batería. Analizamos los beneficios tributarios directos fijados por el Congreso de Intendentes (SUCIVE), la DGI y el Ministerio de Economía y Finanzas (MEF).
    </p>

    <div style="background: #f8fafc; border-left: 4px solid #6366f1; padding: 18px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <h4 style="margin: 0 0 8px 0; color: #4338ca; font-size: 17px;">📋 Paquete de Exoneraciones e Incentivos</h4>
        <ul style="margin: 0; padding-left: 20px; color: #334155;">
            <li><strong>Patente de Rodados SUCIVE:</strong> Alícuota reducida del 3% sobre el valor de mercado sin IVA (con hasta un 50% de bonificación en los primeros años según departamento).</li>
            <li><strong>IMESI (Impuesto Específico Interno):</strong> Tasa del 0% para vehículos de pasajeros 100% eléctricos, frente a tasas del 23% al 46% en motores a nafta.</li>
            <li><strong>Incentivos COMAP (Empresas):</strong> Desgravación de IRAE mediante proyectos de inversión orientados a la descarbonización de flotas comerciales.</li>
            <li><strong>Bonificación Verde en Seguros (BSE):</strong> 15% de descuento en la prima de pólizas Todo Riesgo del Banco de Seguros del Estado.</li>
        </ul>
    </div>

    <div style="text-align: center; margin: 35px 0;">
        <a href="https://ev.servicioti.com.uy" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #0f172a; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: 700; font-size: 15px; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(15,23,42,0.25);">
            ⚡ Calcular Patente y Costo Total de Propiedad en el Simulador EV Uruguay →
        </a>
    </div>

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;" />
    <p style="font-size: 13px; color: #64748b;">
        <em>Guía tributaria y normativa oficial ServicioTI / Andrés Franchi Ugartemendía.</em>
    </p>
</div>
"""
    }
]

def publish_all_cronicas_to_blogger():
    print("=====================================================================")
    print("📢 PUBLICADOR OFICIAL DE CRÓNICAS EV URUGUAY EN BLOGGER (servicioti.com.uy)")
    print("   Blog ID: 8220787747664379807")
    print("=====================================================================\n")

    if not TOKEN_PATH.exists():
        print(f"❌ Error: No se encontró el token de autenticación en {TOKEN_PATH}")
        return False

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    # 1. Obtener entradas existentes para evitar duplicación
    print("1. Consultando entradas existentes en Blogger...")
    existing_posts = service.posts().list(
        blogId=BLOG_ID,
        maxResults=100,
        fetchBodies=False,
        fields="items(id,title,url)"
    ).execute().get("items", [])
    
    title_to_post = {p["title"].strip().lower(): p for p in existing_posts}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    published_urls = {}

    print(f"\n2. Procesando {len(CRONICAS_EDITORIALES)} crónicas editoriales...")
    for item in CRONICAS_EDITORIALES:
        t_key = item["titulo"].strip().lower()
        matched = title_to_post.get(t_key)

        post_body = {
            "kind": "blogger#post",
            "title": item["titulo"],
            "content": item["html"],
            "labels": item["labels"]
        }

        if matched:
            post_id = matched["id"]
            post_url = matched["url"]
            print(f"  ↻ Actualizando entrada existente: '{item['titulo'][:45]}...'")
            service.posts().patch(blogId=BLOG_ID, postId=post_id, body=post_body).execute()
        else:
            print(f"  ✚ Creando nueva entrada en Blogger: '{item['titulo'][:45]}...'")
            new_p = service.posts().insert(blogId=BLOG_ID, body=post_body, isDraft=False).execute()
            post_id = new_p["id"]
            post_url = new_p["url"]

        published_urls[item["id"]] = post_url
        print(f"    ✔ URL oficial Blogger: {post_url}")

        # Actualizar URL y contenido en la base de datos local SQLite
        cursor.execute("""
            UPDATE news_articles 
            SET url = ?, contenido_html = ?
            WHERE id = ?
        """, (post_url, item["html"], item["id"]))

    conn.commit()

    # 3. Crear o actualizar la Página Estática en Blogger: "Movilidad Eléctrica Uruguay"
    print("\n3. Creando / Actualizando Página Estática Centralizadora en Blogger...")
    pages_res = service.pages().list(blogId=BLOG_ID).execute().get("items", [])
    page_title = "Movilidad Eléctrica Uruguay: Crónicas, Ensayos y Directorio 100% Eléctricos | EV ServicioTI"
    
    existing_page = None
    for p in pages_res:
        if "movilidad eléctrica" in p.get("title", "").lower() or "ev uruguay" in p.get("title", "").lower():
            existing_page = p
            break

    # Contenido HTML de la página índice centralizadora
    page_html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8;">
    <div style="text-align: center; padding: 25px 15px; background: #0f172a; color: #ffffff; border-radius: 8px; margin-bottom: 30px;">
        <span style="display: inline-block; background: #38bdf8; color: #0f172a; font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">ServicioTI · Revista &amp; Catálogo Oficial</span>
        <h1 style="color: #ffffff; font-size: 26px; margin: 0 0 10px 0; font-weight: 800;">Movilidad Eléctrica en Uruguay</h1>
        <p style="color: #94a3b8; font-size: 15px; margin: 0; max-width: 650px; margin-left: auto; margin-right: auto;">
            Directorio técnico, ensayos especializados, pruebas de manejo y análisis de costos de propiedad para vehículos 100% eléctricos a batería en Uruguay.
        </p>
        <div style="margin-top: 18px;">
            <a href="https://ev.servicioti.com.uy" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #38bdf8; color: #0f172a; padding: 10px 22px; border-radius: 6px; font-weight: 700; text-decoration: none; font-size: 14px;">
                🚀 Acceder al Catálogo Interactivo en Vivo (ev.servicioti.com.uy) →
            </a>
        </div>
    </div>

    <h2 style="color: #0f172a; font-size: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 20px;">
        📰 Crónicas Editoriales &amp; Ensayos de Movilidad
    </h2>
    <div style="display: grid; gap: 20px;">
"""
    for item in CRONICAS_EDITORIALES:
        p_url = published_urls.get(item["id"], "https://www.servicioti.com.uy")
        page_html += f"""
        <div style="border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
            <h3 style="margin: 0 0 10px 0; font-size: 18px;"><a href="{p_url}" style="color: #0284c7; text-decoration: none;">{item['titulo']}</a></h3>
            <p style="color: #475569; font-size: 14px; margin: 0 0 14px 0;">Análisis técnico especializado sobre homologación URSEA, autonomía y costos operativos en plaza uruguaya.</p>
            <a href="{p_url}" style="color: #0f172a; font-weight: 700; font-size: 13px; text-decoration: none; text-transform: uppercase; letter-spacing: 0.5px;">Leer crónica completa en el blog →</a>
        </div>
        """

    page_html += """
    </div>
</div>
"""

    if existing_page:
        print(f"  ↻ Actualizando página estática: '{existing_page['title']}'")
        service.pages().patch(
            blogId=BLOG_ID,
            pageId=existing_page["id"],
            body={"title": page_title, "content": page_html}
        ).execute()
        hub_page_url = existing_page["url"]
    else:
        print(f"  ✚ Creando nueva página estática en Blogger...")
        new_page = service.pages().insert(
            blogId=BLOG_ID,
            body={"kind": "blogger#page", "title": page_title, "content": page_html},
            isDraft=False
        ).execute()
        hub_page_url = new_page["url"]

    print(f"  ✔ Página estática lista en: {hub_page_url}")

    conn.close()

    # 4. Re-exportar JSON y JS estáticos para que index.html tenga las URLs reales de Blogger
    print("\n4. Re-exportando base de datos a ev_data.json y ev_data.js...")
    from export_to_json import export_db_to_json
    export_db_to_json()

    print("\n=====================================================================")
    print("🎉 ¡TODAS LAS CRÓNICAS FUERON PUBLICADAS Y VINCULADAS CON BLOGGER EXITOSAMENTE!")
    print("=====================================================================")
    return published_urls

if __name__ == "__main__":
    publish_all_cronicas_to_blogger()
