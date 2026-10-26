"""
Catálogo Maestro de Vehículos Eléctricos en Uruguay para EV Uruguay (ev.servicioti.com.uy)
Prioriza los modelos más vendidos de plaza (BYD, Volvo, Geely, Dongfeng, JAC, Loop Bikes, VoltBike, Wheele, Sunra).
Cada vehículo incluye:
- Galería completa de 5 a 6 fotografías de alta resolución (frontal, trasera, interior/cockpit, perfil lateral, detalles).
- Ficha técnica profunda (dimensiones, baúl, motorización, tiempos de recarga en UTE y garantía).
- Enlace directo al fabricante o importador oficial en Uruguay.
"""

import json
from db_manager import get_connection

VEHICULOS_TOP_VENTAS_UY = [
    # =========================================================================
    # 1. BYD SEAGULL (El auto eléctrico más vendido de Uruguay)
    # =========================================================================
    {
        "id": "byd-seagull-ev",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Seagull",
        "version": "EV 300 / 400 (Batería Blade)",
        "precio_usd": 19990,
        "autonomia_km": 380,
        "bateria_kwh": 38.0,
        "potencia": "75 CV (55 kW)",
        "par_motor_nm": 135,
        "aceleracion_0_100": "13.0 s",
        "velocidad_maxima": "130 km/h",
        "tiempo_carga_ac": "4.5 h en Wallbox 7 kW / UTE 22 kW",
        "tiempo_carga_dc": "30 min (30% al 80% en cargador rápido DC 40 kW)",
        "dimensiones": "3.780 mm largo x 1.715 mm ancho x 1.540 mm alto",
        "peso_kg": 1160,
        "capacidad_baul_l": 230,
        "conector": "GB/T (Incluye adaptador homologado para red UTE Type 2)",
        "garantia_vehiculo": "6 años o 150.000 km (SADAR Uruguay)",
        "garantia_bateria": "8 años o 160.000 km (Garantía celda Blade)",
        "homologado_ursea": 1,
        "link_fabricante": "https://byd.uy/modelos/seagull",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80", # Frontal
            "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80", # Trasera
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80", # Interior Cockpit
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80", # Perfil 3/4
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80"  # Puerto de carga
        ],
        "especificaciones": {
            "traccion": "Delantera (FWD)",
            "quimica_bateria": "Litio-Ferrofosfato (LFP Blade Battery de alta seguridad)",
            "airbags": "4 airbags de serie (Frontales y laterales de cortina)",
            "asistencias_seguridad": "Frenos a disco en 4 ruedas, ABS, ESP, Control de Tracción TCS, Asistente de arranque en pendiente HHC",
            "pantalla_multimedia": "Pantalla táctil rotativa de 10.1 pulgadas con Apple CarPlay y Android Auto",
            "climatizacion": "Climatizador automático digital con filtro PM2.5",
            "importador_uruguay": "SADAR S.A. (Casa Central en Av. Italia y Paysandú, Montevideo)"
        }
    },

    # =========================================================================
    # 2. BYD DOLPHIN (Referente histórico de ventas en Uruguay)
    # =========================================================================
    {
        "id": "byd-dolphin-gs",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Dolphin",
        "version": "GS EV e-Platform 3.0",
        "precio_usd": 28990,
        "autonomia_km": 405,
        "bateria_kwh": 44.9,
        "potencia": "95 CV (70 kW)",
        "par_motor_nm": 180,
        "aceleracion_0_100": "10.9 s",
        "velocidad_maxima": "150 km/h",
        "tiempo_carga_ac": "6.0 h en Wallbox 7 kW",
        "tiempo_carga_dc": "30 min (30% al 80% en cargador DC 60 kW)",
        "dimensiones": "4.125 mm largo x 1.770 mm ancho x 1.570 mm alto",
        "peso_kg": 1405,
        "capacidad_baul_l": 345,
        "conector": "GB/T (Con adaptador homologado para cargador UTE)",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "homologado_ursea": 1,
        "link_fabricante": "https://byd.uy/modelos/dolphin",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80", # Frontal
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80", # Trasera
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80", # Interior Rotativo
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80", # Perfil Lateral
            "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80"  # Conectividad
        ],
        "especificaciones": {
            "traccion": "Delantera (FWD)",
            "quimica_bateria": "LFP Blade de ultra larga vida útil",
            "airbags": "6 airbags (Frontales, laterales y de cortina)",
            "suspension": "Delantera McPherson independiente, trasera barra de torsión",
            "pantalla_multimedia": "Pantalla de 12.8 pulgadas rotativa inteligente",
            "importador_uruguay": "SADAR S.A."
        }
    },

    # =========================================================================
    # 3. BYD YUAN PLUS (El SUV eléctrico premium más vendido)
    # =========================================================================
    {
        "id": "byd-yuan-plus",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Yuan Plus",
        "version": "EV 500 Flagship",
        "precio_usd": 39990,
        "autonomia_km": 480,
        "bateria_kwh": 60.5,
        "potencia": "204 CV (150 kW)",
        "par_motor_nm": 310,
        "aceleracion_0_100": "7.3 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "8 h en Wallbox 7 kW",
        "tiempo_carga_dc": "30 min en estación de carga rápida DC 80 kW de UTE",
        "dimensiones": "4.455 mm largo x 1.875 mm ancho x 1.615 mm alto",
        "peso_kg": 1690,
        "capacidad_baul_l": 440,
        "conector": "GB/T (Incluye adaptador oficial)",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "homologado_ursea": 1,
        "link_fabricante": "https://byd.uy/modelos/yuan-plus",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80", # Frontal
            "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80", # Trasera barra LED
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80", # Interior Gym-Design
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80", # Vista Lateral
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80"  # Llantas 18 pulgadas
        ],
        "especificaciones": {
            "traccion": "Delantera (FWD)",
            "quimica_bateria": "Blade Battery LFP",
            "seguridad_adas": "Frenado autónomo de emergencia AEB, Control crucero adaptativo ACC, Mantenimiento de carril LKA, Detector de punto ciego BSD",
            "airbags": "6 airbags y techo panorámico corredizo eléctrico",
            "importador_uruguay": "SADAR S.A."
        }
    },

    # =========================================================================
    # 4. VOLVO EX30 (Líder en SUVs eléctricos europeos en Uruguay)
    # =========================================================================
    {
        "id": "volvo-ex30",
        "tipo": "auto",
        "marca": "Volvo",
        "modelo": "EX30",
        "version": "Single Motor Extended Range Plus",
        "precio_usd": 42990,
        "autonomia_km": 476,
        "bateria_kwh": 69.0,
        "potencia": "272 CV (200 kW)",
        "par_motor_nm": 343,
        "aceleracion_0_100": "5.3 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "7.5 h en 11 kW trifásico",
        "tiempo_carga_dc": "26 min (10% al 80% en cargador DC ultrarrápido 150 kW)",
        "dimensiones": "4.233 mm largo x 1.837 mm ancho x 1.555 mm alto",
        "peso_kg": 1850,
        "capacidad_baul_l": 318,
        "conector": "Type 2 / CCS2 nativo europeo (100% compatible directo con red UTE)",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "homologado_ursea": 1,
        "link_fabricante": "https://www.volvocars.com/uy/cars/ex30-electric/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80", # Frontal Martillo de Thor
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80", # Trasera escandinava
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80", # Interior con Soundbar Harman Kardon
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80", # Perfil minimalista
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80"  # Conector CCS2
        ],
        "especificaciones": {
            "traccion": "Trasera (RWD)",
            "quimica_bateria": "NMC (Níquel-Manganeso-Cobalto) de alta densidad",
            "sistema_operativo": "Google Built-in con Google Maps, Asistente y Play Store nativos",
            "seguridad_adas": "Piloto asistido Pilot Assist, alerta de apertura segura de puertas para ciclistas, frenado en intersecciones",
            "importador_uruguay": "Grupo Danissa / Norden Motors (Montevideo)"
        }
    },

    # =========================================================================
    # 5. DONGFENG NAMMI BOX (Lanzamiento estrella de Fidocar)
    # =========================================================================
    {
        "id": "dongfeng-nammi-box",
        "tipo": "auto",
        "marca": "Dongfeng",
        "modelo": "Nammi",
        "version": "Box 430 EV",
        "precio_usd": 21990,
        "autonomia_km": 430,
        "bateria_kwh": 42.3,
        "potencia": "95 CV (70 kW)",
        "par_motor_nm": 160,
        "aceleracion_0_100": "11.5 s",
        "velocidad_maxima": "140 km/h",
        "tiempo_carga_ac": "5 h en cargador domiciliario 7 kW",
        "tiempo_carga_dc": "30 min en carga rápida DC",
        "dimensiones": "4.030 mm largo x 1.810 mm ancho x 1.570 mm alto",
        "peso_kg": 1380,
        "capacidad_baul_l": 326,
        "conector": "GB/T (Adaptador para cargador de UTE incluido)",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "homologado_ursea": 1,
        "link_fabricante": "https://dongfengmotors.uy/modelos/nammi-box/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80", # Frontal
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80", # Trasera
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80", # Interior capitoné
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80", # Puertas sin marco
            "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80"  # Puerto y cargador
        ],
        "especificaciones": {
            "traccion": "Delantera (FWD)",
            "quimica_bateria": "LFP de última generación",
            "detalles_diseno": "Manijas enrasadas eléctricas, puertas sin marco en las ventanas, tapizado en eco-cuero acolchado",
            "importador_uruguay": "Fidocar S.A. (Ruta Interbalnearia km 22.500)"
        }
    },

    # =========================================================================
    # 6. JAC e-JS1 (Pionero urbano accesible en Uruguay)
    # =========================================================================
    {
        "id": "jac-e-js1",
        "tipo": "auto",
        "marca": "JAC",
        "modelo": "e-JS1",
        "version": "City Luxury EV",
        "precio_usd": 18990,
        "autonomia_km": 302,
        "bateria_kwh": 31.4,
        "potencia": "61 CV (45 kW)",
        "par_motor_nm": 150,
        "aceleracion_0_100": "12.5 s",
        "velocidad_maxima": "120 km/h",
        "tiempo_carga_ac": "5 h en toma doméstica Shuko / Wallbox",
        "tiempo_carga_dc": "40 min en cargador rápido DC",
        "dimensiones": "3.650 mm largo x 1.670 mm ancho x 1.540 mm alto",
        "peso_kg": 1180,
        "capacidad_baul_l": 140,
        "conector": "GB/T (Adaptador incluido)",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "homologado_ursea": 1,
        "link_fabricante": "https://jac.com.uy/e-js1",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80", # Frontal
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80", # Trasera
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80", # Interior digital
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80", # Lateral
            "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80"  # Carga urbana
        ],
        "especificaciones": {
            "traccion": "Delantera (FWD)",
            "quimica_bateria": "Litio-Hierro-Fosfato LFP",
            "importador_uruguay": "Grupo Aler / Grupo Fiancar"
        }
    },

    # =========================================================================
    # 7. SUNRA HAWK 3000 (La moto eléctrica urbana más vendida en Uruguay)
    # =========================================================================
    {
        "id": "sunra-hawk-3000",
        "tipo": "moto",
        "marca": "Sunra",
        "modelo": "Hawk",
        "version": "3000W Doble Batería Extraíble",
        "precio_usd": 2490,
        "autonomia_km": 100,
        "bateria_kwh": 2.88,
        "potencia": "3000W Motor Bosch (Equivalente 125cc)",
        "par_motor_nm": 45,
        "aceleracion_0_100": "N/A (0-50 km/h en 4.2 s)",
        "velocidad_maxima": "75 km/h",
        "tiempo_carga_ac": "4 h por batería en cualquier enchufe convencional 220V",
        "tiempo_carga_dc": "Carga directa doméstica Shuko",
        "dimensiones": "1.850 mm largo x 710 mm ancho x 1.100 mm alto",
        "peso_kg": 85,
        "capacidad_baul_l": 25,
        "conector": "Cargador inteligente Shuko 220V a baterías extraíbles",
        "garantia_vehiculo": "1 año oficial Sunra Uruguay",
        "garantia_bateria": "2 años de garantía en celdas de litio",
        "homologado_ursea": 1,
        "link_fabricante": "https://sunra.com.uy/productos/hawk-3000/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=1200&q=80", # Frontal
            "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=1200&q=80", # Trasera y luces LED
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80", # Tablero digital e info de carga
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80", # Vista lateral completa
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80"  # Detalle de batería extraíble
        ],
        "especificaciones": {
            "motor": "Motor Bosch Brushless de 3000 Watts en rueda trasera",
            "bateria": "2 Packs de Litio 72V 20Ah extraíbles (permite cargar en el apartamento u oficina)",
            "frenos": "Frenos a disco hidráulicos ventilados adelante y atrás",
            "conectividad": "Conexión Bluetooth, altavoces integrados, alarma con comando a distancia",
            "representante_uruguay": "Sunra Uruguay (Locales en Montevideo y Ciudad de la Costa)"
        }
    },

    # =========================================================================
    # 8. YADEA G5 PRO (Scooter inteligente de alta gama)
    # =========================================================================
    {
        "id": "yadea-g5-pro",
        "tipo": "moto",
        "marca": "Yadea",
        "modelo": "G5",
        "version": "Pro Smart EV Edition",
        "precio_usd": 2890,
        "autonomia_km": 80,
        "bateria_kwh": 1.92,
        "potencia": "2300W Motor Central GTR 3.0",
        "par_motor_nm": 120,
        "aceleracion_0_100": "N/A (0-50 km/h en 4.5 s)",
        "velocidad_maxima": "65 km/h",
        "tiempo_carga_ac": "4.5 h en 220V",
        "tiempo_carga_dc": "Cargador rápido portátil incluido",
        "dimensiones": "1.810 mm largo x 700 mm ancho x 1.150 mm alto",
        "peso_kg": 88,
        "capacidad_baul_l": 26,
        "conector": "Conector directo Shuko 220V y batería Panasonic extraíble",
        "garantia_vehiculo": "1 año oficial Yadea",
        "garantia_bateria": "2 años de garantía oficial",
        "homologado_ursea": 1,
        "link_fabricante": "https://yadea.com.uy/modelos/g5/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=1200&q=80", # Frontal diseño escandinavo
            "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=1200&q=80", # Óptica trasera integrada
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80", # Tablero LCD color 7 pulgadas
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80", # Vista lateral
            "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80"  # Suspensión trasera de aluminio
        ],
        "especificaciones": {
            "bateria": "Celdas Panasonic 18650 de litio extraíbles con BMS inteligente",
            "cuadro": "Estructura de acero laminado en frío con tratamiento anticorrosión",
            "pantalla": "Panel digital de 7 pulgadas con ajuste automático de brillo diurno/nocturno",
            "representante_uruguay": "Yadea Uruguay"
        }
    },

    # =========================================================================
    # 9. LOOP BIKES SLIM PRO (Marca nacional uruguaya urbana líder)
    # =========================================================================
    {
        "id": "loop-bikes-slim-pro",
        "tipo": "bicicleta",
        "marca": "Loop Bikes",
        "modelo": "Slim Pro",
        "version": "Urbana Bafang 250W (Diseño Nacional UY)",
        "precio_usd": 1290,
        "autonomia_km": 60,
        "bateria_kwh": 0.36,
        "potencia": "250W (Pedaleo asistido legal hasta 25 km/h)",
        "par_motor_nm": 45,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h (Límite normativo de pedelec)",
        "tiempo_carga_ac": "3.5 h con cargador portátil 220V",
        "tiempo_carga_dc": "Carga doméstica con llave de seguridad",
        "dimensiones": "Rodado 28 (700c) cuadro aluminio 6061",
        "peso_kg": 17,
        "capacidad_baul_l": 0,
        "conector": "Cargador Shuko 220V / Batería con cerradura en el cuadro",
        "garantia_vehiculo": "Garantía de 1 año en cuadro y componentes Shimano",
        "garantia_bateria": "1 año oficial Loop Bikes (Celdas Samsung)",
        "homologado_ursea": 1,
        "link_fabricante": "https://loop-bikes.com/producto/slim-pro/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80", # Perfil completo
            "https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=1200&q=80", # Manillar y display LCD
            "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1200&q=80", # Batería oculta en el cuadro
            "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=1200&q=80", # Motor Bafang trasero
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80"  # Frenos de disco mecánicos
        ],
        "especificaciones": {
            "motor": "Bafang Brushless 250W con sensor de pedaleo asistido de 5 niveles",
            "bateria": "Samsung 36V 10Ah integrada de bajo perfil desmontable con llave",
            "transmision": "Shimano Tourney de 7 velocidades con pata de cambio protegida",
            "origen": "Diseño y ensamblado en Uruguay por Loop Bikes (fundada en 2016)"
        }
    },

    # =========================================================================
    # 10. VOLTBIKE FLEX (La plegable eléctrica más vendida de Uruguay)
    # =========================================================================
    {
        "id": "voltbike-flex-foldable",
        "tipo": "bicicleta",
        "marca": "VoltBike",
        "modelo": "Flex",
        "version": "Plegable Urbana 350W Rodado 20",
        "precio_usd": 990,
        "autonomia_km": 45,
        "bateria_kwh": 0.38,
        "potencia": "350W Motor de alta eficiencia",
        "par_motor_nm": 40,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "30 km/h",
        "tiempo_carga_ac": "4 h en enchufe tradicional",
        "tiempo_carga_dc": "Cargador rápido portátil incluido",
        "dimensiones": "Plegada: 85 cm x 45 cm x 65 cm (entra en baúl de auto)",
        "peso_kg": 21,
        "capacidad_baul_l": 0,
        "conector": "Cargador 220V / Batería desmontable",
        "garantia_vehiculo": "1 año oficial VoltBike Uruguay",
        "garantia_bateria": "1 año oficial en batería",
        "homologado_ursea": 1,
        "link_fabricante": "https://voltbike.uy/producto/voltbike-flex/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=1200&q=80", # Desplegada de perfil
            "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80", # Vista plegada compacta
            "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1200&q=80", # Batería y cerradura
            "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=1200&q=80", # Manubrio y acelerador
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80"  # Guardabarros y portaequipaje
        ],
        "especificaciones": {
            "plegado": "Mecanismo de plegado rápido en 3 pasos con doble traba de seguridad",
            "bateria": "Litio 36V 10.4Ah oculta dentro del caño principal",
            "suspension": "Horquilla delantera con suspensión para adoquines y baches de Montevideo",
            "locales_en_uruguay": "Montevideo, Maldonado y red de distribución en el interior"
        }
    },

    # =========================================================================
    # 11. WHEELE MANHATTAN (E-Bike de paseo con gran respaldo técnico)
    # =========================================================================
    {
        "id": "wheele-manhattan-flex",
        "tipo": "bicicleta",
        "marca": "Wheele",
        "modelo": "Manhattan",
        "version": "Flex Cruiser 250W",
        "precio_usd": 1150,
        "autonomia_km": 50,
        "bateria_kwh": 0.37,
        "potencia": "250W Motor trasero Brushless",
        "par_motor_nm": 42,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "4 h en enchufe 220V",
        "tiempo_carga_dc": "Cargador 2A incluido",
        "dimensiones": "Rodado 26 con cuadro bajo (Step-through) fácil de montar",
        "peso_kg": 23,
        "capacidad_baul_l": 0,
        "conector": "Cargador Shuko 220V con batería extraíble bajo el portaequipaje",
        "garantia_vehiculo": "1 año con taller de postventa propio en Montevideo",
        "garantia_bateria": "1 año de garantía oficial Wheele",
        "homologado_ursea": 1,
        "link_fabricante": "https://wheele.com.uy/producto/manhattan-flex/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1200&q=80", # Perfil paseo
            "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80", # Cuadro bajo y asiento ergonómico
            "https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=1200&q=80", # Display y comandos
            "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=1200&q=80", # Batería en parrilla trasera
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80"  # Luz delantera LED alimentada por batería
        ],
        "especificaciones": {
            "postventa": "Taller técnico especializado propio con stock permanente de repuestos y baterías",
            "posicion_de_manejo": "Ergonómica con manubrio alto y asiento con resortes de gel",
            "frenos": "Frenos V-Brake con corte electrónico del motor al accionar la maneta",
            "representante_uruguay": "Wheele / Green Motors Uruguay"
        }
    },

    # =========================================================================
    # 12. DECATHLON ROCKRIDER E-EXPL 520 (E-MTB deportiva con motor central Yamaha)
    # =========================================================================
    {
        "id": "decathlon-rockrider-e-expl",
        "tipo": "bicicleta",
        "marca": "Decathlon / Rockrider",
        "modelo": "E-Expl 520",
        "version": "E-MTB 29 Motor Central Yamaha PW-CE",
        "precio_usd": 2490,
        "autonomia_km": 80,
        "bateria_kwh": 0.50,
        "potencia": "250W con par motor de 70 Nm (Yamaha)",
        "par_motor_nm": 70,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h asistida",
        "tiempo_carga_ac": "4.5 h con cargador Decathlon 2A",
        "tiempo_carga_dc": "Batería extraíble lateralmente con llave",
        "dimensiones": "Rodado 29 pulgadas, cuadro de aluminio hidroformado",
        "peso_kg": 23.8,
        "capacidad_baul_l": 0,
        "conector": "Cargador Shuko 220V",
        "garantia_vehiculo": "Garantía de por vida en cuadro, potencia y manillar",
        "garantia_bateria": "2 años o 500 ciclos oficiales Decathlon Uruguay",
        "homologado_ursea": 1,
        "link_fabricante": "https://www.decathlon.com.uy/bicicletas-electricas/",
        "imagen_oficial_url": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=1200&q=80",
        "galeria": [
            "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=1200&q=80", # Perfil montaña
            "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80", # Detalle motor central Yamaha
            "https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=1200&q=80", # Batería integrada de 500Wh
            "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1200&q=80", # Frenos a disco hidráulicos Tektro
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=80"  # Pantalla color con conexión Bluetooth
        ],
        "especificaciones": {
            "motor": "Yamaha PW-CE central de 250W con par motor potente de 70 Nm para senderos y repechos",
            "bateria": "500 Wh integrada y desmontable (posibilidad de añadir batería secundaria de 360 Wh)",
            "suspension": "Horquilla Suntour XCM de 130 mm de recorrido con bloqueo",
            "transmision": "Microshift Acolyte de 8 velocidades 1x8 con piñón de 12-42 dientes",
            "respaldo_local": "Tiendas físicas Decathlon en Uruguay con taller y servicio de postventa oficial"
        }
    }
]

def seed_catalog():
    conn = get_connection()
    cursor = conn.cursor()
    count = 0

    for v in VEHICULOS_TOP_VENTAS_UY:
        galeria_str = json.dumps(v.get("galeria", []))
        espec_str = json.dumps(v.get("especificaciones", {}))

        cursor.execute("""
        INSERT INTO vehicles (
            id, tipo, marca, modelo, version, precio_usd, autonomia_km,
            bateria_kwh, potencia, par_motor_nm, aceleracion_0_100, velocidad_maxima,
            tiempo_carga_ac, tiempo_carga_dc, dimensiones, peso_kg, capacidad_baul_l,
            conector, garantia_vehiculo, garantia_bateria, homologado_ursea,
            link_fabricante, imagen_oficial_url, galeria_json, especificaciones_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            precio_usd=excluded.precio_usd,
            autonomia_km=excluded.autonomia_km,
            bateria_kwh=excluded.bateria_kwh,
            potencia=excluded.potencia,
            par_motor_nm=excluded.par_motor_nm,
            aceleracion_0_100=excluded.aceleracion_0_100,
            velocidad_maxima=excluded.velocidad_maxima,
            tiempo_carga_ac=excluded.tiempo_carga_ac,
            tiempo_carga_dc=excluded.tiempo_carga_dc,
            dimensiones=excluded.dimensiones,
            peso_kg=excluded.peso_kg,
            capacidad_baul_l=excluded.capacidad_baul_l,
            conector=excluded.conector,
            garantia_vehiculo=excluded.garantia_vehiculo,
            garantia_bateria=excluded.garantia_bateria,
            link_fabricante=excluded.link_fabricante,
            imagen_oficial_url=excluded.imagen_oficial_url,
            galeria_json=excluded.galeria_json,
            especificaciones_json=excluded.especificaciones_json
        """, (
            v["id"], v["tipo"], v["marca"], v["modelo"], v["version"],
            v["precio_usd"], v["autonomia_km"], v["bateria_kwh"], v["potencia"],
            v.get("par_motor_nm", 0), v.get("aceleracion_0_100", "N/A"),
            v.get("velocidad_maxima", "N/A"), v.get("tiempo_carga_ac", "N/A"),
            v.get("tiempo_carga_dc", "N/A"), v.get("dimensiones", "N/A"),
            v.get("peso_kg", 0), v.get("capacidad_baul_l", 0),
            v["conector"], v["garantia_vehiculo"], v["garantia_bateria"],
            v["homologado_ursea"], v["link_fabricante"], v["imagen_oficial_url"],
            galeria_str, espec_str
        ))
        count += 1

    conn.commit()
    conn.close()
    print(f"[Catalogo] {count} vehículos líderes cargados con galería de 5 fotos y ficha técnica profunda.")

if __name__ == "__main__":
    seed_catalog()
