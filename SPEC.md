# 📦 EV Uruguay: Revista, Catálogo & Radar de Movilidad Eléctrica

> **Proyecto Antigravity / ServicioTI** | Última actualización: 26/10/2026 | Subdominio Oficial: `https://ev.servicioti.com.uy`

---

## 🏷️ Categoría
Plataforma Editorial Web / Directorio Exhaustivo / Inteligencia de Mercado / Movilidad Sustentable / Scrapers & IA

## 📋 Descripción
Directorio centralizado y radar editorial en tiempo real de más del 98% de la movilidad eléctrica disponible en Uruguay (**93 modelos oficiales**: automóviles, SUVs, pickups, utilitarios, triciclos de carga, motocicletas y bicicletas eléctricas). Conecta fuentes oficiales (URSEA UNIT 1130:2020, SUCIVE, UTE Mueve, ACAU), relevamientos de plaza y concesionarias para seguimiento técnico, precios en USD, homologaciones, fichas de 12 parámetros y galerías de 5 fotos de alta resolución a costo $0, con nombres de archivo SEO descriptivos, sin mención a medios de terceros y con autoría y derechos exclusivos de ServicioTI.

## 🛠️ Tecnologías y Arquitectura
- **Backend / Scrapers:** Python 3.12+, Playwright, BeautifulSoup4, urllib, Pillow, JSON.
- **Base de Datos:** SQLite local (`data/ev_uruguay.db`) con soporte para esquemas JSON de galerías, especificaciones técnicas y tabla histórica `monthly_rankings`.
- **Automatización Mensual de Top Ventas (ACAU / SUCIVE):**
  - Módulo `scripts/sync_acau_rankings.py` que sincroniza los empadronamientos oficiales de vehículos 100% eléctricos.
  - Asignación de rangos `es_top_ventas`, `ventas_rank`, `unidades_anuales` y `periodo_ranking`.
  - Tarea periódica de Windows PowerShell `scripts/tarea_mensual_rankings.ps1` con resiliencia (`-StartWhenAvailable`, `-WakeToRun`) programada para el día 5 de cada mes.
  - Acceso directo `actualizar_ranking_mensual.bat`.
- **Doble Exportación de Datos:**
  - `data/ev_data.json`: Formato estándar para consumo API / frontend online.
  - `data/ev_data.js`: Objeto global `window.EV_DATA` para ejecución local `file:///` sin bloqueos de política CORS.
- **Motor Gráfico & Metadatos SEO (Mobile-First 4:5 + Pixel Art + Badges):**
  - `MetadataImageService`: purga metadatos de cámaras/rutas locales e inyecta UTF-8 XMP + EXIF Unicode de Andrés Franchi Ugartemendía (`https://ev.servicioti.com.uy` / ServicioTI), optimizando cada archivo a WebP ultraligero (< 75 KB).
  - Formato vertical 4:5 (1080x1350 px, estilo Instagram) optimizado para pantallas de smartphones sin barras negras ni cortes. Fondo de estudio editorial blanco/claro con sombra suave de contacto en el piso.
  - 6 vistas completas por modelo (558 fotos):
    1. `01-vista-isometrica-frontal-3-4`: Hero elevado de catálogo / web.
    2. `02-vista-trasera-opticas-porton`: Remate posterior y firma lumínica trasera.
    3. `03-interior-tablero-consola-cockpit`: Cockpit, volante y pantalla flotante.
    4. `04-perfil-lateral-carroceria`: Silueta lateral aerodinámica y batalla.
    5. `05-detalle-bateria-conector-carga`: Puerto de recarga y conector (GB/T / CCS2).
    6. `06-detalle-frontal-firma-luminica`: Firma LED delantera y calandra.
  - Miniaturas Circulares (93 badges): `badge-circular-[slug]-ev-servicioti-uruguay.webp` (128x128 px con borde grafito de revista).
  - Coleccionables Retro Pixel Art (93 sprites): `pixel-art-16bit-[slug]-ev-servicioti-uruguay.webp` (64x64 escalado a 128x128 con Nearest-Neighbor y paleta adaptativa arcade).
  - Total de activos visuales: 744 archivos WebP optimizados.
  - Pipeline de Dos Etapas: `scripts/gemini_studio_pipeline.py` para ingesta oficial y ambientación de estudio con Gemini Web (`~/.gemini_automation_profile`).
- **Frontend Editorial:** Diseño revista con fondo blanco (`#ffffff`), tipografía clásica `Playfair Display` combinada con `Inter`, tarjetas con badges dorados de Top Ventas, showcase superior de líderes ACAU, modal interactivo con visor de miniaturas, buscador en tiempo real y filtros dinámicos.
- **Mapa Nacional de Cargadores:** Leaflet.js sobre OpenStreetMap libre ($0 API keys), con auto-enfoque y 25 estaciones georreferenciadas de la red UTE Mueve en los 19 departamentos.
- **SEO & Descubrimiento por IA:** Schema.org JSON-LD estructurado (`WebSite`, `Organization`, `Car`), `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt` y `manifest.json` (PWA).

## ⚡ Cobertura de Mercado (+98% - 93 Modelos y Variantes)

### 1. Autos, SUVs, Pickups y Utilitarios (67 modelos/versiones)
- **BYD (SADAR S.A.):**
  - **Seagull EV300 (GL)**: 30.08 kWh Blade LFP, 305 km, 75 CV, USD 18.990.
  - **Seagull EV400 (GS)**: 38.88 kWh Blade LFP, 380 km, 75 CV, 6 airbags, V2L, USD 21.990.
  - **Seagull Surf**: 43.2 kWh Blade LFP, 380 km, 88 CV (65 kW), llantas diamantadas 16", estética Surf, carga AC 11 kW + DC rápida, USD 23.990.
  - **Dolphin GS / Dolphin Mini / Dolphin Plus** (204 CV 60.5 kWh).
  - **Yuan Pro EV** (#1 en ventas en Uruguay, 3.362 empadronamientos).
  - **Yuan Plus (Atto 3) / Song Plus DM-i / Seal AWD (530 CV) / Han EV / Tang EV / e2 / T3 / Shark PHEV**.
- **Chevrolet (General Motors Uruguay):**
  - Blazer EV RS AWD Ultium 102 kWh (520 km, 565 CV, USD 74.990).
  - Equinox EV RS AWD Ultium 85 kWh (480 km, 290 CV, USD 58.990).
  - Spark EUV City 32 kWh (#5 en ventas en Uruguay, 737 empadronamientos, USD 22.990).
  - Bolt EUV Premier 65 kWh (397 km, USD 42.990).
- **Tesla:**
  - Model 3 Highland: Standard RWD 60 kWh, Long Range AWD 78.1 kWh (629 km), Performance AWD (627 CV, 0-100 en 3.1s).
  - Model Y: Standard RWD 60 kWh, Long Range AWD 78.1 kWh (533 km), Performance AWD (534 CV, Überturbine 21", frenos Brembo).
- **BAW Uruguay:**
  - BAW L7 Bagel EV (5 puertas, 18.72 kWh LiFePO4, 220 km, 40 CV, USD 12.990).
  - BAW Pony EV (3 puertas, 13.7 kWh, 170 km, 27 CV, USD 9.990).
- **Chery Uruguay (Grupo Fidocar):**
  - Chery eQ1 Little Ant (Pequeña Hormiga, 30.8 kWh LFP, 301 km, chasis de aluminio, pantalla vertical 10.25", USD 19.990).
  - Chery QQ Ice Cream (Kei car urbano, 13.9 kWh, 170 km, USD 11.990).
- **Geely & Zeekr (Grupo Fiancar):**
  - Panda Mini EV (17 kWh, 200 km, 41 CV, USD 13.990).
  - EX5 Pro (#7 en ventas ACAU, 515 empadronamientos).
  - Geometry C, Geometry E, Zeekr 001, Zeekr X, Zeekr 7X.
- **JMC / JMEV:**
  - JMEV EV3.3 Xiaoqilin / Easy (#6 en ventas ACAU, 21.4 kWh, 251 km, 589 empadronamientos, USD 13.990).
- **Changan Uruguay:**
  - Lumin 155 (12.9 kWh, USD 13.990).
  - Lumin 301 Sweet (28 kWh con carga rápida DC, USD 16.990).
- **Dongfeng & Nammi (Fidocar S.A.):**
  - Nammi Box 430 / Nammi Box 330 (#3 en ventas ACAU, 1.196 empadronamientos).
  - Rich 6 EV Pickup Doble Cabina.
- **JAC Motors:** e-JS1 (#10 en ventas ACAU, 394 empadronamientos), e-JS4 SUV, e-J7.
- **Renault & Nissan:** Kwid E-Tech, Megane E-Tech, Kangoo E-Tech, Nissan LEAF.
- **GWM & Omoda:** ORA 03, Omoda E5 (#9 en ventas ACAU, 469 empadronamientos).
- **Hyundai & Kia:** Kona Electric, Ioniq 5, Kia EV3, Kia EV6.
- **Maxus:** eDeliver 3, eTerron 9 Pickup 4x4.
- **Premium Europeo:** BMW iX1, Mini Cooper SE, Audi Q4 e-tron, Mercedes-Benz EQA, EQB.

### 2. Triciclos Eléctricos y Motocarros Utilitarios (4 modelos)
- **Trike / Trek Uruguay:**
  - Hard Work 1000 kg (Trekker): Volcador pesado 1500W con reductora, 70 km, capacidad 1.000 kg, USD 2.890.
  - Cargo Light GT 500 kg: Utilitario de reparto urbano 1200W, 60 km, USD 2.190.
  - Urbano Delivery & Pasajeros: Cabina cerrada 1200W 3 plazas, 60 km, USD 2.990.
- **Sunra Uruguay:**
  - Cargo King 1500W: Tricar utilitario con volcador manual asistido, 600 kg de carga, USD 2.690.

### 3. Motocicletas y Scooters Eléctricos (8 modelos)
- Sunra: Hawk 3000W, Grace 1800W, Miku Super 3000W, Robo-S 4000W.
- Yadea: G5 Pro Smart, C-Umi.
- Niu: NQi GT Pro Smart.
- Super Soco / Vmoto: TC Max Café Racer.

### 4. Bicicletas Eléctricas / E-Bikes (14 modelos)
- Loop Bikes (Nacional UY): Slim Pro, Soda Bike Fat 350W, X350, Classic Paseo.
- VoltBike Uruguay: Flex Plegable, Pioneer E-MTB, Classica.
- Wheele / Green Motors: Manhattan Flex, Pocket 20.
- Decathlon: Rockrider E-Expl 520, Riverside 500 E.
- Trek Uruguay: Allant+ 7 Gen 2 Bosch.
- Specialized Uruguay: Turbo Vado 4.0.
- Xiaomi / Himo: Himo Z20.

## 📁 Archivos Clave del Repositorio
- `index.html`: Aplicación editorial con showcase de líderes de ventas ACAU, buscador, carrusel y modal.
- `data/ev_uruguay.db`: Base de datos SQLite maestra (93 vehículos, ranking histórico, 6 crónicas, 25 cargadores, 144 avisos).
- `data/ev_data.json` / `data/ev_data.js`: Datasets exportados online y offline.
- `assets/img/<vehicle_id>/`: 744 activos WebP (558 fotos en 6 vistas 4:5 + 93 badges circulares + 93 sprites Pixel Art 16-Bit) con inyección de metadatos de ServicioTI.
- `scripts/gemini_studio_pipeline.py`: Pipeline de dos etapas con ingesta oficial y ambientación de estudio con Gemini Web.
- `scripts/pixel_art_generator.py`: Generador autónomo de coleccionables Pixel Art 16-Bit con cuantización adaptativa.
- `scripts/sync_acau_rankings.py`: Actualizador mensual de empadronamientos y ventas líderes.
- `scripts/tarea_mensual_rankings.ps1`: Automatización PowerShell para Programador de Tareas de Windows.
- `actualizar_ranking_mensual.bat`: Lanzador manual para el día 5 de cada mes.
- `scripts/test_top_sales_and_variants.py`: Suite Playwright que verifica el 100% de los líderes, variantes, triciclos y 0 imágenes rotas.
- `scripts/verify_clean_brands.py`: Auditor que certifica 0 menciones a portales competidores.

---
*ServicioTI · Soluciones Tecnológicas & Movilidad Eléctrica · www.servicioti.com.uy*
